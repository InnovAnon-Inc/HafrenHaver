from __future__ import division

class SmoothIter:
	def __init__ (self, beat):
		self.seq = beat[::-1].__iter__ ()
		self.length = len (beat)
		self.last = 1
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		s = self.seq.next ()
		e = self.last - s
		self.last = s
		#print "s=,",s,"e=",e
		return s, e