import setuptools
import os
import pathlib

with open("README.md", "r") as fh:
    long_description = fh.read()


PATH = os.path.dirname(__file__)


def include_data(themes_directory, *extra):
    content = list()
    path = pathlib.Path(themes_directory)
    for current, _, _ in os.walk(themes_directory):
        relative = os.path.relpath(current, path.parent)
        content.append(os.path.join(relative, "*"))
    content.extend(extra)
    return content


def get_version():
    with open(os.path.join(PATH, "mikula", "VERSION")) as version_file:
        version = version_file.read().strip()
    return version


print(include_data(os.path.join("mikula", "themes"),
                   "VERSION",
                    "LICENSE"))

setuptools.setup(
    name="mikula",
    version=get_version(),
    author="Roman Kosobrodov",
    author_email="mikula@kosobrodov.net",
    description="Static web gallery generator",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RomanKosobrodov/mikula",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        'mikula': include_data(os.path.join("mikula", "themes"), "VERSION")
    },
    scripts=['bin/mikula'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
    install_requires=[
        "boto3==1.10.26",
        "Jinja2==2.10.3",
        "Markdown==3.1.1",
        "Pillow==6.2.1",
        "PyYAML==5.1.2"
    ]
)
