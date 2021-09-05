"""
Main file of The Real Script, program to generate random jazz standards.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, Union, List

import numpy as np


CROMATIC_VALUES = np.arange(12)

O = np.nan
SCALE_MASKS = {"heptatonic": {"diatonic": [1, O, 1, O, 1, 1, O, 1, O, 1, O, 1]}}

NOTE_NAME_TUPLE = ("C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")
NOTE_VALUES = dict(zip(NOTE_NAME_TUPLE, CROMATIC_VALUES))
NOTE_NAMES = dict(zip(CROMATIC_VALUES, NOTE_NAME_TUPLE))

DEGREES = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")
C_MAJOR_DEGREE_VALUES = dict(zip(DEGREES[0:9], {0, 2, 4, 5, 7, 9, 11}))


def modulate(a: Union[int, np.array], b: Union[int, np.array]) -> np.array:
    """Modulate the note or scale 'a' by adding the scalar or vector 'b'."""
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
        scale_size: Optional[str] = "heptatonic",
        mode: Optional[str] = "I",
    ) -> None:
        """Class instance constructor."""
        self.tonic = tonic
        self.scale_type = scale_type
        self.scale_size = scale_size
        self.cromatic_values = self.init_cromatic_values()
        self.mode = mode
        self.mode_mask = self.init_mode_mask()
        self.scale_values = self.init_scale_values()
        self.chord_values = self.init_chord_values()

    def init_cromatic_values(self) -> np.array:
        """Modulate cromatic values to the provided tonic."""
        return modulate(CROMATIC_VALUES, NOTE_VALUES[self.tonic])

    def init_mode_mask(self) -> List[int]:
        """Retrieve scale mask and displace it to the selected mode."""
        mode_value = C_MAJOR_DEGREE_VALUES[self.mode]
        scale_mask = SCALE_MASKS[self.scale_size][self.scale_type] * 2
        return [scale_mask[number] for number in range(mode_value, 12 + mode_value)]

    def init_scale_values(self) -> np.array:
        """Mask the chromatic values to obtain the scale values."""
        return np.array(self.cromatic_values) * np.array(self.mode_mask)

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
