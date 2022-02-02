#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange
import numpy

from chroma import random_chromatic

class Key:
	def __init__(self, chroma, key):
		assert len(chroma) == 12
		assert all(starmap(le, zip(chroma, chroma[1:])))
		assert 0 <= key and key < len(chroma)
		self.chroma = chroma
		self.key    = key
	def __len__(self): return len(self.chroma)
	#def ratio(self, i):
	def __getitem__(self, i):
		#print("key.ratio(i=%s)" % (i,))
		#print("key: %s" % (self.key,))
		#print("chroma: %s" % (self.chroma,))
		a = self.chroma[(i + self.key) % len(self.chroma)]
		b =         int((i + self.key) / len(self.chroma))
		#print("chromatic a: %s, b: %s" % (a, b,))
		return a * 2**b
def random_key(chroma=None): # TODO parameterize limit
	if chroma is None: chroma = random_chromatic()
	key    = randrange(0, len(chroma))
	print("key: %s" % (key,))
	return Key(chroma, key)
key = random_key()

#for i in range(0, len(key.chroma)):
#    print("i=%s: %s" % (i, key.ratio(i),))

