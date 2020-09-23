#! /usr/bin/env python3

from math      import gcd
from numba     import jit
from random    import choice, getrandbits, randrange

from bjorklund import bjorklund

def random_index (array): return randrange (0, len (array))
	
def random_bool (): return bool (getrandbits (1))

def relative_primes (n): return (k for k in range (1, n + 1) if gcd (n, k) == 1)
def random_bjorklund (n):
	k = choice (list (relative_primes (n)))
	return bjorklund (n, k)
# https://stackoverflow.com/questions/17350330/python-array-rotation
@jit
def rotate  (li, rot):
	if rot == 0: return li
	return li[rot:] + li[:rot]
@jit
def reverse (li):      return li[::-1]
def random_bjorklund2 (n, rev=None, rot=None):
	if rev is None: rev = random_bool ()
	if rot is None: rot = randrange (0, n)
	b = random_bjorklund (n)
	if rev: b = reverse (b)
	b = rotate (b, rot)
	return b

def random_bjorklund3 (n, k, rev=None, rot=None):
	if rev is None: rev = random_bool ()
	if rot is None: rot = randrange (0, n)
	b = bjorklund (n, k)
	if rev: b = reverse (b)
	b = rotate (b, rot)
	return b

# Python program to print all subsets with given sum 

# The vector v stores current subset. 
def printAllSubsetsRec (arr, n, v, sum):

	# If remaining sum is 0, then print all
	# elements of current subset.
	if sum == 0:
		#for value in v:
		#	print (value, end=" ")
		#print()
		#return
		return [v]

	# If no remaining elements,
	if n == 0: return []

	# We consider two cases for every element.
	# a) We do not include last element.
	# b) We include last element in current subset.
	a = printAllSubsetsRec (arr, n - 1, v, sum)
	#v1 = [] + v
	#v1.append (arr[n - 1])
	v1 = [] + v + [arr[n - 1]]
	b = printAllSubsetsRec (arr, n - 1, v1, sum - arr[n - 1])
	c = []
	for subset in a + b:
		if subset not in c: c = c + [subset]
	return c


# Wrapper over printAllSubsetsRec()
def printAllSubsets (arr, n, sum):
	v = []
	return printAllSubsetsRec (arr, n, v, sum)

# This code is contributed by ihritik

# https://stackoverflow.com/questions/56206696/recursive-program-to-get-all-subsets-with-given-sum-includes-repetitions
#@jit
def subsets (arr, _sum, c = []):
	if sum (c) == _sum: yield c
	else:
		for i in arr:
			if sum (c + [i]) <= _sum: yield from subsets (arr, _sum, c + [i])
