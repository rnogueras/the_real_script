"""
Main file of The Real Script, program to generate random jazz standards.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, Union, List, Tuple, Type, Sequence

import numpy as np


C_SCALES = {
    "cromatic": np.arange(12),
    "diatonic": (0, 2, 4, 5, 7, 9, 11),
    "melodic minor": (0, 2, 3, 5, 7, 9, 11),
    "harmonic minor": (0, 2, 3, 5, 7, 8, 11),
    "major pentatonic": (0, 2, 4, 7, 9),
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


def flatten(values: Union[int, np.array]) -> Union[int, np.array]:
    """Flatten note values to scale 0-11."""
    while (values > 11).any():
        values = np.where(values > 11, values - 12, values)
    while (values < 0).any():
        values = np.where(values < 0, values + 12, values)
    if values.size == 1:
        values = int(values)
    return values


def invert(values: np.array, inversion: int) -> np.array:
    """Return the specified musical inversion of the values."""
    return np.hstack([values[inversion:], values[:inversion]]).astype(int)


def calculate_intervals(values: np.array) -> Tuple[int]:
    """Calculate intervals between the provided note values."""
    return tuple(
        [flatten(next_note - note) for note, next_note in zip(values, values[1:])]
    )


class Set:
    """
    A set is a collection of tones. A chord, a scale or a
    melody are examples of sets.
    """

    def __init__(self, values: np.array) -> None:
        """Class instance constructor."""
        self.values = values
        self.intervals = calculate_intervals(self.values)
        self.tonic = NOTES[values[0]]
        self.notes = [NOTES[value] for value in self.values]
        self.name = self.init_name()
        self.interval_names = [INTERVALS[interval] for interval in self.intervals]

    def __iter__(self):
        """Return values if iteration is called."""
        for note in self.values:
            yield note

    def __repr__(self):
        """Return notes if print is called."""
        return str(self.notes)

    def init_name(self) -> str:
        """Get name of the set."""
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
        self.cromatic_values = Set(invert(C_SCALES["cromatic"], NOTES.index(tonic)))
        self.scale = self.init_scale()

    def init_scale(self) -> Type[Set]:
        """Return main scale of the tonality."""
        tonic_value = NOTES.index(self.tonic)
        inversion_values = invert(C_SCALES[self.scale_type], DEGREES.index(self.mode))
        intervals = calculate_intervals(inversion_values)
        modal_values = np.hstack([tonic_value, (tonic_value + np.cumsum(intervals))])
        return Set(flatten(modal_values))

    def pick_chord(self, degree: str, amount: int = 4) -> Type[Set]:
        """Returns the chord in the chosen degree with the specified amount of notes."""
        degree_value = DEGREES.index(degree)
        three_octaves_scale = list(self.scale) * 3
        full_chord = three_octaves_scale[degree_value : degree_value + 14 : 2]
        return Set(full_chord[0:amount])
