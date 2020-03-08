from mikula.implementation.customize import customize
import tempfile
import os


REQUIRED_TEMPLATES = ("album.html", "error.html", "image.html", "pages.html")


def test_customize():
    with tempfile.TemporaryDirectory() as tmp_dir:
        theme = "vibrant"
        prototype = "default"
        customize(theme=theme, prototype=prototype, destination=tmp_dir)
        path = os.path.join(tmp_dir, theme)
        assert os.path.isdir(path)

        for template in REQUIRED_TEMPLATES:
            assert os.path.isfile(os.path.join(path, template))

        path = os.path.join(path, "assets")
        assert os.path.isdir(path)

        assert os.path.isdir(os.path.join(path, "images"))
        assert os.path.isdir(os.path.join(path, "styles"))


if __name__ == "__main__":
    test_customize()
