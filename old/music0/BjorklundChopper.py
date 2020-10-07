from __future__ import division

class BjorklundChopper:
	def __init__ (self, bjork):
		g = gcd (len (bjork.seq), sum (bjork.seq))
		self.seq = list (bjork.seq)[:int (len (bjork.seq) / g)]
		#print "c=",bjork.seq
		#print "d=",self.seq
		# TODO idk wtf I'm doing
		#self.seq = list (chain.from_iterable (repeat (list (bjork.seq)[:int (len (bjork.seq) / g)], g)))
		self.length = len (bjork.seq)
	def __len__ (self): return self.length