#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange
import numpy

@unique
class Tetra1(Enum):
	MAJOR    = (2, 2, 1)
	MINOR    = (2, 1, 2)
	PHRYGIAN = (1, 2, 2)
	HARMONIC = (1, 3, 1)
	MISC1    = (3, 1, 1)
	MISC2    = (1, 1, 3)
@unique
class Tetra2(Enum):
	MISC1    = (3, 2, 1)
	MISC2    = (3, 1, 2)
	MISC3    = (2, 2, 2)
	MISC4    = (1, 3, 2)
	MISC5    = (2, 1, 3)
	MISC6    = (1, 2, 3)
TETRA_EPSILON1 = 0.5
TETRA_EPSILON2 = 0.5
def random_tetrachords():
	if   random() < TETRA_EPSILON1: ltetra, utetra = Tetra1, Tetra1
	elif random() < TETRA_EPSILON2: ltetra, utetra = Tetra1, Tetra2
	else:                           ltetra, utetra = Tetra2, Tetra1
	ltetra = choice(list(ltetra))
	utetra = choice(list(utetra))
	print("lower tetra: %s" % (ltetra,))
	print("upper tetra: %s" % (utetra,))
	ltetra = ltetra.value
	utetra = utetra.value
	print("lower tetra: %s" % (ltetra,))
	print("upper tetra: %s" % (utetra,))
	assert len(ltetra) == 3
	assert len(utetra) == 3
	return ltetra, utetra

from itertools import accumulate

#scale  = list(accumulate((0,) + scale))
#assert scale[-1] == len(chroma)
#scale  = scale[:-1]
#print("scale: %s" % (scale,))

class Scale:
	def __init__(self, chroma, scale, mode):
		#assert sum(scale) == len(key.chroma)
		assert sum(scale) == len(chroma)
		assert 0 <= mode and mode < len(scale)
		self.chroma = chroma
		#self.orig   = scale
		scale       = scale[mode:] + scale[:mode]
		scale       = list(accumulate((0,) + scale))
		#assert scale[-1] == len(key.chroma)
		assert scale[-1] == len(chroma)
		scale       = tuple(scale[:-1])
		print("scale: %s" % (scale,))
		self.scale  = scale
		self.mode   = mode
	def __len__(self): return len(self.scale)
	#def ratio(self, i):
	def __getitem__(self, i):
		a = self.scale[i % len(self.scale)]
		#a = self.chroma.ratio(a)
		a = self.chroma[a]
		b =        int(i / len(self.scale))
		#print("scale a: %s, b: %s" % (a, b,))
		return a * 2**b

def random_scale(key, ltetra=None, utetra=None):
    if ltetra is None and utetra is None: ltetra, utetra = random_tetrachords()
    if ltetra is None:                    ltetra         = random_tetrachord (utetra)
    if utetra is None:                    utetra         = random_tetrachord (ltetra)

    step  = len(key.chroma) - sum(ltetra) - sum(utetra)
    print("step: %s" % (step,))
    scale = (*ltetra, step, *utetra)
    assert len(scale) == len(ltetra) + 1 + len(utetra)

    mode   = randrange(0, len(scale))
    print("mode: %s" % (mode,))

    scale = Scale(key, scale, mode)
    return scale
#ratios = tuple((scale.ratio(i) for i in range(0, len(scale.scale))))

#for i in range(0, len(scale.scale)):
#    print("i=%s: %s" % (i, scale.ratio(i),))

#ratios = [chroma[(scale[(i + mode) % len(scale)]) % len(chroma)] for i in range(0, len(scale))]

#ratios = tuple((scale[i] for i in range(0, len(scale))))
#print("ratios: %s" % (ratios,))

