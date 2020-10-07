from __future__ import division
from itertools import *

from CountIter import *

class ChangeIterHelper:
	def __init__ (self, bjork, seq):
		self.length = len (bjork.sequence)
		#assert sum (seq) == self.length
		self.bjork = CountIter (bjork)
		#print list (CountIter (bjork))
		self.seq = seq.__iter__ ()
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		s = self.seq.next ()
		b = self.bjork.next ()
		#print "s=",s
		#print "b=",b
		#print "l=", len (self)
		#return [s] * (b + len (self) % b)
		return [s] * b
		#return [self.seq.next ()] * self.bjork.next ()
class ChangeIter:
	def __init__ (self, bjork, seq):
		helper = ChangeIterHelper (bjork, seq)
		self.length = len (helper)
		self.seq = chain.from_iterable (helper)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): return self.seq.next ()
class FIter:
	def __init__ (self, bjork, seq):
		self.length = len (bjork.sequence)
		self.bjork = bjork.sequence.__iter__ ()
		self.seq = seq.__iter__ ()
		self.cur = seq[:-1]
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		if self.bjork.next (): self.cur = self.seq.next ()
		return self.cur