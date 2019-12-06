import os
import pathlib


def include_themes(themes_directory):
    wildcards = list()
    path = pathlib.Path(themes_directory)
    for current, _, _ in os.walk(themes_directory):
        relative = os.path.relpath(current, path.parent)
        wildcards.append(os.path.join(relative, "*"))
    return wildcards


def test_include_themes():
    current = os.path.dirname(__file__)
    themes = os.path.abspath(os.path.join(current, "../themes"))
    output = include_themes(themes)
    assert len(output) > 0


if __name__ == "__main__":
    test_include_themes()