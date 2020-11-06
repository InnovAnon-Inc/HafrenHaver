#! /usr/bin/env python3

# TODO load balancing at next level: Aggregator		
# one thread per buffer
# filter unique results here ?

from itertools import zip_longest, dropwhile, chain

class Aggregator:
	def __init__ (self, buffers): self.buffers = buffers
	def req_helper (self, qs=(), lang=None): # ?
		#for buf in self.buffers:
		#	kwargs = buf.convert (queries=qs, lang=lang)
		#	res = buf.req (**kwargs)
		#	yield from res
			
		def f (buf):
			kwargs = buf.convert (queries=qs, lang=lang)
			res = buf.req (**kwargs)
			yield from res
		t = map (f, self.buffers)
		t = zip_longest (*t)
		f = lambda a: a is not None
		
		for ab in t:
			k = filter (f, ab)
			yield from k
	def req (self, qs=(), lang=None):
		t = self.req_helper (qs, lang)
		# TODO check duplicate file contents
		f = lambda fname: False
		return dropwhile (f, t)
			
		# TODO get rate limits ?
		# TODO select result with best limit ?
		# query all that have not exhausted rate limits ?
		# buffers to query: function of (current number of results, rate limit)
		# when invokation count % rate limit is 0, query buffer ?
		
		# sort threads/buffers by best rate limit
		
		# first run:
		# start two threads, each thread queries a different buffer
		# return result from first thread to join
		# restart thread
		
		# next run:
		# return result from first thread to join (usually the one with the best rate limit, due to sorting order)
		# restart thread

from prefetcher import PixabayPrefetcher, PexelsPrefetcher
"""
class DefaultAggregator (Aggregator):
	def __init__ (self, session=None, *args, **kwargs):
		b0 = PixabayPrefetcher (session, *args, **kwargs)
		b1 =  PexelsPrefetcher (session, *args, **kwargs)
		buffers = (b0, b1)
		Aggregator.__init__ (self, buffers, *args, **kwargs)
	def __enter__ (self):
		for buf in self.buffers: buf.__enter__ ()
		return self
	def __exit__ (self, type, value, traceback):
		for buf in self.buffers: buf.__exit__ (type, value, traceback)
		return False
"""
from requests import Session

def default_aggregator (cb, *args, **kwargs):
	with Session () as s0, Session () as s1:
		with PixabayPrefetcher (s0, *args, **kwargs) as b0, PexelsPrefetcher (s1, *args, **kwargs) as b1:
			buffers = (b0, b1)
			a = Aggregator (buffers, *args, **kwargs)
			r = cb (a)
	return r

if __name__ == "__main__":
	import requests
	
	def main ():
		if False:
			with requests.Session () as s:		
				#b0 = PixabayBuffer (s)
				#b1 =  PexelsBuffer (s)
				#bs = [b0, b1]
				#a  = Aggregator (bs)
				#a = DefaultAggregator (s)
				#a = DefaultAggregator (None)
				with DefaultAggregator (None) as a:
					p  = a.req (qs=('test',))
					
					print (p)
					print ()
					for h in p:
						print (h)
						#print ("time     : %s" % (a.get_time      (),))
						#print ("limit    : %s" % (a.get_limit     (),))
						#print ("remaining: %s" % (a.get_remaining (),))
						#print ("reset    : %s" % (a.get_reset     (),))
						print ()
					
					p  = a.req (qs=('test',))
					print (len (tuple (p)))
					
					#print ("time     : %s" % (a.get_time      (),))
					#print ("limit    : %s" % (a.get_limit     (),))
					#print ("remaining: %s" % (a.get_remaining (),))
					#print ("reset    : %s" % (a.get_reset     (),))
		else:
			def cb (a):
				p  = a.req (qs=('test',))
				
				print (p)
				print ()
				for h in p:
					print (h)
					#print ("time     : %s" % (a.get_time      (),))
					#print ("limit    : %s" % (a.get_limit     (),))
					#print ("remaining: %s" % (a.get_remaining (),))
					#print ("reset    : %s" % (a.get_reset     (),))
					print ()
				
				p  = a.req (qs=('test',))
				print (len (tuple (p)))
				
				#print ("time     : %s" % (a.get_time      (),))
				#print ("limit    : %s" % (a.get_limit     (),))
				#print ("remaining: %s" % (a.get_remaining (),))
				#print ("reset    : %s" % (a.get_reset     (),))
			r = default_aggregator (cb)
			print ("r: %s" % (r,))
				
	main ()
	quit ()
