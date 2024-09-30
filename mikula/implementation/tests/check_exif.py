import argparse
from PIL import Image
from PIL.TiffImagePlugin import IFDRational
from mikula.implementation.exif import get_exif

MAX_LENGTH = 24


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print Exif")
    parser.add_argument("filename",
                        type=str,
                        help="Name of image file")
    args = parser.parse_args()
    image = Image.open(args.filename)
    exif = get_exif(image)

    for k, v in exif.items():
        if type(v) is IFDRational:
            print(f"{k}: {v.numerator}/{v.denominator} \u2248 {float(v):.3f}")
        else:
            if type(v) is str:
                print(f"{k}: \"{v}\"")
            else:
                if hasattr(v, "__len__") and len(v) > MAX_LENGTH:
                    print(f"{k}: {v[:MAX_LENGTH]}..")
                else:
                    print(f"{k}: {v}")
