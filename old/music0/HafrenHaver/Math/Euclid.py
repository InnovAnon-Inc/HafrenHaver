"""InnovAnon Inc. Proprietary"""

class Euclid:
	
	# l[h] = l[k] * a + r
	# l[h] = l[k] ** a * r
	
	def __init__ (self, quotient, remainder, iszero):
		self.quotient = quotient
		self.remainder = remainder
		self.iszero = iszero
	
	def euclid (self, a, b):
		"""https://plus.maths.org/content/music-and-euclids-algorithm"""
		q = self.quotient (a, b)
		r = self.remainder (a, b, q)
		if self.iszero (r): return [r]
		return [r] + self.euclid (b, r)
	
	def __repr__ (self):
		return "Euclid (", self.quotient, ",", self.remainder, ",", self.iszero, ")"