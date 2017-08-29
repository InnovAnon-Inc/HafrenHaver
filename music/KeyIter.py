from __future__ import division

from Bjorklund import *
from SkipIter import *

# 111111100000
# 10 10 10 10 10 11
# 10 10 1 10 10 1 10
# ab cd e fg ab c de
class KeyIter:
	def __init__ (self, scale, scaleType, scaleMode):
		self.itr = SkipIter (Bjorklund.factory (len (scale), scaleType, scaleMode), scale)
		self.length = len (self.itr)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		return self.itr.next ()