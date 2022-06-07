import os
import uuid
from collections import OrderedDict
from mikula.implementation.images import is_image, get_image_info
from mikula.implementation.md import render_markdown, DEFAULT_PAGE_META
from mikula.implementation.util import walk
from mikula.implementation.image_cache import query
from functools import partial
from multiprocessing import Pool


SORT_BY_DATE = 0
SORT_BY_NAME = 1
SORT_BY_ORDER = 2
SORT_METHOD = {"date": SORT_BY_DATE, "name": SORT_BY_NAME, "order": SORT_BY_ORDER}


def node_parser(node, directory, album_index, cache, config_changed, sort_code, image_format):
    source_dir, subdirs, files = node
    images = OrderedDict()
    index_content = ""
    index_meta = dict()
    path = os.path.relpath(directory, source_dir)
    file_index = len(files)

    excluded = None

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
                cache_data = None
            else:
                cache_data = query(cache, fn)

            if cache_data is None:
                image_id = str(uuid.uuid4())
                image_file = f"{image_id}.{image_format.lower()}"
                update_required = True
            else:
                image_file, _ = cache_data
                image_file = os.path.basename(image_file)
                update_required = False

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
                excluded = (fn, images[fn][0])
                del images[fn]
    parsed = (path, subdirs, images, index_meta, index_content)

    return relative, parsed, excluded


def discover(directory, config, cache):
    image_format = config.get("image_format", "jpeg")
    config["image_format"] = image_format
    sort_by = config.get("sort_by", "name")
    config["sort_by"] = sort_by

    config_changed = cache.config_changed(config)
    if config_changed:
        cache.reset()
        cache.update_config(config)

    nodes = walk(directory, topdown=False)
    parsed = OrderedDict()
    excluded = dict()

    runner = partial(node_parser,
                     directory=directory,
                     album_index=len(nodes),
                     cache=cache.to_dictionary(),
                     config_changed=config_changed,
                     sort_code=SORT_METHOD.get(sort_by.lower(), "name"),
                     image_format=config["image_format"])

    num_processes = config.get("parallel_workers", None)
    with Pool(processes=num_processes) as pool:
        for relative, node_parsed, node_excluded in pool.imap(runner, nodes):
            parsed[relative] = node_parsed
            print(f'parsing "{relative}"')
            if node_excluded is not None:
                excluded[relative] = node_excluded
    return parsed, excluded, config_changed
