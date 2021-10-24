from mikula.implementation.configure import read_configuration, update_configuration
from mikula.implementation.parse_pages import parse_pages, generate_page_list
from mikula.implementation.images import process_images
from mikula.implementation.discovery import discover
from mikula.implementation.blog import render_blog
from mikula.implementation.util import copy_user_assets, copy_assets, get_theme_directory, create_directories
from mikula.implementation.util import directory_basename
from mikula.implementation.rendering import render
from mikula.implementation.render_common import create_page, load_templates, create_default_error_page, \
    create_redirect_page
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

    copy_assets(theme_directory, output)
    copy_user_assets(source, output)

    cache = ImageCache(album_directory)
    if clean:
        cache.reset()

    templates = load_templates(theme_directory=theme_directory)

    pages = parse_pages(source_directory=source)
    page_list = generate_page_list(pages)
    for page, parsed in pages.items():
        meta, content = parsed
        content_type = meta.get("content", "page")
        if content_type.lower() == "page":
            create_page(page=parsed,
                        page_list=page_list,
                        destination_directory=output,
                        filename=f'{page}.html',
                        template=templates["page"],
                        config=config)
            continue
        if content_type.lower() == "blog":
            if "source" not in meta:
                print(f'Warning: page "{page}" defines content type "blog" but source is undefined. '
                      f'Empty page will be generated')
                continue
            blog_source = os.path.abspath(os.path.join(source, meta["source"]))
            blog_destination = os.path.join(output, directory_basename(blog_source))
            render_blog(blog_directory=blog_source,
                        page_list=page_list,
                        output_directory=blog_destination,
                        templates=templates,
                        config=config)
            index_dst = os.path.join(output, "index.html")
            create_redirect_page(meta, destination=index_dst)
        if content_type.lower() == "gallery":
            if "source" not in meta:
                print(f'Warning: page "{page}" defines content type "gallery" but source is undefined. '
                      f'Empty page will be generated')
                continue
            album_source = os.path.abspath(os.path.join(source, meta["source"]))
            album, excluded, config_changes = discover(directory=album_source, config=config, cache=cache)
            album_destination = os.path.join(output, directory_basename(album_source))
            create_directories(album, album_destination, overwrite=config_changes)

            process_images(album_source, album, excluded, album_destination, config, cache)
            render(album=album,
                   pages=page_list,
                   output_directory=album_destination,
                   templates=templates,
                   config=config)
            index_dst = os.path.join(output, "index.html")
            create_redirect_page(meta, destination=index_dst)

    if "error" not in pages:
        create_default_error_page(page_list=page_list,
                                  destination_directory=output,
                                  template=templates["error"],
                                  config=config)

    elapsed = time.perf_counter() - start_time
    print(f"\nDone in {elapsed:.1f} seconds")
    print(f'\nGallery built in "{output}" using theme "{theme}"')
