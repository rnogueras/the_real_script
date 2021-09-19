import pytest

import numpy as np

from main import flatten, INTERVALS


TEST_C_MAJOR_SCALE_VALUES = np.array([0, 2, 4, 5, 7, 9, 11])
TEST_A_MINOR_SCALE_VALUES = np.array([9, 11, 0, 2, 4, 5, 7])


@pytest.mark.parametrize(
    "modulator_a, modulator_b",
    [
        (INTERVALS.index("P1"), INTERVALS.index("P8")),
        (INTERVALS.index("P1"), INTERVALS.index("P8")),
        (INTERVALS.index("P8") * 3, INTERVALS.index("P8") * 3),
        (INTERVALS.index("P5"), INTERVALS.index("P4")),
        (INTERVALS.index("P4"), INTERVALS.index("P5")),
        (INTERVALS.index("m2"), INTERVALS.index("M7")),
        (INTERVALS.index("M2"), INTERVALS.index("m7")),
        (INTERVALS.index("m3"), INTERVALS.index("M6")),
        (INTERVALS.index("M3"), INTERVALS.index("m6")),
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
