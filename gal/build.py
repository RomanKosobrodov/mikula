import os
import markdown
import io
from jinja2 import Environment, PackageLoader, select_autoescape

from gal.implementation.images import process_images
from gal.implementation.util import create_directories
from gal.implementation.rendering import render_page


def build_from(directory, output):
    env = Environment(
        loader=PackageLoader('gal', './themes/default'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    nodes = tuple(os.walk(directory))
    destination_nodes = create_directories(nodes, output)
    indices = range(len(nodes))
    for index in reversed(indices):
        source_dir, subdirs, files = nodes[index]
        destination_dir = destination_nodes[index][0]
        process_images(source_dir, files, destination_dir)

        files_lower = [f.lower() for f in files]
        if "index.md" in files_lower:
            filepath = os.path.join(source_dir, "index.md")
        else:
            filepath = "./themes/default/index.md"

        template = env.get_template("page.html")
        top_level = (index == 0)
        render_page(filepath, destination_dir, template, top_level=top_level)
