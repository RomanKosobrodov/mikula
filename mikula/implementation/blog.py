import os
import glob
import datetime
from collections import OrderedDict
from mikula.implementation.md import render_markdown, DEFAULT_PAGE_META


def get_file_date(fn):
    timestamp = os.path.getmtime(fn)
    return datetime.datetime.fromtimestamp(timestamp)


def parse_blog_directory(blog_directory):
    parsed = OrderedDict()
    pattern = os.path.join(blog_directory, f"*.md")
    filelist = glob.glob(pattern)
    for fn in filelist:
        basename, ext = os.path.splitext(os.path.basename(fn))
        meta, content = render_markdown(fn, DEFAULT_PAGE_META)
        if "title" not in meta:
            meta["title"] = basename
        meta["date"] = meta.get("date", get_file_date(fn))
        parsed[basename] = (meta, content)
    ordered_posts = OrderedDict(sorted(parsed.items(), key=lambda x: x[1][0]["date"]))
    return reversed(ordered_posts)
