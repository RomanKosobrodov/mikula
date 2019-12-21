import os
import uuid
import glob
from collections import OrderedDict
from mikula.implementation.images import is_image
from mikula.implementation.md import render_markdown, DEFAULT_ERROR, DEFAULT_PAGE_META
from mikula.implementation import settings
from mikula.implementation.util import walk

PAGES_DIR = settings.pages_source
IGNORED = settings.ignored


def parse_pages(source_directory):
    parsed = OrderedDict()
    pattern = os.path.join(source_directory, PAGES_DIR, "*.md")
    for fn in glob.glob(pattern):
        meta, content = render_markdown(fn, DEFAULT_PAGE_META)
        basename, _ = os.path.splitext(os.path.basename(fn))
        if "title" not in meta:
            meta["title"] = basename
        parsed[basename] = (meta, content)
    return parsed


def discover(directory, image_format):
    nodes = walk(directory, exclude=IGNORED, topdown=False)
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
                index_meta, index_content = render_markdown(fn, DEFAULT_PAGE_META)
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
                    html = ""
                meta["basename"] = basename
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

    top_dir, _, files = nodes[-1]
    if "error.md" in files:
        fn = os.path.join(top_dir, "error.md")
        error_meta, error_content = render_markdown(fn)
    else:
        error_meta = {"title": "Server Error", "page_title": "Server Error"}
        error_content = DEFAULT_ERROR

    return parsed, excluded, (error_meta, error_content)
