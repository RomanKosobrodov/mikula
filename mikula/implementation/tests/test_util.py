from mikula.implementation.util import walk
import os
import shutil

DIR_TREE = (("one", ["1", "2", "3"]),
            ("two", ["12", "22", "3"]),
            ("three", ["22", "33", "3"]))
EXCLUDE = ("3", "22")

def build_directory_tree(destination, dir_tree):
    if not os.path.isdir(destination):
        os.mkdir(destination)
    else:
        shutil.rmtree(destination)

    for parent, subdirs in dir_tree:
        path = os.path.join(destination, parent)
        os.mkdir(path)
        for subdir in subdirs:
            dir_name = os.path.join(path, subdir)
            os.mkdir(dir_name)


def run_walk(topdown):
    dst = os.path.join(os.path.dirname(__file__), "data")
    build_directory_tree(dst, DIR_TREE)
    result = walk(dst, exclude=EXCLUDE, topdown=topdown)
    shutil.rmtree(dst)
    for r, s, f in result:
        basename = os.path.basename(r)
        assert basename not in EXCLUDE
    return result


def test_walk():
    td = run_walk(topdown=True)
    dt = run_walk(topdown=False)
    assert len(td) == len(dt)
    dt.reverse()
    assert td == dt


if __name__ == "__main__":
    test_walk()
