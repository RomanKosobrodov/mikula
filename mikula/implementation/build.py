from mikula.implementation.configure import read_configuration, update_configuration
from mikula.implementation.images import process_images
from mikula.implementation.discovery import discover, parse_pages
from mikula.implementation.util import create_directories, copy_user_assets, copy_assets, get_theme_directory
from mikula.implementation.rendering import render
from mikula.implementation.image_cache import ImageCache
import os
import time


def build(theme, clean, album_directory=os.getcwd()):
    start_time = time.perf_counter()
    source = os.path.join(album_directory, "source")
    output = os.path.join(album_directory, "build")
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

    cache = ImageCache(album_directory)
    if clean:
        cache.reset()
    album, excluded, error_page, config_changes = discover(directory=source, config=config, cache=cache)
    pages = parse_pages(source_directory=source)

    create_directories(album, output, overwrite=config_changes)
    copy_assets(theme_directory, output)
    copy_user_assets(source, output)

    process_images(source, album, excluded, output, config, cache)

    render(album, error_page, pages, output, theme_directory, config)
    elapsed = time.perf_counter() - start_time
    print(f"\nDone in {elapsed:.1f} seconds")
    print(f'\nGallery built in "{output}" using theme "{theme}"')
