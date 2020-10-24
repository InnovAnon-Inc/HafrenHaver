#! /usr/bin/env python3

from aggregator import Aggregator
#from aggregator import default_aggregator

class Recycler:
	def __init__ (self, aggregator):
		self.aggregator = aggregator
	def req (self, n, **kwargs):
		aggregator = self.aggregator
		rets = aggregator.req ()
		# TODO combos take n
		pass
	# cid, search => ?
	
class Artwork: # keyword => result list => image
	def __init__ (self, recycler):
		self.recycler = recycler

	# TODO pagination
	# TODO cache how many results have been consumed by each consumer... when a consumer exhausts results, 
	# pages[qs, lang, orientation, category, min_width, min_height, colors, safesearch, order]

	# queries enter system here ?

	def get_artwork (cid): pass
	
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
