import os
import shutil
from distutils.dir_util import copy_tree
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


def create(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)
    if not os.path.isdir(directory):
        os.mkdir(directory)


def create_directories(parsed, output_directory):
    create(output_directory)

    gallery_dir = os.path.join(output_directory, settings.gallery_dir)
    create(gallery_dir)

    images_dir = os.path.join(gallery_dir, settings.images_dir)
    create(images_dir)

    thumbnails_dir = os.path.join(images_dir, settings.thumbnails_dir)
    create(thumbnails_dir)

    for directory in reversed(parsed.keys()):
        absolute = os.path.join(output_directory, directory)
        if not os.path.isdir(absolute):
            os.mkdir(absolute)


def copy_assets(theme, output_directory):
    src = os.path.join(theme, "assets")
    dst = os.path.join(output_directory, settings.assets_dir)
    shutil.copytree(src, dst)


def copy_user_assets(source, output):
    src = os.path.join(os.path.abspath(source), settings.assets_source)
    dst = os.path.join(os.path.abspath(output), settings.user_assets_dir)
    if os.path.isdir(src):
        copy_tree(src, dst)


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
