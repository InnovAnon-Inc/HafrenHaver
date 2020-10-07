"""InnovAnon Inc. Proprietary"""

from itertools import *

from Eratosthenes import *
from Hamming import *

class Smooth:
	"""https://en.wikipedia.org/wiki/Smooth_number"""
	def __init__ (self, n):
		e = EratosthenesWheel (n, [2])
		e.sieve ()
		self.primes = tuple (e.primes ())
		assert self.primes[-1] is n, "primes=%s, n=%s" % (self.primes, n)
	def generate (self):
		return Smooth.smooth (self.primes)
	"""
	def leaves (self, primest):
		#assert isinstance (primes, list)
		primes, j = primest
		for i in xrange (j, len (primes)):
			b, e = primes[i]
			yield (primes[:i] + [(b, e + 1)] + primes[i + 1:], i)
	def next_row (self, row): return chain.from_iterable (imap (self.leaves, row))
	#def next_row (self, row): return sorted (chain.from_iterable (imap (self.leaves, row)), key=self.product)
	#def product (self, row):
	#	arr, ignore = row
	#	pows = [b ** e for b, e in arr]
	#	return reduce (mul, pows, 1)
	def rec (self, *arr):
		# 2**1 * 3**1 * 5**1
		# 2**2 * 3**1 * 5**1   2**1 * 3**2 * 5**1   2**1 * 3**1 * 5**2
		# 2**2 * 3**2 
		return chain (arr, chain.from_iterable (starmap (self.rec, [self.next_row (arr)])))
	def generate (self):
		return self.rec ((zip (self.primes, [0] * len (self.primes)), 0))
	"""
	@staticmethod
	def smooth_rec (wheel):
		if len (wheel) is 1: return Hamming.p (wheel[0])
		return Hamming.pp (wheel[0], Smooth.smooth_rec (wheel[1:]))
	@staticmethod
	def smooth (wheel): return chain ([1], Smooth.smooth_rec (wheel))
	
if __name__ == "__main__":
	for k in Smooth (5).generate ():
		print k
	for k, j in Smooth (5).generate ():
		print k, reduce (mul, [b ** e for b, e in k], 1)
		#time.sleep (1)

# 2**a (2+1)**b (2*2+1)**c