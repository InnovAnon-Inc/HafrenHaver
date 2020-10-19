#! /usr/bin/env python3

from results import Results

from rest import RESTParam, RESTParamList, RESTParamQuery, IAHeaderRESTClient
from rest import IARESTClient

from cache import memoized_key, memoized_cacher3

def pexels (key, queries, locale=None, page=None, per_page=None, session=None):
	q = RESTParamQuery ('query', queries)
	params = [q]	
	
	if locale is not None:
		locale   = RESTParam ('locale'  , locale)
		params.append (lang)
	if page        is not None:
		page     = RESTParam ('page'    , page)
		params.append (page)
	if per_page    is not None:
		per_page = RESTParam ('per_page', per_page)
		params.append (per_page)
	
	send_headers = { "Authorization" : key, }
	headers = ('X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset')
	client  = IAHeaderRESTClient ('https', 'api.pexels.com', 'v1/search', params, send_headers=send_headers, headers=headers, session=session)
	r, h = client.get ()
	lim   = h.get ('X-RateLimit-Limit')
	rem   = h.get ('X-RateLimit-Remaining')
	reset = h.get ('X-RateLimit-Reset')
	
	total_hits = r['total_results']
	total      = total_hits
	#page_no    = r['page']
	#pp         = r['per_page']
	hits       = r['photos']
	
	c = client.cred
	assert c is not None
	assert len (c) > 0
	#          0           1     2    3    4      5  6
	return total, total_hits, hits, lim, rem, reset, c

def pexels_cacher (key, queries, locale=None, page=None, per_page=None, session=None):
	nullify = (3, 4, 5,)
	kn      = (5,)
	#                                              0        1       2     3         4        5
	ret = memoized_cacher3 (nullify, kn, pexels, key, queries, locale, page, per_page, session)
	return ret
def pexels2 (queries=None, locale=None, page=None, per_page=None, session=None):
	key = memoized_key (pexels)
	return pexels_cacher (key, queries, locale, page, per_page, session)	
	
class PexelsResults (Results):
	def __init__ (self, session=None, *args, **kwargs):
		def pexels3 (queries=None, locale=None, page=None, per_page=None): return pexels2 (queries, locale, page, per_page, session)
		Results.__init__ (self, pexels3, 1, 80, *args, **kwargs)
		#self.session = session
	def make_key (self, queries, locale=None):
		queries = tuple (queries)
		key     = (queries, locale)
		return key

if __name__ == "__main__":
	import requests
	
	def main ():
		type1 = False
		layer = 0
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
