"""InnovAnon Inc. Proprietary"""

from fractions import *

class FractionUtil:
	@staticmethod
	def frac_pow (a, b):
		if isinstance (a, Fraction):
			return Fraction (
				FractionUtil.frac_pow (a.numerator, b),
				FractionUtil.frac_pow (a.denominator, b))
		return a ** b