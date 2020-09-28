from __future__ import division
from fractions import *
from itertools import *

class Util:
	@staticmethod
	def list_to_number (l):
		s = 0
		for k in xrange (len (l)):
			s += l[k] * (10 ** (len (l) - k - 1))
		return s
	@staticmethod
	def play (base, note):
		return int (round (base * note))
	@staticmethod
	def equal_spacing (n):
		for h in xrange (n):
			yield (h + 1) / n
	@staticmethod
	def normalize_octave (ss):
		for s in ss:
			yield 1 + (s - 1) / (2 - 1)
	@staticmethod
	def normalize_frequency (ss):
		for s in ss:
			yield log (s) / log (2)
	@staticmethod
	def normalize_radians (ss):
		for s in ss:
			yield s * 2 * pi
	@staticmethod
	def points (ss):
		for s in ss:
			yield (cos (s), sin (s))
	@staticmethod
	def min_max_normalize (m, i, a):
		return 1 + (m - i) / (a - i)
	@staticmethod
	def lcm (a, b, r):
		return int (a * b / r)
	@staticmethod
	def lcm_pair (a, b):
		r = gcd (a, b)
		m = Util.lcm (a, b, r)
		#print a, b, r, m
		return (int (b / r), int (a / r), int (m / r))
	@staticmethod
	def fundyChord (key, fundy, chord):
		return [key[(fundy + noteNum) % len (key)] for noteNum in chord]
	@staticmethod
	def rhythmToBeat (r):
		for k in xrange (r):
			yield k/r
	@staticmethod
	def rhythmChordToBeatChord (rc):
		return sorted (list (set (chain.from_iterable ([Util.rhythmToBeat (r) for r in rc]))))