import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from mikula.implementation import settings
from mikula.implementation.render_common import create_page, render_pages

GALLERY = settings.gallery_dir
IMAGES = settings.images_dir
THUMBNAILS = settings.thumbnails_dir
USER_ASSETS = settings.user_assets_dir


def render(album, error_page, pages, output_directory, theme, config):
    for key in album.keys():
        print(f'"{key}"')
        path, subdirs, images, index_meta, index_content = album[key]
        for x in images:
            print(f'   "{x}": {images[x]}')

    env = Environment(
        loader=FileSystemLoader(theme),
        autoescape=select_autoescape(['html', 'xml'])
    )
    album_template = env.get_template("album.html")
    error_template = env.get_template("error.html")

    page_list = list()
    if len(pages) > 0:
        pages_template = env.get_template("pages.html")
        page_list = render_pages(pages, output_directory, pages_template, config)

    create_page(error_page, page_list, output_directory, "error.html", error_template, config)