import os
import shutil

SKELETON_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "skeleton")


def make_directory(directory, root):
    full_path = os.path.abspath(os.path.join(root, directory))
    if os.path.isdir(full_path):
        return full_path
    os.mkdir(full_path)
    return full_path


def initialise(root=os.path.join(os.getcwd())):
    source_dir = make_directory("source", root)
    shutil.copytree(SKELETON_DIR, source_dir, dirs_exist_ok=True)
    make_directory("build", root)
    print("Gallery initialised.")
    print(f'Start adding your pictures and captions into "{source_dir}"')
    print("Run `mikula build` to generate your gallery and `mikula serve` to test it.")
