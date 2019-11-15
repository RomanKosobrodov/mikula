import os
import uuid
from collections import OrderedDict
from gal.implementation.images import is_image
from gal.implementation.md import render_markdown


def discover(directory):
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
                basename, ext = os.path.splitext(file)
                markdown_fn = os.path.join(source_dir, f"{basename}.md")
                if os.path.isfile(markdown_fn):
                    meta, html = render_markdown(markdown_fn)
                    filelist.append((file, image_id, meta, html))
                else:
                    filelist.append((file, image_id, dict(), ""))

        parsed[source_dir] = (subdirs, filelist, index_meta, index_content)
    return parsed
