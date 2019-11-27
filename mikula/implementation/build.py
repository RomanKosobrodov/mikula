from mikula.implementation.configure import read_configuration
from mikula.implementation.images import process_images
from mikula.implementation.discovery import discover
from mikula.implementation.util import create_directories
from mikula.implementation.rendering import render


def build(source, output, theme):
    config = read_configuration(directory=source, filename="configuration.yaml")
    album, excluded, error_page, pages = discover(source, config["image_format"])
    create_directories(album, theme, output)
    process_images(source, album, excluded, output, config)
    render(album, error_page, pages, output, theme)
