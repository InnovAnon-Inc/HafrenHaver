#! /usr/bin/env python3

from itertools import product
from numba import jit
from string import ascii_lowercase, digits
from math import prod

ACRONYMS     = (
	'IA',  # InnovAnon: Innovations Anonymous (inc)
	'FFF', # Free Code for a Free World!      (slogan)
	'HH',  # Hafren Haver                     (project)
)

def a2n1 (alpha):
	alpha = alpha.lower ()                     # normalize
	ref   = tuple (ascii_lowercase)
	ret   = (ref.index (c) + 1 for c in alpha) # 1-based index of letter in alphabet
	ret   = (str (c)           for c in ret)   # interpret numbers as strings
	ret   = "".join (ret)                      # convert to string
	return ret

def a2n0 (alpha):
	alpha = alpha.lower ()                       # normalize
	ref   = tuple (digits + ascii_lowercase)
	ret   = (ref.index (c)       for c in alpha) # 0-based index of letter in alphabet
	ret   = (str (c)             for c in ret)   # interpret numbers as strings
	ret   = "".join (ret)                        # convert to string
	return ret

def a2b (alpha):
	alpha = alpha.lower ()                       # normalize
	ref   = tuple (digits + ascii_lowercase)
	ret   = (ref.index (c)       for c in alpha) # 0-based index of letter in alphabet
	b     = max (ret) + 1                        # base of string
	ret   = int (alpha, b)                       # convert string from base to decimal
	ret   = str (ret)                            # convert string
	return ret

def numberToBase (n, b): # https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
	if n == 0: return (0,)
	digits = []
	while n:
		digits.append (int (n % b))
		n //= b
	digits = digits[::-1]
	return tuple (digits)
def a2bn_helper (ret, b, f=sum):
	while True:
		n   = f (c for c in ret) # sum of digits
		ret = numberToBase (n, b)  # convert to sum to specified base
		if n < b: break
	ret   = (str (c) for c in ret)             # convert digits to strings
	ret   = "".join (ret)                      # convert to string
	return ret
def a2bn1 (alpha, b=10, f=sum):
	alpha = alpha.lower ()                     # normalize
	ref   = tuple (ascii_lowercase)
	ret   = (ref.index (c) + 1 for c in alpha) # 1-based index of letter in alphabet
	return a2bn_helper (ret, b, f)
	
def a2bn2 (alpha, f=sum):
	alpha = alpha.lower ()                     # normalize
	ref   = tuple (digits + ascii_lowercase)
	ret   = (ref.index (c) for c in alpha)     # 0-based index of letter in alphabet
	ret   = tuple (ret)                        # needed for max and conversions
	b     = max (ret) + 1                      # base of string
	return a2bn_helper (ret, b, f)
	
def a2bn11 (alpha, b=10): return a2bn1 (alpha, b, sum)
def a2bn12 (alpha, b=10): return a2bn1 (alpha, b, prod)
def a2bn21 (alpha):       return a2bn2 (alpha,    sum)
def a2bn22 (alpha):       return a2bn2 (alpha,    prod)

def numerology1 (acronyms=ACRONYMS):
	functions = (a2n0, a2n1, a2b)
	p         = product (functions, acronyms)
	ns        = (f (acronym) for f, acronym in p)
	ns        = tuple (ns)
	assert len (ns) == len (set (ns))
	return ns
def numerology2 (acronyms=ACRONYMS):
	functions = (a2bn11, a2bn21, a2bn12, a2bn22)
	p         = product (functions, acronyms)
	ns        = (f (acronym) for f, acronym in p)
	ns        = tuple (ns)
	ns        = set (ns)
	return tuple (ns)
def numerology (acronyms=ACRONYMS):
	t1 = numerology1 (acronyms)
	t2 = numerology2 (acronyms)
	t  = (*t1, *t2)
	t  = set (t)
	return tuple (t)
	
if __name__ == "__main__":
	def main (): print (numerology ())
	main ()
