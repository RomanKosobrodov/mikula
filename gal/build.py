import os
from jinja2 import Environment, PackageLoader, select_autoescape

from gal.implementation.images import process_images
from gal.implementation.util import create_directories
from gal.implementation.rendering import render_album


def build_from(directory, output):
    env = Environment(
        loader=PackageLoader('gal', './themes/default'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    nodes = tuple(os.walk(directory))
    destination_nodes, assets_dir = create_directories(nodes, output)
    indices = range(len(nodes))
    for index in reversed(indices):
        source_dir, subdirs, files = nodes[index]
        image_list = process_images(source_dir, files, assets_dir)
        files_lower = [f.lower() for f in files]
        if "index.md" in files_lower:
            filepath = os.path.join(source_dir, "index.md")
        else:
            filepath = "./themes/default/index.md"

        album_template = env.get_template("album.html")
        image_template = env.get_template("image.html")
        top_level = (index == 0)

        render_album(index_file=filepath,
                    destination_node=destination_nodes[index],
                    image_list=image_list,
                    album_template=album_template,
                    image_template=image_template,
                    top_level=top_level)
