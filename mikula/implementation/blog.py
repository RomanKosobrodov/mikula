import os
import glob
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import datetime
from collections import OrderedDict
from mikula.implementation.md import render_markdown, DEFAULT_PAGE_META
from mikula.implementation.settings import assets_dir
from mikula.implementation.images import convert_image


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
        parsed[basename] = (fn, meta, content)
    ordered_posts = OrderedDict(sorted(parsed.items(), key=lambda x: x[1][1]["date"]))
    return reversed(ordered_posts.items())


def render_post(post, page_list, output_directory, filename, template, config):
    _, meta, content = post
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

    url = os.path.join(f"{date.year}", f"{date.month:02d}", f"{date.day:02d}", filename)
    return url


def locate_thumbnail_file(post_source, thumbnail_path):
    if thumbnail_path is None:
        return None

    if os.path.isfile(thumbnail_path):
        return os.path.abspath(thumbnail_path)

    # filename without path in the same folder or with a path relative to post folder
    one_up = os.path.dirname(post_source)
    relative = os.path.join(one_up, thumbnail_path)
    if os.path.isfile(relative):
        return os.path.abspath(relative)

    # filename relative to root which is two levels above post_source
    relative = os.path.join(os.path.dirname(one_up), thumbnail_path)
    if os.path.isfile(relative):
        return os.path.abspath(relative)
    return None


def process_thumbnail(post_source, thumbnail_path, destination_fn, config):
    abs_path = locate_thumbnail_file(post_source, thumbnail_path)
    if abs_path is None:
        return None
    _, _, converted_fn = convert_image(original=abs_path,
                                       converted=os.path.basename(destination_fn),
                                       directory="",
                                       images_dst=None,
                                       thumbnails_dst=os.path.dirname(destination_fn),
                                       source_directory="",
                                       config=config)
    return converted_fn


def render_blog(posts, page_list, output_directory, theme, config):
    env = Environment(
        loader=FileSystemLoader(theme),
        autoescape=select_autoescape(['html', 'xml'])
    )
    post_template = env.get_template("post.html")
    blog_posts = list()
    for post, parsed in posts:
        fn, meta, _ = parsed
        filename = meta.get("permalink", post)
        url = render_post(parsed, page_list, output_directory, filename, post_template, config)
        date_str = meta["date"].strftime("%Y-%m-%d")
        title = meta.get("title", filename)
        thumbnail = meta.get("thumbnail", None)
        if thumbnail is not None:
            basename, ext = os.path.splitext(os.path.basename(thumbnail))
            image_ext = config.get("image_format", "png")
            destination_fn = os.path.join(output_directory, assets_dir, f"{basename}.{image_ext}")
            process_thumbnail(post_source=fn,
                              thumbnail_path=thumbnail,
                              destination_fn=destination_fn,
                              config=config)
            relative_thumbnail = os.path.relpath(destination_fn, os.path.join(output_directory, url))
        else:
            relative_thumbnail = None
        blog_posts.append((date_str, title, url, relative_thumbnail))
    blog_template = env.get_template("blog.html")

    padding = config.get("padding", 0.1)
    html = blog_template.render(root_="..",
                                page_list_=page_list,
                                posts_=blog_posts,
                                thumbnail_padding_=padding,
                                config_=config,
                                **meta)
    fn = os.path.join(output_directory, "blog", "index.html")
    with open(fn, "w") as fid:
        fid.write(html)

    print(blog_posts)
