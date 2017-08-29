"""InnovAnon Inc. Proprietary"""

from fractions import *

from Euclid import *
	
class NormalEuclid:
	@staticmethod
	def quotient (a, b): return int (Fraction (a, b))
	@staticmethod
	def remainder (a, b, q): return a - b * q
	@staticmethod
	def iszero (r): return r is 0

if __name__ == "__main__":
	normal_euclid = Euclid (
		NormalEuclid.quotient, NormalEuclid.remainder, NormalEuclid.iszero)
	print normal_euclid.euclid (12, 5)