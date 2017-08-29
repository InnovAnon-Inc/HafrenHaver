"""InnovAnon Inc. Proprietary"""

from itertools import *

class Hamming:
	"""http://rosettacode.org/wiki/Hamming_numbers#Cyclic_generator_method_.232."""
	@staticmethod
	def merge (r, s):
		# This is faster than heapq.merge.
		rr = r.next ()
		ss = s.next ()
		while True:
			if rr < ss:
				yield rr
				rr = r.next ()
			else:
				yield ss
				ss = s.next ()
	@staticmethod
	def p (n):
		def gen():
			x = n
			while True:
				yield x
				x *= n
		return gen ()
	@staticmethod
	def pp (n, s):
		def gen ():
			for x in (Hamming.merge (s, chain ([n], (n * y for y in fb)))):
				yield x
		r, fb = tee (gen ())
		return r
 
	@staticmethod
	def hamming (a, b = None):
		if not b:
			b = a + 1
		seq = (chain ([1], Hamming.pp (5, Hamming.pp (3, Hamming.p (2)))))
		return list (islice (seq, a - 1, b - 1))
if __name__ == "__main__":
	print Hamming.hamming (1, 100)