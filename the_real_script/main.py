"""
Main file of The Real Script, program to generate random jazz standards.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, Tuple, Type, Sequence

import numpy as np


C_SCALES = {
    "cromatic": np.arange(12),
    "diatonic": (0, 2, 4, 5, 7, 9, 11),
    "melodic minor": (0, 2, 3, 5, 7, 9, 11),
    "harmonic minor": (0, 2, 3, 5, 7, 8, 11),
}
NOTES = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
DEGREES = ("I", "II", "III", "IV", "V", "VI", "VII")
# fmt: off
INTERVALS = [
    "P1", "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7", "P8"
]
# fmt: on
SET_INTERVALS = {
    "M": (4, 3),
    "m": (3, 4),
    "maj7": (4, 3, 4),
    "m7": (3, 4, 3),
    "7": (4, 3, 3),
    "m7b5": (3, 3, 4),
}
SET_NAMES = {intervals: chord for chord, intervals in SET_INTERVALS.items()}

PITCH_SET_BUILD_TYPES = (tuple, list, np.ndarray)


def invert(values: np.array, inversion: int) -> np.array:
    """Return the specified musical inversion of the values."""
    return np.hstack([values[inversion:], values[:inversion]]).astype(int)


def calculate_intervals(values: np.array) -> Tuple[int]:
    """Calculate intervals between the provided note values."""
    return tuple(
        [(next_note - note) % 12 for note, next_note in zip(values, values[1:])]
    )


# TODO: Make pitch sets constructable from either values or tonic + intervals.
class PitchSet:
    """
    A pitch set is a collection of tones. Chords, scales and melodies are examples
    of sets. Simple arithmetical operations can be performed with them.
    """

    def __init__(self, values: Sequence[int]) -> None:
        """Class instance constructor."""
        if not isinstance(values, PITCH_SET_BUILD_TYPES):
            raise TypeError(
                f"Valid types to build a PitchSet are: {PITCH_SET_BUILD_TYPES}"
            )
        self.values = np.array(values) % 12
        self.intervals = calculate_intervals(self.values)
        self.tonic = NOTES[self.values[0]]
        self.notes = [NOTES[value] for value in self.values]
        self.name = self.init_name()
        self.interval_names = [INTERVALS[interval] for interval in self.intervals]

    def __iter__(self):
        """Make class iterable."""
        for note in self.values:
            yield note

    def __getitem__(self, index):
        """Make class indexable."""
        return self.values[index]

    def __add__(self, summand):
        """Make class summable."""

        if isinstance(summand, PitchSet):
            return PitchSet(self.values + summand.values)

        elif isinstance(summand, np.ndarray) and summand.dtype == int:
            return PitchSet(self.values + summand)

        elif isinstance(summand, (tuple, list)) and all(
            isinstance(element, int) for element in summand
        ):
            return PitchSet(self.values + np.array(summand))
        elif isinstance(summand, int):
            return PitchSet(self.values + summand)
        else:
            raise TypeError("Invalid summand type.")

    def __radd__(self, summand):
        """Reverse sum."""
        return self.__add__(summand)

    def __repr__(self):
        """Return notes when print is called."""
        return f"{self.name}: {self.notes}"

    def init_name(self) -> str:
        """Initialize name of the set."""
        try:
            return self.tonic + SET_NAMES[self.intervals]
        except KeyError:
            return "Unknown set"


class Tonality:
    """Tonality class."""

    def __init__(
        self,
        tonic: str,
        scale_type: Optional[str] = "diatonic",
        mode: Optional[str] = "I",
    ) -> None:
        """Class instance constructor."""
        self.tonic = tonic
        self.scale_type = scale_type
        self.mode = mode
        self.cromatic_values = PitchSet(invert(C_SCALES["cromatic"], NOTES.index(tonic)))
        self.scale = self.init_scale()

    def init_scale(self) -> Type[PitchSet]:
        """Return main scale of the tonality."""
        tonic_value = NOTES.index(self.tonic)
        inversion_values = invert(C_SCALES[self.scale_type], DEGREES.index(self.mode))
        intervals = calculate_intervals(inversion_values)
        modal_values = np.hstack([tonic_value, (tonic_value + np.cumsum(intervals))])
        return PitchSet(modal_values % 12)

    def chord(self, degree: str, amount: int = 4) -> Type[PitchSet]:
        """Returns the chord in the chosen degree with the specified number of notes."""
        degree_value = DEGREES.index(degree)
        three_octaves_scale = list(self.scale) * 3
        full_chord = three_octaves_scale[degree_value : degree_value + 14 : 2]
        return PitchSet(full_chord[0:amount])
