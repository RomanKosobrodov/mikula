import os
import datetime
from multiprocessing import Pool
from PIL import Image, ExifTags
import piexif
from mikula.implementation.exif import get_exif
from mikula.implementation.settings import images_dir, thumbnails_dir

EXIF_ORIENTATION = 0x0112
EXIF_USER_COMMENT = 0X9286
EXIF_MAKER_NOTE = 0x927C
EXIF_DATE_TIME = 0x0132  # The format is "YYYY:MM:DD HH:MM:SS" with time shown in 24-hour format

ALL_ZEROS_LENGTH = 20
ALL_ZEROS = bytearray(ALL_ZEROS_LENGTH)

ORIENTATION = {
    2: Image.FLIP_LEFT_RIGHT,
    3: Image.ROTATE_180,
    4: Image.FLIP_TOP_BOTTOM,
    5: Image.TRANSPOSE,
    6: Image.ROTATE_270,
    7: Image.TRANSVERSE,
    8: Image.ROTATE_90
}
TAG_CODE = {key: value for key, value in zip(ExifTags.TAGS.values(), ExifTags.TAGS.keys())}
IMAGES = images_dir
THUMBNAILS = thumbnails_dir


def is_image(filename):
    try:
        Image.open(filename)
    except IOError:
        return False
    return True


def get_image_info(filename):
    timestamp = os.path.getmtime(filename)
    filedate = datetime.datetime.fromtimestamp(timestamp)
    date = filedate.strftime("%Y:%m:%d %H:%M:%S")
    try:
        img = Image.open(filename)
        exif = get_exif(img)
        width, height = img.size
        if exif is not None:
            if "Orientation" in exif.keys():
                code = exif["Orientation"]
                angle = ORIENTATION.get(code, None)
                if angle == Image.ROTATE_270 or angle == Image.ROTATE_90:
                    width, height = height, width
            if "DateTime" in exif.keys():
                date = exif["DateTime"]
            if "UserComment" in exif.keys():
                # remove user comment if starts with zeros (empty)
                if exif["UserComment"][:ALL_ZEROS_LENGTH] == ALL_ZEROS:
                    del exif["UserComment"]
            # remove maker note (useless)
            if "MakerNote" in exif.keys():
                del exif["MakerNote"]
        if width > 0:
            aspect = height / width
        else:
            aspect = 0.0
        return aspect, date, exif
    except IOError:
        return 0.0, "0000:00:00 00:00:00", None


def rescale_image(img, config, is_thumbnail):
    aspect = img.height / img.width
    if is_thumbnail:
        rescale_dimension = config.get("rescale_thumbnail", "width")
        image_size = config.get("thumbnail_size", 400)
    else:
        rescale_dimension = config.get("rescale_image", "width")
        image_size = config.get("image_size", 600)

    if rescale_dimension.lower() == "height":
        height = image_size
        width = int(height / aspect)
    else:
        width = image_size
        height = int(aspect * width)

    return img.resize((width, height), Image.LANCZOS)


def update_exif(img, config):
    if "exif" in img.info:
        exif = piexif.load(img.info["exif"])
        image_orientation = exif["0th"].get(piexif.ImageIFD.Orientation, 1)
        angle = ORIENTATION.get(image_orientation, None)
        if angle is not None:
            img = img.transpose(angle)
        exif["0th"][piexif.ImageIFD.Orientation] = 1
        if "add_copyright" in config:
            c = exif["0th"].get(piexif.ImageIFD.Copyright, "")
            if len(c) == 0:
                exif["0th"][piexif.ImageIFD.Copyright] = config["add_copyright"]
        exif_bytes = piexif.dump(exif)
    else:
        exif_bytes = b""
    return img, exif_bytes


def convert_image(original, converted, directory, images_dst, thumbnails_dst,
                  source_directory, config):
    file_path = os.path.join(source_directory, directory, original)
    img = Image.open(file_path)
    img, exif_bytes = update_exif(img, config)
    image_format = config.get("image_format", "png")
    if img.mode in ("RGBA", "P") and image_format.lower() == "jpeg":
        img = img.convert("RGB")
    else:
        if "I" in img.mode:
            img.putdata(img.getdata(), scale=255.0 / 65535.0, offset=0.0)
            img = img.convert("L")
    image_fn = None
    thumbnail_fn = None
    if images_dst is not None:
        rescaled = rescale_image(img, config, is_thumbnail=False)
        image_fn = os.path.join(images_dst, converted)
        rescaled.save(image_fn, format=image_format, exif=exif_bytes)
    if thumbnails_dst is not None:
        rescaled = rescale_image(img, config, is_thumbnail=True)
        thumbnail_fn = os.path.join(thumbnails_dst, converted)
        rescaled.save(thumbnail_fn, format=image_format, exif=exif_bytes)
    img.close()
    return file_path, image_fn, thumbnail_fn


def update_meta_with_exif(meta, exif, album_meta):
    if exif is None:
        if "exif" in meta:
            del meta["exif"]
        return meta

    if "exif" in meta:
        exif_tags = meta["exif"]
    else:
        exif_tags = album_meta.get("exif", tuple())

    meta["exif"] = dict()
    for tag in exif_tags:
        if tag in exif.keys():
            meta["exif"][tag] = exif[tag]

    return meta


def converter(args):
    original_fn, image_fn, thumbnail_fn = convert_image(*args)
    original, _, directory, *rest = args
    relative = os.path.join(directory, original)
    return relative, original_fn, image_fn, thumbnail_fn


def process_images(source_directory, parsed, excluded, destination, config, cache):
    if not os.path.isdir(destination):
        os.mkdir(destination)
    images_dst = os.path.join(destination, IMAGES)
    thumbnails_dst = os.path.join(destination, THUMBNAILS)
    parallel_tasks = list()
    for directory, content in parsed.items():
        relative, subdirs, images, index_meta, index_content = content
        if directory in excluded.keys():
            excluded_original, excluded_converted = excluded[directory]
            original_fn, image_fn, thumbnail_fn = convert_image(excluded_original, excluded_converted, directory,
                                                                images_dst, thumbnails_dst,
                                                                source_directory, config)
            cache.update(original_fn, image_fn, thumbnail_fn)
        for original, record in images.items():
            converted, meta, _, _, exif, update_required = record
            if update_required:
                parallel_tasks.append((original, converted, directory,
                                       images_dst, thumbnails_dst,
                                       source_directory, config))
            else:
                print(f"{os.path.join(directory, original)}")
            update_meta_with_exif(meta, exif, index_meta)

    num_processes = config.get("parallel_workers", None)
    with Pool(processes=num_processes) as pool:
        for relative, original_fn, image_fn, thumbnail_fn in pool.imap(converter, parallel_tasks):
            cache.update(original_fn, image_fn, thumbnail_fn)
            print(f"{relative} - updated")
