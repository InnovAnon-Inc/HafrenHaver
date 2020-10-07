from __future__ import division
from ProdIter import *

class BaseFreqIter:
	def __init__ (self, rangeIter, chakraIter, solfeggios):
		self.prodIter = ProdIter (rangeIter, chakraIter)
		self.solfeggios = solfeggios
	def __len__ (self): return len (self.prodIter)
	def __iter__ (self): return self
	def next (self): return self.solfeggios[self.prodIter.next ()]