import setuptools
import os
import pathlib

with open("README.md", "r") as fh:
    long_description = fh.read()


def include_themes(themes_directory):
    wildcards = list()
    path = pathlib.Path(themes_directory)
    for current, _, _ in os.walk(themes_directory):
        relative = os.path.relpath(current, path.parent)
        wildcards.append(os.path.join(relative, "*"))
    return wildcards


setuptools.setup(
    name="mikula",
    version="0.0.3",
    author="Roman Kosobrodov",
    author_email="mikula@kosobrodov.net",
    description="Static web gallery generator",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RomanKosobrodov/mikula",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_data={
        'mikula': include_themes("mikula/themes")
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
