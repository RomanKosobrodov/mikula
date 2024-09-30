import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from mikula.implementation.md import DEFAULT_ERROR


def load_templates(theme_directory):
    templates = dict()
    env = Environment(
        loader=FileSystemLoader(theme_directory),
        autoescape=select_autoescape(['html', 'xml'])
    )
    templates["page"] = env.get_template("pages.html")
    templates["album"] = env.get_template("album.html")
    templates["image"] = env.get_template("image.html")
    templates["error"] = env.get_template("error.html")
    templates["post"] = env.get_template("post.html")
    templates["blog"] = env.get_template("blog.html")
    return templates


def create_page(page, page_list, destination_directory, filename, template, config):
    meta, content = page
    user_content = Template(content)
    html = template.render(user_content_=user_content,
                           page_list_=page_list,
                           config_=config,
                           **meta)
    fn = os.path.join(destination_directory, filename)
    with open(fn, "w", encoding="utf-8") as fid:
        fid.write(html)


def create_default_error_page(page_list, destination_directory, template, config):
    error_meta = {"title": "Server Error", "page_title": "Server Error"}
    error_content = DEFAULT_ERROR
    create_page(page=(error_meta, error_content),
                page_list=page_list,
                destination_directory=destination_directory,
                filename="error.html",
                template=template,
                config=config)


def create_redirect_page(meta, destination):
    if "index_page" in meta:
        if meta["index_page"]:
            target = os.path.join(meta["source"], "index.html")
            document = "<html><head>"
            document += f'<meta http-equiv="refresh" content="0; URL={target}" />\n'
            document += "</head><body></body></html>"
            with open(destination, "w", encoding="utf-8") as dst:
                dst.write(document)


def render_pages(pages, destination_directory, template, config):
    page_list = list()
    render_list = list()
    for basename, page in pages.items():
        fn = f"{basename}.html"
        meta, _ = page
        blog_page = meta.get("render_blog_here", False)
        if blog_page:
            fn = "blog/index.html"
            page_list.append((meta["title"], fn))
            continue
        home_page = meta.get("render_gallery_here", False)
        if home_page:
            fn = "index.html"
        else:
            render_list.append((page, fn))
        hidden = meta.get("hidden", False)
        if not hidden:
            page_list.append((meta["title"], fn))

    for content, fn in render_list:
        create_page(content, page_list, destination_directory, fn, template, config)

    return page_list
