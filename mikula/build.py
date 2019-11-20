import os

from mikula.implementation.images import process_images
from mikula.implementation.discovery import discover
from mikula.implementation.util import create_directories
from mikula.implementation.rendering import render


def build_from(directory, output, theme):
    album, excluded = discover(directory)
    create_directories(album, theme, output)
    process_images(directory, album, excluded, output)
    render(album, excluded, output, theme)

