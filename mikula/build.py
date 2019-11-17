import os

from mikula.implementation.images import process_images
from mikula.implementation.discovery import discover
from mikula.implementation.util import create_directories
from mikula.implementation.rendering import render


def build_from(directory, output, theme):
    album = discover(directory)
    destination, assets_dir = create_directories(album, output)
    process_images(album, assets_dir)
    render(album, output, theme)

