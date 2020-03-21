from mikula.implementation.configure import read_configuration
from mikula.implementation.images import process_images
from mikula.implementation.discovery import discover, parse_pages
from mikula.implementation.util import create_directories, copy_user_assets, copy_assets, get_theme_directory
from mikula.implementation.rendering import render
import os


def build(theme):
    source = os.path.join(os.getcwd(), "source")
    output = os.path.join(os.getcwd(), "build")
    if not os.path.isdir(source):
        print(f'Source directory "{source}" does not exist.')
        print("Use `mikula init` to generate a template for your gallery.")
        return
    if not os.path.isdir(output):
        print(f'Output directory "{output}" does not exist.')
        print("Use `mikula init` to generate a template for your gallery.")
        return

    theme_directory = get_theme_directory(theme)
    config = read_configuration(directory=source, filename="configuration.yaml")
    album, excluded, error_page = discover(source, config["image_format"])
    pages = parse_pages(source_directory=source)
    create_directories(album, output)
    copy_assets(theme_directory, output)
    copy_user_assets(source, output)
    process_images(source, album, excluded, output, config)
    render(album, error_page, pages, output, theme_directory)
    print(f'\nGallery built in "{output}" using theme "{theme}"')
