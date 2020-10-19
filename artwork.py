#! /usr/bin/env python3
		
class Pager:
	def __init__ (self, results):
		self.results  = results
		#self.nquery   = 0
		#self.page     = {}
		self.per_page = results.max_page
		#self.index    = {}
		#self.session  = session
	def req (self, **kwargs):
		# TODO check rate limit ?
		results  = self.results
		per_page = self.per_page
		
		res  = results.req (1, per_page, **kwargs)
		vtotal, vtotal_hits, hits, vcreds = res
		for index in range (0, per_page):
			res = hits[index]
			ret = vtotal, vtotal_hits, res, vcreds
			yield ret
		
		max_page = vtotal_hits // per_page
		for page in range (2, max_page + 1):
			res  = results.req (page, per_page, **kwargs)
			vtotal, vtotal_hits, hits, vcreds = res
			for index in range (0, per_page):
				res = hits[index]
				ret = vtotal, vtotal_hits, res, vcreds
				yield ret
				
		page     = max_page + 1
		max_ndx  = vtotal_hits - (max_page * per_page)
		if max_ndx != 0:
			res  = results.req (page, per_page, **kwargs)
			vtotal, vtotal_hits, hits, vcreds = res
			for index in range (0, max_ndx):
				res = hits[index]
				ret = vtotal, vtotal_hits, res, vcreds
				yield ret
				
		# TODO append vcreds
		
	def get_time      (self): return self.results.get_time      ()
	def get_limit     (self): return self.results.get_limit     ()
	def get_remaining (self): return self.results.get_remaining ()
	def get_reset     (self): return self.results.get_reset     ()
	
from pixabay_results import PixabayResults

class PixabayPager (Pager):
	def __init__ (self, session=None, *args, **kwargs):
		results = PixabayResults (session, *args, **kwargs)
		Pager.__init__ (self, results, *args, **kwargs)

from pexels_results import PexelsResults

class PexelsPager (Pager):
	def __init__ (self, session=None, *args, **kwargs):
		results =  PexelsResults (session, *args, **kwargs)
		Pager.__init__ (self, results, *args, **kwargs) 






		
		
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


		
# TODO load balancing at next level: Aggregator		
# one thread per buffer
# filter unique results here ?
class Aggregator:
	def __init__ (self, buffers):
		self.buffers = buffers
	def get_results (self, qs, lang, page=None, per_page=None): # ?
		# TODO get rate limits ?
		# TODO select result with best limit ?
		# query all that have not exhausted rate limits ?
		pass
	
# TODO recycling at next-next level: stream of unique combinations of results: Recycler
# only invoke aggregator when unique combos are exhausted
class Recycler:
	def __init__ (self, aggregator):
		self.aggregator = aggregator
	# cid, search => ?
		
# TODO level for managing multiple streams of unique combos... for networking: OnePunch

# qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None
class Artwork: # keyword => result list => image
	def __init__ (self, recycler):
		self.recycler = recycler

	# TODO pagination
	# TODO cache how many results have been consumed by each consumer... when a consumer exhausts results, 
	# pages[qs, lang, orientation, category, min_width, min_height, colors, safesearch, order]

	# queries enter system here ?

	def get_artwork (cid): pass
	


# cache name: OnePunch


if __name__ == "__main__":
	import requests
	
	def main ():
		type1 = False
		layer = 1
		if layer == 0:
			if type1: r = PixabayResults ()
			else:     r =  PexelsResults ()
		if layer == 1:
			s = requests.Session ()
			#s = None
			if type1: r = PixabayPager (s)
			else:     r =  PexelsPager (s)
		
		if layer == 0:
			print ("0-19")
			if type1: p0 = r.req (     qs=('test',))                      #  0-19
			else:     p0 = r.req (queries=('test',))                      #  0-19
			print ()
			
			print ("40-59")
			if type1: p1 = r.req (     qs=('test',), page=3)              # 40-59
			else:     p1 = r.req (queries=('test',), page=3)              # 40-59
			print ()
			
			print ("15-29")
			if type1: p2 = r.req (     qs=('test',), page=2, per_page=15) # 15-29
			else:     p2 = r.req (queries=('test',), page=2, per_page=15) # 15-29
			print ()
			
			print ("25-49")
			if type1: p3 = r.req (     qs=('test',), page=2, per_page=25) # 25-49
			else:     p3 = r.req (queries=('test',), page=2, per_page=25) # 25-49
			print ()

			for p in (p0, p1, p2, p3):
				print (p)
				print ()
		if layer == 1:
			if type1: p = r.req (     qs=('test',))
			else:     p = r.req (queries=('test',))
			
			print (p)
			print ()
			for h in p:
				print (h)
				print ()
				
			if type1: p = r.req (     qs=('test',))
			else:     p = r.req (queries=('test',))
			print (len (tuple (p)))
		#print ("time     : %s" % (r.time,))
		#print ("limit    : %s" % (r.limit,))
		#print ("remaining: %s" % (r.remaining,))
		#print ("reset    : %s" % (r.reset,))
		
		print ("time     : %s" % (r.get_time      (),))
		print ("limit    : %s" % (r.get_limit     (),))
		print ("remaining: %s" % (r.get_remaining (),))
		print ("reset    : %s" % (r.get_reset     (),))
	main ()
	quit ()
