"""InnovAnon Inc. Proprietary"""

from Eratosthenes import *

class Eratosthenes2 (Eratosthenes):
	# 0 1 2 | 3 5 7 9 11 13 15 17 19
	def __init__ (self, n): Eratosthenes.__init__ (self, n)
	def isValidIndex (self, i):
		if i <= 2: return False
		if i > self.n: return False
		if i % 2 is 0: return False
		return True
	def actual_size (self): return (len (self) - 2) / 2
	def indexOf (self, n):
		if not self.isValidIndex (n): raise Exception ()
		return (n - 2) / 2
	def allIndices (self):
		return xrange (2 + 1, len (self) + 1, 2)
	def testIndices (self):
		return xrange (2 + 1, self.max_test () + 1, 2)
	def multiplesIndices (self, i):
		return xrange (i + 2 * i, len (self) + 1, i * 2)
	def prefix (self): return [2]

if __name__ == "__main__":
	e = Eratosthenes2 (100)
	e.sieve ()
	print list (e.primes ())