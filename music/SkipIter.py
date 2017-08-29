from __future__ import division

from fractions import *
from itertools import *

# binary sequence bjork skips over seq
class SkipIter:
	# 00000 111
	# 01 01 01 00
	# 01 0 01 0 01
	# 01001001 01001001 01001001 01001001 01001001 | 01001001
	# abcdeabc deabcdea bcdeabcd eabcdeab cdeabcde | abcdeabc
	#  b  e  c  e  c  a  c  a  d  a  d  b  d  b  e |  b  e  c
	
	# abcdefab cdefabcd efabcdef abcdefab cdefabcd   efabcdef | abcdefab
	#  b  e  b  d  a  d  f  c  d  b  e  b  d  b  d    f  c  f |  b  e  b
	# bjork = subset (0, len (bjork) / gcd (len (bjork), sum (bjork)))
	# bjork repeats len(seq)/gcd   times
	# seq   repeats len(bjork)/gcd times
	# output is bjork.pulseAmt*len(seq)
	
	# 10010010 10010010 10010010 10010010 10010010
	# abcdefab cdefabcd efabcdef abcdefab cdefabcd
	# adacfcebe adacfc
	
	# 00001111
	# 01010101 01010101 01010101
	# abcabcab cabcabca bcabcabc
	#  b a c b  a c b a  c b a c
	# 01 01 01
	# ab ca bc
	#  b  a  c
	def __init__ (self, bjork, seq):
		#bjork = BjorklundChopper (bjork)
		#g = gcd (len (seq), len (bjork))
		g = gcd (len (seq), len (bjork.sequence))
		self.bjork = chain.from_iterable (repeat (
			bjork.sequence, int (len (seq)       / g)))
		self.seq   = chain.from_iterable (repeat (
			seq,       int (len (bjork.sequence) / g)))
		self.length = int (sum (bjork.sequence) * len (seq) / g)
		#print "e=",self.length
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		bj = self.bjork.next ()
		seq = self.seq.next ()
		if bj: return seq
		return self.next ()