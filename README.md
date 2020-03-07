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
Use pip to install Mikula
```bash
pip install mikula
```
If you don't have administrator's privileges or don't want to install it globally, run the following command:
```bash
pip install --user mikula
```
When updating from a previous version:
```bash
pip install --update mikula
```
Check your installation:
```bash
mikula --version
```

## Getting Started with Mikula
Once you installed Mikula, clone a sample gallery from [GitHub](https://github.com/RomanKosobrodov/mikula-sample-gallery):

```bash
git clone https://github.com/RomanKosobrodov/mikula-sample-gallery
```

### Navigate to the gallery directory

```bash
cd mikula-sample-gallery
```

### Configure Mukula
```bash
mikula configure
```
If you have a AWS S3 account you can provide your access key, secret and region.
Otherwise, skip these settings.

### Build sample gallery

Choose the output directory and run:
```bash
mikula build --output=<your-output-directory>
```

### View
Run the development server and check the results
```bash
mikula serve
```
Click on the [link](http://localhost:5000) to open the gallery in your browser.
To exit the server press `Ctrl + C` (or `Command + C` on Mac).

### Deploy
If you configured your AWS S3 credentials you can deploy your gallery to AWS S3.
Choose a name for the bucket which is unique for AWS and run:
```bash
mikula deploy --bucket <your-bucket-name>
```
Check that everything is working as expected by opening your website.
The url has the following format:
```
<your-bucket-name>.s3-website-<your-AWS-region>.amazonaws.com
```

## Installing from source

### Get the source

Clone the project repository from GitHub:
```bash
git clone https://github.com/RomanKosobrodov/mikula.git
```

### Install dependencies

You will need development requirements:
```bash
pip install -r requirements-dev.txt
```
As usual, it is a good idea to use a virtual environment.

### Run Mikula

To run the package installed from source use the following command:
```bash
python -m mikula <command> <options>
```
Where `<command>` is one of `configure`, `build`, `serve` or `deploy`, and `<options>` are 
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
python3.7 setup.py sdist bdist_wheel
twine upload dist/* 
```
