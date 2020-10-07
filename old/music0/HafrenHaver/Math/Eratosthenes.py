"""InnovAnon Inc. Proprietary"""

from bitarray import *
from itertools import *
from math import *
from operator import *
from time import sleep

from IntegerSqrt import *
from ItertoolsUtil import *

class Eratosthenes:
	def __init__ (self, n):
		self.n = n
		self.sqrt = int (IntegerSqrt.exact_sqrt (len (self))[0])
		#self.A = [True] * self.actual_size ()
		self.A = bitarray (True) * self.actual_size ()
	def __len__ (self): return self.n
	def __length_hint__ (self): self.actual_size ()
	def __iter__ (self): return chain ([False, False], iter (self.A))
	def __repr__ (self): return "Eratosthenes (", self.n, ")"
	def __str__ (self): return str (list (self.primes ()))
	def __getitem__ (self, key):
		if not self.isValidIndex (key): return False
		return self.A[self.indexOf (key)]
	def __setitem__ (self, key, value):
		if not self.isValidIndex (key): raise Exception (key)
		self.A[self.indexOf (key)] = value
	def max_test (self): return self.sqrt
	def clearMultiples (self, i):
		"""https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Pseudocode"""
		for j in self.multiplesIndices (i):
			#if isValidIndex (j):
			self[j] = False
	def sieve (self):
		"""https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Pseudocode"""
		for i in self.testIndices ():
			if self[i]:
				self.clearMultiples (i)
	def primes (self):
		return chain (self.prefix (),
			[i for i in self.allIndices () if self[i]])

	def isValidIndex (self, i):
		if i <= 1: return False
		if i > self.n: return False
		return True
	def actual_size (self): return len (self) - 2 + 1
	def indexOf (self, n):
		if n <= 1: raise Exception ()
		return n - 2
	def allIndices (self):
		return xrange (2, len (self) + 1)
	def testIndices (self):
		return xrange (2, self.max_test () + 1)
	def multiplesIndices (self, i):
		return xrange (i + i, len (self) + 1, i)
	def prefix (self): return []

if __name__ == "__main__":
	e = Eratosthenes (100)
	e.sieve ()
	print list (e.primes ())