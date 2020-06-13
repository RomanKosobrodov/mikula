import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from mikula.implementation import settings
from mikula.implementation.render_common import create_page, render_pages
from mikula.implementation.render_default import parse_subdirectories

GALLERY = settings.gallery_dir
IMAGES = settings.images_dir
THUMBNAILS = settings.thumbnails_dir
USER_ASSETS = settings.user_assets_dir


def render_album_page(album, keys, index, template):
    gallery_root, child_albums, meta, content = parse_subdirectories(album, keys, index)
    # thumbnails, aspects = parse_images(album, keys, index)
    # max_columns = config.get("max_columns", 1)
    # heights, counts = calculate_heights(aspects, max_columns)
    # padding = config.get("padding", 0.1)
    # user_content = Template(content)
    # if "page_title" not in meta.keys():
    #     meta["page_title"] = meta.get("title", "")
    # meta["assets"] = os.path.join(gallery_root, USER_ASSETS)
    # titles_links = parent_albums(album, keys, index)
    components = keys[index].split(os.sep)
    if index > 0:
        path = [os.sep.join(components[:k+1]) for k in range(len(components))]
    else:
        path = []
    print(f"Rendering '{keys[index]}';  path={path}")
    html = template.render(root_=gallery_root,
                           album_=album,
                           keys_=keys,
                           path_=path,
                           index_=index)
    return html


def render(album, error_page, pages, output_directory, theme, config):
    env = Environment(
        loader=FileSystemLoader(theme),
        autoescape=select_autoescape(['html', 'xml'])
    )
    album_template = env.get_template("album.html")
    error_template = env.get_template("error.html")

    keys = tuple(reversed(album.keys()))
    for index in range(len(keys)):
        album_page = render_album_page(album, keys, index, album_template)
        dst_directory = os.path.join(output_directory, keys[index])
        album_filename = os.path.join(dst_directory, "index.html")
        with open(album_filename, 'w') as fid:
            fid.write(album_page)



        # path, subdirs, images, index_meta, index_content = album[key]
        # print(f'{key}: {subdirs}')
        # for x in images:
        #     print(f'   "{x}": {images[x]}')


    page_list = list()
    if len(pages) > 0:
        pages_template = env.get_template("pages.html")
        page_list = render_pages(pages, output_directory, pages_template, config)

    create_page(error_page, page_list, output_directory, "error.html", error_template, config)