#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange
import numpy

@unique
class BrainWave(Enum):
	LAMBDA  = (100.0, 200.0)
	GAMMA   = ( 40.0, 100.0)
	BETA    = ( 13.0,  39.0)
	ALPHA   = (  7.0,  13.0)
	THETA   = (  4.0,   7.0)
	DELTA   = (  0.5,   4.0)
	EPSILON = (  0.1,   0.5)

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

def interpolate_helper(basef, key, rng, octave):
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
def interpolate(basef, key, rng):
	octave = 0
	#while basef * pow(2, octave) > rng[1]: octave = octave - 1
	while basef * 2**octave >= rng[0]: octave = octave - 1
	indices = interpolate_helper(basef, key, rng, octave)
	#while basef * pow(2, octave) <= rng[0]:
	while basef * 2**octave < rng[1]:
		octave  = octave + 1
		indices = indices + interpolate_helper(basef, key, rng, octave)
	return indices

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

