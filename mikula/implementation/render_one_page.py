import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from mikula.implementation import settings
from mikula.implementation.render_common import create_page, render_pages
from mikula.implementation.render_default import parse_subdirectories

IMAGES = settings.images_dir
THUMBNAILS = settings.thumbnails_dir
USER_ASSETS = settings.assets_dir


def render_album_page(album, keys, index, template, page_list):
    gallery_root, child_albums, meta, content = parse_subdirectories(album, keys, index)

    path = ["."]
    if index > 0:
        components = keys[index].split(os.sep)
        path = path + [os.sep.join(components[:k+1]) for k in range(len(components))]

    relative, _, image_dict, *rest = album[keys[index]]
    relative_path = os.path.join(relative, IMAGES)

    image_sources = list()
    for k, v in image_dict.items():
        image_sources.append(os.path.join(relative_path, v[0]))

    html = template.render(root_=gallery_root,
                           album_=album,
                           keys_=keys,
                           path_=path,
                           index_=index,
                           sources_=image_sources,
                           page_list_=page_list)
    return html


def render(album, error_page, pages, output_directory, theme, config):
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

    keys = tuple(reversed(album.keys()))
    for index in range(len(keys)):
        album_page = render_album_page(album, keys, index, album_template, page_list)
        dst_directory = os.path.join(output_directory, keys[index])
        album_filename = os.path.join(dst_directory, "index.html")
        with open(album_filename, 'w') as fid:
            fid.write(album_page)

    return page_list
