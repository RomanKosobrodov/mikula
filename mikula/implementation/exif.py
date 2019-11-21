import math


def nominal_f_number(n, m):
    return f"f{n/m}"


FRACTIONS = (0.0, 1 / 3, 0.5, 2 / 3, 1.0)


def closest_fraction_index(f):
    diff = 1.0
    fraction_index = 0
    for k, d in enumerate(FRACTIONS):
        r = abs(d - f)
        if r < diff:
            fraction_index, diff = k, r
    return fraction_index


def lut_index(n, m, start_value):
    ratio = -n / m
    whole = int(math.floor(ratio))
    fraction_index = closest_fraction_index(ratio-whole)
    return fraction_index + (whole - start_value) * 4


MIN_SPEED_NUMBER = -15
NOMINAL_SPEEDS = ['1/32000', '1/25600', '1/24000', '1/20000', '1/16000', '1/12800', '1/12000', '1/10000', '1/8000',
                  '1/6400', '1/6000', '1/5000', '1/4000', '1/3200', '1/3000', '1/2500', '1/2000', '1/1600', '1/1500',
                  '1/1250', '1/1000', '1/800', '1/750', '1/640', '1/500', '1/400', '1/350', '1/320', '1/250', '1/200',
                  '1/180', '1/160', '1/125', '1/100', '1/90', '1/80', '1/60', '1/50', '1/45', '1/40', '1/30', '1/25',
                  '1/20', '1/20', '1/15', '1/13', '1/10', '1/10', '1/8', '1/6', '1/6', '1/5', '1/4', '1/3', '1/3',
                  '1/2.5', '1/2', '1/1.6', '1/1.5', '1/1.3', '1', '1.3', '1.5', '1.6', '2', '2.5', '3', '3', '4', '5',
                  '6', '6', '8', '10', '10', '13', '15', '20', '20', '25', '30']


def nominal_shutter_speed(n, m):
    index = lut_index(n, m, MIN_SPEED_NUMBER)
    return NOMINAL_SPEEDS[index]


NOMINAL_APERTURE_NUMBERS = ['0.5', '0.56', '0.6', '0.6', '0.7', '0.8', '0.8', '0.9', '1', '1.1', '1.2', '1.2', '1.4', '1.6', '1.7', '1.8', '2', '2.2', '2.4', '2.5', '2.8', '3.2', '3.3', '3.5', '4', '4.5', '4.8', '5.0', '5.6', '6.3', '6.7', '7.1', '8', '9', '9.5', '10', '11', '13', '13', '14', '16', '18', '19', '20', '22', '25', '27', '28', '32', '36', '38', '40', '45', '50', '55', '60', '64', '72', '76', '80', '90', '100', '110', '115', '128', '144', '152', '160', '180', '200', '220', '230', '256']
MIN_APERTURE_NUMBER = -2


def nominal_aperture(n, m):
    index = lut_index(-n, m, MIN_APERTURE_NUMBER)
    return NOMINAL_APERTURE_NUMBERS[index]

