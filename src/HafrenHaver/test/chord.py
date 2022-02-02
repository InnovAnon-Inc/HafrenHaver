#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange
import numpy

@unique
class Chord(Enum):
    #MAJOR        = (4, 3)    # 5, consonant, bright
    #               5, 4     # 3
    #               3, 5     # 4
    MAJOR7       = (4, 3, 4) # 1, consonant, bright
    #               1, 4, 3  # 4
    #               4, 1, 4  # 3
    #               3, 4, 1  # 4
    DOMINANT7    = (4, 3, 3) # 2, dissonant, bright,  tritone   resolution
    #               2, 4, 3  # 3
    #               3, 2, 4  # 3
    #               3, 3, 2  # 4
    #MINOR        = (3, 4)    # 5, consonant, dark
    #               5, 3     # 4
    #               4, 5     # 3
    MINOR7       = (3, 4, 3) # 2, consonant, dark
    #               2, 3, 4  # 3
    #               3, 2, 3  # 4
    #               4, 3, 2  # 3
    MINORMAJ7    = (3, 4, 4) # 1, dissonant, dark,    ?         resolution
    #               1, 3, 4  # 4
    #               4, 1, 3  # 4
    #               4, 4, 1  # 3
    #DIMINISHED   = (3, 3)    # 6, dissonant, dark
    #               6, 3     # 3
    #               3, 6     # 3
    DIMINISHED7  = (3, 3, 4) # 2, dissonant, dark,    tritone   resolution
    #               2, 3, 3  # 4
    #               4, 2, 3  # 3
    #               3, 4, 2  # 3
    DIMINISHEDF7 = (3, 3, 3) # 3, dissonant, dark?,   tritone   resolution
    #AUGMENTED    = (4, 4)    # 4, dissonant, bright,  augmented resolutions
    AUGMENTED7   = (4, 4, 3) # 1, dissonant, bright,  augmented resolutions
    #               1, 4, 4  # 3
    #               3, 1, 4  # 4
    #               4, 3, 1  # 4
    AUGMENTEDM7  = (4, 4, 2) # 2, dissonant, bright,  augmented resolutions
    #               2, 4, 4  # 2
    #               2, 2, 4  # 4
    #               4, 2, 2  # 4
    #SUSMAJ2      = (2, 5)    # 5, dissonant, bright?, ?         resolution
    #               5, 2     # 5
    #               5, 5     # 2
    SUSMAJ2MAJ7  = (2, 5, 4) # 1, dissonant, bright?, ?         resolution
    #               1, 2, 5  # 4
    #               4, 1, 2  # 5
    #               5, 4, 1  # 2
    SUSMAJ2MIN7  = (2, 5, 3) # 2, dissonant, dark?,   ?         resolution
    #               2, 2, 5  # 3
    #               3, 2, 2  # 5
    #               5, 3, 2  # 2
    #SUSMIN2      = (1, 6)    # 5, dissonant, dark?,   ?         resolution
    #               5, 1     # 6
    #               6, 5     # 1
    #               1, 6     # 5
    SUSMIN2MAJ7  = (1, 6, 4) # 1, ?,         ?,       ?         resolution
    #               1, 1, 6  # 4
    #               4, 1, 1  # 6
    #               6, 4, 1  # 1
    SUSMIN2MIN7  = (1, 6, 3) # 2, dissonant, dark?,   ?         resolution
    #               2, 1, 6  # 3
    #               3, 2, 1  # 6
    #               6, 3, 2  # 1
    #SUS4         = (5, 2)    # 5, dissonant, ?,       ?         resolution
    #               5, 5     # 2
    #               2, 5     # 5
    SUS4MAJ7     = (5, 2, 4) # 1, dissonant, bright?, ?         resolution
    #               1, 5, 2  # 4
    #               4, 1, 5  # 2
    #               2, 4, 1  # 5
    SUS4MIN7     = (5, 2, 3) # 2, dissonant, dark?,   ?         resolution
    #               2, 5, 2  # 3
    #               3, 2, 5  # 2
    #               2, 3, 2  # 5

@unique
class Function(Enum):
    TONIC       = 1
    DOMINANT    = 2
    SUBDOMINANT = 3

chord_progressions = (
    (),                                            # TONIC,), # 1
    (Function.DOMINANT,),                          # TONIC,), # 2
    (Function.SUBDOMINANT,),                       # TONIC,), # 2
    (Function.SUBDOMINANT, Function.DOMINANT,),    # TONIC,), # 3
    (Function.DOMINANT,    Function.SUBDOMINANT,), # TONIC,), # 3
)
# TODO cp-builder

"""
class Chord:
    def __init__(self, chroma, io):
        self.chroma = chroma
        self.io     = io # [(interval, octave)...]
	def __len__(self): return len(self.io)
	#def ratio(self, i):
	def __getitem__(self, i):
		a = self.io[i % len(self.io)]
		#a = self.chroma.ratio(a)
		a = self.chroma[a]
		b =        int(i / len(self.io))
		#print("scale a: %s, b: %s" % (a, b,))
		return a * 2**b
"""

