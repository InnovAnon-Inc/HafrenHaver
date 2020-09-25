#! /usr/bin/env python3

class Pattern:
	def __init__ (self, order):
		#rev = {}
		#I   = range (0, len (order))
		#for i, v in zip (I, order):
		#	if v in rev: temp = rev[v]
		#	else:        temp = []
		#	rev[v] = tuple (temp + [i])
		self.order = order
		#self.rev   = rev
	def __repr__ (self): return "Pattern [order=%s]" % (self.order,)
	# TODO __str__
	def __len__ (self): return len (self.order)
	def __getitem__  (self, key): return self.order[key]
	def __iter__     (self):       return iter     (self.order)
	def __reversed__ (self):       return reversed (self.order)
	def __contains__ (self, item): return item in self.order
	def uniq_elements (self): return tuple (set (self.order))
	def nuniq         (self): return len (self.uniq_elements ())
	
	
	"""
	#@jit
	def elem (self, i): return self.order[i]
	#@jit
	def all (self): return self.order
	@jit
	def indices (self, k):
		I = range (0, len (self.order))
		#for i, v in zip (I, self.order):
		#	if v == k: yield i
		I = zip (I, self.order)
		I = filter (lambda iv: v == k, I)
		return (i for i, v in I)
	"""
