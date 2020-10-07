"""InnovAnon Inc. Proprietary"""

from fractions import *
from itertools import *

from Smooth import *

class PrimeLimit:
	"""https://en.wikipedia.org/wiki/Limit_%28music%29#Prime_limit"""
	"""generally preferred for the analysis of scales"""
	"""For a prime number n, the n-prime-limit contains all rational numbers
	that can be factored using primes no greater than n.
	In other words, it is the set of rationals with numerator and denominator
	both n-smooth."""
	@staticmethod
	def consecutive_smooth_numbers (n):
		sn = Smooth (n).generate ()
		prev = sn.next ()
		while True:
			cur = sn.next ()
			if cur - 1 is prev: yield Fraction (cur, prev)
			prev = cur

if __name__ == "__main__":
	for k in PrimeLimit.consecutive_smooth_numbers (5):
		print k