"""InnovAnon Inc. Proprietary"""

from fractions import *

class Intervals:
	#epsilon = Fraction (729, 512)
	@staticmethod
	def add_intervals (a=Fraction (3, 2), b=1, epsilon=Fraction (2187, 2048)):
		"""http://www.medieval.org/emfaq/harmony/pyth4.html"""
		b *= a
		if b >= 2: b /= a.denominator
		if b <= epsilon: return [b]
		return [b] + Intervals.add_intervals (a, b)
	@staticmethod
	def subtract_intervals (a=Fraction (3, 2), b=2,
		epsilon=Fraction (256, 243)):
		#b /= a
		#if b <= foo_epsilon: return [b]
		#return [b] + Intervals.subtract_intervals (b, a)
		return [2 / f for f in Intervals.add_intervals () if 2 / f >= epsilon]

if __name__ == "__main__":
	print Intervals.add_intervals ()
	print
	print Intervals.subtract_intervals ()