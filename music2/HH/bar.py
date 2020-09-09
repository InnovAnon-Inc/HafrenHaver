#! /usr/bin/env python

#from numba  import jit
from random import randrange

#@jit
class Bar:
	def __init__ (self, nbeat):
		self.nbeat = nbeat
def random_bar (prod, nphrase):
	#prod       = nsegment * nbar
	if nphrase == 1:
		min_length = max (5  // prod,     1)
		max_length = max (13 // prod + 1, 3)
	else:
		min_length = max (11 // prod,     1)
		max_length = max (43 // prod + 1, 3)
	nbeat      = randrange (min_length, max_length + 1)
	return Bar (nbeat)
