from mikula.implementation.configure import read_configuration, update_configuration
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
    if not os.path.isdir(theme_directory):
        print(f'Unable to find theme "{theme_directory}"')
        return
    theme_configuration = read_configuration(directory=theme_directory, filename="configuration.yaml")
    config = read_configuration(directory=source, filename="configuration.yaml")
    config = update_configuration(config, theme_configuration)
    album, excluded, error_page = discover(directory=source,
                                           image_format=config.get("image_format", "png"),
                                           sort_by=config.get("sort_by", "name"))
    pages = parse_pages(source_directory=source)
    create_directories(album, output)
    copy_assets(theme_directory, output)
    copy_user_assets(source, output)
    process_images(source, album, excluded, output, config)
    render(album, error_page, pages, output, theme_directory,config)
    print(f'\nGallery built in "{output}" using theme "{theme}"')
