import argparse
from gal.build import build_from


parser = argparse.ArgumentParser(description="Static Image Gallery")
parser.add_argument("--input",
                    help="Input directory containing images, metadata and settings",
                    required=True)
parser.add_argument("--output",
                    help="Output directory",
                    required=True)
parser.add_argument("--theme",
                    help="theme directory",
                    default="./themes/default",
                    required=False)

args = parser.parse_args()

build_from(args.input, args.output, args.theme)
