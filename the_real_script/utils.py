"""
The Real Script utils.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, Union, Tuple, List, Sequence

import numpy as np

from constants import NOTES, INTERVALS, PITCHSET_NAMES, C_BASE_SCALES, DEGREES


def invert(values: np.array, inversion: int) -> np.array:
    """Return the specified musical inversion of the values."""
    if np.abs(inversion) > (len(values) - 1):
        raise ValueError("Inversion out of range")
    
    return np.hstack([values[inversion:], values[:inversion]]).astype(int)


def calculate_intervals(values: np.array) -> Tuple[int]:
    """Calculate intervals between the provided note values."""
    return tuple(
        [(next_note - note) % 12 for note, next_note in zip(values, values[1:])]
    )

# TODO: init family (major, minor, dominant)
# TODO: init type (chord, scale, other)
class PitchSet:
    """
    A PitchSet is a collection of notes. Chords, scales and 
    melodies can be instanciated as PitchSets. Simple arithmetical 
    operations can be performed with them.
    """

    def __init__(self, values: Sequence[int]) -> None:
        """Class instance constructor."""
        
        valid_builder_types = (int, tuple, list, np.ndarray, PitchSet)
        
        if not isinstance(values, valid_builder_types):
            raise TypeError(
                f"Valid object types to build a PitchSet are: {valid_builder_types}"
            )
            
        if isinstance(values, int):
            values = [values]
        if isinstance(values, PitchSet):
            values = values.values
            
        valid_builder_data_types = (int, np.int_)
        are_valid = [isinstance(value, valid_builder_data_types) for value in values]
            
        if not all(are_valid):
            raise TypeError(
                f"A PitchSet can only be constructed from integers."
            )

        # Value attributes
        self.values = np.array(values) % 12
        self.interval_values = calculate_intervals(self.values)
        self.structure_values = np.hstack([0, np.cumsum(self.interval_values)])
        
        # Name attributes
        self.tonic = NOTES[self.values[0]]
        self.notes = [NOTES[value] for value in self.values]
        self.name = self.init_name()
        self.intervals = [INTERVALS[interval] for interval in self.interval_values]
        self.structure = [INTERVALS[interval] for interval in self.structure_values]
        self.third = self.init_third()


    def __iter__(self) -> str:
        """Make class iterable."""
        for notes in self.notes:
            yield notes

    def __getitem__(self, index) -> str:
        """Make class indexable."""
        return self.notes[index]

    def __add__(self, summand) -> "PitchSet":
        """Make class summable."""
        return PitchSet(self.values + PitchSet(summand).values)

    def __radd__(self, summand) -> "PitchSet":
        """Reverse sum."""
        return self.__add__(summand)

    def __sub__(self, subtrahend) -> "PitchSet":
        """Make class subtractable."""
        return PitchSet(self.values - PitchSet(subtrahend).values)
        
    def __rsub__(self, minuend) -> "PitchSet":
        """Reverse subtraction."""
        return PitchSet(minuend) - self
    
    def __repr__(self) -> str:
        """Return name when print is called."""
        return self.name

    def init_name(self) -> str:
        """Initialize set name."""
        try:
            return self.tonic + PITCHSET_NAMES[self.interval_values]
        except KeyError:
            return f"Unknown set: {self.notes}"
        
    def init_third(self) -> str:
        """Initialize third""" 
        if 3 in self.structure_values:
            return "minor"
        elif 4 in self.structure_values:
            return "major"
        else:
            return "suspended"
        
    def invert(self, inversion: int) -> "PitchSet":
        """Return specified inversion of the set."""
        return PitchSet(invert(self.values, inversion=inversion))


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
        self.cromatic = PitchSet(invert(C_BASE_SCALES["cromatic"], NOTES.index(tonic)))
        self.scale = self.init_scale()
        
    def __repr__(self):
        """Return scale when print is called."""
        return f"{self.scale}"

    def init_scale(self) -> PitchSet:
        """Return main scale of the tonality."""
        tonic_value = NOTES.index(self.tonic)
        inversion_values = invert(C_BASE_SCALES[self.scale_type], DEGREES.index(self.mode))
        interval_values = calculate_intervals(inversion_values)
        modal_values = np.hstack([tonic_value, (tonic_value + np.cumsum(interval_values))])
        return PitchSet(modal_values)

    def chords(self, degrees: Sequence[Union[str, int]], size: int = 4) -> List[PitchSet]:
        """Return list of chords from the chosen degrees with the specified number of notes."""
        
        if isinstance(degrees, (str, int)):
            degrees = [degrees]
  
        chords = []
        for degree in degrees:
            
            if isinstance(degree, int):
                degree_value = degree - 1
            if isinstance(degree, str):
                degree_value = DEGREES.index(degree)
            
            if degree_value not in range(0, 7):
                raise ValueError(f"Invalid degree: {degree}")
            
            three_octaves_scale = list(self.scale.values) * 3
            seven_note_chord = three_octaves_scale[degree_value : degree_value + 14 : 2]
            cropped_chord = seven_note_chord[0:size]
            chords.append(PitchSet(cropped_chord))
            
        if len(chords) == 1:
            chords = chords[0]

        return chords
