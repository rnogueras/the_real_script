import pytest

import numpy as np

from main import modulate, INTERVALS


TEST_C_MAJOR_SCALE_VALUES = np.array([0, 2, 4, 5, 7, 9, 11])
TEST_C_MINOR_SCALE_VALUES = np.array([0, 2, 3, 5, 7, 8, 10])
TEST_C_MODE_DIFFERENCES = np.array([0, 0, 1, 0, 0, 1, 1])


@pytest.mark.parametrize(
    "modulator_a, modulator_b",
    [
        (INTERVALS["P1"], INTERVALS["P8"]),
        (INTERVALS["P1"], -INTERVALS["P8"]),
        (INTERVALS["P8"] * 4, -INTERVALS["P8"] * 4),
        (INTERVALS["P5"], -INTERVALS["P4"]),
        (INTERVALS["P4"], -INTERVALS["P5"]),
        (INTERVALS["M3"], -INTERVALS["m6"]),
        (INTERVALS["m3"] * 3, -INTERVALS["M6"] * 3),
        (INTERVALS["m2"] * 5, -INTERVALS["M7"] * 5),
        (INTERVALS["M2"] * 7, -INTERVALS["m7"] * 7),
    ],
)
def test_modulate_by_scalar(modulator_a, modulator_b):
    scale_a = modulate(TEST_C_MAJOR_SCALE_VALUES, modulator_a)
    scale_b = modulate(TEST_C_MAJOR_SCALE_VALUES, modulator_b)

    np.testing.assert_array_equal(scale_a, scale_b)
    assert (
        not (scale_a > 11).any()
        or (scale_a < 0).any()
        or (scale_b > 11).any()
        or (scale_b < 0).any()
    )


@pytest.mark.parametrize(
    "modulator_a, modulator_b",
    [
        (-TEST_C_MODE_DIFFERENCES, INTERVALS["P1"]),
        (INTERVALS["P1"], TEST_C_MODE_DIFFERENCES),
        (INTERVALS["P1"], TEST_C_MODE_DIFFERENCES + 12),
    ],
)
def test_modulate_by_scale(modulator_a, modulator_b):
    scale_a = modulate(TEST_C_MAJOR_SCALE_VALUES, modulator_a)
    scale_b = modulate(TEST_C_MINOR_SCALE_VALUES, modulator_b)
    np.testing.assert_array_equal(scale_a, scale_b)
