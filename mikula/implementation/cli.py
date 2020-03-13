import argparse
from mikula.implementation.initialise import initialise
from mikula.implementation.configure import configure, read_configuration, DEFAULTS
from mikula.implementation.build import build
from mikula.implementation.serve import serve
from mikula.implementation.deploy import deploy
from mikula.implementation.customize import customize
import os


def create_parser():
    parser = argparse.ArgumentParser(description="Static Image Gallery Generator",
                                     usage="mikula [-h] {configure,build,serve,deploy} ...")
    parser.add_argument("--version",
                        help="Print version number",
                        action="store_true",
                        default=False)

    subparsers = parser.add_subparsers()

    serve_parser = subparsers.add_parser("init")
    serve_parser.set_defaults(function=initialise)

    serve_parser = subparsers.add_parser("configure")
    serve_parser.add_argument("--reset",
                              help="Reset AWS credentials",
                              action="store_true",
                              default=False)
    serve_parser.set_defaults(function=configure)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--theme",
                              help="Mikula theme",
                              default="default",
                              required=False)
    build_parser.set_defaults(function=build)

    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--port",
                              help="port number (default is 5000)",
                              type=int,
                              default=5000,
                              required=False)
    serve_parser.set_defaults(function=serve)

    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("--bucket",
                               help="Name of AWS S3 bucket",
                               required=True)
    deploy_parser.add_argument("--region",
                               help="Name of AWS S3 region",
                               default=read_configuration().get("region", DEFAULTS["region"]),
                               required=False)
    deploy_parser.set_defaults(function=deploy)

    customize_parser = subparsers.add_parser("customize")
    customize_parser.add_argument("--theme",
                                  help="Name for your new theme",
                                  required=True)
    customize_parser.add_argument("--prototype",
                                  help="Name of prototype Mikula theme you wish to customize",
                                  default="default",
                                  required=False)
    customize_parser.add_argument("--destination",
                                  help="Destination directory for the custom theme",
                                  default=os.path.join(os.getcwd(), "themes"),
                                  required=False)
    customize_parser.set_defaults(function=customize)

    return parser

