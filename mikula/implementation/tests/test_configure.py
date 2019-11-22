from mikula.implementation.configure import configure, DEFAULTS
import os
import yaml


def test_default_configuration():
    fn = "c_o_n_f_i_g.yaml"
    configure(".", filename=fn)
    with open(fn, "r") as fid:
        res = yaml.load(fid, Loader=yaml.Loader)
    os.remove(fn)
    assert res == DEFAULTS


if __name__ == "__main__":
    test_default_configuration()
