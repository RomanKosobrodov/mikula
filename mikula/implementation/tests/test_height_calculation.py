from mikula.implementation.rendering import cum_sum, calculate_heights, find_closest
import math


TOLERANCE = 1e-6


def test_cum_sum():
    x = [1, 2, 3, 4, 5]
    cs = cum_sum(x)
    reference = [1, 3, 6, 10, 15]
    assert cs == reference


def test_find_closest_within():
    x = [1, 2, 3, 4, 5]
    c = find_closest(x, 3.1)
    assert x[c] == 3


def test_find_closest_exact():
    x = [1, 2, 3, 4, 5]
    c = find_closest(x, 3)
    assert x[c] == 3


def test_find_closest_before():
    x = [1, 2, 3, 4, 5]
    c = find_closest(x, -3)
    assert x[c] == 1


def test_find_closest_after():
    x = [1, 2, 3, 4, 5]
    c = find_closest(x, 10)
    assert x[c] == 5


def test_calculate_height_one_equal():
    num_elements = 9
    cols = 1
    ratios = [0.1] * num_elements
    heights, counts = calculate_heights(ratios, max_columns=cols)
    cs = cum_sum(ratios)
    reference = cs[-1]
    assert len(heights) == cols
    assert heights[0] == reference
    assert counts[0] == num_elements


def test_calculate_height_two_equal():
    num_elements = 9
    cols = 2
    ratios = [0.1] * num_elements
    heights, counts = calculate_heights(ratios, max_columns=cols)
    assert len(heights) == cols
    assert abs(heights[0] - 0.9) < TOLERANCE
    assert abs(heights[1] - 0.5) < TOLERANCE
    assert counts[0] == num_elements
    assert counts[1] == int(math.ceil(num_elements/2))


def test_calculate_height_three_equal():
    num_elements = 9
    cols = 3
    ratios = [0.1] * num_elements
    heights, counts = calculate_heights(ratios, max_columns=cols)
    assert len(heights) == cols
    assert abs(heights[0] - 0.9) < TOLERANCE
    assert abs(heights[1] - 0.5) < TOLERANCE
    assert abs(heights[2] - 0.3) < TOLERANCE
    assert counts[0] == num_elements
    assert counts[1] == int(math.ceil(num_elements/2))
    assert counts[2] == num_elements // 3


def test_calculate_height_unequal():
    cols = 3
    ratios = [0.1, 0.5, 0.25, 0.4, 0.1, 0.7, 0.5, 0.1, 0.1]
    heights, counts = calculate_heights(ratios, max_columns=cols)
    assert len(heights) == cols
    assert len(counts) == cols
    assert abs(heights[0] - 2.75) < TOLERANCE
    assert abs(heights[1] - 1.4) < TOLERANCE
    assert abs(heights[2] - 1.2) < TOLERANCE
    assert counts == [9, 4, 3]


if __name__ == "__main__":
    test_cum_sum()
    test_find_closest_within()
    test_find_closest_exact()
    test_find_closest_before()
    test_find_closest_after()
    test_calculate_height_one_equal()
    test_calculate_height_two_equal()
    test_calculate_height_three_equal()
    test_calculate_height_unequal()
