import os
import datetime
from PIL import Image, ExifTags
from mikula.implementation.exif import nominal_shutter_speed, nominal_f_number, nominal_aperture
from mikula.implementation.settings import gallery_dir, images_dir, thumbnails_dir

EXIF_ORIENTATION = 0x0112
EXIF_DATE_TIME = 0x0132  # The format is "YYYY:MM:DD HH:MM:SS" with time shown in 24-hour format
ROTATION = {3: Image.ROTATE_180, 6: Image.ROTATE_270, 8: Image.ROTATE_90}
TAG_CODE = {key: value for key, value in zip(ExifTags.TAGS.values(), ExifTags.TAGS.keys())}
GALLERY = gallery_dir
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
        exif = img._getexif()
        width, height = img.size
        if exif is not None:
            if EXIF_ORIENTATION in exif.keys():
                code = exif[EXIF_ORIENTATION]
                angle = ROTATION.get(code, None)
                if angle == Image.ROTATE_270 or angle == Image.ROTATE_90:
                    width, height = height, width
            if EXIF_DATE_TIME in exif.keys():
                date = exif[EXIF_DATE_TIME]

        if width > 0:
            aspect = height / width
        else:
            aspect = 0.0
        return aspect, date
    except IOError:
        return 0.0, "0000:00:00 00:00:00"


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

    return img.resize((width, height), Image.ANTIALIAS)


def convert_image(original, converted, directory, images_dst, thumbnails_dst,
                  source_directory, config):
    file_path = os.path.join(source_directory, directory, original)
    img = Image.open(file_path)
    exif = img._getexif()
    if exif is not None:
        if EXIF_ORIENTATION in exif.keys():
            code = exif[EXIF_ORIENTATION]
            angle = ROTATION.get(code, None)
            if angle is not None:
                img = img.transpose(angle)

    rescaled = rescale_image(img, config, is_thumbnail=False)
    image_dst = os.path.join(images_dst, converted)
    image_format = config.get("image_format", "png")
    rescaled.save(image_dst, format=image_format)

    rescaled = rescale_image(img, config, is_thumbnail=True)
    thumbnail_dst = os.path.join(thumbnails_dst, converted)
    rescaled.save(thumbnail_dst, format=image_format)
    img.close()
    return exif


def update_meta_with_exif(meta, exif, album_meta):
    def get_exif_values(tags):
        output = dict()
        for tag in tags:
            if tag in TAG_CODE.keys():
                if tag == "ShutterSpeedValue":
                    value = exif.get(TAG_CODE[tag], None)
                    if value is not None:
                        output[tag] = nominal_shutter_speed(*value)
                    continue
                if tag == "FNumber":
                    value = exif.get(TAG_CODE[tag], None)
                    if value is not None:
                        output[tag] = nominal_f_number(*value)
                    continue
                if tag == "ApertureValue":
                    value = exif.get(TAG_CODE[tag], None)
                    if value is not None:
                        output[tag] = nominal_aperture(*value)
                    continue
                output[tag] = exif.get(TAG_CODE[tag], None)
        return output

    if exif is None:
        if "exif" in meta:
            del meta["exif"]
        return meta

    if "exif" in meta:
        exif_tags = meta["exif"]
    else:
        exif_tags = album_meta.get("exif", tuple())
    meta["exif"] = get_exif_values(exif_tags)


def process_images(source_directory, parsed, excluded, output, config):
    images_dst = os.path.join(output, GALLERY, IMAGES)
    thumbnails_dst = os.path.join(images_dst, THUMBNAILS)
    for directory, content in parsed.items():
        relative, subdirs, images, index_meta, index_content = content
        if directory in excluded.keys():
            excluded_original, excluded_converted = excluded[directory]
            convert_image(excluded_original, excluded_converted, directory, images_dst, thumbnails_dst,
                          source_directory, config)
        for original, record in images.items():
            converted, meta, *rest = record
            print(os.path.join(directory, original))
            exif = convert_image(original, converted, directory, images_dst, thumbnails_dst, source_directory, config)
            update_meta_with_exif(meta, exif, index_meta)
