#! /usr/bin/env python

from math      import pow
#from numba     import jit
from random    import choice
from solfeggio import random_solfeggio

# TODO
ratios_db = [
	# symmetric scale #1
	[1/1, 16/15,  9/8, 6/5, 5/4, 4/3, 64/45, 3/2, 8/5, 5/3, 16/9, 15/8],
	[1/1, 16/15,  9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 16/9, 15/8],
	# symmetric scale #2
	[1/1, 16/15, 10/9, 6/5, 5/4, 4/3, 64/45, 3/2, 8/5, 5/3,  9/5, 15/8],
	[1/1, 16/15, 10/9, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3,  9/5, 15/8],
	# asymmetric scale standard
	[1/1, 16/15,  9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3,  9/5, 15/8],
	[1/1, 16/15,  9/8, 6/5, 5/4, 4/3, 64/45, 3/2, 8/5, 5/3,  9/5, 15/8],
	# asymmetric scale extended
	[1/1, 16/15,  9/8, 6/5, 5/4, 4/3, 25/18, 3/2, 8/5, 5/3,  9/5, 15/8],
	[1/1, 16/15,  9/8, 6/5, 5/4, 4/3, 36/25, 3/2, 8/5, 5/3,  9/5, 15/8],
	# 7-limit tuning
	[1/1, 15/14,  8/7, 6/5, 5/4, 4/3,  7/5,  3/2, 8/5, 5/3,  7/4, 15/8],
	[1/1, 15/14,  8/7, 6/5, 5/4, 4/3, 10/7,  3/2, 8/5, 5/3,  7/4, 15/8],
	# 17-limit tuning
	[1/1, 14/13,  8/7, 6/5, 5/4, 4/3,  7/5,  3/2, 8/5, 5/3,  7/4, 13/7],
	[1/1, 14/13,  8/7, 6/5, 5/4, 4/3, 17/12, 3/2, 8/5, 5/3,  7/4, 13/7],
	[1/1, 14/13,  8/7, 6/5, 5/4, 4/3, 10/7,  3/2, 8/5, 5/3,  7/4, 13/7],
	[1/1, 14/13,  8/7, 6/5, 5/4, 4/3, 24/17, 3/2, 8/5, 5/3,  7/4, 13/7],
]

#      TONIC_FUNCTION = 0
#   DOMINANT_FUNCTION = 1
#SUBDOMINANT_FUNCTION = 2

#@jit
class Chromatic:
	def __init__ (self, solfeggio, ratios):
		self.solfeggio = solfeggio
		self.ratios    = ratios
	def __repr__ (self): return str ("Chromatic=[%s, ratios=%s]" % (self.solfeggio, self.ratios))
	def ratio (self, index, octave): return self.ratios[index] * pow (2, octave)
	def pitch (self, index, octave): return self.solfeggio.pitch (self.ratio (index))
	# TODO circle of thirds
	def function (self, index): return index % 3
##@jit
def random_chromatic (solfeggio=None):
	if not solfeggio: solfeggio = random_solfeggio ()
	ratios = choice (ratios_db)
	return Chromatic (solfeggio, ratios)
	
if __name__ == "__main__":
	##@jit
	def main ():
		chromatic = random_chromatic ()
		print (chromatic)
	main ()
