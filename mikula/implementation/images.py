import os
from PIL import Image

EXIF_ORIENTATION = 0x0112
ROTATION = {3: 180, 6: 270, 8: 90}


def is_image(filename):
    try:
        Image.open(filename)
    except IOError:
        return False
    return True


def process_images(parsed, assets_dir, height=600, image_format="png", thumbnail_height=200):
    for directory, content in parsed.items():
        subdirs, filelist, index_meta, index_content = content
        for file, image_file, _, _ in filelist:
            file_path = os.path.join(directory, file)
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

            image_dst = os.path.join(assets_dir, "images", image_file)
            img.save(image_dst, format=image_format)

            thumbnail_width = int(thumbnail_height / aspect)
            img.thumbnail((thumbnail_width, thumbnail_height))
            thumbnail_dst = os.path.join(assets_dir, "images", "thumbnails", image_file)
            img.save(thumbnail_dst, format=image_format)
            img.close()
