import os
from PIL import Image
from gal.implementation.util import extension


EXIF_ORIENTATION = 0x0112
ROTATION = {3: 180, 6: 270, 8: 90}


def process_images(source_dir, source_files, destination_dir, height=600, format="png"):
    ignored = ["txt", "html", "md", "json", "yml", "yaml"]
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
            base, _ = os.path.splitext(file)
            destination = os.path.join(destination_dir, f"{base}.{format}")
            img.save(destination, format=format)
            img.close()
        except IOError:
            print(f"unknown format of image file: '{file_path}'")
