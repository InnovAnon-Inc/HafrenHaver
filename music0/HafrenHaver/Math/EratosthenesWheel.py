"""InnovAnon Inc. Proprietary"""

from Eratosthenes import *

class EratosthenesWheel (Eratosthenes):
	"""https://stackoverflow.com/questions/30553925/adding-wheel-factorization-to-an-indefinite-sieve"""
	# 2 4 6| 8 10  12
	#  3  6|  9    12
	#1   5 |7    11  |13 17|19 23|25 29|31 35|37 41|43 47|49 53|55 59|61 65|67 71|73 77|79 83|85 89|91 95|97 101|103 107|109 113|115 119|121 125|127 131|133 137|139 143|145 149
	#       1    2    3  4  5  6
	#       a                              b              c                          d              e                                f                   g
	#a = b mod c
	#b = qk + a
	#
	# 6k + 1, 6k + 5
	# (6k + 1)(6p + 1), (6k + 1)(6p + 5)     (6k + 5)(6p + 1), (6k + 5)(6p + 5)
	# 5 7 11 13 17 19
	#
	# q:=num gaps
	# for each gap < sqrt (n)
	#    if prime
	#       for each permutation of gap multiples < n
	#          clear bit
	# sqrt (n)/q * n/q!
	def __init__ (self, n, wheel):
		self.wheel = wheel
		self.product = reduce (mul, wheel, 1)
		self.gaps = list (xrange (1, self.product))
		for p in wheel:
			for j in xrange (p, self.product, p):
				try: self.gaps.remove (j)
				except: pass
		"""
		for k in xrange (len (wheel)):
			p = wheel[k]
			print "k=", k, "p=", p
			for j in xrange (p, self.product, p * reduce (mul, wheel[:k], 1)):
				print "j=", j
				#for gap in self.gaps[:j-1]:
				for gap in self.gaps[]:
				#try:
					print j-1,"gap=", gap,"gaps=",self.gaps[:j-1]
					print "to rem=",j,gap,j * gap
					if j * gap < self.product:
						self.gaps.remove (j * gap)
				#except: pass
		"""
		"""
		self.gaps = list (Eratosthenes2 (self.product).primes ())
		map (self.gaps.remove, self.wheel)
		self.gaps = [1] + self.gaps
		"""
		
		#n += self.product % n
		#n += self.product - self.product % n
		n += self.product - n % self.product
		Eratosthenes.__init__ (self, n)
		self.A[0] = False # 1 is not prime
	def isValidIndex (self, i):
		#if i <= self.product: return False
		if i < 1: return False
		if i > self.n: return False
		# TODO
		#if not self.gaps.contains ((i - self.product) % self.product):
		#	return False
		try: self.gaps.index (i % self.product)
		except: return False
		return True
	def actual_size (self):
		#return (len (self) - self.product) / self.product * len (self.gaps)
		return len (self) / self.product * len (self.gaps) + 1
	def indexOf (self, n):
		if not self.isValidIndex (n): raise Exception ()
		#return (n - self.product) / self.product + self.gaps.index (
		#	(n - self.product) % self.product)
		ret = n / self.product * len (self.gaps) + self.gaps.index (n % self.product)
		#print "n=%s, ret=%s" % (n, ret)
		#assert n == self.invIndexOf (ret) , "n=%s, ret=%s, inv=%s" % (n, ret , self.invIndexOf (ret))
		assert n in self.invIndexOf (ret)
		return ret
	def invIndexOf (self, ninv):
		#ninv = n / self.product * len (self.gaps) + self.gaps.index (n % self.product)
		#return (ninv - 0) / len (self.gaps) * self.product + len (self.gaps)
		#return (ninv - 0) / len (self.gaps) * self.product + 1
		
		#i = 0
		#try: i = self.gaps.index (ninv % self.product)
		#except: pass
		#return (ninv - 0) / len (self.gaps) * self.product + i
		for gap in self.gaps:
			yield (ninv - 0) / len (self.gaps) * self.product + gap
		
		#return (ninv - 0) * self.product / len (self.gaps)
		#return int (ceil (1.0 * (ninv - 0) / len (self.gaps))) * self.product
		#return int (ceil (1.0 * (ninv - 0) * self.product / len (self.gaps)))
	def allIndices (self):
		# start at product + gaps
		# increment by product
		# so... 1..n/6
		#   then iterate gaps
		#for base in xrange (self.product, len (self) + 1, self.product):
		#for base in xrange (0, len (self) + 1 - self.gaps[0], self.product):
		for base in xrange (0, len (self) + 1, self.product):
			for gap in self.gaps:
				ret = base + gap
				#if ret <= len (self):
				if ret > len (self): break
				yield ret
	def testIndices (self):
		#for base in xrange (self.product, self.max_test () + 1, self.product):
		for base in self.testIndicesBases ():
			for gap in self.gaps:
				ret = base + gap
				#if ret <= len (self):
				#if ret <= self.max_test ():
				if ret > self.max_test (): break
				yield ret
	def testIndicesBases (self):
		# 0 6
		# 1 5 7 11
		#return xrange (0, self.max_test () + 1 - self.gaps[0], self.product)
		return xrange (0, self.max_test () + 1, self.product)
	def multiplesIndices (self, i):
		for gap in self.gaps[1:]:
				ret = i * (self.product * 0 + gap)
				#if ret <= len (self): yield ret
				if ret > len (self): break
				yield ret
		for k in xrange (1, len (self) / i / self.product + 1):
			for gap in self.gaps:
				ret = i * (self.product * k + gap)
				#if ret <= len (self): yield ret
				if ret > len (self): break
				yield ret
	def prefix (self): return self.wheel

if __name__ == "__main__":
	def test (e):
		e.sieve ()
		print e
		
		for f in xrange (100):
			g = Eratosthenes (f)
			g.sieve ()
		
	def comp (a, b):
		ap = list (a.primes ())
		bp = list (b.primes ())[:len (ap)]
		if ap != bp: raise Exception ((ap, bp))

	print "TEST 0"
	e = Eratosthenes (100)
	test (e)
	print
	
	print "TEST 1"
	f = Eratosthenes2 (100)
	test (f)
	comp (e, f)
	print
	
	print "TEST 2"
	g = EratosthenesWheel (100, [2])
	test (g)
	comp (f, g)
	print g.gaps
	print
	
	print "TEST 3"
	h = EratosthenesWheel (100, [2, 3])
	test (h)
	comp (g, h)
	print h.gaps
	print

	print "TEST 4"
	i = EratosthenesWheel (100, [2, 3, 5])
	test (i)
	comp (h, i)
	print i.gaps
	print
	
	print "TEST 5"
	j = EratosthenesWheel (100, [2, 3, 5, 7])
	test (j)
	comp (i, j)
	print j.gaps
	print
	
	print "TEST 6"
	k = EratosthenesWheel (100, [2, 3, 5, 7, 11])
	test (k)
	comp (j, k)
	print len (k.gaps)
	print
	#time.sleep (5)
	
	print "SUCCESS"
	"""
	def info (k, e):
		print k, ":", e.product, "/", len (e.gaps), "=", 1.0 * e.product / len (e.gaps)
		print e.gaps
	l = []
	L = [2, 3, 5, 7, 11, 13, 17, 19]
	p = reduce (mul, L, 1)
	print "product=", p
	for k in L:
		l.append (k)
		e = EratosthenesWheel (p, l)
		info (k, e)
	"""
	#SevernSieve (100)