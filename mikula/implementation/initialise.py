import os
import shutil

SKELETON_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "skeleton")


def make_directory(directory, root):
    full_path = os.path.abspath(os.path.join(root, directory))
    if os.path.isdir(full_path):
        return full_path
    os.mkdir(full_path)
    return full_path


def initialise(root=None):
    if root is None:
        root = os.path.join(os.getcwd())
    shutil.copytree(SKELETON_DIR, root, dirs_exist_ok=True)
    source_path = os.path.abspath(os.path.join(root, "source"))
    print("Gallery initialised.")
    print(f'Start adding your pictures and captions into "{source_path}"')
    print("Run `mikula build` to generate your gallery and `mikula serve` to test it.")
