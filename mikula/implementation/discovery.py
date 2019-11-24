import os
import uuid
from collections import OrderedDict
from mikula.implementation.images import is_image
from mikula.implementation.md import render_markdown, INCLUDE_TEMPLATE


def discover(directory, image_format):
    nodes = tuple(os.walk(directory, topdown=False))
    parsed = OrderedDict()
    excluded = dict()
    for source_dir, subdirs, files in nodes:
        images = OrderedDict()
        index_content = ""
        index_meta = dict()
        path = os.path.relpath(directory, source_dir)
        for file in files:
            fn = os.path.join(source_dir, file)
            if "index.md" in file.lower():
                index_meta, index_content = render_markdown(fn)
                continue
            if is_image(fn):
                image_id = str(uuid.uuid4())
                image_file = f"{image_id}.{image_format.lower()}"
                basename, _ = os.path.splitext(file)
                markdown_fn = os.path.join(source_dir, f"{basename}.md")
                if os.path.isfile(markdown_fn):
                    meta, html = render_markdown(markdown_fn)
                    meta["title"] = meta.get("title", basename)
                else:
                    meta = {"title": basename}
                    html = INCLUDE_TEMPLATE
                images[file] = (image_file, meta, html)

        relative = os.path.relpath(source_dir, directory)

        if "thumbnail" in index_meta.keys():
            fn = index_meta["thumbnail"]
            if fn in images.keys():
                file_id, *rest = images[fn]
                index_meta["thumbnail"] = file_id
                should_remove = index_meta.get("exclude_thumbnail", False)
                if should_remove:
                    excluded[relative] = (fn, images[fn][0])
                    del images[fn]
        parsed[relative] = (path, subdirs, images, index_meta, index_content)
    # TODO: Add rendering of error.html template
    return parsed, excluded
