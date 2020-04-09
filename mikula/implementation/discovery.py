import os
import uuid
import glob
from collections import OrderedDict
from mikula.implementation.images import is_image, get_image_info
from mikula.implementation.md import render_markdown, DEFAULT_ERROR, DEFAULT_PAGE_META
from mikula.implementation.hypertext import render_hypertext
from mikula.implementation import settings
from mikula.implementation.util import walk


PAGES_DIR = settings.pages_source
IGNORED = settings.ignored
SORT_BY_DATE = 0
SORT_BY_NAME = 1
SORT_BY_ORDER = 2
SORT_METHOD = {"date": SORT_BY_DATE, "name": SORT_BY_NAME, "order": SORT_BY_ORDER}


def parse_pages(source_directory):
    parsed = OrderedDict()
    extensions = ['md', 'html']
    filelist = list()
    for e in extensions:
        pattern = os.path.join(source_directory, PAGES_DIR, f"*.{e}")
        filelist.extend(glob.glob(pattern))
    index = len(filelist)
    for fn in filelist:
        basename, ext = os.path.splitext(os.path.basename(fn))
        if ext == '.md':
            meta, content = render_markdown(fn, DEFAULT_PAGE_META)
        else:
            meta, content = render_hypertext(fn, DEFAULT_PAGE_META)
        if "title" not in meta:
            meta["title"] = basename
        meta["order"] = meta.get("order", index)
        index = index + 1
        parsed[basename] = (meta, content)
    ordered_pages = OrderedDict(sorted(parsed.items(), key=lambda x: x[1][0]["order"]))
    return ordered_pages


def discover(directory, config, cache):
    image_format = config.get("image_format", "jpeg")
    config["image_format"] = image_format
    sort_by = config.get("sort_by", "name")
    config["sort_by"] = sort_by

    config_changed = cache.config_changed(config)
    if config_changed:
        cache.reset()
        cache.update_config(config)

    sort_code = SORT_METHOD.get(sort_by.lower(), "name")
    nodes = walk(directory, exclude=IGNORED, topdown=False)
    parsed = OrderedDict()
    excluded = dict()
    album_index = len(nodes)
    for source_dir, subdirs, files in nodes:
        images = OrderedDict()
        index_content = ""
        index_meta = dict()
        path = os.path.relpath(directory, source_dir)
        file_index = len(files)
        for file in files:
            fn = os.path.join(source_dir, file)
            if "index.md" in file.lower():
                index_meta, index_content = render_markdown(fn, DEFAULT_PAGE_META)
                index_meta["order"] = index_meta.get("order", album_index)
                album_index += 1
                continue
            if is_image(fn):
                aspect, image_date, exif = get_image_info(fn)
                if config_changed:
                    update_required = True
                else:
                    update_required = cache.require_update(fn)

                if update_required:
                    image_id = str(uuid.uuid4())
                    image_file = f"{image_id}.{image_format.lower()}"
                else:
                    image_file, thumbnail_file = cache.get_filenames()
                    image_file = os.path.basename(image_file)

                basename, _ = os.path.splitext(file)
                markdown_fn = os.path.join(source_dir, f"{basename}.md")
                if os.path.isfile(markdown_fn):
                    meta, html = render_markdown(markdown_fn)
                    meta["title"] = meta.get("title", basename)
                else:
                    meta = {"title": basename}
                    html = ""
                meta["basename"] = basename
                if sort_code == SORT_BY_DATE:
                    meta["order"] = image_date
                elif sort_code == SORT_BY_NAME:
                    meta["order"] = os.path.basename(fn)
                else:
                    meta["order"] = meta.get("order", file_index)
                    file_index += 1
                images[file] = (image_file, meta, html, aspect, exif, update_required)

        images = OrderedDict(sorted(images.items(), key=lambda x: x[1][1]["order"]))

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

    return parsed, excluded, (error_meta, error_content), config_changed
