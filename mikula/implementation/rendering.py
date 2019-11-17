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
    for filename, image_file, image_meta, _ in filelist:
        basename, _ = os.path.splitext(filename)
        image_name = image_meta.get("title", basename)
        image_url = f"{image_name}.html"
        thumbnail_url = os.path.join(destination, "assets", "images", "thumbnails", image_file)
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


def get_image_name(source, meta):
    if "title" in meta:
        basename = meta["title"]
    else:
        basename, _ = os.path.splitext(source)
    return f"{basename}.html"


def get_image_page(image_list, index):
    if index < 0 or index >= len(image_list):
        return None
    source, _, meta, _ = image_list[index]
    return get_image_name(source, meta)


def render_image_page(image_list, image_index, image_template, album_url, images_directory):
    source, image_file, meta, user_template = image_list[image_index]
    user_generated = Template(user_template)
    html = user_generated.render(auto_generated=image_template,
                                 album_url=album_url,
                                 image=os.path.join(images_directory, image_file),
                                 previous=get_image_page(image_list, image_index - 1),
                                 next=get_image_page(image_list, image_index + 1))
    return html, get_image_name(source, meta)


def render(album, output_directory, theme):
    env = Environment(
        loader=FileSystemLoader(theme),
        autoescape=select_autoescape(['html', 'xml'])
    )
    album_template = env.get_template("album.html")
    image_template = env.get_template("image.html")

    images_directory = os.path.join(output_directory, "assets", "images")
    keys = tuple(album.keys())
    for index in range(len(keys)):
        album_page, album_filename = render_album_page(album, keys, index, album_template, output_directory)
        with open(album_filename, 'w') as fid:
            fid.write(album_page)

        _, file_list, _, _ = album[keys[index]]
        directory = os.path.dirname(album_filename)
        for k in range(len(file_list)):
            image_page, filename = render_image_page(image_list=file_list,
                                                     image_index=k,
                                                     image_template=image_template,
                                                     album_url=album_filename,
                                                     images_directory=images_directory)
            fn = os.path.join(directory, filename)
            with open(fn, "w") as fid:
                fid.write(image_page)
