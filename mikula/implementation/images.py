import os
from PIL import Image, ExifTags
from mikula.implementation.exif import nominal_shutter_speed, nominal_f_number, nominal_aperture
from mikula.implementation.settings import gallery_dir, images_dir, thumbnails_dir

EXIF_ORIENTATION = 0x0112
ROTATION = {3: 180, 6: 270, 8: 90}
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


def convert_image(original, converted, directory, images_dst, thumbnails_dst,
                  source_directory, height, image_format, thumbnail_height):
    file_path = os.path.join(source_directory, directory, original)
    img = Image.open(file_path)
    exif = img._getexif()
    if exif is not None:
        if EXIF_ORIENTATION in exif.keys():
            code = exif[EXIF_ORIENTATION]
            angle = ROTATION.get(code, None)
            if angle is not None:
                img = img.rotate(angle, expand=True)
    aspect = img.height / img.width
    width = int(height / aspect)
    img = img.resize((width, height), Image.ANTIALIAS)

    image_dst = os.path.join(images_dst, converted)
    img.save(image_dst, format=image_format)

    thumbnail_width = int(thumbnail_height / aspect)
    img.thumbnail((thumbnail_width, thumbnail_height))
    thumbnail_dst = os.path.join(thumbnails_dst, converted)
    img.save(thumbnail_dst, format=image_format)
    img.close()
    return exif


def extract_exif_meta(meta, exif, album_meta):
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
    return meta


def process_images(source_directory, parsed, excluded, output, config):
    image_format = config["image_format"]
    height = config["image_height"]
    thumbnail_height = config["thumbnail_height"]
    images_dst = os.path.join(output, GALLERY, IMAGES)
    thumbnails_dst = os.path.join(images_dst, THUMBNAILS)
    for directory, content in parsed.items():
        relative, subdirs, images, index_meta, index_content = content
        if directory in excluded.keys():
            excluded_original, excluded_converted = excluded[directory]
            convert_image(excluded_original, excluded_converted, directory, images_dst, thumbnails_dst,
                          source_directory, height,
                          image_format, thumbnail_height)
        for original, record in images.items():
            converted, meta, _ = record
            print(os.path.join(directory, original))
            exif = convert_image(original, converted, directory, images_dst, thumbnails_dst, source_directory, height,
                                 image_format, thumbnail_height)
            meta = extract_exif_meta(meta, exif, index_meta)
