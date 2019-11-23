from mikula.implementation.configure import configure, DEFAULTS, save_credentials, read_credentials
import os
import yaml


def test_default_configuration():
    fn = "c_o_n_f_i_g.yaml"
    configure(".", filename=fn)
    with open(fn, "r") as fid:
        res = yaml.load(fid, Loader=yaml.Loader)
    os.remove(fn)
    assert res == DEFAULTS


def test_credentials():
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
    test_default_configuration()
    test_credentials()
