from __future__ import division

class CountIter:
	def __init__ (self, bjork):
		#self.bjork = cycle (bjork)
		self.bjork = bjork.sequence.__iter__ ()
		self.length = sum (bjork.sequence)
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		count = 1
		while True:
			bj = self.bjork.next ()
			if bj is 1: return count
			count += 1