#! /usr/bin/env python3

from enum   import Enum
from numba  import jit
from random import choice

class SolfeggioType (Enum):
	RED    = 0
	ORANGE = 1
	YELLOW = 2
	GREEN  = 3
	BLUE   = 4
	VIOLET = 5
solfeggio_db = {
	SolfeggioType.RED    : ( 8,  2, 14),
        SolfeggioType.ORANGE : ( 1,  7, 13),
        SolfeggioType.YELLOW : ( 6,  0, 12),
        SolfeggioType.GREEN  : ( 5, 11, 17),
        SolfeggioType.BLUE   : ( 4, 16, 10),
        SolfeggioType.VIOLET : ( 3,  9, 15),
}
solfeggios = (
    528, #  0
    147, #  1
    417, #  2
    258, #  3
    396, #  4
    369, #  5
    285, #  6
    471, #  7
    174, #  8
    582, #  9
    963, # 10
    693, # 11
    852, # 12
    714, # 13
    741, # 14
    825, # 15
    639, # 16
    936, # 17
)

# TODO harmonic frequencies of various elements

# TODO empirically tuning to the resonant frequency of target object

class Solfeggio:
	def __init__ (self, base_frequency): self.base_frequency = base_frequency
	def __repr__ (self): return str ("Solfeggio=[base_frequency=%s]" % self.base_frequency)
	@jit
	def pitch (self, ratio): return self.base_frequency * ratio
        #def draw (self, screen):
        #    index = solfeggios.indexof
        #    color = 
def random_solfeggio ():
	base_frequency = choice (list (solfeggio_db.values ()))
	base_frequency = choice (base_frequency)
	base_frequency = solfeggios[base_frequency]
	return Solfeggio (base_frequency)
class Solfeggios:
	def draw (self, screen):
            outer.draw (screen)
            inner.draw (screen)
            for s in self.circles: s.draw (screen)
            for s in self.lines:   s.draw (screen)
if __name__ == "__main__":
	def main ():
		solfeggio = random_solfeggio ()
		print (solfeggio)
	main ()
	
