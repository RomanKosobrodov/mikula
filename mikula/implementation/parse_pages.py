import os
import glob
from collections import OrderedDict
from mikula.implementation.md import render_markdown, DEFAULT_PAGE_META
from mikula.implementation.hypertext import render_hypertext
from mikula.implementation.util import directory_basename


def parse_pages(source_directory):
    parsed = OrderedDict()
    file_list = list()
    for e in ('md', 'html'):
        pattern = os.path.join(source_directory, f"*.{e}")
        file_list.extend(glob.glob(pattern))
    index = len(file_list)
    for fn in file_list:
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


def generate_page_list(pages):
    page_list = list()
    for page, parsed in pages.items():
        meta, content = parsed
        hidden_page = meta.get("hidden", False)
        if hidden_page:
            continue
        title = meta["title"]
        url = f"{page}.html"
        if "source" in meta:
            basename = directory_basename(meta["source"])
            url = os.path.join(basename, "index.html")
        page_list.append((title, url))
    return page_list

