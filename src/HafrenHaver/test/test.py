#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange
import numpy

class Integer:
    def __init__(self, factors):
        self.factors = factors
    def value(self): return accumulate(operators.mul, 1, map(lambda b, e: b**e, self.factors))
class Ratio:
    def __init__(self, numerator, denominator):
        self.numerator   = numerator
        self.denominator = denominator
    def value(self): return float(self.numerator) / float(self.denominator)


@unique
class Chroma(Enum): # TODO compute from scratch
	LIMIT3a                     = (256/243, 9/8, 32/27, 81/64, 4/3,  729/512, 3/2, 128/81, 27/16, 16/9, 243/128)
	LIMIT3b                     = (256/243, 9/8, 32/27, 81/64, 4/3, 1024/729, 3/2, 128/81, 27/16, 16/9, 243/128)
	LIMIT5_SYMMETRIC1a          = ( 16/15,  9/8,  6/5,   5/4,  4/3,   45/32,  3/2,   8/5,   5/3,  16/9,  15/8)
	LIMIT5_SYMMETRIC1b          = ( 16/15,  9/8,  6/5,   5/4,  4/3,   64/45,  3/2,   8/5,   5/3,  16/9,  15/8)
	LIMIT5_SYMMETRIC2a          = ( 16/15, 10/9,  6/5,   5/4,  4/3,   45/32,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_SYMMETRIC2b          = ( 16/15, 10/9,  6/5,   5/4,  4/3,   64/45,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_STANDARDa = ( 16/15,  9/8,  6/5,   5/4,  4/3,   45/32,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_STANDARDb = ( 16/15,  9/8,  6/5,   5/4,  4/3,   64/45,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_EXTENDEDa = ( 16/15,  9/8,  6/5,   5/4,  4/3,   25/18,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_EXTENDEDb = ( 16/15,  9/8,  6/5,   5/4,  4/3,   36/25,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT7a                     = ( 15/14,  8/7,  6/5,   5/4,  4/3,    7/5,   3/2,   8/5,   5/3,   7/4,  15/8)
	LIMIT7b                     = ( 15/14,  8/7,  6/5,   5/4,  4/3,   10/7,   3/2,   8/5,   5/3,   7/4,  15/8)
	LIMIT17a                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,    7/5,   3/2,   8/5,   5/3,   7/4,  13/7)
	LIMIT17b                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,   17/12,  3/2,   8/5,   5/3,   7/4,  13/7)
	LIMIT17c                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,   10/7,   3/2,   8/5,   5/3,   7/4,  13/7)
	LIMIT17d                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,   24/17,  3/2,   8/5,   5/3,   7/4,  13/7)
limits = (
		#(,), # 2-limit
		(Chroma.LIMIT3a,                     Chroma.LIMIT3b),
		(Chroma.LIMIT5_SYMMETRIC1a,          Chroma.LIMIT5_SYMMETRIC1b,          Chroma.LIMIT5_SYMMETRIC2a,          Chroma.LIMIT5_SYMMETRIC2b,
		 Chroma.LIMIT5_ASYMMETRIC_STANDARDa, Chroma.LIMIT5_ASYMMETRIC_STANDARDb, Chroma.LIMIT5_ASYMMETRIC_EXTENDEDa, Chroma.LIMIT5_ASYMMETRIC_EXTENDEDb,),
		(Chroma.LIMIT7a,                     Chroma.LIMIT7b,),
		(Chroma.LIMIT17a,                    Chroma.LIMIT17b,                    Chroma.LIMIT17c,                    Chroma.LIMIT17d,),
)

def random_base_frequency():
	return 432 + (1 - 2 * random()) * 32
def frequency(base, ratio, octave):
	return base * ratio * 2**octave
def random_limit():
	return choice((3, 5, 7, 17,))
def random_chromatic_helper(limit=None):
	if limit is None: limit = random_limit()
	print("limit: %s" % (limit,))
	if limit ==  3:   return choice(limits[0])
	if limit ==  5:   return choice(limits[1])
	if limit ==  7:   return choice(limits[2])
	if limit == 17:   return choice(limits[3])
	raise Error()
def get_chromatic(chroma): return (1/1, *chroma.value)
def random_chromatic(limit=None):
	chroma = random_chromatic_helper(limit)
	print("chroma: %s" % (chroma,))
	chroma = get_chromatic(chroma)
	print("chroma: %s" % (chroma,))
	return chroma

class Key:
	def __init__(self, chroma, key):
		assert len(chroma) == 12
		assert all(starmap(le, zip(chroma, chroma[1:])))
		assert 0 <= key and key < len(chroma)
		self.chroma = chroma
		self.key    = key
	def __len__(self): return len(self.chroma)
	#def ratio(self, i):
	def __getitem__(self, i):
		#print("key.ratio(i=%s)" % (i,))
		#print("key: %s" % (self.key,))
		#print("chroma: %s" % (self.chroma,))
		a = self.chroma[(i + self.key) % len(self.chroma)]
		b =         int((i + self.key) / len(self.chroma))
		#print("chromatic a: %s, b: %s" % (a, b,))
		return a * 2**b
def random_key(): # TODO parameterize limit
	chroma = random_chromatic()
	key    = randrange(0, len(chroma))
	print("key: %s" % (key,))
	return Key(chroma, key)
key = random_key()

#for i in range(0, len(key.chroma)):
#    print("i=%s: %s" % (i, key.ratio(i),))




@unique
class BrainWave(Enum):
	LAMBDA  = (100.0, 200.0)
	GAMMA   = ( 40.0, 100.0)
	BETA    = ( 13.0,  39.0)
	ALPHA   = (  7.0,  13.0)
	THETA   = (  4.0,   7.0)
	DELTA   = (  0.5,   4.0)
	EPSILON = (  0.1,   0.5)
brain1  = choice((BrainWave.LAMBDA, BrainWave.GAMMA, BrainWave.BETA,))                     #    audible drone
brain2  = choice((BrainWave.ALPHA,  BrainWave.THETA, BrainWave.DELTA, BrainWave.EPSILON,)) # subaudible drone + occasional fast notes in high register
brain1  = brain1.value
brain2  = brain2.value

#@unique
class Register(Enum):
	SOPRANO  = ()
	ALTO     = ()
	TENOR    = ()
	BARITONE = ()
	BASS     = ()

# TODO melody = choice(SOPRANO, ALTO, TENOR, BARITONE, BASS)
AUDIBLE  = (20, 20000) # pitches must be within this range, melodies centered around vocal octaves

@unique
class Tempo(Enum):
	LARGHISSIMO      = ( 20,  24)
	GRAVE            = ( 25,  45)
	LENTO            = ( 40,  60)
	LARGO            = ( 45,  50)
	LARGHETTO        = ( 60,  69)
	ADAGIO           = ( 66,  76)
	ADAGIETTO        = ( 72,  76)
	ADANTE           = ( 76, 108)
	ADANTINO         = ( 80, 108)
	MARCIA_MODERATO  = ( 83,  85)
	ADANTE_MODERATO  = ( 92,  98)
	MODERATO         = ( 98, 112)
	ALLEGRETTO       = (102, 110)
	ALLEGRO_MODERATO = (116, 120)
	ALLEGRO          = (120, 156)
	VIVACE           = (156, 176)
	VIVACISSIMO      = (172, 176)
	#ALLEGRISSIMO     = (172, 176)
	PRESTO           = (168, 200)
	PRESTISSIMO      = (200, 220)

#tempo1           = (GRAVE[0] * 60, GRAVE[1] * 60)
tempo1           = (Tempo.LARGHISSIMO.value[0] / 60, Tempo.PRESTISSIMO.value[1] / 60)
#tempo2           = 

REFRESH          = (20, 60)

RED              = (400, 484)
ORANGE           = (484, 508)
YELLOW           = (508, 526)
GREEN            = (526, 606)
BLUE             = (606, 668)
VIOLET           = (668, 789)
color            = (RED[0] * 10**12, VIOLET[1] * 10**12)

basef = random_base_frequency()
def interpolate_helper(rng, octave):
	indices = []
	#for index in range(0, len(scale.scale)):
	#for index in range(0, len(scale.chroma)):
	for index in range(0, len(key)):
		#pitch = basef * pow(2, octave) * scale.ratio(index)
		#pitch = basef * 2**octave * scale[index]
		#pitch = basef * 2**octave * scale.chroma[index]
		pitch = basef * 2**octave * key[index]
		if rng[0] <= pitch and pitch <= rng[1]:
			indices = indices + [(index, octave)]
			#indices = indices + [basef * pow(2, octave) * scale.ratio(index)]
	return indices
def interpolate(rng):
	octave = 0
	#while basef * pow(2, octave) > rng[1]: octave = octave - 1
	while basef * 2**octave >= rng[0]: octave = octave - 1
	indices = interpolate_helper(rng, octave)
	#while basef * pow(2, octave) <= rng[0]:
	while basef * 2**octave < rng[1]:
		octave  = octave + 1
		indices = indices + interpolate_helper(rng, octave)
	return indices
brains1 = interpolate(brain1)
assert len(brains1) > 0
brains2 = interpolate(brain2)
assert len(brains2) > 0
tempos  = interpolate(tempo1) 
assert len(tempos)  > 0
audible = interpolate(AUDIBLE)
assert len(audible) > 0
# TODO expand audible range
refresh = interpolate(REFRESH)
assert len(refresh) > 0
colors  = interpolate(color)
assert len(colors)  > 0

print("brains1:  %s" % (brains1,))
print("brains2:  %s" % (brains2,))
print("tempos:   %s" % (tempos,))
print("audible:  %s" % (audible,))
print("refresh:  %s" % (refresh,))
print("colors:   %s" % (colors,))

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

@unique
class Variance(Enum):
    SONG    = 1
    SECTION = 2
    PHRASE  = 3
    MEASURE = 4
    BEAT    = 5
variances = {
    Variance.SONG    : 1.0 * 2**-1,
    Variance.SECTION : 1.0 * 2**-2,
    Variance.PHRASE  : 1.0 * 2**-3,
    Variance.MEASURE : 1.0 * 2**-4,
}
def get_choices(): return list(variances.keys())
def get_weights():
    s = sum(variances.values())
    return [v / s for v in variances.values()]

harmonic_variance                  = choice(list(Variance))
if harmonic_variance in variances:
    variances[harmonic_variance]   = variances[harmonic_variance]   / 2

if harmonic_variance.value > Variance.SONG.value:
    while True:
        modulation_variance        = numpy.random.choice(get_choices(), p=get_weights())
        if modulation_variance.value <= harmonic_variance.value: break
    variances[modulation_variance] = variances[modulation_variance] / 2
else:   modulation_variance        = None
if harmonic_variance.value > Variance.SONG.value:
    while True:
        borrow_variance            = numpy.random.choice(get_choices(), p=get_weights())
        if borrow_variance.value     <= harmonic_variance.value: break
    variances[borrow_variance]     = variances[borrow_variance]     / 2
else:   borrow_variance            = None

accent_variance                    = numpy.random.choice(get_choices(), p=get_weights())
variances[accent_variance]         = variances[accent_variance]     / 2
dynamics_variance                  = numpy.random.choice(get_choices(), p=get_weights())
variances[dynamics_variance]       = variances[dynamics_variance]   / 2

meter_variance                     = numpy.random.choice(get_choices(), p=get_weights())
variances[meter_variance]          = variances[meter_variance]      / 2
tempo_variance                     = numpy.random.choice(get_choices(), p=get_weights())
variances[tempo_variance]          = variances[tempo_variance]      / 2

print("harmonic_variance  : %s" % (harmonic_variance,))
print("modulation_variance: %s" % (modulation_variance,))
print("borrow_variance    : %s" % (borrow_variance,))
print("accent_variance    : %s" % (accent_variance,))
print("dynamics_variance  : %s" % (dynamics_variance,))
print("meter_variance     : %s" % (meter_variance,))
print("tempo_variance     : %s" % (tempo_variance,))





# number of chord changes, number of modulations, number of borrowed chords
# consonance cadence, brightness cadence
# TODO meter, accents, rhythms

# 

# TODO count uniq song sections, decide # different verse structures

# dynamics
# 1: per section
# 2: per phrase
# 3: within phrases

# mode/key changes
# 1: none
# 2: per section
# 3: per phrase
# 4: within phrases

# tempo modulations
# 1-4

# t-s-d harmonic cadence
# 1-4

# secondary/borrowed cadence & chords

# bjorklund accent patterns
# 1-4

# rhythm cadence & rhythms
# whole, half, quarter, eighth, sixteenth, triplets


# ct-nct cadence

# chords
# melody
# countermelodies

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

@unique
class Tetra1(Enum):
	MAJOR    = (2, 2, 1)
	MINOR    = (2, 1, 2)
	PHRYGIAN = (1, 2, 2)
	HARMONIC = (1, 3, 1)
	MISC1    = (3, 1, 1)
	MISC2    = (1, 1, 3)
@unique
class Tetra2(Enum):
	MISC1    = (3, 2, 1)
	MISC2    = (3, 1, 2)
	MISC3    = (2, 2, 2)
	MISC4    = (1, 3, 2)
	MISC5    = (2, 1, 3)
	MISC6    = (1, 2, 3)
TETRA_EPSILON1 = 0.5
TETRA_EPSILON2 = 0.5
def random_tetrachords():
	if   random() < TETRA_EPSILON1: ltetra, utetra = Tetra1, Tetra1
	elif random() < TETRA_EPSILON2: ltetra, utetra = Tetra1, Tetra2
	else:                           ltetra, utetra = Tetra2, Tetra1
	ltetra = choice(list(ltetra))
	utetra = choice(list(utetra))
	print("lower tetra: %s" % (ltetra,))
	print("upper tetra: %s" % (utetra,))
	ltetra = ltetra.value
	utetra = utetra.value
	print("lower tetra: %s" % (ltetra,))
	print("upper tetra: %s" % (utetra,))
	assert len(ltetra) == 3
	assert len(utetra) == 3
	return ltetra, utetra
ltetra, utetra = random_tetrachords()

step  = len(key.chroma) - sum(ltetra) - sum(utetra)
print("step: %s" % (step,))
scale = (*ltetra, step, *utetra)
assert len(scale) == len(ltetra) + 1 + len(utetra)

from itertools import accumulate

#scale  = list(accumulate((0,) + scale))
#assert scale[-1] == len(chroma)
#scale  = scale[:-1]
#print("scale: %s" % (scale,))

mode   = randrange(0, len(scale))
print("mode: %s" % (mode,))

class Scale:
	def __init__(self, chroma, scale, mode):
		#assert sum(scale) == len(key.chroma)
		assert sum(scale) == len(chroma)
		assert 0 <= mode and mode < len(scale)
		self.chroma = chroma
		#self.orig   = scale
		scale       = scale[mode:] + scale[:mode]
		scale       = list(accumulate((0,) + scale))
		#assert scale[-1] == len(key.chroma)
		assert scale[-1] == len(chroma)
		scale       = tuple(scale[:-1])
		print("scale: %s" % (scale,))
		self.scale  = scale
		self.mode   = mode
	def __len__(self): return len(self.scale)
	#def ratio(self, i):
	def __getitem__(self, i):
		a = self.scale[i % len(self.scale)]
		#a = self.chroma.ratio(a)
		a = self.chroma[a]
		b =        int(i / len(self.scale))
		#print("scale a: %s, b: %s" % (a, b,))
		return a * 2**b
scale = Scale(key, scale, mode)
#ratios = tuple((scale.ratio(i) for i in range(0, len(scale.scale))))
ratios = tuple((scale[i] for i in range(0, len(scale))))

#for i in range(0, len(scale.scale)):
#    print("i=%s: %s" % (i, scale.ratio(i),))

#ratios = [chroma[(scale[(i + mode) % len(scale)]) % len(chroma)] for i in range(0, len(scale))]
print("ratios: %s" % (ratios,))




# http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
def wavelength_to_rgb(wavelength, gamma=0.8):

	'''This converts a given wavelength of light to an
	approximate RGB color value. The wavelength must be given
	in nanometers in the range from 380 nm through 750 nm
	(789 THz through 400 THz).

	Based on code by Dan Bruton
	http://www.physics.sfasu.edu/astro/color/spectra.html
	'''

	wavelength = float(wavelength)
	if wavelength >= 380 and wavelength <= 440:
		attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
		R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
		G = 0.0
		B = (1.0 * attenuation) ** gamma
	elif wavelength >= 440 and wavelength <= 490:
		R = 0.0
		G = ((wavelength - 440) / (490 - 440)) ** gamma
		B = 1.0
	elif wavelength >= 490 and wavelength <= 510:
		R = 0.0
		G = 1.0
		B = (-(wavelength - 510) / (510 - 490)) ** gamma
	elif wavelength >= 510 and wavelength <= 580:
		R = ((wavelength - 510) / (580 - 510)) ** gamma
		G = 1.0
		B = 0.0
	elif wavelength >= 580 and wavelength <= 645:
		R = 1.0
		G = (-(wavelength - 645) / (645 - 580)) ** gamma
		B = 0.0
	elif wavelength >= 645 and wavelength <= 750:
		attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
		R = (1.0 * attenuation) ** gamma
		G = 0.0
		B = 0.0
	else:
		R = 0.0
		G = 0.0
		B = 0.0
	R *= 255
	G *= 255
	B *= 255
	return (int(R), int(G), int(B))











#from numba  import jit

import pygame
from pygame.locals import *

import math
from math import log

from datetime import datetime

#brains1 = [basef * 2**octave * scale[index] for index, octave in brains1]
#brains2 = [basef * 2**octave * scale[index] for index, octave in brains2]
#tempos = [basef * 2**octave * scale[index] for index, octave in tempos]
#audible = [basef * 2**octave * scale[index] for index, octave in audible]
#refresh = [basef * 2**octave * scale[index] for index, octave in refresh]
#colors = [basef * 2**octave * scale[index] for index, octave in colors]
brains1 = [basef * 2**octave * scale.chroma[index] for index, octave in brains1]
brains2 = [basef * 2**octave * scale.chroma[index] for index, octave in brains2]
tempos = [basef * 2**octave * scale.chroma[index] for index, octave in tempos]
audible = [basef * 2**octave * scale.chroma[index] for index, octave in audible]
refresh = [basef * 2**octave * scale.chroma[index] for index, octave in refresh]
colors = [basef * 2**octave * scale.chroma[index] for index, octave in colors]

c      = 2.99792458 * 10**17
colors2 = [wavelength_to_rgb(c / color) for color in colors]

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
	return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
colors2 = '\n'.join((get_color_escape(*color) + str(color) + RESET for color in colors2))
print("colors2:   %s" % (colors2,))

pitch1  = choice(brains1)
pitch2  = choice(brains2)
#pitch3  = choice(tempos) / 60
pitch3  = choice(tempos)
# TODO
#pitch1 = 432
#pitch2 = 20
#pitch3 = 1
print("pitches: %s, %s, %s" % (pitch1, pitch2, pitch3,))

duration = 10.0          # in seconds



class Audio:
	def __init__(self, sample_rate, bits):
		pygame.mixer.pre_init(frequency=sample_rate, size=-bits, channels=2)
		pygame.init()
		self.sample_rate = sample_rate
		self.bits        = bits
	def __del__(self): pygame.quit()
class Sound:
	def __init__(self, audio, duration):
		self.audio     = audio
		sample_rate    = self.audio.sample_rate
		self.n_samples = int(round(duration*sample_rate))
		#self.buf       = numpy.zeros((self.n_samples, 2), dtype=numpy.float)
		self.dt        = numpy.int16
		#self.buf       = numpy.zeros((self.n_samples, 2), dtype=self.dt)
		self.buf       = numpy.zeros((self.n_samples, 2))
	def make_sound(self):
		#max_sample = numpy.iinfo(numpy.int16).max
		#buf        = (self.buf * max_sample).astype(numpy.int16)
		#print("buf: %s" % (buf,))
		buf        = self.buf
		max_sample = numpy.iinfo(self.dt).max
		buf        = numpy.int16(buf / numpy.max(numpy.abs(buf)) * max_sample)
		return pygame.sndarray.make_sound(buf)
	def play_sound(self, loops=1):
		sound = self.make_sound()
		sound.play(loops=loops)
		pygame.time.wait(int(sound.get_length() * 1000))
	def sine_wave(self, pitch, duration, volume):
		print("sine_wave(pitch=%s, duration=%s, volume=%s)" % (pitch, duration, volume,))
		sample_rate = self.audio.sample_rate
		max_sample  = numpy.iinfo(self.dt).max
		assert max_sample == 2**(self.audio.bits - 1) - 1
		volume      = volume * max_sample

		size        = int(round(sample_rate * duration))
		#temp        = numpy.arange(0, size) / sample_rate
		#temp        = numpy.linspace(0, size, size)
		temp        = numpy.linspace(0, duration, size, False)
		temp        = volume * numpy.sin(2.0 * numpy.pi * pitch * temp)
		temp        = self.dt(temp)
		#temp        = numpy.vstack((temp, temp)).reshape((-1, 2), order='F')
		temp        = numpy.repeat(temp.reshape(size, 1), 2, axis = 1)
		return temp
	def sine_waves_1(self, pitch, duration, volume):
		print("sine_waves_1(pitch=%s, duration=%s, volume=%s)" % (pitch, duration, volume,))
		sample_rate = self.audio.sample_rate
		max_sample  = numpy.iinfo(self.dt).max
		assert max_sample == 2**(self.audio.bits - 1) - 1
		#volume      = volume * max_sample
		size        = int(round(sample_rate * duration))
		return (self.sine_wave(pitch * 2**v, duration, volume / 2**v) for v in range(int(round(log(volume * max_sample)))))
		#return (self.sine_wave(pitch * 2**v, duration, volume / 2**v) for v in range(4))
	def sine_waves_2(self, pitch, duration, volume):
		print("sine_waves_1(pitch=%s, duration=%s, volume=%s)" % (pitch, duration, volume,))
		sample_rate = self.audio.sample_rate
		max_sample  = numpy.iinfo(self.dt).max
		assert max_sample == 2**(self.audio.bits - 1) - 1
		#volume      = volume * max_sample
		size        = int(round(sample_rate * duration))
		#return (self.sine_wave(pitch * 2**v, duration, volume / 2**v) for v in range(int(round(log(volume * max_sample)))))
		return (self.sine_wave(pitch * 2**v, duration, volume / (v + 1)) for v in range(int(round((log(20000 / pitch))))))

		#temp        = numpy.linspace(0, duration, size)
		#res         = numpy.zeros(size, dtype=self.dt)
		#for v in range(int(round(log(volume)))):
		#	#print("v: %s" % (2 ** v,))
		#	p       = pitch * 2**v
		#	V       = volume / 2**v
		#	t       = V * numpy.sin(2.0 * numpy.pi * p * temp)
		#	t       = self.dt(temp)
		#	res     = res + t
		#temp        = numpy.repeat(res.reshape(size, 1), 2, axis = 1)
		#return temp
	def add_wave(self, wave_func, pitch, duration, volume, offset):
		sample_rate = self.audio.sample_rate
		temp        = wave_func(pitch, duration, volume)
		start       = int(round(sample_rate *  offset))
		end         = int(round(sample_rate * (offset + duration)))
		buf         = self.buf
		#buf         = numpy.zeros((self.n_samples, 2))
		#for s in range(start, end - 1):
		for s in range(start, end):
			t = s - start
			buf[s][0] = buf[s][0] + temp[t][0]
			buf[s][1] = buf[s][1] + temp[t][1]
		max_sample  = numpy.iinfo(self.dt).max
		#self.buf = numpy.int16(buf / numpy.max(numpy.abs(buf)) * max_sample)
	def add_waves(self, wave_func, pitch, duration, volume, offset):
		sample_rate = self.audio.sample_rate
		temp        = wave_func(pitch, duration, volume)
		start       = int(round(sample_rate *  offset))
		end         = int(round(sample_rate * (offset + duration)))
		buf         = self.buf
		#buf         = numpy.zeros((self.n_samples, 2))
		for T in temp:
			for s in range(start, end - 1):
				t = s - start
				buf[s][0] = buf[s][0] + T[t][0]
				buf[s][1] = buf[s][1] + T[t][1]
		max_sample  = numpy.iinfo(self.dt).max
		#self.buf = numpy.int16(buf / numpy.max(numpy.abs(buf)) * max_sample)




if __name__ == "__main__":
	#from time import sleep

	def main ():
		sample_rate = 44100
		bits        = 16
		duration    = 10
		audio = Audio(sample_rate, bits)
		sound = Sound(audio, duration)

		#for k in range(duration): sound.sine_wave(432, 0.5, k)

		#buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
		#arr = stereo_sine_wave(0, n_samples, n_samples, pitch1)
		#print("arr: %s" % (arr,))
		#buf = buf + arr

		#pitch1 = 432
		#pitch2 = 7.83 / 2
		#pitch3 = 1
		sound.add_wave(sound.sine_wave, pitch2, duration, 1.0, 0)
		#sound.add_waves(sound.sine_waves_1, pitch2, duration, 1.0, 0)
		sound.add_wave(sound.sine_wave, pitch1, duration, 0.5, 0)
		#for k in range(int(round(duration * pitch1))): sound.add_waves(sound.sine_waves_1, 432.0 * 3 / 2, 0.5 / pitch1, 0.25, float(k) / pitch1)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_2, 432,           0.5 / pitch3, 0.25, float(k) / pitch3)
		#sound.add_waves(sound.sine_waves_2, pitch1, duration, 1.0, 0)
		#sound.add_waves(sound.sine_waves_1, pitch1, duration, 1.0, 0)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_1, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_2, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch3))): sound.add_wave(sound.sine_wave, pitch1, 0.5 / pitch3, 1.0, k / pitch3)

		#for k in range(int(round(duration * pitch3))): sound.add_wave(sound.sine_waves_1, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch2))): play(buf, pitch2, 0.5 / pitch2, k / pitch2)

		#sound = pygame.sndarray.make_sound(buf)
		#play once, then loop forever
		#sound.play(loops = 1)

		sound.play_sound()
		#sleep(0.1)
		#sleep(duration)
		#pygame.time.delay(1000)
		while pygame.mixer.music.get_busy(): pygame.time.Clock().tick()

		#pygame.quit()
	main ()
