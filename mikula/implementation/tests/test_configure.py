from mikula.implementation.configure import configure, DEFAULTS, save_credentials, read_credentials, read_configuration
import os
import yaml
import tempfile


def check_default_configuration():
    fn = "c_o_n_f_i_g.yaml"
    configure(".")
    with open(fn, "r") as fid:
        res = yaml.load(fid, Loader=yaml.Loader)
    os.remove(fn)
    assert res == DEFAULTS


def test_utf8_encoding_in_config():
    content = """
---
meta:
  description: "Это описание"
  keywords: "галерея, Mikula"
  author: "Микула Селянинович"
image_format: "jpeg"
image_height: 1100
thumbnail_height: 500
sort_by: "name"
footer:
  copyright:
    year_start: 2021
    year_end: "*"
    author: "Все права защищены"
  credits:
    mikula: true
    theme: true
AWS_region: ap-southeast-2
"""
    td = tempfile.gettempdir()
    fn = os.path.join(td, "tmp_4382746.yaml")
    with open(fn, mode="w", encoding="utf-8") as fid:
        fid.write(content)
        fid.flush()

    conf = read_configuration(td, fn)
    assert(len(conf) > 0)

    os.remove(fn)


def check_credentials():
    fn = "creds"
    key = "key"
    secret = "secret"

    user_dir = os.path.expanduser("~")
    credentials_fn = os.path.join(user_dir, ".mikula", fn)

    save_credentials(credentials_fn, {"aws_access_key_id": key,
                                      "aws_secret_access_key": secret})
    creds = read_credentials(fn)
    os.remove(credentials_fn)

    assert creds is not None
    assert creds.get("aws_access_key_id", None) == key
    assert creds.get("aws_secret_access_key", None) == secret


if __name__ == "__main__":
    # check_default_configuration()
    test_utf8_encoding_in_config()
    # check_credentials()
