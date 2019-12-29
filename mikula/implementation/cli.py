import argparse
import os
from mikula.implementation.configure import configure, read_configuration, DEFAULTS
from mikula.implementation.build import build
from mikula.implementation.serve import serve
from mikula.implementation.deploy import deploy


def create_parser():
    parser = argparse.ArgumentParser(description="Static Image Gallery Generator",
                                     usage="mikula [-h] {configure,build,serve,deploy} ...")
    subparsers = parser.add_subparsers()

    serve_parser = subparsers.add_parser("configure")
    serve_parser.add_argument("--source",
                              help="Path to the gallery source files",
                              required=False,
                              default=os.getcwd())
    serve_parser.add_argument("--reset",
                              help="Reset AWS credentials",
                              action="store_true",
                              default=False)
    serve_parser.set_defaults(function=configure)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--source",
                              help="Gallery source directory containing images, metadata and settings",
                              default=os.getcwd(),
                              required=False)
    build_parser.add_argument("--output",
                              help="Output directory",
                              required=True)
    build_parser.add_argument("--theme",
                              help="theme",
                              default="default",
                              required=False)
    build_parser.set_defaults(function=build)

    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--gallery",
                              help="path to the gallery",
                              default=os.getcwd(),
                              required=False)
    serve_parser.add_argument("--port",
                              help="Output directory",
                              type=int,
                              default=5000,
                              required=False)
    serve_parser.set_defaults(function=serve)

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("--gallery",
                               help="path to the gallery",
                               default=os.getcwd(),
                               required=False)
    deploy_parser.add_argument("--bucket",
                               help="Name of AWS S3 bucket",
                               required=True)
    deploy_parser.add_argument("--region",
                               help="Name of AWS S3 region",
                               default=read_configuration().get("region", DEFAULTS["region"]),
                               required=False)
    deploy_parser.set_defaults(function=deploy)

    return parser

