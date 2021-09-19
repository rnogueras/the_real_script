"""
Main file of The Real Script, program to generate random jazz standards.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, List

import numpy as np


# Scales
CROMATIC_VALUES = np.arange(12)
SCALE_INDEX = {
    "diatonic": (0, 2, 4, 5, 7, 9, 11),
    "melodic minor": (0, 2, 3, 5, 7, 9, 11),
    "harmonic minor": (0, 2, 3, 5, 7, 8, 11),
    "major pentatonic": (0, 2, 4, 7, 9),
}

# Note names
NOTES = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
NOTE_VALUES = dict(zip(NOTES, CROMATIC_VALUES))
NOTE_NAMES = dict(zip(CROMATIC_VALUES, NOTES))

# Degrees
DEGREES = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")
DEGREE_VALUES = dict(zip(DEGREES, range(0, 9)))
DEGREE_NAMES = dict(zip(range(0, 9), DEGREES))

# Intervals
INTERVALS = ["P1", "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7", "P8"]
INTERVAL_VALUES = dict(zip(INTERVALS, range(0, 13)))
INTERVAL_NAMES = dict(zip(range(0, 13), INTERVALS))

# Chords
CHORD_INTERVALS = {
    "M": (4, 3),
    "m": (3, 4),
    "maj7": (4, 3, 4),
    "m7": (3, 4, 3),
    "7": (4, 3, 3),
    "m7b5": (3, 3, 4),
}
CHORD_NAMES = {intervals: chord for chord, intervals in CHORD_INTERVALS.items()}


def flatten(notes: np.array) -> np.array:
    """Flatten note values to scale 0-11."""
    while (notes > 11).any():
        notes = np.where(notes > 11, notes - 12, notes)
    while (notes < 0).any():
        notes = np.where(notes < 0, notes + 12, notes)
    return notes


def calculate_intervals(chord: np.array) -> List[int]:
    """Calculate intervals between the provided note values."""
    return [
        flatten(next_note - note) for note, next_note in zip(chord, chord[1:])
    ]


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
        self.cromatic_values = self.init_cromatic_values()
        self.mode_index = self.init_mode_index()
        self.mode_values = self.init_mode_values()
        self.chord_values = self.init_chord_values()

    def init_cromatic_values(self) -> np.array:
        """Return the cromatic scale modulated to the tonic."""
        return flatten(CROMATIC_VALUES + NOTE_VALUES[self.tonic])

    def init_mode_index(self) -> List[int]:
        """Transform base scale index into the selected mode index."""
        scale_index = SCALE_INDEX[self.scale_type]
        scale_size = len(scale_index)
        mode = DEGREE_VALUES[self.mode]

        if (mode + 1) > scale_size:
            raise AttributeError(
                f"The {self.scale_type} only has {scale_size} degrees "
                f"but the {self.mode} was requested. "
            )

        double_scale_index = scale_index * 2
        mode_range = range(mode, mode + scale_size)

        return [double_scale_index[number] for number in mode_range]

    def init_mode_values(self) -> np.array:
        """Use mode index on the chromatic values to get the mode values."""
        return self.cromatic_values[self.mode_index]

    def init_chord_values(self) -> np.array:
        """Get the full chord (7 notes) of every degree in the mode."""
        repeated_mode = list(self.mode_values) * 3
        return [
            repeated_mode[index : index + 14 : 2]
            for index, _ in enumerate(self.mode_values)
        ]

    def get_note_names(self) -> List[str]:
        """Return mode note names from mode values."""
        return list(np.vectorize(NOTE_NAMES.get)(self.mode_values))

    def get_chord_note_names(self, degree: str, amount: int = 4) -> List[str]:
        """Return chord note names of the specified chord."""
        degree = DEGREE_VALUES[degree]
        selected_chord = self.chord_values[degree]
        note_names = np.vectorize(NOTE_NAMES.get)(selected_chord)
        return list(note_names[0:amount])


scale = Tonality("G")
flatten(scale.mode_values + 3)

scale.get_chord_note_names("III")
