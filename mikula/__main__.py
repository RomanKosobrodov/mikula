import argparse
from mikula.implementation.build import build_gallery
from mikula.implementation.serve import serve

parser = argparse.ArgumentParser(description="Static Image Gallery Generator")
subparsers = parser.add_subparsers()

build_parser = subparsers.add_parser("build")
build_parser.add_argument("--input",
                          help="Input directory containing images, metadata and settings",
                          required=True)
build_parser.add_argument("--output",
                          help="Output directory",
                          required=True)
build_parser.add_argument("--theme",
                          help="theme directory",
                          default="./themes/default",
                          required=False)
build_parser.set_defaults(function=build_gallery)

serve_parser = subparsers.add_parser("serve")
serve_parser.add_argument("--gallery",
                          help="path to the gallery")
serve_parser.add_argument("--port",
                          help="Output directory",
                          type=int,
                          default=4200,
                          required=False)
serve_parser.set_defaults(function=serve)

deploy_parser = subparsers.add_parser("deploy")
deploy_parser.add_argument("--gallery",
                           help="path to the gallery")
deploy_parser.set_defaults(function=print)

args = parser.parse_args()

command = args.function
delattr(args, "function")
kwargs = vars(args)

command(**kwargs)
