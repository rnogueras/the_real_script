"""
Main file of The Real Script, program to generate random jazz standards.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, Union, List

import numpy as np

x = np.nan

CROMATIC_VALUES = np.arange(12)
SCALE_MASKS = {
    "heptatonic": {
        "diatonic": [1, x, 1, x, 1, 1, x, 1, x, 1, x, 1],
    }
}
CROMATIC_NAMES = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
NOTE_VALUES = dict(zip(CROMATIC_NAMES, CROMATIC_VALUES))
NOTE_NAMES = dict(zip(CROMATIC_VALUES, CROMATIC_NAMES))
BASE_DEGREE_VALUES = {"I": 0, "II": 2, "III": 4, "IV": 5, "V": 7, "VI": 9, "VII": 11}


def modulate(a: Union[int, np.array], b: Union[int, np.array]) -> np.array:
    """Modulate the note or scale 'a' by adding 'b'."""
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
        self.mode = mode
        self.scale_mask = self.init_scale_mask(scale_size, scale_type, mode)
        self.cromatic_values = self.init_cromatic_values(tonic)
        self.scale_values = self.init_scale_values(np.array(self.scale_mask))

    def init_cromatic_values(self, tonic: str) -> np.array:
        """Init cromatic values."""
        return modulate(CROMATIC_VALUES, NOTE_VALUES[tonic])

    def init_scale_mask(self, scale_size: str, scale_type: str, mode: str) -> np.array:
        """Init scale mask."""
        mode_value = BASE_DEGREE_VALUES[mode]
        repeated_mask = SCALE_MASKS[scale_size][scale_type] * 2
        return [repeated_mask[number] for number in range(mode_value, 12 + mode_value)]

    def init_scale_values(self, scale_mask: np.array) -> np.array:
        """Init scale values."""
        return self.cromatic_values * scale_mask

    def get_note_names(self) -> List[str]:
        """Return scale note names."""
        return [
            NOTE_NAMES[value]
            for value in self.scale_values[~np.isnan(self.scale_values)]
        ]
