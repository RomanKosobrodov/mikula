import yaml
import os

DEFAULTS = {
    "image_format": "png",
    "image_height": 600,
    "thumbnail_height": 200
}


def configure(directory, filename="configuration.yaml"):
    fn = os.path.join(directory, filename)
    with open(fn, "w") as fid:
        yaml.dump(DEFAULTS, fid)


def read_configuration(directory=".", filename="configuration.yaml"):
    fn = os.path.join(directory, filename)
    config = DEFAULTS
    if os.path.isfile(fn):
        with open(fn, "r") as fid:
            user_defined = yaml.load(fid, Loader=yaml.Loader)
            config.update(user_defined)
    return config
