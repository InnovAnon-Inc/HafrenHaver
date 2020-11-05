#! /usr/bin/env python3

from itertools import starmap

from recycler import Recycler, default_recycler

# cid, [(n, kwargs)...] => [res...]
class Artwork:
	def __init__ (self, recycler): self.recycler = recycler
	def req (self, *queries):
		f = lambda n, kwargs: self.recycler.req (n, **kwargs)
		return starmap (f, queries)

	# TODO pagination
	# TODO cache how many results have been consumed by each consumer... when a consumer exhausts results, 
	# pages[qs, lang, orientation, category, min_width, min_height, colors, safesearch, order]

	# queries enter system here ?

# TODO fetch actual results from buffer
		
#"""

# map keywords => [(image, credits), ...]
# TODO how to decide when to pull more images

# db1[keywords] = [(image, credits), ...]

# db2[caller] = [keywords, ...]
# check whether caller has used these keywords
# if so, pull more images ?


# count distinct pairs of caller, keywords
# record time of last call to web service
# if sufficient time has passed, select a keyword pair

# don't update cache until result list is exhausted, account for artwork's timeout
# PaginatedCache




# TODO download results before aggregator ?
# fetch ~page at a time ? ... function of page size and rate limit
# prefetching functionality here, but multithreading in next level ?
# fetch results one at a time until rate limit is exhausted ? no, bc other searches




# return result from buffer
# if buffer is nearly exhausted, spawn worker thread to prefetch another page ?
# TODO fetch results one at a time until up to quota of rate limit is used

# get rate limit, schedule requests to exhaust rate limit, repeat requests until cache miss



	
# TODO recycling at next-next level: stream of unique combinations of results: Recycler
# only invoke aggregator when unique combos are exhausted



		
# TODO level for managing multiple streams of unique combos... for networking: OnePunch

# qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None





# cache name: OnePunch


if __name__ == "__main__":
	from aggregator import default_aggregator
	
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
