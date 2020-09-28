from __future__ import division

from fractions import *
from itertools import *

class ProdIter:
	def __init__ (self, progIter, noteNumIter):
		g = gcd (len (progIter), len (noteNumIter))
		#g = 1
		self.progIter = chain.from_iterable (repeat (
			list (progIter), int (len (noteNumIter) / g)))
		self.noteNumIter = chain.from_iterable (repeat (
			list (noteNumIter), int (len (progIter) / g)))
		self.length = int (len (progIter) * len (noteNumIter) / g)
		#self.seq = zip (self.progIter, self.noteNumIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		#return self.seq.next ()
		return (self.progIter.next (), self.noteNumIter.next ())