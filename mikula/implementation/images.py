import os
from PIL import Image, ExifTags
from mikula.implementation.exif import nominal_shutter_speed, nominal_f_number, nominal_aperture

EXIF_ORIENTATION = 0x0112
ROTATION = {3: 180, 6: 270, 8: 90}
TAG_CODE = {key: value for key, value in zip(ExifTags.TAGS.values(), ExifTags.TAGS.keys())}


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
        return meta

    all_tags = set(meta.get("exif", tuple()))
    all_tags.update(album_meta.get("exif", tuple()))
    extracted = get_exif_values(all_tags)
    return meta.update(extracted)


def process_images(source_directory, parsed, excluded, output, height=600, image_format="png", thumbnail_height=200):
    images_dst = os.path.join(output, "gallery", "images")
    thumbnails_dst = os.path.join(images_dst, "thumbnails")
    for directory, content in parsed.items():
        relative, subdirs, images, index_meta, index_content = content
        if directory in excluded.keys():
            excluded_original, excluded_converted = excluded[directory]
            convert_image(excluded_original, excluded_converted, directory, images_dst, thumbnails_dst,
                          source_directory, height,
                          image_format, thumbnail_height)
        for original, record in images.items():
            converted, meta, _ = record
            exif = convert_image(original, converted, directory, images_dst, thumbnails_dst, source_directory, height,
                                 image_format, thumbnail_height)
            meta = extract_exif_meta(meta, exif, index_meta)
