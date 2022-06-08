import os
import shutil
from mikula.implementation import settings


def input_yes_no(question):
    reply = None
    while reply not in ("y", "n"):
        reply = str(input(question+' (y/n): ')).lower().strip()
    return True if reply == "y" else False


def extension(file):
    _, ext = os.path.splitext(file)
    ext = ext.upper()
    return ext[1:]


def create(directory, overwrite=True):
    if os.path.isdir(directory) and overwrite:
        shutil.rmtree(directory)
    if not os.path.isdir(directory):
        os.mkdir(directory)


def create_directories(parsed, output_directory, overwrite=True):
    create(output_directory, overwrite)

    images_dir = os.path.join(output_directory, settings.images_dir)
    create(images_dir, overwrite)

    thumbnails_dir = os.path.join(output_directory, settings.thumbnails_dir)
    create(thumbnails_dir, overwrite)

    for directory in reversed(parsed.keys()):
        absolute = os.path.join(output_directory, directory)
        if not os.path.isdir(absolute):
            os.mkdir(absolute)


def copy_assets(theme, output_directory, clean):
    src = os.path.join(theme, "assets")
    dst = os.path.join(output_directory, settings.assets_dir)
    create(dst, overwrite=clean)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def copy_user_assets(source, output):
    src = os.path.join(os.path.abspath(source), settings.assets_dir)
    dst = os.path.join(os.path.abspath(output), settings.assets_dir)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)


def walk(path, exclude=tuple(), topdown=False):
    nodes = list()
    for root, dirs, files in os.walk(path, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        nodes.append((root, dirs, files))
    if not topdown:
        nodes.reverse()
    return nodes


def get_theme_directory(theme):
    if os.path.isdir(theme):
        return theme
    d = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(d, os.pardir, "themes", theme))


def directory_basename(source_directory):
    return os.path.basename(os.path.abspath(source_directory))
