"""
Main file of The Real Script, program to generate random jazz standards.

created: 2021-09-04
author: Roberto Nogueras Zondag
email: rnogueras@protonmail.com
"""

from typing import Optional, Tuple, List, Type, Sequence

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
PITCHSET_INTERVALS = {
    
    # Triads
    "M": (4, 3),
    "m": (3, 4),
    
    # 7th chords
    "maj7": (4, 3, 4),
    "m7": (3, 4, 3),
    "7": (4, 3, 3),
    "m7b5": (3, 3, 4),
    "m7(maj7)": (3, 4, 4),
    "maj7(#5)": (4, 4, 3),
    "dim": (3, 3, 3),
    
    # Cromatic
    " cromatic": tuple(np.full(11, 1)),
    
    # Diatonic modes
    " ionian": (2, 2, 1, 2, 2, 2),
    " dorian": (2, 1, 2, 2, 2, 1),
    " phrygian": (1, 2, 2, 2, 1, 2),
    " lydian": (2, 2, 2, 1, 2, 2),
    " mixolydian": (2, 2, 1, 2, 2, 1),
    " aeolian": (2, 1, 2, 2, 1, 2),
    " locrian": (1, 2, 2, 1, 2, 2),
    
    # Harmonic minor modes
    " harmonic minor": (2, 1, 2, 2, 1, 3),
    
    # Melodic minor modes
    " melodic minor": (2, 1, 2, 2, 2, 2),

}
PITCHSET_NAMES = {intervals: chord for chord, intervals in PITCHSET_INTERVALS.items()}


def invert(values: np.array, inversion: int) -> np.array:
    """Return the specified musical inversion of the values."""
    return np.hstack([values[inversion:], values[:inversion]]).astype(int)


def calculate_intervals(values: np.array) -> Tuple[int]:
    """Calculate intervals between the provided note values."""
    return tuple(
        [(next_note - note) % 12 for note, next_note in zip(values, values[1:])]
    )


# TODO: Make pitch sets constructable from either values or tonic + intervals (like in LDR).
class PitchSet:
    """
    A pitch set is a collection of tones. Chords, scales and 
    melodies are examples of pitch sets. Simple arithmetical 
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
                f"A pitch set can only be constructed from integers."
            )

        # Values
        self.values = np.array(values) % 12
        self.interval_values = calculate_intervals(self.values)
        
        # Names
        self.tonic = NOTES[self.values[0]]
        self.notes = [NOTES[value] for value in self.values]
        self.name = self.init_name()
        self.intervals = [INTERVALS[interval] for interval in self.interval_values]

    def __iter__(self):
        """Make class iterable."""
        for notes in self.notes:
            yield notes

    def __getitem__(self, index):
        """Make class indexable."""
        return self.notes[index]

    def __add__(self, summand):
        """Make class summable."""
        return PitchSet(self.values + PitchSet(summand).values)

    def __radd__(self, summand):
        """Reverse sum."""
        return self.__add__(summand)

    def __sub__(self, subtrahend):
        """Make class subtractable."""
        return PitchSet(self.values - PitchSet(subtrahend).values)
        
    def __rsub__(self, minuend):
        """Reverse subtraction."""
        return PitchSet(minuend) - self
    
    def __repr__(self):
        """Return name when print is called."""
        return self.name

    def init_name(self) -> str:
        """Initialize name of the set."""
        try:
            return self.tonic + PITCHSET_NAMES[self.interval_values]
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
        self.cromatic = PitchSet(invert(C_SCALES["cromatic"], NOTES.index(tonic)))
        self.scale = self.init_scale()
        
    def __repr__(self):
        """Return scale when print is called."""
        return f"{self.scale}"

    def init_scale(self) -> Type[PitchSet]:
        """Return main scale of the tonality."""
        tonic_value = NOTES.index(self.tonic)
        inversion_values = invert(C_SCALES[self.scale_type], DEGREES.index(self.mode))
        interval_values = calculate_intervals(inversion_values)
        modal_values = np.hstack([tonic_value, (tonic_value + np.cumsum(interval_values))])
        return PitchSet(modal_values)

    def chords(self, degrees: Sequence[str], size: int = 4) -> List[Type[PitchSet]]:
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
            chords.append(PitchSet(seven_note_chord[0:size]))
            
        if len(chords) == 1:
            chords = chords[0]

        return chords