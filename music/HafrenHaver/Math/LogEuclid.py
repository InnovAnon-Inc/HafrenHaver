"""InnovAnon Inc. Proprietary"""

from fractions import *
from math import *

from Euclid import *
from FractionUtil import *

class LogEuclid (Euclid):
	@staticmethod
	def quotient (a, b): return int (log (a) / log (b))
	@staticmethod
	def remainder (a, b, q): return Fraction (
		a, FractionUtil.frac_pow (b, q))
	def __init__ (self, epsilon=Fraction (531441, 524288)):
		Euclid.__init__ (
			self, LogEuclid.quotient, LogEuclid.remainder, self.iszero)
		self.epsilon = epsilon
	def iszero (self, r): return r <= self.epsilon

if __name__ == "__main__":
	log_euclid = LogEuclid ()
	print log_euclid.euclid (2, Fraction (3, 2))