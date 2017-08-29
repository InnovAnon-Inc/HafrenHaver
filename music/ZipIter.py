from __future__ import division
from itertools import *

from Util import *

lcm_pair = Util.lcm_pair

class ZipIter:
	def __init__ (self, rangeIter, chakraIter, solfeggio):
		#print rangeIter
		#print chakraIter
		(a, b, c) = lcm_pair (len (rangeIter), len (chakraIter))
		#(a, b, c) = lcm_pair (rangeIter.length, chakraIter.length)
		self.rangeIter = cycle (
			#repeat (
				rangeIter
			#, a)
		)
		self.chakraIter = cycle (
			#repeat (
				chakraIter
			#, b)
		)
		self.solfeggio = solfeggio
		self.length = c
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		r = self.rangeIter.next ()
		c = self.chakraIter.next ()
		return self.solfeggio[r, c]