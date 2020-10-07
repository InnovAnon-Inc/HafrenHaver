"""InnovAnon Inc. Proprietary"""

from fractions import *
from itertools import *

class OddLimit:
	"""https://en.wikipedia.org/wiki/Limit_%28music%29#Odd_limit"""
	"""generally preferred for the analysis of simultaneous intervals and chords"""
	"""For a positive odd number n,
	the n-odd-limit contains all rational numbers
	such that the largest odd number that divides
	either the numerator or denominator is not greater than n."""

	@staticmethod
	def odd_numerators (n):
		for j in xrange (1, n + 1, 2):
			for k in xrange (1, j):
				yield Fraction (j, k)

	@staticmethod
	def odd_denominators (n):
		for j in xrange (1, n + 1, 2):
			# TODO pick a reasonable max
			#for k in xrange (j, j ** 2):
			for k in xrange (j, j * 2):
				yield Fraction (k, j)

if __name__ == "__main__":
	for p in xrange (1, 10):
		print "p=", p
		print list (OddLimit.odd_denominators (p))
		print list (OddLimit.odd_numerators (p))
		print