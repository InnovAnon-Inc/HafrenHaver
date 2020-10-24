#! /usr/bin/env python3

from itertools import combinations

from aggregator import Aggregator

class Recycler:
	def __init__ (self, aggregator): self.aggregator = aggregator
	def req (self, n=1, **kwargs):
		agg = self.aggregator
		res = agg.req (**kwargs)
		res = combinations (res, n)
		# TODO chain all permutations ?
		return res
		
from aggregator import default_aggregator

def default_recycler (cb, *args, **kwargs):
	def cb2 (a):
		r = Recycler (a)
		r = cb (r)
		return r
	a = default_aggregator (cb2, *args, **kwargs)
	return a

if __name__ == "__main__":
	def main ():
		if False:
			def cb (a):
				r = Recycler (a)
				p  = r.req (n=2, qs=('test',))
				
				print (p)
				print ()
				for h in p:
					print (h)
					#print ("time     : %s" % (a.get_time      (),))
					#print ("limit    : %s" % (a.get_limit     (),))
					#print ("remaining: %s" % (a.get_remaining (),))
					#print ("reset    : %s" % (a.get_reset     (),))
					print ()
				
				p  = r.req (n=2, qs=('test',))
				print (len (tuple (p)))
				
				#print ("time     : %s" % (a.get_time      (),))
				#print ("limit    : %s" % (a.get_limit     (),))
				#print ("remaining: %s" % (a.get_remaining (),))
				#print ("reset    : %s" % (a.get_reset     (),))
			a = default_aggregator (cb)
			print ("a: %s" % (a,))
		else:
			def cb (r):
				p  = r.req (n=2, qs=('test',))
				
				print (p)
				print ()
				for h in p:
					print (h)
					#print ("time     : %s" % (a.get_time      (),))
					#print ("limit    : %s" % (a.get_limit     (),))
					#print ("remaining: %s" % (a.get_remaining (),))
					#print ("reset    : %s" % (a.get_reset     (),))
					print ()
				
				p  = r.req (n=2, qs=('test',))
				print (len (tuple (p)))
				
				#print ("time     : %s" % (a.get_time      (),))
				#print ("limit    : %s" % (a.get_limit     (),))
				#print ("remaining: %s" % (a.get_remaining (),))
				#print ("reset    : %s" % (a.get_reset     (),))
			r = default_recycler (cb)
			print ("r: %s" % (r,))
	main ()
	quit ()
