import os
import shutil


def extension(file):
    _, ext = os.path.splitext(file)
    ext = ext.upper()
    return ext[1:]


def create(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    if not os.path.isdir(directory):
        os.mkdir(directory)


def create_directories(parsed, theme, output_directory):
    create(output_directory)

    gallery_dir = os.path.join(output_directory, "gallery")
    create(gallery_dir)

    images_dir = os.path.join(gallery_dir, "images")
    create(images_dir)

    thumbnails_dir = os.path.join(images_dir, "thumbnails")
    create(thumbnails_dir)

    assets_dir = os.path.join(theme, "assets")
    dst = os.path.join(output_directory, "assets")
    shutil.copytree(assets_dir, dst)

    for directory in reversed(parsed.keys()):
        absolute = os.path.join(output_directory, directory)
        if not os.path.isdir(absolute):
            os.mkdir(absolute)
