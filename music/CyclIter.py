from __future__ import division
from itertools import *
"""
# turns list seq into infinite cycle
class CyclIter:
	def __init__ (self, seq, length):
		self.itr = cycle (seq)
		self.length = length
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): return self.itr.next ()
"""