import os
from jinja2 import Template


def create_page(page, page_list, destination_directory, filename, template, config):
    meta, content = page
    user_content = Template(content)
    html = template.render(user_content_=user_content,
                           page_list_=page_list,
                           config_=config,
                           **meta)
    fn = os.path.join(destination_directory, filename)
    with open(fn, "w") as fid:
        fid.write(html)


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
