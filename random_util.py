#! /usr/bin/env python3

from math      import gcd
#from numba     import jit
from random    import choice, getrandbits, randrange

from bjorklund import bjorklund

#@jit
def random_index (array): return randrange (0, len (array))
#@jit
def random_bool (): return bool (getrandbits (1))

def relative_primes (n, minn=1, maxn=None):
	if maxn is None: maxn = n
	assert minn <= n
	f = lambda k: gcd (n, k) == 1
	rng = range (minn, maxn + 1)
	return filter (f, rng)
	#return (k for k in range (minn, n + 1) if gcd (n, k) == 1)
def random_bjorklund (n):
	k = choice (list (relative_primes (n)))
	return bjorklund (n, k)
# https://stackoverflow.com/questions/17350330/python-array-rotation
#@jit
def rotate  (li, rot):
	if rot == 0: return li
	return li[rot:] + li[:rot]
#@jit
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
##@jit
from itertools import chain
##@jit
def subsets_helper (arr, s, c, i):
	t = (*c, i)
	if sum (t) <= s: return subsets (arr, s, t)
	return ()
##@jit
def subsets (arr, s, c = ()):
	# TODO wtf
	#if sum (c) == s: return (c,)
	#f = lambda i: subsets_helper (arr, s, c, i)
	#k = map (f, arr)
	#k = chain (*k)
	#return k
	
	if sum (c) == s: yield c
	else:
		#for i in arr:
		#	t = (*c, i)
		#	if sum (t) <= _sum: yield from subsets (arr, _sum, t)

		#f = (lambda i: (sum ((*c, i)) <= s))
		#k = filter (f, arr)
		#f = lambda i: subsets (arr, s, (*c, i))
		#k = map (f, k)
		
		f = lambda i: subsets_helper (arr, s, c, i)
		k = map (f, arr)
		
		k = chain (*k)
		yield from k
		
		

# relatively prime pair a, b s.t. a >= minn, b >= minn, a * b <= maxn
def random_relatively_prime_pair (minn, maxn):
	#print ("random_relatively_prime_pair (%s, %s)" % (minn, maxn))
	while True:
		a = randrange (minn, maxn // minn)
		#print ("a: %s" % (a,))
		bn = random_relatively_prime_to (a, minn, maxn)
		if bn is None: continue
		b, n = bn
		return a, b, n
		
# random number b, relatively prime to a, s.t., minn <= a * b <= maxn
def random_relatively_prime_to (a, minn, maxn):
	#print ("random_relatively_prime_to (%s, %s, %s)" % (a, minn, maxn))
	assert a >= minn
	assert a <= maxn // minn
	print ("a: %s, minn: %s, maxn: %s" % (a, minn, maxn // a))
	bs = relative_primes (a, minn, maxn // a)
	bs = tuple (bs)
	if len (bs) == 0: return None
	print ("bs: %s" % (bs,))
	#print ("bs: %s" % (bs,))
	b = choice (bs)
	assert b >= minn, "b: %s, minn: %s" % (b, minn)
	n = a * b
	assert n <= maxn
	return b, n
		
		
		
if __name__ == "__main__":
	def main ():
		print (tuple (subsets ((2, 3, 5, 7), 23)))
	main ()
	quit ()
