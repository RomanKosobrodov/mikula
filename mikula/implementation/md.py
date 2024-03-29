import markdown
import yaml
import copy

DEFAULT_ERROR = "<p class='error-message'>Something bad happened. Please visit the site later.</p>"
DEFAULT_PAGE_META = {"place_before": False}
REPLACEMENTS = {"(c)": "&#169;",
                "(C)": "&#9400;",
                "(r)": "&#174;",
                "(R)": "&#174;",
                "(tm)": "&#8482;",
                "(TM)": "&#8482;",
                "(p)": "&#167;",
                "(P)": "&#167;",
                "+-":  "&#177;"}


def replace_typographics(document):
    for rep, code in REPLACEMENTS.items():
        document = document.replace(rep, code)
    return document


def extract_meta(document, defaults):
    if defaults is None:
        metadata = dict()
    else:
        metadata = copy.deepcopy(defaults)

    parts = document.lstrip().split("---")
    if len(parts) > 2 and parts[0] == "":
        meta = parts[1]
        from_yaml = yaml.load(meta, yaml.Loader)
        metadata.update(from_yaml)
        if len(parts) == 3:   # no `---` in the rest of the document
            rest = parts[2]
        else:
            rest = "---".join(parts[2:])
        return metadata, rest.lstrip()
    else:
        return metadata, document


def parse_markdown(md_file, meta_defaults):
    with open(file=md_file, mode="r", encoding="utf-8") as fid:
        content = fid.read()
    meta, document = extract_meta(content, meta_defaults)
    return meta, document


def render_document(document):
    html = markdown.markdown(document, extensions=['extra'])
    return replace_typographics(html)


def render_markdown(md_file, meta_defaults=None):
    meta, document = parse_markdown(md_file, meta_defaults)
    html = render_document(document)
    return meta, html
