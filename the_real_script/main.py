"""
Main file of The Real Script, program to generate random jazz standards.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, Union, List

import numpy as np


# Scales
CROMATIC_VALUES = np.arange(12)
SCALE_INDEX = {"diatonic": [0, 2, 4, 5, 7, 9, 11]}

# Note names
NOTE_NAME_TUPLE = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
NOTE_VALUES = dict(zip(NOTE_NAME_TUPLE, CROMATIC_VALUES))
NOTE_NAMES = dict(zip(CROMATIC_VALUES, NOTE_NAME_TUPLE))

# Degrees
DEGREE_TUPLE = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")
DEGREE_VALUES = dict(zip(DEGREE_TUPLE, range(0, 9)))
DEGREE_NAMES = dict(zip(range(0, 9), DEGREE_TUPLE))


# Intervals
INTERVALS = dict(
    zip(
        ["P1", "m2", "M2", "m3", "M3", "P4", "TT", "P5", "m6", "M6", "m7", "M7", "P8"],
        list(CROMATIC_VALUES) + [12],
    )
)


def modulate(a: Union[int, np.array], b: Union[int, np.array]) -> np.array:
    """Modulate the note, chord or scale 'a' by adding 'b'."""
    outcome = np.array(a + b)
    while (outcome > 11).any():
        outcome = np.where(outcome > 11, outcome - 12, outcome)
    while (outcome < 0).any():
        outcome = np.where(outcome < 0, outcome + 12, outcome)
    return outcome


class Scale:
    """Scale class."""

    def __init__(
        self,
        tonic: str,
        scale_type: Optional[str] = "diatonic",
        mode: Optional[str] = "I",
    ) -> None:
        """Class instance constructor."""
        self.tonic = tonic
        self.scale_type = scale_type
        self.cromatic_values = self.init_cromatic_values()
        self.mode = DEGREE_VALUES[mode]
        self.mode_index = self.init_mode_index()
        self.mode_values = self.init_mode_values()
        self.chord_values = self.init_chord_values()

    def init_cromatic_values(self) -> np.array:
        """Return the cromatic scale modulated to the tonic."""
        return modulate(CROMATIC_VALUES, NOTE_VALUES[self.tonic])

    def init_mode_index(self) -> List[int]:
        """Retrieve scale index and transform it into the selected mode index."""
        scale_index = SCALE_INDEX[self.scale_type]
        double_scale_index = scale_index * 2
        mode_range = range(self.mode, self.mode + len(scale_index))
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

    def get_notes(self) -> List[str]:
        """Translate mode note values to names."""
        return list(np.vectorize(NOTE_NAMES.get)(self.mode_values))

    # TODO: enable option to calculate only one chord
    def get_chord_notes(self) -> List[str]:
        """Translate chord note values to names."""
        return {
            DEGREE_NAMES[index]: list(np.vectorize(NOTE_NAMES.get)(chord))
            for index, chord in enumerate(self.chord_values)
        }
