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
    "": (4, 3),
    "m": (3, 4),
    
    # 7th chords
    "maj7": (4, 3, 4),
    "m7": (3, 4, 3),
    "7": (4, 3, 3),
    "m7b5": (3, 3, 4),
    "m7(maj7)": (3, 4, 4),
    "maj7(#5)": (4, 4, 3),
    "dim": (3, 3, 3),
    
    # Cromatic scale
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
