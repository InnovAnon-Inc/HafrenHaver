#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange
import numpy

class Integer:
    def __init__(self, factors):
        self.factors = factors
    def value(self): return accumulate(operators.mul, 1, map(lambda b, e: b**e, self.factors))
class Ratio:
    def __init__(self, numerator, denominator):
        self.numerator   = numerator
        self.denominator = denominator
    def value(self): return float(self.numerator) / float(self.denominator)

@unique
class Chroma(Enum): # TODO compute from scratch
	LIMIT3a                     = (256/243, 9/8, 32/27, 81/64, 4/3,  729/512, 3/2, 128/81, 27/16, 16/9, 243/128)
	LIMIT3b                     = (256/243, 9/8, 32/27, 81/64, 4/3, 1024/729, 3/2, 128/81, 27/16, 16/9, 243/128)
	LIMIT5_SYMMETRIC1a          = ( 16/15,  9/8,  6/5,   5/4,  4/3,   45/32,  3/2,   8/5,   5/3,  16/9,  15/8)
	LIMIT5_SYMMETRIC1b          = ( 16/15,  9/8,  6/5,   5/4,  4/3,   64/45,  3/2,   8/5,   5/3,  16/9,  15/8)
	LIMIT5_SYMMETRIC2a          = ( 16/15, 10/9,  6/5,   5/4,  4/3,   45/32,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_SYMMETRIC2b          = ( 16/15, 10/9,  6/5,   5/4,  4/3,   64/45,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_STANDARDa = ( 16/15,  9/8,  6/5,   5/4,  4/3,   45/32,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_STANDARDb = ( 16/15,  9/8,  6/5,   5/4,  4/3,   64/45,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_EXTENDEDa = ( 16/15,  9/8,  6/5,   5/4,  4/3,   25/18,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT5_ASYMMETRIC_EXTENDEDb = ( 16/15,  9/8,  6/5,   5/4,  4/3,   36/25,  3/2,   8/5,   5/3,   9/5,  15/8)
	LIMIT7a                     = ( 15/14,  8/7,  6/5,   5/4,  4/3,    7/5,   3/2,   8/5,   5/3,   7/4,  15/8)
	LIMIT7b                     = ( 15/14,  8/7,  6/5,   5/4,  4/3,   10/7,   3/2,   8/5,   5/3,   7/4,  15/8)
	LIMIT17a                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,    7/5,   3/2,   8/5,   5/3,   7/4,  13/7)
	LIMIT17b                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,   17/12,  3/2,   8/5,   5/3,   7/4,  13/7)
	LIMIT17c                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,   10/7,   3/2,   8/5,   5/3,   7/4,  13/7)
	LIMIT17d                    = ( 14/13,  8/7,  6/5,   5/4,  4/3,   24/17,  3/2,   8/5,   5/3,   7/4,  13/7)
limits = (
		#(,), # 2-limit
		(Chroma.LIMIT3a,                     Chroma.LIMIT3b),
		(Chroma.LIMIT5_SYMMETRIC1a,          Chroma.LIMIT5_SYMMETRIC1b,          Chroma.LIMIT5_SYMMETRIC2a,          Chroma.LIMIT5_SYMMETRIC2b,
		 Chroma.LIMIT5_ASYMMETRIC_STANDARDa, Chroma.LIMIT5_ASYMMETRIC_STANDARDb, Chroma.LIMIT5_ASYMMETRIC_EXTENDEDa, Chroma.LIMIT5_ASYMMETRIC_EXTENDEDb,),
		(Chroma.LIMIT7a,                     Chroma.LIMIT7b,),
		(Chroma.LIMIT17a,                    Chroma.LIMIT17b,                    Chroma.LIMIT17c,                    Chroma.LIMIT17d,),
)

def random_base_frequency():
	return 432 + (1 - 2 * random()) * 32
def frequency(base, ratio, octave):
	return base * ratio * 2**octave
def random_limit():
	return choice((3, 5, 7, 17,))
def random_chromatic_helper(limit=None):
	if limit is None: limit = random_limit()
	print("limit: %s" % (limit,))
	if limit ==  3:   return choice(limits[0])
	if limit ==  5:   return choice(limits[1])
	if limit ==  7:   return choice(limits[2])
	if limit == 17:   return choice(limits[3])
	raise Error()
def get_chromatic(chroma): return (1/1, *chroma.value)
def random_chromatic(limit=None):
	chroma = random_chromatic_helper(limit)
	print("chroma: %s" % (chroma,))
	chroma = get_chromatic(chroma)
	print("chroma: %s" % (chroma,))
	return chroma

