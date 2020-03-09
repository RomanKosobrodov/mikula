# Mikula

Static image gallery generator inspired by Jekyll and JAlbum.
Mikula is written in Python and supports uploads to AWS S3.

## Motivation

I used JAlbum some time ago.
With enough tweaking to the themes it produced acceptable results but I always wanted more 
flexibility in designing my albums. Jekyll inspired me to create my own gallery generator in Python,
so here it is, welcome Mikula.

## Name

Mikula is a Ukrainian version of name Nicholas.


## Installation

### Python 
You will need Python version 3.8 or above to run Mikula.
If you don't have Python 3.8 installed on your system follow the instructions on [python.org](https://www.python.org/downloads/).

### Pip
`Pip` is python package manager. Check that you have the correct version installed by running:
```bash
pip --version
```
You should see pip version number and python path with `(python 3.8)` or higher at the end.
If you see a different version number or get `command not found` install pip:
```bash
python3.8 -m pip install pip
```
You might also want to upgrade pip to the latest version:
```bash
python3.8 -m pip install --upgrade pip
```

### Install Mikula with pip
With pip set up, install Mikula
```bash
pip install mikula
```
If you don't have administrator's privileges or don't want to install it globally, run the following command:
```bash
pip install --user mikula
```
When updating from a previous version:
```bash
pip install --upgrade mikula
```
Check your installation:
```bash
mikula --version
```

## Getting Started with Mikula
### Create a directory for your new gallery
Mikula is a command-line tool, so fire up your favourite Terminal program.
Create a directory for your new gallery. For example:
```bash
mkdir ~/mikula-gallery
```
or 
```bash
mkdir ~/Desktop/mikula-gallery
```
Navigate into this directory:
```bash
cd ~/mikula-gallery
```
or 
```bash
cd ~/Desktop/mikula-gallery
```

### Initialise Mikula
When you run
```bash
mikula init
```
it will create a stub gallery consisting of one album, including one picture and three pages: Home, About and Contact.
Put your source files (images and text) into the `source` directory. Create a subdirectory for each album in the gallery. 
When you build your gallery it will be saved in the `build` directory. You can use Mikula to deploy it to AWS S3 bucket 
(provided you have an AWS account with sufficient priviligies) or upload it manually to your web server.

### Configure AWS credentials
If you choose to use AWS S3 to host your gallery, provide Mikula with your AWS credentials by running this command:
```bash
mikula configure
```
This step is optional if you use a different hosting method.

### Build the gallery
Run
```bash
mikula build
```
to generate your gallery in the `build` directory.

### Try it
You can test the results by running a local web server:
```bash
mikula serve
```
You gallery should be available on [http://localhost:5000](http://localhost:5000) 
Optionally, you can specify a different port number, for example:
```bash
mikula serve --port 1234
```
will run the server on [http://localhost:1234](http://localhost:1234)

### Deployment
Run 
```bash
mikula deploy --bucket <bucket-name> --region <AWS-region>
```
to deploy the website on AWS S3.
Alternatively, copy the content of the `build` directory to your web server. For example:
```bash
scp -rp build user@example.com:/www/
```
will copy all the files and subdirectories from `build` into `/www/` on your server.

# Installing from source

## Get the source

Clone the project repository from GitHub:
```bash
git clone https://github.com/RomanKosobrodov/mikula.git
```

## Install dependencies

You will need development requirements:
```bash
pip install -r requirements-dev.txt
```
As usual, it is a good idea to use a virtual environment.

## Run Mikula

To run the package installed from source use the following command:
```bash
python -m mikula <command> <options>
```
Where `<command>` is one of `init`, `configure`, `build`, `serve` or `deploy`, and `<options>` are 
command arguments. Run
```bash
python -m mikula -h
```
to get a list of all supported commands and arguments.

### Package and upload to PyPI

Run `setup.py` to build the package and `twine` to upload it to PyPI:
```bash
rm dist/*
rm -rf build/*
python3.8 setup.py sdist bdist_wheel
twine upload dist/* 
```
