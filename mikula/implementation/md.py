import markdown
import yaml
import re


IMAGES_TOKEN = "<p><code>images</code></p>"
INCLUDE_TEMPLATE = "{% include auto_generated %}"
DEFAULT_ERROR = "<p class='error-message'>Something bad happened. Please visit the site later.</p>"
import markdown
import yaml
import re


IMAGES_TOKEN = "<p><code>images</code></p>"
INCLUDE_TEMPLATE = "{% include auto_generated %}"
DEFAULT_ERROR = "<p class='error-message'>Something bad happened. Please visit the site later.</p>"

def extract_meta(document):
    def remove_first_line(text):
        split = text.splitlines()
        return "\n".join(split[1:])

    pattern = r"(?<=---\n)(?P<meta>.+(?=---))(?P<rest>.+)"
    compiled = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    matched = compiled.search(document)
    if matched is not None:
        meta = matched.group("meta")
        metadata = yaml.load(meta, yaml.Loader)
        rest = matched.group("rest")
        return metadata, remove_first_line(rest)
    else:
        return dict(), document


def render_markdown(md_file):
    with open(md_file, "r") as fid:
        content = fid.read()
    meta, document = extract_meta(content)
    html = markdown.markdown(document)
    if IMAGES_TOKEN not in html:
        html += "\n" + IMAGES_TOKEN
    html = html.replace(IMAGES_TOKEN, INCLUDE_TEMPLATE)
    return meta, html


def extract_meta(document):
    def remove_first_line(text):
        split = text.splitlines()
        return "\n".join(split[1:])

    pattern = r"(?<=---\n)(?P<meta>.+(?=---))(?P<rest>.+)"
    compiled = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    matched = compiled.search(document)
    if matched is not None:
        meta = matched.group("meta")
        metadata = yaml.load(meta, yaml.Loader)
        rest = matched.group("rest")
        return metadata, remove_first_line(rest)
    else:
        return dict(), document


def render_markdown(md_file, add_default_template=True):
    with open(md_file, "r") as fid:
        content = fid.read()
    meta, document = extract_meta(content)
    html = markdown.markdown(document)
    if IMAGES_TOKEN not in html and add_default_template:
        html += "\n" + IMAGES_TOKEN
    html = html.replace(IMAGES_TOKEN, INCLUDE_TEMPLATE)
    return meta, html
