import os
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader, select_autoescape

from gal.implementation.rendering import parse_subdirectories, parse_images, render_album_page


TEST_ALBUM = {
    os.path.normpath("../images/album_one/day_one"): ([],
                                                      [('teapot.JPG', '26a03', {}, '')],
                                                      {},
                                                      '<h1>Japanese tea pot</h1>'),
    os.path.normpath("../images/album_one"): (['day_one'],
                                              [('donkey.jpg', '7b2dd', {}, ''),
                                               ('tanuki.jpg', 'b5b04', {'title': 'Friendly Tanuki'}, '<h1>Tanuki</h1>')],
                            {'title': 'animals'}, '<p><code>images</code></p>\n<h1>Album One</h1>'),
    os.path.normpath("../images/album_two"): ([], [('thistle.JPG', '8c532', {}, ''), ('frontyard.JPG', '99438', {}, '')],
                            {'title': 'flowers'}, '<h1>Flowers</h1>'),
    os.path.normpath("../images"): (['album_one', 'album_two'], [], {'title': 'Sample Gallery'}, '<h1>Gallery Title</h1>')
}


album = OrderedDict(TEST_ALBUM)
keys = tuple(album.keys())
index_top = len(keys) - 1
destination = "."


env = Environment(
    loader=FileSystemLoader(os.path.normpath("../../themes/default")),
    autoescape=select_autoescape(['html', 'xml'])
)
album_template = env.get_template("album.html")
image_template = env.get_template("image.html")


def test_process_subdirectories():
    output, fn = parse_subdirectories(keys=keys, album=album, index=index_top, destination=destination)
    ref = [("animals", os.path.normpath("./album_one/index.html")),
           ("flowers", os.path.normpath("./album_two/index.html"))]
    assert output == ref
    ref_filename = os.path.normpath(os.path.join(destination, "index.html"))
    assert fn == ref_filename


def test_process_images():
    index = 2
    output = parse_images(keys=keys, album=album, index=index, destination=destination)
    assert output == [('thistle', os.path.normpath('./assets/images/thumbnails/8c532.JPG')),
                      ('frontyard', os.path.normpath('./assets/images/thumbnails/99438.JPG'))]

    index = index_top
    output = parse_images(keys=keys, album=album, index=index, destination=destination)
    assert output == []


def test_render_album_page():
    output, filename = render_album_page(album, keys, index_top, album_template, destination)


if __name__ == "__main__":
    test_process_subdirectories()
    test_process_images()
    test_render_album_page()
