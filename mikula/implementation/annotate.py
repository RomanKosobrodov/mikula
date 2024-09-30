from mikula.implementation.images import is_image
from mikula.implementation.settings import source_dir
from mikula.implementation.util import walk
from mikula.implementation.md import parse_markdown
import os

skip_directories = ("_assets_", "blog")


def annotate(source):
    src = os.path.join(os.getcwd(), source)
    if source == "":
        src = os.path.join(os.getcwd(), source_dir)
    nodes = walk(src, topdown=False, exclude=skip_directories)
    for node in nodes:
        parent, dirs, files = node
        if os.path.basename(parent) in skip_directories:
            continue

        thumbnail = None
        annotation = "---\n"
        if "index.md" in files:
            fn = os.path.join(parent, "index.md")
            meta, _ = parse_markdown(fn, meta_defaults=dict())
            if "thumbnail" in meta and "exclude_thumbnail" in meta and meta["exclude_thumbnail"]:
                thumbnail = meta["thumbnail"]
            if "meta" in meta:
                annotation += "meta:\n"
                for k, v in meta["meta"].items():
                    annotation += f"  {k}: {v}\n"

        order = 0
        for file in files:
            fn = os.path.join(parent, file)
            if file == thumbnail:
                continue
            if is_image(fn):
                order += 1
                abs_name, _ = os.path.splitext(file)
                markdown_fn = os.path.join(parent, os.path.basename(abs_name) + ".md")
                if not os.path.isfile(markdown_fn):
                    with open(markdown_fn, "w", encoding="utf-8") as fid:
                        fid.write(annotation)
                        fid.write(f"order: {order}\n")
                        fid.write(f"title: {file}\n")
                        fid.write("---\n")
