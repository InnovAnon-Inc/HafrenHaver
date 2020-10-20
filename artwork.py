#! /usr/bin/env python3
		
class Buffer: # fetch / prefetch results
	def __init__ (self, pager):
		self.pager = pager
	def req (self, **kwargs):
		pager = self.pager
		rets  = pager.req (**kwargs)
		# TODO might need to lock session
		# TODO prefetch first result in bg thread
		for ret in rets:
			# TODO join bg thread
			# TODO prefetch next result in bg thread
			vtotal, vtotal_hits, res, vcreds = ret
			# TODO fetch results: get session from pager's results... need to store session there
			session = self.pager.results.get_session ()
			res = download_file (res, session)
			res, limit, remaining, reset = res
			if limit     is not None: self.pager.results.limit     = limit
			if remaining is not None: self.pager.results.remaining = remaining
			if reset     is not None: self.pager.results.reset     = reset
			print ("limit: %s, remaining: %s, reset: %s" % (limit, remaining, reset))
			ret = vtotal, vtotal_hits, res, vcreds
			yield ret
	def get_time      (self): return self.pager.get_time      ()
	def get_limit     (self): return self.pager.get_limit     ()
	def get_remaining (self): return self.pager.get_remaining ()
	def get_reset     (self): return self.pager.get_reset     ()
	
import os
from pathlib import Path
import requests
import shutil

def download_file (url, session=requests): # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    assert url
    index = -1
    while True:
        local_filename = url.split ('/')[index] # TODO use entire url for filename
        if local_filename: break
        index = index - 1
    assert local_filename, "url: %s" % (url,)
    newdir         = "cache"                                            # create directory for cached images
    p              = Path (newdir)
    if not p.is_dir (): os.makedirs (newdir, 0o0777)
    local_filename = "%s/%s" % (newdir, local_filename,)                # put file in directory
    p              = Path (local_filename)
    if p.is_file (): return local_filename, None, None, None            # don't redownload
    
    with session.get (url, stream=True) as r:
        h     = r.headers
        lim   = h.get ('X-RateLimit-Limit')
        rem   = h.get ('X-RateLimit-Remaining')
        reset = h.get ('X-RateLimit-Reset')
        with open (local_filename, 'wb') as f: shutil.copyfileobj (r.raw, f)

    # TODO validate downloaded file
	
    return local_filename, lim, rem, reset


"""
def image_key (f, *args):
	print ("image_key (%s, %s)" % (f, args))
	url   = args
	fname = url.split ('/')[-1]
	return "cache/%s" % (fname,)
def image_indb (key):
	print ("image_indb (%s)" % (key,))
	return cacher_indb (key)
def image_getdb (key):
        print ("image_getdb (%s)" % (key,))
        ret = key_getdb (key)
        ret = make_tuple (ret) # TODO convert to image object
        return ret
def image_setdb (key, val):
        print ("image_setdb (%s, %s)" % (key, val))
        val = str (val) # TODO
        with open (key, "w") as f: f.write (val)
def image (f, *args):
        print ("image (%s, %s)" % (f, args))
        return helper (image_key, image_indb, image_getdb, image_setdb, f, *args)    
""" 	
	
"""
def download (url, session):
	r = session.get (url)
	if r.status_code != 200:
		print ("error: %s" % (r,))
		return None
	print ("r: %s" % (r,))
	return r.json ()

from cache import memoized_cacher3

def download_cacher (url, session=None):
	nullify = ()
	kn      = (1,)
	#                                                0        1
	ret = memoized_cacher3 (nullify, kn, download, url, session)
	return ret
"""

		
		


		
# TODO load balancing at next level: Aggregator		
# one thread per buffer
# filter unique results here ?
class Aggregator:
	def __init__ (self, buffers):
		self.buffers = buffers
	def req (self, qs, lang, page=None, per_page=None): # ?
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
		
		pass


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
	from pixabay_pager import PixabayPager
	from  pexels_pager import  PexelsPager
	
	def main ():
		type1 = False
		s = requests.Session ()
		#s = None
		if type1: r = PixabayPager (s)
		else:     r =  PexelsPager (s)
		r = Buffer (r)
		
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
		
		print ("time     : %s" % (r.get_time      (),))
		print ("limit    : %s" % (r.get_limit     (),))
		print ("remaining: %s" % (r.get_remaining (),))
		print ("reset    : %s" % (r.get_reset     (),))
	main ()
	quit ()
