import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mikula",
    version="0.0.1",
    author="Roman Kosobrodov",
    author_email="user@example.com",
    description="Static image gallery generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RomanKosobrodov/mikula",
    packages=setuptools.find_packages(),
    package_data={
        "mikula": ["themes/*"]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["boto3>=1.10.26",
                      "botocore>=1.13.26",
                      "Jinja2>=2.10.3",
                      "Markdown>=3.1.1",
                      "Pillow>=6.2.1",
                      "PyYAML>=5.1.2"]

)
