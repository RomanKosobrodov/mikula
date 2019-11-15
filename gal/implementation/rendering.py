import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template


def parse_subdirectories(album, keys, index, destination):
    album_root = keys[-1]

    def form_path(dir_path):
        index_url = dir_path.replace(album_root, destination)
        index_url = os.path.join(index_url, "index.html")
        return os.path.normpath(index_url)

    current = keys[index]
    subdirectories, _, album_meta, album_md = album[current]
    output = list()

    for directory in subdirectories:
        source_full_path = os.path.join(current, directory)
        url = form_path(source_full_path)
        _, _, meta, _ = album[source_full_path]
        title = meta.get("title", directory)
        output.append((title, url))

    return output, form_path(current), album_meta, album_md


def parse_images(album, keys, index, destination, image_format="png"):
    output = list()
    _, filelist, *rest = album[keys[index]]
    for filename, image_id, image_meta, _ in filelist:
        basename, _ = os.path.splitext(filename)
        image_name = image_meta.get("title", basename)
        image_url = f"{image_name}.html"
        thumbnail_url = os.path.join(destination, "assets", "images", "thumbnails", f"{image_id}.{image_format}")
        output.append((image_url, os.path.normpath(thumbnail_url)))
    return output


def parent_album(keys, index, destination):
    parent = os.path.dirname(keys[index])
    if parent in keys:
        root = keys[-1]
        path = parent.replace(root, destination)
        url = os.path.join(path, "index.html")
        return url


def render_album_page(album, keys, index, template, destination):
    albums, filename, meta, user_template = parse_subdirectories(album, keys, index, destination)
    thumbnails = parse_images(album, keys, index, destination)
    user_generated = Template(user_template)
    html = user_generated.render(auto_generated=template,
                                 back=parent_album(keys, index, destination),
                                 albums=albums,
                                 thumbnails=thumbnails)
    return html, filename


def render_image_page(album, directory, image, template):
    pass


def render(album, output_directory, theme):
    env = Environment(
        loader=FileSystemLoader(theme),
        autoescape=select_autoescape(['html', 'xml'])
    )
    album_template = env.get_template("album.html")
    image_template = env.get_template("image.html")

    keys = tuple(album.keys())
    for index in range(len(keys)):
        album_page, filename = render_album_page(album, keys, index, album_template, output_directory)
        with open(filename, 'w') as fid:
            fid.write(album_page)

#     page_names = [f"{basename}.html" for basename, _, _ in image_list]
#     thumbnails = list()
#     for index, element in enumerate(image_list):
#         basename, thumbnail, path = element
#         previous_page = get_links(page_names, index - 1)
#         next_page = get_links(page_names, index + 1)
#         filename = os.path.join(current, page_names[index])
#         this_album = "index.html"
#         image_page = image_template.render(image=path,
#                                            album=this_album,
#                                            previous=previous_page,
#                                            next=next_page)
#         with open(filename, "w") as fid:
#             fid.write(image_page)
#         thumbnail_url = os.path.relpath(thumbnail, current)
#         image_page = os.path.relpath(filename, current)
#         thumbnails.append((image_page, thumbnail_url))
#
