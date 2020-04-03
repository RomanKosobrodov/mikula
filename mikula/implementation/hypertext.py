from mikula.implementation.md import extract_meta
from jinja2 import Template


def render_hypertext(html_file, meta_defaults=None):
    with open(html_file, "r") as fid:
        content = fid.read()
    meta, document = extract_meta(content, meta_defaults)
    user_content = Template(document)
    html = user_content.render(**meta)
    return meta, html
