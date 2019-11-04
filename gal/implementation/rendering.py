import markdown
import io
import os


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
