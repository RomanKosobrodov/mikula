import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template


def parse_subdirectories(album, keys, index):
    output = list()
    current = keys[index]
    relative, subdirectories, _, album_meta, album_md = album[current]
    for directory in subdirectories:
        key = os.path.normpath(os.path.join(current, directory))
        _, _, _, meta, _ = album[key]
        title = meta.get("title", directory)
        url = os.path.join(directory, "index.html")
        thumbnail_filename = meta.get("thumbnail", None)
        if thumbnail_filename is not None:
            thumbnail_url = os.path.join(relative, "gallery", "images", "thumbnails", thumbnail_filename)
        else:
            thumbnail_url = None
        output.append((title, url, thumbnail_url))
    return relative, output, album_meta, album_md


def parse_images(album, keys, index):
    output = list()
    relative, _, image_files, *rest = album[keys[index]]

    for original, (image_file, image_meta, _) in image_files.items():
        basename, _ = os.path.splitext(original)
        image_name = image_meta.get("title", basename)
        image_url = f"{image_name}.html"
        thumbnail_url = os.path.join(relative, "gallery", "images", "thumbnails", image_file)
        output.append((image_name, image_url, os.path.normpath(thumbnail_url)))
    return output


def parent_album(index, length):
    if index < length - 1:
        return "../index.html"
    return None


def render_album_page(album, keys, index, template):
    gallery_root, child_albums, meta, user_template = parse_subdirectories(album, keys, index)
    thumbnails = parse_images(album, keys, index)
    user_generated = Template(user_template)
    html = user_generated.render(page_title=meta.get("title", keys[index]),
                                 gallery_root=gallery_root,
                                 auto_generated=template,
                                 back=parent_album(index, len(keys)),
                                 albums=child_albums,
                                 thumbnails=thumbnails)
    return html


def get_image_page(image_files, image_keys, index):
    if index < 0 or index >= len(image_keys):
        return None
    original = image_keys[index]
    _, meta, _ = image_files[original]
    return f"{meta['title']}.html"


def render_image_page(gallery_root, image_files, image_keys, image_index,
                      image_template, relative_path):
    image_file, meta, user_template = image_files[image_keys[image_index]]
    user_generated = Template(user_template)
    html = user_generated.render(page_title=meta["title"],
                                 gallery_root=gallery_root,
                                 auto_generated=image_template,
                                 image=os.path.join(relative_path, image_file),
                                 exif=meta.get("exif", None),
                                 previous=get_image_page(image_files, image_keys, image_index - 1),
                                 next=get_image_page(image_files, image_keys, image_index + 1))
    return html, f"{meta['title']}.html"


def render(album, output_directory, theme):
    env = Environment(
        loader=FileSystemLoader(theme),
        autoescape=select_autoescape(['html', 'xml'])
    )
    album_template = env.get_template("album.html")
    image_template = env.get_template("image.html")

    keys = tuple(album.keys())
    for index in range(len(keys)):
        album_page = render_album_page(album, keys, index, album_template)
        dst_directory = os.path.join(output_directory, keys[index])
        album_filename = os.path.join(dst_directory, "index.html")
        with open(album_filename, 'w') as fid:
            fid.write(album_page)

        relative, _, image_files, _, _ = album[keys[index]]
        image_keys = tuple(image_files.keys())
        relative_path = os.path.join(relative, "gallery", "images")
        for k in range(len(image_keys)):
            image_page, filename = render_image_page(gallery_root=relative,
                                                     image_files=image_files,
                                                     image_keys=image_keys,
                                                     image_index=k,
                                                     image_template=image_template,
                                                     relative_path=relative_path)
            fn = os.path.join(dst_directory, filename)
            with open(fn, "w") as fid:
                fid.write(image_page)
