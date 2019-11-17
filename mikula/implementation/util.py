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


def create_directories(parsed, output_directory):
    create(output_directory)

    assets_dir = os.path.join(output_directory, "assets")
    create(assets_dir)

    images_dir = os.path.join(assets_dir, "images")
    create(images_dir)

    thumbnails_dir = os.path.join(images_dir, "thumbnails")
    create(thumbnails_dir)

    styles_dir = os.path.join(assets_dir, "styles")
    create(styles_dir)

    destination = dict()
    source_directory = None
    for directory in reversed(parsed.keys()):
        if source_directory is None:
            source_directory = directory
            destination[directory] = output_directory
            continue

        rerooted = directory.replace(source_directory, output_directory)
        if not os.path.isdir(rerooted):
            os.mkdir(rerooted)
        destination[directory] = rerooted

    return destination, assets_dir

