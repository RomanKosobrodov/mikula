# Mikula

Static image gallery generator inspired by Jekyll and JAlbum.
Mikula is written in Python and supports uploads to AWS S3.

## Motivation

I used JAlbum some time ago while it was free.
With enough tweaking to the themes it produced acceptable results but I always wanted more 
flexibility in designing my albums. Jekyll inspired me to create my own gallery generator in Python,
so here it is, welcome Mikula.

## Name

Mikula is a Ukrainian version of name Nicholas.


## Installation
Use pip

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
If you have a AWS S3 account you can provide your access key id, access key and region.
Otherwise, skip these settings.

### Build sample gallery

Choose the output directory and run:
```bash
mikula build --output=<your-output-directory>
```

### View it
Run the development server and check the results
```bash
mikula serve
```
Click on the [link](http://localhost:5000) to open the gallery in your browser.
To exit the server press `Ctrl + C` (or `Command + C` on Mac).

### Deploy it
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

## Packaging
Run `setup.py` to build the package and `twine` to upload it to PyPI:
```bash
rm dist/*
rm -rf build/*
python3.7 setup.py sdist bdist_wheel
twine upload dist/* 
```
