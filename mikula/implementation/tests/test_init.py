from mikula.implementation.initialise import initialise
import tempfile
import os


def test_init():
    with tempfile.TemporaryDirectory() as tmp_dir:
        initialise(root=tmp_dir)
        assert os.path.isdir(os.path.join(tmp_dir, "source", "__assets__"))
        assert os.path.isdir(os.path.join(tmp_dir, "source", "__pages__"))
        assert os.path.isfile(os.path.join(tmp_dir, "source", "index.md"))
        assert os.path.isdir(os.path.join(tmp_dir, "build"))


if __name__ == "__main__":
    test_init()
