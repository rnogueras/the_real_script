import pytest

import numpy as np

from main import flatten, Tonality, INTERVAL_VALUES


TEST_C_MAJOR_SCALE_VALUES = np.array([0, 2, 4, 5, 7, 9, 11])
TEST_A_MINOR_SCALE_VALUES = np.array([9, 11, 0, 2, 4, 5, 7])
TEST_C_MAJOR = Tonality("C")
TEST_A_MINOR = Tonality("C", mode="VI")


@pytest.mark.parametrize(
    "modulator_a, modulator_b",
    [
        (INTERVAL_VALUES["P1"], INTERVAL_VALUES["P8"]),
        (INTERVAL_VALUES["P1"], INTERVAL_VALUES["P8"]),
        (INTERVAL_VALUES["P8"] * 3, INTERVAL_VALUES["P8"] * 3),
        (INTERVAL_VALUES["P5"], INTERVAL_VALUES["P4"]),
        (INTERVAL_VALUES["P4"], INTERVAL_VALUES["P5"]),
        (INTERVAL_VALUES["m2"], INTERVAL_VALUES["M7"]),
        (INTERVAL_VALUES["M2"], INTERVAL_VALUES["m7"]),
        (INTERVAL_VALUES["m3"], INTERVAL_VALUES["M6"]),
        (INTERVAL_VALUES["M3"], INTERVAL_VALUES["m6"]),
    ],
)
def test_flatten(modulator_a, modulator_b):
    scale_a = flatten(TEST_C_MAJOR_SCALE_VALUES + modulator_a)
    scale_b = flatten(TEST_C_MAJOR_SCALE_VALUES - modulator_b)

    np.testing.assert_array_equal(scale_a, scale_b)
    assert (
        not (scale_a > 11).any()
        or (scale_a < 0).any()
        or (scale_b > 11).any()
        or (scale_b < 0).any()
    )


def test_init_mode_values():
    np.testing.assert_array_equal(TEST_C_MAJOR.mode_values, TEST_C_MAJOR_SCALE_VALUES)
    np.testing.assert_array_equal(TEST_A_MINOR.mode_values, TEST_A_MINOR_SCALE_VALUES)