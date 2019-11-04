import os
import markdown
import io
from PIL import Image

from jinja2 import Environment, PackageLoader, select_autoescape

EXIF_ORIENTATION = 0x0112
ROTATION = {3: 180, 6: 270, 8: 90}


def extension(file):
    _, ext = os.path.splitext(file)
    ext = ext.lower()
    return ext[1:]


def create(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def create_directories(parsed, output_directory):
    create(output_directory)
    assets_dir = os.path.join(output_directory, "assets")
    create(assets_dir)
    images_dir = os.path.join(assets_dir, "images")
    create(images_dir)
    thumbnails_dir = os.path.join(images_dir, "thumbnails")
    create(thumbnails_dir)
    styles_dir = os.path.join(assets_dir, "styles")
    create(styles_dir)

    destination = list()
    root_directory = parsed[0][0]
    for parent, subdirs, files in parsed:
        rerooted = parent.replace(root_directory, output_directory)
        destination.append((rerooted, subdirs, files))
        for subdir in subdirs:
            new_path = os.path.join(rerooted, subdir)
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
    return destination


def process_images(source_dir, source_files, destination_dir, height=600, format="png"):
    ignored = ["txt", "html", "md", "json", "yml", "yaml"]
    for file in source_files:
        if extension(file) in ignored:
            continue
        file_path = os.path.join(source_dir, file)
        try:
            img = Image.open(file_path)
            exif = img._getexif()
            if exif is not None:
                if EXIF_ORIENTATION in exif.keys():
                    code = exif[EXIF_ORIENTATION]
                    angle = ROTATION[code]
                    img = img.rotate(angle, expand=True)
            aspect = img.height / img.width
            width = int(height / aspect)
            img = img.resize((width, height), Image.ANTIALIAS)
            base, _ = os.path.splitext(file)
            destination = os.path.join(destination_dir, f"{base}.{format}")
            img.save(destination, format=format)
            img.close()
        except IOError:
            print(f"unknown format of image file: '{file_path}'")


def render_markdown(md):
    buffer = io.BytesIO()
    markdown.markdownFromFile(input=md, output=buffer)
    output = buffer.getvalue()
    return output.decode()


def render_page(index_file, destination_dir, page_template, top_level):
    div_token = "<p><code>images</code></p>"
    html = render_markdown(index_file)
    gen = os.walk(destination_dir)
    current, subdirs, files = next(gen)
    files = [f for f in files if "index.html" not in f]
    if top_level:
        previous = None
    else:
        previous = os.path.join(os.path.dirname(current), "index.html")
    albums = [os.path.join(s, "index.html") for s in subdirs]
    image_div = page_template.render(previous=previous, albums=albums, images=files)
    html = html.replace(div_token, image_div)
    filename = os.path.join(destination_dir, "index.html")
    with open(filename, "w") as fid:
        fid.write(html)


def build_from(directory, output):
    env = Environment(
        loader=PackageLoader('gal', './themes/default'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    nodes = tuple(os.walk(directory))
    destination_nodes = create_directories(nodes, output)
    indices = range(len(nodes))
    for index in reversed(indices):
        source_dir, subdirs, files = nodes[index]
        destination_dir = destination_nodes[index][0]
        process_images(source_dir, files, destination_dir)

        files_lower = [f.lower() for f in files]
        if "index.md" in files_lower:
            filepath = os.path.join(source_dir, "index.md")
        else:
            filepath = "./themes/default/index.md"

        template = env.get_template("page.html")
        top_level = (index == 0)
        render_page(filepath, destination_dir, template, top_level=top_level)
