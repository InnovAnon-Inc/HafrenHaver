# TODO

"""InnovAnon Inc. Proprietary"""

from itertools import *
from math import *
from operator import *
from time import sleep

from IntegerSqrt import *
from ItertoolsUtil import *

class SevernSieve:
	def __init__ (self, n):
		e = EratosthenesWheel (6, [2])
		e.n = 6
		
		k=1
		while True:
			print "n=",e.n
			print "wheel=",e.wheel
			print "product=",e.product
			#print "gaps=",e.gaps
			print "len (A)=", len (e.A)
			
			e.sieve ()
			p = list (e.primes ())
			print p
			e.wheel.append (p[k])
			e.gaps = [1] + p[k+1:]
			e.product *= p[k]
			e.n = e.product * p[k+1]
			#e.n += e.product - e.n % e.product
			e.sqrt = int (IntegerSqrt.exact_sqrt (e.n)[0])
			e.A = [True] * e.actual_size ()
			e.A[0] = False # 1 is not prime
			k += 1
			sleep (1)
		"""
		e.sieve ()
		p = list (e.primes ())
		print p
		e.wheel.append (p[2])
		e.gaps = [1] + p[3:]
		e.product *= p[2]
		e.n = e.product * p[3]
		e.sqrt = int (IntegerSqrt.exact_sqrt (e.n)[0])
		e.A = [True] * e.actual_size ()
		e.A[0] = False # 1 is not prime
		
		e.sieve ()
		print list (e.primes ())
		sleep (1)
		"""
		
		# 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81
		#   |   x   x   x   x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x     x
		#     |     2     x       2        x        2        x        2        x        2        x        2        x        2        x        2        x        2        x        2        x        2        x        2        x        2        x
		#         |         2              3              2              x              6              x              2              3              2              x              6              x              2              3              2
		#             |                 2                    3                    2                    5                    6                    x                    2                    3                    10                   x
		
		max_test = int (IntegerSqrt.exact_sqrt (n)[0])
		product = 2
		gaps = [1]
		wheel = [2]
		sieve = [True] * (n / product * len (gaps) + 1)
		sieve[0] = False
		#for i in xrange (0, max_test + 1, product):
		
		INV = [None] * n
		
		i = 0
		while i <= max_test:
			flag = False
			for igap in gaps:
				I = i + igap
				if I > max_test: break
				print I, len (INV)
				INV[I] = I / product * len (gaps) + gaps.index (I % product)
				if not sieve[I / product * len (gaps) + gaps.index (I % product)]: continue
				
				for jgap in gaps[1:]:
					J = I * (product * 0 + jgap)
					if J > n: break
					assert sieve[J / product * len (gaps) + gaps.index (J % product)]
					INV[J] = J / product * len (gaps) + gaps.index (J % product)
					sieve[J / product * len (gaps) + gaps.index (J % product)] = False
				for j in xrange (1, n / I / product + 1):
					for jgap in gaps:
						J = I * (product * j + jgap)
						if J > n: break
						#assert sieve[J / product * len (gaps) + gaps.index (J % product)]
						INV[J] = J / product * len (gaps) + gaps.index (J % product)
						sieve[J / product * len (gaps) + gaps.index (J % product)] = False
				new_gaps = [1]
				new_product = product * I
				new_wheel = wheel + [I]
				for ii in xrange (0, product * I, product):
					for iigap in gaps:
						II = ii + iigap
						if II > product * I: break
						if not sieve[II / product * len (gaps) + gaps.index (II % product)]: continue
						if II in wheel: continue
						if II == I: continue
						if II is not 1: new_gaps.append (II)
				print "new_wheel=", new_wheel
				print "new_gaps=", new_gaps
				print "new_product=",new_product
				print "INV=",INV
				
				new_sieve = [True] * (n / new_product * len (new_gaps) + 1)
				#new_sieve = [False] * (n / new_product * len (new_gaps) + 1)
				new_sieve[0] = False
				
				#       | 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
				#         0   1   2   3   4    5     6     7     8     9     10    11    12    13    14    15    16    17    18    19    20    21
				# 2     | 1   3   5   7   9    11    13    15    17    19    21    23    25    27    29    31    33    35    37    39    41    43    45    47    49
				# 2 3   | 1       5   7        11    13          17    19          23    25          29    31          35    37          41    43          47    49
				# 2 3 5 | 1           7        11    13          17    19          23                29    31                37          41    43
				
				primes = []
				primes.extend (wheel)
				for ii2 in xrange (0, (n / product * len (gaps) + 1), product):
					for ii2gap in gaps:
						II2 = ii2 + ii2gap
						if II2 > n: break
						if sieve[II2 / product * len (gaps) + gaps.index (II2 % product)]:
							primes.append (II2)
				
				for ii2 in xrange (0, (n / new_product * len (new_gaps) + 1), new_product):
					for ii2gap in new_gaps:
						II2 = ii2 + ii2gap
						if II2 >n: break
						
						print "II2=",II2
						inv = INV[II2]
						if inv is None:
							new_sieve[II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)] = False
						else:
							new_sieve[II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)] = sieve[inv]
						"""
						inv = II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)
						#inv2 = [(II2 - 0) / len (gaps) * product + gap for gap in gaps]
						inv3 = [(inv - 0) / len (gaps) * product + gap for gap in gaps]
						print ii2,ii2gap,"II2=",II2,":new[inv=",inv,"] = (inv3=",inv3,")"
						
						#print II2,"inverting=", inv,"ind=",list ([(inv - 0) / len (gaps) * product + gap for gap in gaps])
						for ind in [(inv - 0) / len (gaps) * product + gap for gap in gaps]:
							if ind >= len (sieve): break
							#print ind, list ([(II2 - 0) / len (gaps) * product + gap for gap in gaps])
							new_sieve[
									II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)] = sieve[ind]
						"""
						"""
						II = ii + iigap
						II / product * len (gaps) + gaps.index (II % product)
						
						for ii in xrange (0, (n / product * len (gaps) + 1), product):
							for iigap in gaps:
								II = ii + iigap
								if II >= (n / product * len (gaps) + 1): break
								print "new_sieve[",	II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product),"] =", sieve[
										II / product * len (gaps) + gaps.index (II % product)]
								new_sieve[
									II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)] = sieve[
										II / product * len (gaps) + gaps.index (II % product)]
						"""
				"""						
				for ii in xrange (0, (n / product * len (gaps) + 1), product):
					for iigap in gaps:
						II = ii + iigap
						if II >= (n / product * len (gaps) + 1): break
						if not sieve[II / product * len (gaps) + gaps.index (II % product)]: continue
						if II in wheel: continue
						
						II2 = None
						for ii2 in xrange (0, (n / new_product * len (new_gaps) + 1), new_product):
							#if II2 is not None: break
							for ii2gap in new_gaps:
								II2 = ii2 + ii2gap
								#if II2 == II: break
								#if II2 in new_wheel: continue
								print "good", II, II2,II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product),II / product * len (gaps) + gaps.index (II % product),sieve[
									II / product * len (gaps) + gaps.index (II % product)]
								if new_sieve[
									II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)]: continue
								new_sieve[
									II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)] = sieve[
									II / product * len (gaps) + gaps.index (II % product)]
						
				"""	
				"""
					for ii in xrange (0, new_product * I, new_product):
					for iigap in new_gaps:
						II = ii + iigap
						#if II > new_product * I: break
						#if II in wheel: continue
						#iiold = ii / new_product * product
						IIold = None
						for iiold in xrange (0, product * I, product):
							if IIold is not None: break
							for iioldgap in gaps:
								print "iiold=",iiold,"iioldgap=",iioldgap,"IIold=",iiold+iioldgap
								if iiold + iioldgap == II:
									IIold = iiold + iioldgap
									break
						if IIold is None: print "ii=",ii,"iigap=",iigap,"II=",II
						new_sieve[II / new_product * len (new_gaps) + new_gaps.index (II % new_product)] = sieve[IIold / product * len (gaps) + gaps.index (IIold % product)]
				"""
				
				new_primes = []
				new_primes.extend (new_wheel)
				for ii2 in xrange (0, (n / new_product * len (new_gaps) + 1), new_product):
					for ii2gap in new_gaps:
						II2 = ii2 + ii2gap
						if II2 > n: break
						if new_sieve[II2 / new_product * len (new_gaps) + new_gaps.index (II2 % new_product)]:
							new_primes.append (II2)
				assert primes == new_primes, "primes: %s, new_primes: %s" % (primes, new_primes)
				
				print "end loop"
				print sieve
				print new_sieve
				
				product = new_product
				gaps = new_gaps
				sieve = new_sieve
				wheel = new_wheel
				INV = [] * n

				print len (sieve), (n / product * len (gaps) + 1)
				assert len (sieve) == (n / product * len (gaps) + 1)
				flag = True
				break
			if not flag: i += product
		print sieve	
		
		"""				
				for j in xrange (0, n / product + 1, product * i)
			
			
			for igap in gaps:
				i * igap
			if not sieve[i]: continue
			#for j in xrange (i + i, n, i):
			#	sieve[j] = False	
			for j in xrange (0, n / product + 1, product * i):
				for gap in gaps:
					k = ((j * product) + gap) * i
					if k is 0: continue
					if k > n: break
					assert sieve[k]
					sieve[k] = False
			product *= i
			try:
				gaps.remove (0)
				gaps.append (1)
			except: pass
			try: gaps.remove (i)
			except: pass
			wheel.append (i)
			for k in xrange (i, product):
				if sieve[i]:
					print "i=",i
					gaps.append (i)
			print "wheel=",wheel
			print "gaps=",gaps
		"""




		"""		
		
		self.e = Eratosthenes3 (30, [2, 3])
		e.sieve ()
		
		next_prime = e.primes ()[len (self.e.wheel)]
		self.e.wheel.append (next_prime)
		self.e.product *= next_prime
		self.gaps.remove (next_prime) # should be at index 1 (i.e., gaps[0] is 1)
		# extend gaps to include new product
		# populate with primes ()
		
		# 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
		#   |   x   x   x   x     x     x     x     x     x     x     x     x     x     x
		#     |     o     x       o        x        o        x        o        x        o
		#         |         o              o              o              x              o
		#             |                 o                    o                    o
		
		self.gaps = list (xrange (1, self.product))
		#for p in wheel:
		for k in xrange (len (wheel)):
			p = wheel[k]
			for j in xrange (p, self.product, p * reduce (mul, wheel[:k], 1)):
				try: self.gaps.remove (j)
				except: pass
		#n += self.product % n
		#n += self.product - self.product % n
		n += self.product - n % self.product
		Eratosthenes.__init__ (self, n)
		self.A[0] = False # 1 is not prime
		"""
"""
wheel = [2]
product = 2
gaps = [1]
sieve = [True] * 4 / product
sieve[1 - 1] = False

for i in xrange (1, len (sieve) + 1, product):
	for gap in gaps:
		if sieve[i + gap - 1]:
			for j in xrange (i + i, len (sieve) + 1, product)

def multiplesIndices (self, i):
		for gap in self.gaps[1:]:
				ret = i * (self.product * 0 + gap)
				if ret <= len (self): yield ret
		for k in xrange (1, len (self) / i / self.product + 1):
			for gap in self.gaps:
				ret = i * (self.product * k + gap)
				if ret <= len (self): yield ret
"""

	# sieve 2 3 = 6... 5 times
	# gaps  (2): 1 5

	# find 5
	# sieve 2 3 5 = 30... 7 times
	# gaps (8)
	
	# find 7
	# sieve 2 3 5 7 = 210
	# gaps (48)
	
	# wheel is 2: 1 and primes up to 2 (after 2): 1
	# wheel is 2 3: 1 and primes up to 6 (after 3): 1 5
	# wheel is 2 3 5: 1 and primes up to 30 (after 5): 1 7 11 13 17 19 23 29
	# wheel is 2 3 5 7: 1 and primes up to 210 (after 7): 1 11 13 17 19 23 29

if __name__ == "__main__":
	SevernSieve (100)