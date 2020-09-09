#! /usr/bin/env python

#from numba  import jit
from random import choice

# TODO
solfeggio_db = [432]

# TODO harmonic frequencies of various elements

# TODO empirically tuning to the resonant frequency of target object

#@jit
class Solfeggio:
	def __init__ (self, base_frequency): self.base_frequency = base_frequency
	def __repr__ (self): return str ("Solfeggio=[base_frequency=%s]" % self.base_frequency)
	def pitch (self, ratio): return self.base_frequency * ratio
##@jit
def random_solfeggio ():
	base_frequency = choice (solfeggio_db)
	return Solfeggio (base_frequency)

if __name__ == "__main__":
	##@jit
	def main ():
		solfeggio = random_solfeggio ()
		print (solfeggio)
	main ()
	
