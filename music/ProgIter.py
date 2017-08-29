from __future__ import division

from Bjorklund import *
from SkipIter import *

class ProgIter:
	def __init__ (self, key, blen, progType, progMode):
		self.itr = SkipIter (Bjorklund.factory (blen, progType, progMode), key)
		self.length = len (self.itr)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		return self.itr.next ()