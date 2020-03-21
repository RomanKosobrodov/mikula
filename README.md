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
title: Funny cat's images
---

# Images of cats
This page contains a collection of amusing feline pictures.
```

The following metadata fields are recognised by Mikula:

| Field             | Value         | Description                                                                 |
| ----------------- | ------------- | --------------------------------------------------------------------------- |
| page_title        | string        | Page title displayed by the browser                                         |
| title             | string        | Album or image title displayed on the parent page                           |
| thumbnail         | file path     | Name of the file to be used as an album thumbnail                           |
| exclude_thumbnail | {true, false} | Set to true to exclude album thumbnail from the gallery. Default is true    |
| place_before      | {true, false} | Set to place the text before the image(s). Default is false.                |
| exif              | list          | Extract information from EXIF data. See below for a list of supported tags. |
| show_exif         | {true, false} | Set to true to show minimal EXIF data below the image.                      |

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

the page rendered by Mikula will include the image followed by the text:
```markdown
Sunflowers
Picture of sunflowers taken on 2018:05:13 10:13:46 in my garden with Canon EOS 450D. 
ISO speed 100, shutter speed 1/500 at f1.4.
```

## Supported EXIF tags
The following EXIF Tags are supported:

| Tag ID | Tag Name                     |
| ------ | -----------------------------|
| 0X000B | ProcessingSoftware           |
| 0X00FE | NewSubfileType               |
| 0X00FF | SubfileType                  |
| 0X0100 | ImageWidth                   |
| 0X0101 | ImageLength                  |
| 0X0102 | BitsPerSample                |
| 0X0103 | Compression                  |
| 0X0106 | PhotometricInterpretation    |
| 0X0107 | Thresholding                 |
| 0X0108 | CellWidth                    |
| 0X0109 | CellLength                   |
| 0X010A | FillOrder                    |
| 0X010D | DocumentName                 |
| 0X010E | ImageDescription             |
| 0X010F | Make                         |
| 0X0110 | Model                        |
| 0X0111 | StripOffsets                 |
| 0X0112 | Orientation                  |
| 0X0115 | SamplesPerPixel              |
| 0X0116 | RowsPerStrip                 |
| 0X0117 | StripByteCounts              |
| 0X0118 | MinSampleValue               |
| 0X0119 | MaxSampleValue               |
| 0X011A | XResolution                  |
| 0X011B | YResolution                  |
| 0X011C | PlanarConfiguration          |
| 0X011D | PageName                     |
| 0X0120 | FreeOffsets                  |
| 0X0121 | FreeByteCounts               |
| 0X0122 | GrayResponseUnit             |
| 0X0123 | GrayResponseCurve            |
| 0X0124 | T4Options                    |
| 0X0125 | T6Options                    |
| 0X0128 | ResolutionUnit               |
| 0X0129 | PageNumber                   |
| 0X012D | TransferFunction             |
| 0X0131 | Software                     |
| 0X0132 | DateTime                     |
| 0X013B | Artist                       |
| 0X013C | HostComputer                 |
| 0X013D | Predictor                    |
| 0X013E | WhitePoint                   |
| 0X013F | PrimaryChromaticities        |
| 0X0140 | ColorMap                     |
| 0X0141 | HalftoneHints                |
| 0X0142 | TileWidth                    |
| 0X0143 | TileLength                   |
| 0X0144 | TileOffsets                  |
| 0X0145 | TileByteCounts               |
| 0X014A | SubIFDs                      |
| 0X014C | InkSet                       |
| 0X014D | InkNames                     |
| 0X014E | NumberOfInks                 |
| 0X0150 | DotRange                     |
| 0X0151 | TargetPrinter                |
| 0X0152 | ExtraSamples                 |
| 0X0153 | SampleFormat                 |
| 0X0154 | SMinSampleValue              |
| 0X0155 | SMaxSampleValue              |
| 0X0156 | TransferRange                |
| 0X0157 | ClipPath                     |
| 0X0158 | XClipPathUnits               |
| 0X0159 | YClipPathUnits               |
| 0X015A | Indexed                      |
| 0X015B | JPEGTables                   |
| 0X015F | OPIProxy                     |
| 0X0200 | JPEGProc                     |
| 0X0201 | JpegIFOffset                 |
| 0X0202 | JpegIFByteCount              |
| 0X0203 | JpegRestartInterval          |
| 0X0205 | JpegLosslessPredictors       |
| 0X0206 | JpegPointTransforms          |
| 0X0207 | JpegQTables                  |
| 0X0208 | JpegDCTables                 |
| 0X0209 | JpegACTables                 |
| 0X0211 | YCbCrCoefficients            |
| 0X0212 | YCbCrSubSampling             |
| 0X0213 | YCbCrPositioning             |
| 0X0214 | ReferenceBlackWhite          |
| 0X02BC | XMLPacket                    |
| 0X1000 | RelatedImageFileFormat       |
| 0X1001 | RelatedImageWidth            |
| 0X1002 | RelatedImageLength           |
| 0X4746 | Rating                       |
| 0X4749 | RatingPercent                |
| 0X800D | ImageID                      |
| 0X828D | CFARepeatPatternDim          |
| 0X828E | CFAPattern                   |
| 0X828F | BatteryLevel                 |
| 0X8298 | Copyright                    |
| 0X829A | ExposureTime                 |
| 0X829D | FNumber                      |
| 0X83BB | IPTCNAA                      |
| 0X8649 | ImageResources               |
| 0X8769 | ExifOffset                   |
| 0X8773 | InterColorProfile            |
| 0X8822 | ExposureProgram              |
| 0X8824 | SpectralSensitivity          |
| 0X8825 | GPSInfo                      |
| 0X8827 | ISOSpeedRatings              |
| 0X8828 | OECF                         |
| 0X8829 | Interlace                    |
| 0X882A | TimeZoneOffset               |
| 0X882B | SelfTimerMode                |
| 0X9000 | ExifVersion                  |
| 0X9003 | DateTimeOriginal             |
| 0X9004 | DateTimeDigitized            |
| 0X9101 | ComponentsConfiguration      |
| 0X9102 | CompressedBitsPerPixel       |
| 0X9201 | ShutterSpeedValue            |
| 0X9202 | ApertureValue                |
| 0X9203 | BrightnessValue              |
| 0X9204 | ExposureBiasValue            |
| 0X9205 | MaxApertureValue             |
| 0X9206 | SubjectDistance              |
| 0X9207 | MeteringMode                 |
| 0X9208 | LightSource                  |
| 0X9209 | Flash                        |
| 0X920A | FocalLength                  |
| 0X920B | FlashEnergy                  |
| 0X920C | SpatialFrequencyResponse     |
| 0X920D | Noise                        |
| 0X9211 | ImageNumber                  |
| 0X9212 | SecurityClassification       |
| 0X9213 | ImageHistory                 |
| 0X9214 | SubjectLocation              |
| 0X9215 | ExposureIndex                |
| 0X9216 | TIFF/EPStandardID            |
| 0X927C | MakerNote                    |
| 0X9286 | UserComment                  |
| 0X9290 | SubsecTime                   |
| 0X9291 | SubsecTimeOriginal           |
| 0X9292 | SubsecTimeDigitized          |
| 0X9C9B | XPTitle                      |
| 0X9C9C | XPComment                    |
| 0X9C9D | XPAuthor                     |
| 0X9C9E | XPKeywords                   |
| 0X9C9F | XPSubject                    |
| 0XA000 | FlashPixVersion              |
| 0XA001 | ColorSpace                   |
| 0XA002 | ExifImageWidth               |
| 0XA003 | ExifImageHeight              |
| 0XA004 | RelatedSoundFile             |
| 0XA005 | ExifInteroperabilityOffset   |
| 0XA20B | FlashEnergy                  |
| 0XA20C | SpatialFrequencyResponse     |
| 0XA20E | FocalPlaneXResolution        |
| 0XA20F | FocalPlaneYResolution        |
| 0XA210 | FocalPlaneResolutionUnit     |
| 0XA214 | SubjectLocation              |
| 0XA215 | ExposureIndex                |
| 0XA217 | SensingMethod                |
| 0XA300 | FileSource                   |
| 0XA301 | SceneType                    |
| 0XA302 | CFAPattern                   |
| 0XA401 | CustomRendered               |
| 0XA402 | ExposureMode                 |
| 0XA403 | WhiteBalance                 |
| 0XA404 | DigitalZoomRatio             |
| 0XA405 | FocalLengthIn35mmFilm        |
| 0XA406 | SceneCaptureType             |
| 0XA407 | GainControl                  |
| 0XA408 | Contrast                     |
| 0XA409 | Saturation                   |
| 0XA40A | Sharpness                    |
| 0XA40B | DeviceSettingDescription     |
| 0XA40C | SubjectDistanceRange         |
| 0XA420 | ImageUniqueID                |
| 0XA430 | CameraOwnerName              |
| 0XA431 | BodySerialNumber             |
| 0XA432 | LensSpecification            |
| 0XA433 | LensMake                     |
| 0XA434 | LensModel                    |
| 0XA435 | LensSerialNumber             |
| 0XA500 | Gamma                        |
| 0XC4A5 | PrintImageMatching           |
| 0XC612 | DNGVersion                   |
| 0XC613 | DNGBackwardVersion           |
| 0XC614 | UniqueCameraModel            |
| 0XC615 | LocalizedCameraModel         |
| 0XC616 | CFAPlaneColor                |
| 0XC617 | CFALayout                    |
| 0XC618 | LinearizationTable           |
| 0XC619 | BlackLevelRepeatDim          |
| 0XC61A | BlackLevel                   |
| 0XC61B | BlackLevelDeltaH             |
| 0XC61C | BlackLevelDeltaV             |
| 0XC61D | WhiteLevel                   |
| 0XC61E | DefaultScale                 |
| 0XC61F | DefaultCropOrigin            |
| 0XC620 | DefaultCropSize              |
| 0XC621 | ColorMatrix1                 |
| 0XC622 | ColorMatrix2                 |
| 0XC623 | CameraCalibration1           |
| 0XC624 | CameraCalibration2           |
| 0XC625 | ReductionMatrix1             |
| 0XC626 | ReductionMatrix2             |
| 0XC627 | AnalogBalance                |
| 0XC628 | AsShotNeutral                |
| 0XC629 | AsShotWhiteXY                |
| 0XC62A | BaselineExposure             |
| 0XC62B | BaselineNoise                |
| 0XC62C | BaselineSharpness            |
| 0XC62D | BayerGreenSplit              |
| 0XC62E | LinearResponseLimit          |
| 0XC62F | CameraSerialNumber           |
| 0XC630 | LensInfo                     |
| 0XC631 | ChromaBlurRadius             |
| 0XC632 | AntiAliasStrength            |
| 0XC633 | ShadowScale                  |
| 0XC634 | DNGPrivateData               |
| 0XC635 | MakerNoteSafety              |
| 0XC65A | CalibrationIlluminant1       |
| 0XC65B | CalibrationIlluminant2       |
| 0XC65C | BestQualityScale             |
| 0XC65D | RawDataUniqueID              |
| 0XC68B | OriginalRawFileName          |
| 0XC68C | OriginalRawFileData          |
| 0XC68D | ActiveArea                   |
| 0XC68E | MaskedAreas                  |
| 0XC68F | AsShotICCProfile             |
| 0XC690 | AsShotPreProfileMatrix       |
| 0XC691 | CurrentICCProfile            |
| 0XC692 | CurrentPreProfileMatrix      |
| 0XC6BF | ColorimetricReference        |
| 0XC6F3 | CameraCalibrationSignature   |
| 0XC6F4 | ProfileCalibrationSignature  |
| 0XC6F6 | AsShotProfileName            |
| 0XC6F7 | NoiseReductionApplied        |
| 0XC6F8 | ProfileName                  |
| 0XC6F9 | ProfileHueSatMapDims         |
| 0XC6FA | ProfileHueSatMapData1        |
| 0XC6FB | ProfileHueSatMapData2        |
| 0XC6FC | ProfileToneCurve             |
| 0XC6FD | ProfileEmbedPolicy           |
| 0XC6FE | ProfileCopyright             |
| 0XC714 | ForwardMatrix1               |
| 0XC715 | ForwardMatrix2               |
| 0XC716 | PreviewApplicationName       |
| 0XC717 | PreviewApplicationVersion    |
| 0XC718 | PreviewSettingsName          |
| 0XC719 | PreviewSettingsDigest        |
| 0XC71A | PreviewColorSpace            |
| 0XC71B | PreviewDateTime              |
| 0XC71C | RawImageDigest               |
| 0XC71D | OriginalRawFileDigest        |
| 0XC71E | SubTileBlockSize             |
| 0XC71F | RowInterleaveFactor          |
| 0XC725 | ProfileLookTableDims         |
| 0XC726 | ProfileLookTableData         |
| 0XC740 | OpcodeList1                  |
| 0XC741 | OpcodeList2                  |
| 0XC74E | OpcodeList3                  |
| 0XC761 | NoiseProfile                 |

Not all of these tags will be available in the EXIF created by your camera or scanner. 


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
