import markdown
import io
import os


def render_markdown(md):
    buffer = io.BytesIO()
    markdown.markdownFromFile(input=md, output=buffer)
    output = buffer.getvalue()
    return output.decode()


def get_links(page_list, index):
    if index < 0 or index >= len(page_list):
        return None
    return page_list[index]


def render_page(index_file, destination_node, image_list, album_template, image_template, top_level):
    div_token = "<p><code>images</code></p>"
    html = render_markdown(index_file)
    current, subdirs, _ = destination_node
    if top_level:
        previous = None
    else:
        previous = os.path.join(os.path.dirname(current), "index.html")
    albums = [os.path.join(s, "index.html") for s in subdirs]

    page_names = [f"{basename}.html" for basename, _, _ in image_list]
    thumbnails = list()
    for index, element in enumerate(image_list):
        basename, thumbnail, path = element
        previous_page = get_links(page_names, index - 1)
        next_page = get_links(page_names, index + 1)
        filename = os.path.join(current, page_names[index])
        this_album = "index.html"
        image_page = image_template.render(image=path,
                                           album=this_album,
                                           previous=previous_page,
                                           next=next_page)
        with open(filename, "w") as fid:
            fid.write(image_page)
        thumbnail_url = os.path.relpath(thumbnail, current)
        image_page = os.path.relpath(filename, current)
        thumbnails.append((image_page, thumbnail_url))

    image_div = album_template.render(previous=previous, albums=albums, thumbnails=thumbnails)
    html = html.replace(div_token, image_div)
    filename = os.path.join(current, "index.html")
    with open(filename, "w") as fid:
        fid.write(html)
