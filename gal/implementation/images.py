import os
from PIL import Image
from gal.implementation.util import extension
import uuid

EXIF_ORIENTATION = 0x0112
ROTATION = {3: 180, 6: 270, 8: 90}


def process_images(source_dir, source_files, assets_dir, height=600, format="png", thumbnail_height=200):
    ignored = ["txt", "html", "md", "json", "yml", "yaml"]
    image_list = list()
    for file in source_files:
        if extension(file) in ignored:
            continue
        file_path = os.path.join(source_dir, file)
        try:
            img = Image.open(file_path)
            exif = img._getexif()
            if exif is not None:
                if EXIF_ORIENTATION in exif.keys():
                    code = exif[EXIF_ORIENTATION]
                    angle = ROTATION[code]
                    img = img.rotate(angle, expand=True)
            aspect = img.height / img.width
            width = int(height / aspect)
            img = img.resize((width, height), Image.ANTIALIAS)

            image_id = uuid.uuid4()
            image_dst = os.path.join(assets_dir, "images", f"{image_id}.{format}")
            img.save(image_dst, format=format)

            thumbnail_width = int(thumbnail_height / aspect)
            img.thumbnail((thumbnail_width, thumbnail_height))
            thumbnail_dst = os.path.join(assets_dir, "images", "thumbnails", f"{image_id}.{format}")
            img.save(thumbnail_dst, format=format)
            img.close()

            basename, ext = os.path.splitext(file)
            image_list.append((basename, thumbnail_dst, image_dst))
        except IOError as e:
            print(f"unknown format of image file: '{file_path}'")
    return image_list
