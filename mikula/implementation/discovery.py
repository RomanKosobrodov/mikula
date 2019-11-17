import os
import uuid
from collections import OrderedDict
from mikula.implementation.images import is_image
from mikula.implementation.md import render_markdown, INCLUDE_TEMPLATE


def discover(directory, image_format="png"):
    nodes = tuple(os.walk(directory, topdown=False))
    parsed = OrderedDict()
    for source_dir, subdirs, files in nodes:
        filelist = list()
        index_content = ""
        index_meta = dict()
        for file in files:
            fn = os.path.join(source_dir, file)
            if "index.md" in file.lower():
                index_meta, index_content = render_markdown(fn)
                continue
            if is_image(fn):
                image_id = str(uuid.uuid4())
                image_file = f"{image_id}.{image_format.lower()}"
                basename, ext = os.path.splitext(file)
                markdown_fn = os.path.join(source_dir, f"{basename}.md")
                if os.path.isfile(markdown_fn):
                    meta, html = render_markdown(markdown_fn)
                else:
                    meta = dict()
                    html = INCLUDE_TEMPLATE
                filelist.append((file, image_file, meta, html))
        parsed[source_dir] = (subdirs, filelist, index_meta, index_content)
    return parsed
