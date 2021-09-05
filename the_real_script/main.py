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
DEGREES = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4, "VI": 5, "VII": 6, "VIII":7}

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
        self.mode = DEGREES[mode]
        self.mode_index = self.init_mode_index()
        self.scale_values = self.init_scale_values()
        self.chord_values = self.init_chord_values()

    def init_cromatic_values(self) -> np.array:
        """Return the cromatic scale modulated to the tonic."""
        return modulate(CROMATIC_VALUES, NOTE_VALUES[self.tonic])

    def init_mode_index(self) -> List[int]:
        """Retrieve scale index and transform it into the selected mode index."""
        scale = SCALE_INDEX[self.scale_type]
        double_scale = scale * 2
        mode_indexes = range(self.mode, self.mode + len(scale))
        return [double_scale[index] for index in mode_indexes]
    
    def init_scale_values(self) -> np.array:
        """Use the mode index on the chromatic values to obtain the scale values."""
        return self.cromatic_values[self.mode_index]

    def init_chord_values(self) -> np.array:
        """Get the full chord (7 notes) of every degree in the scale."""
        scale_without_nans = self.scale_values[~np.isnan(self.scale_values)]
        repeated_scale = list(scale_without_nans) * 3
        return [
            repeated_scale[index : index + 14 : 2]
            for index, _ in enumerate(scale_without_nans)
        ]

    def get_scale_note_names(self) -> List[str]:
        """Translate scale note values to names."""
        scale_without_nans = self.scale_values[~np.isnan(self.scale_values)]
        return list(np.vectorize(NOTE_NAMES.get)(scale_without_nans))

    def get_chord_note_names(self) -> List[str]:
        """Translate chord note values to names."""
        return {
            DEGREES[index]: list(np.vectorize(NOTE_NAMES.get)(chord))
            for index, chord in enumerate(self.chord_values)
        }
