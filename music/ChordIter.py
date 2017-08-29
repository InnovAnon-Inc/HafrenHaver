from __future__ import division

class ChordIter:
	def __init__ (self, prodIter, key):
		self.prodIter = prodIter
		self.key = key
		self.length = len (prodIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		fundy, noteNums = self.prodIter.next ()
		return [key[(fundy + noteNum) % len (key)] for noteNum in noteNums]