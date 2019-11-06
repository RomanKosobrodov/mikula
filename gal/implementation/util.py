import os
import shutil


def extension(file):
    _, ext = os.path.splitext(file)
    ext = ext.lower()
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

    destination = list()
    root_directory = parsed[0][0]
    for parent, subdirs, files in parsed:
        rerooted = parent.replace(root_directory, output_directory)
        destination.append((rerooted, subdirs, files))
        for subdir in subdirs:
            new_path = os.path.join(rerooted, subdir)
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
    return destination, assets_dir
