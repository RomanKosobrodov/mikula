from mikula.implementation.configure import read_configuration
from mikula.implementation.images import process_images
from mikula.implementation.discovery import discover
from mikula.implementation.util import create_directories
from mikula.implementation.rendering import render


def build(directory, output, theme):
    config = read_configuration(directory=directory, filename="configuration.yaml")
    album, excluded = discover(directory, config["image_format"])
    create_directories(album, theme, output)
    process_images(directory, album, excluded, output, config)
    render(album, output, theme)
