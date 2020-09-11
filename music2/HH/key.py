#! /usr/bin/env python3

from numba       import jit

from chromatic   import random_chromatic
from random_util import random_index

class Key:
	def __init__ (self, chromatic, key):
		self.chromatic = chromatic
		self.key       = key
	def __repr__ (self): return str ("Key=[%s, key=%s]" % (self.chromatic, self.key))
	@jit
	def adjust (self, index):
		rlen   = len (self.chromatic.ratios)
		index  = index + self.key
		octave = 0
		while index >= rlen:
			octave = octave + 1
			index  = index  - rlen
		while index < 0:
			octave = octave - 1
			index  = index  + rlen
		return (index, octave)
	@jit
	def ratio (self, index, octave):
		(index, doctave) = self.adjust (index)
		octave = octave + doctave
		return self.chromatic.ratio (index, octave)
	@jit
	def pitch (self, index, octave):
		(index, doctave) = self.adjust (index)
		octave = octave + doctave
		return self.chromatic.pitch (index, octave)
	@jit
	def function (self, index):
		#(index, doctave) = self.adjust (index)
		#return self.chromatic.function (index)
		return self.chromatic.function (index)
	@jit
	def degree (self, index):
		(index, doctave) = self.adjust (index)
		#return self.chromatic.degree (index)
		return index
	@jit
	def increment (self, dkey=1):
		index, doctave = self.adjust (dkey)
		return Key (self.chromatic, index), doctave
	@jit
	def decrement (self, dkey=1): return self.increment (-dkey)
	@jit
	def brighter (self):
		dkey = len (self.chromatic.ratios)
		dkey = dkey // 2 + 1
		return self.increment (dkey)
	@jit
	def darker (self):
		dkey = len (self.chromatic.ratios)
		#dkey = dkey // 2 - 1
		dkey = dkey // 2 + 1
		return self.decrement (dkey)
def random_key (chromatic=None, solfeggio=None):
	if not chromatic: chromatic = random_chromatic (solfeggio)
	ratios = chromatic.ratios
	key    = random_index (ratios)
	return Key (chromatic, key)
if __name__ == "__main__":
	def main ():
		key = random_key ()
		print (key)
	main ()
