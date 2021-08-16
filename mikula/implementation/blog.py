import os
import glob
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
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
    return reversed(ordered_posts.items())


def render_post(post, page_list, output_directory, filename, template, config):
    meta, content = post
    user_content = Template(content)
    html = template.render(user_content_=user_content,
                           page_list_=page_list,
                           config_=config,
                           **meta)
    date = meta["date"]
    directory = os.path.join(output_directory, "blog", f"{date.year}", f"{date.month:02d}", f"{date.day:02d}")
    os.makedirs(directory, exist_ok=True)
    fn = os.path.join(directory, filename)
    with open(fn, "w") as fid:
        fid.write(html)


def render_blog(posts, page_list, output_directory, theme, config):
    env = Environment(
        loader=FileSystemLoader(theme),
        autoescape=select_autoescape(['html', 'xml'])
    )
    post_template = env.get_template("post.html")
    for post, parsed in posts:
        meta, _ = parsed
        filename = meta.get("permalink", post)
        render_post(parsed, page_list, output_directory, filename, post_template, config)
    # blog_template = env.get_template("blog.html")