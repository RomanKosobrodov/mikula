import os

from gal.implementation.images import process_images
from gal.implementation.discovery import discover
from gal.implementation.util import create_directories
from gal.implementation.rendering import render


def build_from(directory, output, theme):
    album = discover(directory)
    destination, assets_dir = create_directories(album, output)
    process_images(album, assets_dir)
    render(album, output, theme)

