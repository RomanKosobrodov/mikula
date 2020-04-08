# Mikula

Static image gallery generator inspired by Jekyll and JAlbum.
Mikula is written in Python and supports uploads to AWS S3.

## Motivation

I take a lot of pictures both on film and digitally and need a simple way to publish them on the web. I used JAlbum for a number of years.
With a little bit of tinkering it produced acceptable results but I always wanted more 
flexibility in designing my own themes and albums. Jekyll provided an inspiration for creating Mikula - a static gallery 
generator written in Python.

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
It is also a good idea to upgrade pip to the latest version:
```bash
python3.8 -m pip install --upgrade pip
```
Depending on your system configuration you might want to install `pip` globally with `sudo`:
```bash
sudo python3.8 -m pip install --upgrade pip
```

### Install Mikula with pip
With `pip` set up, install Mikula
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
When you build your gallery it will be saved in the `build` directory. You can use Mikula to deploy the generated gallery 
to AWS S3 bucket (provided you have an AWS account with sufficient priviligies) or upload it manually to your web server.
More cloud platforms might be supported in the future.

### Configure AWS credentials
If you choose to use AWS S3 to host your gallery, provide Mikula with your AWS credentials by running this command:
```bash
mikula configure
```
This step is not required if you plan to use a different hosting method.

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

### Theme Customisation

Mikula themes can be customised. To create a new theme based on an existing one
use the following command:
```bash
mikula customise --theme <my-awesome-theme> --prototype <default> --destination <theme-directory>
```
This will copy the prototype theme in the specified destination directory.
The custom theme can be used with the `build` command:
```bash
mikula build --theme <my-awesome-theme>
```

# Markdown metadata
You can add metadata in the beginning of your Markdown file. The metadata block starts and finishes with a line containing 
three dashes:
```markdown
---
title: Funny cats' images
---

# Images of cats
This page contains a collection of amusing feline pictures.
```

The following metadata fields are recognised by Mikula:

| Field             | Value         | Description                                                                   |
| ----------------- | ------------- | ----------------------------------------------------------------------------- |
| page_title        | string        | Page title displayed by the browser                                           |
| title             | string        | Album or image title displayed on the parent page                             |
| thumbnail         | file path     | Name of an image file to be used as an album thumbnail                        |
| exclude_thumbnail | {true, false} | Set to `true` to exclude album thumbnail from the gallery. Default is `false`.|
| place_before      | {true, false} | Set to place the text before the image(s). Default is `false`.                |
| exif              | list          | Extract information from EXIF data. See below for a list of supported tags.   |
| show_exif         | {true, false} | Set to true to show minimal EXIF data below the image.                        |
| order             | number        | If defined, albums and images are sorted by order (low values come first)     |
| hidden            | {true, false} | When `true` the page is rendered but not included in the navigation bar. This is useful for a "thank you" page displayed after a visitor submits a contact form. | 

You can also define your own fields and use them in the document.

## Using metadata
Here is an example of how you can include metadata in your markdown document. Suppose you have an image file `sunflowers.jpg`
which is taken with Canon EOS 450D and has the EXIF data embedded in the image file. If we now create a markdown file 
`sunflowers.md` with the following content:
```markdown
---
page_title: Garden - Sunflowers
title: Sunflowers
place_before: false
exif:
    - Model
    - DateTime
    - ISOSpeedRatings
    - ShutterSpeedValue
    - FNumber
---

# {{title}}
Picture of sunflowers taken on {{exif["DateTime"]}} in my garden with {{exif["Make"]}} {{exif["Model"]}}.
ISO speed {{exif["ISOSpeedRatings"]}}, shutter speed {{exif["ShutterSpeedValue"]}} at f{{exif["FNumber"]}}.
```

the page rendered by Mikula will show the following text (styling removed for clarity):
```markdown
Sunflowers
Picture of sunflowers taken on 2018:05:13 10:13:46 in my garden with Canon EOS 450D. 
ISO speed 100, shutter speed 1/500 at f1.4.
```
A list of supported EXIF tags is included in [EXIF-tags.md](https://github.com/RomanKosobrodov/mikula/blob/master/EXIF-tags.md).

# Gallery configuration

Gallery configuration is stored in `source/configuration.yaml`. 


# Installing from source

If you plan to contribute to Mikula you will need to install it from the source.

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
As always, it is a good idea to use a virtual environment.

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


