import os
import glob
import datetime
import re
import shutil
import uuid
from jinja2 import Template
from collections import OrderedDict
from mikula.implementation.md import parse_markdown, render_document, DEFAULT_PAGE_META
from mikula.implementation.settings import assets_dir
from mikula.implementation.images import convert_image
from mikula.implementation.discovery import should_convert


def parse_blog_directory(blog_directory):
    parsed = OrderedDict()
    pattern = os.path.join(blog_directory, f"*.md")
    filelist = glob.glob(pattern)
    for fn in filelist:
        basename, ext = os.path.splitext(os.path.basename(fn))
        meta, document = parse_markdown(fn, DEFAULT_PAGE_META)
        if "title" not in meta:
            meta["title"] = basename
        meta["date"] = meta.get("date", get_file_date(fn))
        parsed[basename] = (fn, meta, document)
    ordered_posts = OrderedDict(sorted(parsed.items(), key=lambda x: x[1][1]["date"]))
    return reversed(ordered_posts.items())


def get_file_date(fn):
    timestamp = os.path.getmtime(fn)
    return datetime.datetime.fromtimestamp(timestamp)


def find_markdown_images(content):
    md_image = r"!\[[^\]]*\]\((?P<filename>.*?)\s*(?=\"|\))(\".*\")?\)"
    r = re.compile(md_image)
    result = r.findall(content)
    return result


def find_local_resources(content):
    md_link = r"\[(?P<text>.*?)\]\((?P<url>.*?)\)"
    r = re.compile(md_link)
    return r.findall(content)


def locate_referenced_file(post_source, reference_path):
    if reference_path is None:
        return None

    if os.path.isfile(reference_path):
        return os.path.abspath(reference_path)

    # filename without path in the same folder or with a path relative to post folder
    one_up = os.path.dirname(post_source)
    relative = os.path.join(one_up, reference_path)
    if os.path.isfile(relative):
        return os.path.abspath(relative)

    # filename relative to root which is two levels above post_source
    relative = os.path.join(os.path.dirname(one_up), reference_path)
    if os.path.isfile(relative):
        return os.path.abspath(relative)
    return None


def process_post_resource(post_source, link_source, output_directory):
    abs_path = locate_referenced_file(post_source, link_source)
    if abs_path is None:
        return None

    destination_dir = os.path.join(os.path.dirname(output_directory), assets_dir)
    if not os.path.isdir(destination_dir):
        os.mkdir(destination_dir)

    destination_fn = os.path.join(destination_dir, os.path.basename(abs_path))
    shutil.copyfile(abs_path, destination_fn)
    return destination_fn


def process_post_image(post_source, image_path, is_thumbnail, output_directory,
                       config, config_changed, image_format, cache):
    abs_path = locate_referenced_file(post_source, image_path)
    if abs_path is None:
        return None

    destination_dir = os.path.join(os.path.dirname(output_directory), assets_dir)
    if not os.path.isdir(destination_dir):
        os.mkdir(destination_dir)

    update_required, _, _, _, image_file = should_convert(filename=abs_path,
                                                          cache=cache.to_dictionary(),
                                                          config_changed=config_changed,
                                                          image_format=image_format)
    if update_required:
        fn, image_fn, thumbnail_fn = convert_image(original=abs_path,
                                                   converted=image_file,
                                                   directory="",
                                                   images_dst=destination_dir if not is_thumbnail else None,
                                                   thumbnails_dst=destination_dir if is_thumbnail else None,
                                                   source_directory="",
                                                   config=config)
        cache.update(fn, image_fn, thumbnail_fn)

    destination_fn = os.path.join(destination_dir, image_file)
    return destination_fn


def process_post(content_filename, document, output_directory, rendered_url, config, cache):
    converted = document
    image_format = config.get("image_format", "jpeg")
    config_changed = cache.config_changed(config)

    for image_source, _ in find_markdown_images(document):
        destination_fn = process_post_image(post_source=content_filename,
                                            image_path=image_source,
                                            is_thumbnail=False,
                                            output_directory=output_directory,
                                            config=config,
                                            config_changed=config_changed,
                                            image_format=image_format,
                                            cache=cache)
        if destination_fn is not None:
            relative = os.path.relpath(destination_fn, os.path.join(output_directory, rendered_url))
            if os.path.sep == "\\":
                relative = relative.replace(os.path.sep, "/")
            converted = converted.replace("](" + image_source, "](" + relative, 1)

    for link_text, link_file in find_local_resources(converted):
        destination_fn = process_post_resource(post_source=content_filename,
                                               link_source=link_file,
                                               output_directory=output_directory)
        if destination_fn is not None:
            relative = os.path.relpath(destination_fn, os.path.join(output_directory, rendered_url))
            if os.path.sep == "\\":
                relative = relative.replace(os.path.sep, "/")
            old_src = f"[{link_text}]({link_file})"
            new_src = f"[{link_text}]({relative})"
            converted = converted.replace(old_src, new_src, 1)
    return converted


def render_post(post, page_list, output_directory, filename, template, config, cache):
    source_fn, meta, document = post
    date = meta["date"]
    if "page_title" not in meta.keys() and "title" in meta.keys():
        meta["page_title"] = meta["title"]
    directory = os.path.join(output_directory, f"{date.year}", f"{date.month:02d}", f"{date.day:02d}")
    os.makedirs(directory, exist_ok=True)
    fn = os.path.join(directory, filename)
    url = os.path.join(f"{date.year}", f"{date.month:02d}", f"{date.day:02d}", filename)

    converted = process_post(content_filename=source_fn,
                             document=document,
                             output_directory=output_directory,
                             rendered_url=url,
                             config=config,
                             cache=cache)

    content = render_document(converted)
    user_content = Template(content)
    html = template.render(user_content_=user_content,
                           page_list_=page_list,
                           config_=config,
                           **meta)

    with open(file=fn, mode="w", encoding="utf-8") as fid:
        fid.write(html)

    return url


def render_blog(blog_directory, blog_metadata, page_list, output_directory, templates, config, cache):
    post_template = templates["post"]
    blog_posts = list()

    image_format = config.get("image_format", "jpeg")
    config_changed = cache.config_changed(config)

    for post, parsed in parse_blog_directory(blog_directory):
        fn, meta, _ = parsed
        filename = meta.get("permalink", post)
        url = render_post(post=parsed,
                          page_list=page_list,
                          output_directory=output_directory,
                          filename=filename,
                          template=post_template,
                          config=config,
                          cache=cache)
        date_str = meta["date"].strftime("%Y-%m-%d")
        title = meta.get("title", filename)
        thumbnail = meta.get("thumbnail", None)
        if thumbnail is not None:
            destination_fn = process_post_image(post_source=fn,
                                                image_path=thumbnail,
                                                is_thumbnail=True,
                                                output_directory=output_directory,
                                                config=config,
                                                config_changed=config_changed,
                                                image_format=image_format,
                                                cache=cache)
            if destination_fn is None:
                print(f'Warning: Unable to find thumbnail file "{thumbnail}" defined in file "{fn}"')
                relative_thumbnail = None
            else:
                relative_thumbnail = os.path.relpath(destination_fn, os.path.join(output_directory, url))
        else:
            relative_thumbnail = None
        blog_posts.append((date_str, title, url, relative_thumbnail))

    if len(blog_posts) > 0:
        blog_template = templates["blog"]
        padding = config.get("padding", 0.1)
        html = blog_template.render(root_="",
                                    page_list_=page_list,
                                    posts_=blog_posts,
                                    thumbnail_padding_=padding,
                                    config_=config,
                                    **blog_metadata)
        fn = os.path.join(output_directory, "index.html")
        with open(fn, "w", encoding="utf-8") as fid:
            fid.write(html)
