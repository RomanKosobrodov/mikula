from mikula.implementation.cli import create_parser
from mikula import __version__

parser = create_parser()
args = parser.parse_args()

if args.version:
    print(f"Mikula version {__version__}")
    exit(0)

if "function" in args:
    command = args.function
    delattr(args, "function")
    delattr(args, "version")
    kwargs = vars(args)
    command(**kwargs)
