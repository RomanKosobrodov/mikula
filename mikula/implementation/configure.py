import yaml
import os

DEFAULTS = {
    "image_format": "png",
    "image_height": 600,
    "thumbnail_height": 200,
    "region": ""
}

AWS_REGIONS = ("us-east-2", "us-east-1", "us-west-1", "us-west-2",
               "ap-east-1", "ap-south-1", "ap-northeast-3", "ap-northeast-2",
               "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
               "ca-central-1", "cn-north-1", "cn-northwest-1",
               "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1",
               "sa-east-1", "me-south-1")


def save_credentials(filename, credentials):
    with open(filename, "w") as fid:
        fid.write("[default]\n")
        for key, value in credentials.items():
            fid.write(f"{key}={value}\n")


def configure(reset=False):
    user_dir = os.path.expanduser("~")
    mikula_dir = os.path.join(user_dir, ".mikula")
    if not os.path.isdir(mikula_dir):
        os.mkdir(mikula_dir)
    credentials_fn = os.path.join(mikula_dir, "credentials")
    if not os.path.isfile(credentials_fn) or reset:
        credentials = dict()
        print("Enter your AWS credentials for S3 service")
        credentials["aws_access_key_id"] = input("AWS Access Key ID: ")
        credentials["aws_secret_access_key"] = input("AWS Secret Access Key: ")
        region = input("AWS region: ")
        if len(region) > 0:
            if region in AWS_REGIONS:
                credentials["region"] = region
            else:
                print(f"Unsupported region '{region}'. Please select one of the regions: {AWS_REGIONS}")
                return
        save_credentials(credentials_fn, credentials)


def read_configuration(directory=".", filename="configuration.yaml"):
    fn = os.path.join(directory, filename)
    config = DEFAULTS
    if os.path.isfile(fn):
        with open(fn, "r") as fid:
            user_defined = yaml.load(fid, Loader=yaml.Loader)
            config.update(user_defined)
    return config


def read_credentials(filename="credentials"):
    def parse_credentials(s):
        key, value = s.split("=")
        return key.strip(), value.strip()

    user_dir = os.path.expanduser("~")
    credentials_fn = os.path.join(user_dir, ".mikula", filename)
    if not os.path.isfile(credentials_fn):
        return None

    credentials = dict()
    with open(credentials_fn, "r") as fid:
        for line in fid.readlines():
            if "=" in line:
                k, v = parse_credentials(line)
                credentials[k] = v
    return credentials
