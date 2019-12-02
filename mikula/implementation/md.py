import markdown
import yaml
import re
import copy

DEFAULT_ERROR = "<p class='error-message'>Something bad happened. Please visit the site later.</p>"
DEFAULT_PAGE_META = {"place_before": False}


def extract_meta(document, defaults):
    def remove_first_line(text):
        split = text.splitlines()
        return "\n".join(split[1:])

    pattern = r"(?<=---\n)(?P<meta>.+(?=---))(?P<rest>.+)"
    compiled = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    matched = compiled.search(document)
    if defaults is None:
        metadata = dict()
    else:
        metadata = copy.deepcopy(defaults)
    if matched is not None:
        meta = matched.group("meta")
        from_yaml = yaml.load(meta, yaml.Loader)
        metadata.update(from_yaml)
        rest = matched.group("rest")
        return metadata, remove_first_line(rest)
    else:
        return metadata, document


def render_markdown(md_file, meta_defaults=None):
    with open(md_file, "r") as fid:
        content = fid.read()
    meta, document = extract_meta(content, meta_defaults)
    html = markdown.markdown(document)
    return meta, html
