#! /usr/bin/env python3

from enum      import Enum
from math      import pow
#from numba     import jit
from random    import choice

from solfeggio import random_solfeggio

ratios_db = { # odd? limit
	3: ( # 2-3
		# pythagorean #1
		(256/243,  9/8, 32/27, 81/64, 4/3,  729/512, 3/2, 128/81, 27/16, 16/9, 243/128),
		# pythagorean #2
		(256/243,  9/8, 32/27, 81/64, 4/3, 1024/729, 3/2, 128/81, 27/16, 16/9, 243/128),
	),
	5: ( # 2-3-5
		# symmetric scale #1
		( 16/ 15,  9/8,  6/ 5,  5/ 4, 4/3,   64/ 45, 3/2,   8/ 5,  5/ 3, 16/9,  15/  8),
		( 16/ 15,  9/8,  6/ 5,  5/ 4, 4/3,   45/ 32, 3/2,   8/ 5,  5/ 3, 16/9,  15/  8),
		# symmetric scale #2
		( 16/ 15, 10/9,  6/ 5,  5/ 4, 4/3,   64/ 45, 3/2,   8/ 5,  5/ 3,  9/5,  15/  8),
		( 16/ 15, 10/9,  6/ 5,  5/ 4, 4/3,   45/ 32, 3/2,   8/ 5,  5/ 3,  9/5,  15/  8),
		# asymmetric scale standard
		( 16/ 15,  9/8,  6/ 5,  5/ 4, 4/3,   45/ 32, 3/2,   8/ 5,  5/ 3,  9/5,  15/  8),
		( 16/ 15,  9/8,  6/ 5,  5/ 4, 4/3,   64/ 45, 3/2,   8/ 5,  5/ 3,  9/5,  15/  8),
		# asymmetric scale extended
		( 16/ 15,  9/8,  6/ 5,  5/ 4, 4/3,   25/ 18, 3/2,   8/ 5,  5/ 3,  9/5,  15/  8),
		( 16/ 15,  9/8,  6/ 5,  5/ 4, 4/3,   36/ 25, 3/2,   8/ 5,  5/ 3,  9/5,  15/  8),
	),
	7: ( # 2-3-5-7
		# 7-limit tuning
		( 15/ 14,  8/7,  6/ 5,  5/ 4, 4/3,    7/  5, 3/2,   8/ 5,  5/ 3,  7/4,  15/  8),
		( 15/ 14,  8/7,  6/ 5,  5/ 4, 4/3,   10/  7, 3/2,   8/ 5,  5/ 3,  7/4,  15/  8),
	),
	17: ( # 2-3-5-7-11-13-17
		# 17-limit tuning
		( 14/ 13,  8/7,  6/ 5,  5/ 4, 4/3,    7/  5, 3/2,   8/ 5,  5/ 3,  7/4,  13/  7),
		( 14/ 13,  8/7,  6/ 5,  5/ 4, 4/3,   17/ 12, 3/2,   8/ 5,  5/ 3,  7/4,  13/  7),
		( 14/ 13,  8/7,  6/ 5,  5/ 4, 4/3,   10/  7, 3/2,   8/ 5,  5/ 3,  7/4,  13/  7),
		( 14/ 13,  8/7,  6/ 5,  5/ 4, 4/3,   24/ 17, 3/2,   8/ 5,  5/ 3,  7/4,  13/  7),
	),
}
class ChordFunction (Enum):
	TONIC       = 0
	DOMINANT    = 1
	SUBDOMINANT = 2
class Chromatic:
	def __init__ (self, solfeggio, ratios):
		self.solfeggio = solfeggio
		self.ratios    = ratios
	def __repr__ (self): return str ("Chromatic=[%s, ratios=%s]" % (self.solfeggio, self.ratios))
#	@jit
	def ratio (self, index, octave): return self.ratios[index] * pow (2, octave)
#	@jit
	def pitch (self, index, octave): return self.solfeggio.pitch (self.ratio (index))
	# TODO circle of thirds
#	@jit
	def function (self, index): return ChordFunction (index % 3)
	# TODO get monoaural acoustic beat
	
	
	
def random_chromatic (solfeggio=None):
	if not solfeggio: solfeggio = random_solfeggio ()
	ratios = choice (list (ratios_db.values ()))
	ratios = choice (ratios)
	ratios = (1/1, *ratios)
	return Chromatic (solfeggio, ratios)
if __name__ == "__main__":
	def main ():
		chromatic = random_chromatic ()
		print (chromatic)
	main ()
