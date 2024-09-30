from mikula.implementation.exif import nominal_shutter_speed, NOMINAL_SPEEDS, nominal_f_number, \
    NOMINAL_APERTURE_NUMBERS, nominal_aperture

REF = [-15.0, -14.67, -14.5, -14.33, -14.0, -13.67, -13.5, -13.33, -13.0, -12.67, -12.5, -12.33, -12.0, -11.67, -11.5,
       -11.33, -11.0, -10.67, -10.5, -10.33, -10.0, -9.667, -9.5, -9.333, -9.0, -8.667, -8.5, -8.333, -8.0, -7.667,
       -7.5, -7.333, -7.0, -6.667, -6.5, -6.333, -6.0, -5.667, -5.5, -5.333, -5.0, -4.667, -4.5, -4.333, -4.0, -3.667,
       -3.5, -3.333, -3.0, -2.667, -2.5, -2.333, -2.0, -1.667, -1.5, -1.333, -1.0, -0.6667, -0.5, -0.3333, 0.0, 0.3333,
       0.5, 0.6667, 1.0, 1.333, 1.5, 1.667, 2.0, 2.333, 2.5, 2.667, 3.0, 3.333, 3.5, 3.667, 4.0, 4.333, 4.5, 4.667, 5.0]


def test_nominal_shutter_speed():
    r = nominal_shutter_speed(-65536, 65536)
    assert r == "2"

    for k, r in enumerate(REF):
        r = nominal_shutter_speed(-r, 1)
        assert r == NOMINAL_SPEEDS[k]


def test_nominal_shutter_speed_1_125():
    r = nominal_shutter_speed(458752,65536)
    assert r=="1/125"


def test_nominal_f_number():
    r = nominal_f_number(11, 10)
    assert "1.1" in r


F_REF = [-2.0, -1.667, -1.5, -1.333, -1.0, -0.6667, -0.5, -0.3333, 0.0, 0.3333, 0.5, 0.6667, 1.0, 1.333, 1.5, 1.667, 2.0, 2.333, 2.5, 2.667, 3.0, 3.333, 3.5, 3.667, 4.0, 4.333, 4.5, 4.667, 5.0, 5.333, 5.5, 5.667, 6.0, 6.333, 6.5, 6.667, 7.0, 7.333, 7.5, 7.667, 8.0, 8.333, 8.5, 8.667, 9.0, 9.333, 9.5, 9.667, 10.0, 10.33, 10.5, 10.67, 11.0, 11.33, 11.5, 11.67, 12.0, 12.33, 12.5, 12.67, 13.0, 13.33, 13.5, 13.67, 14.0, 14.33, 14.5, 14.67, 15.0, 15.33, 15.5, 15.67, 16.0]


def test_nominal_aperture():
    for k, r in enumerate(F_REF):
        r = nominal_aperture(r, 1)
        assert r == NOMINAL_APERTURE_NUMBERS[k]


def test_nominal_aperture_11():
    r = nominal_aperture(458752, 65536)
    assert r == "11"


if __name__ == "__main__":
    test_nominal_shutter_speed()
    test_nominal_f_number()
    # test_nominal_aperture()
