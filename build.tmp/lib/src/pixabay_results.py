#! /usr/bin/env python3

from results import Results

from rest import RESTParam, RESTParamList, RESTParamQuery, IAHeaderRESTClient
from rest import IARESTClient

def pixabay (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None, session=None):
	key    = RESTParam ('key', key)
	params = [key]	
	
	if qs          is not None:
		q           = RESTParamQuery ('q'          , qs)
		params.append (q)
	if lang        is not None:
		lang        = RESTParam      ('lang'       , lang)
		params.append (lang)
	if orientation is not None:
		orientation = RESTParam      ('orientation', orientation)
		params.append (orientation)
	if category    is not None:
		category    = RESTParam      ('category'   , category)
		params.append (category)
	if min_width   is not None:
		min_width   = RESTParam      ('min_width'  , min_width)
		params.append (min_width)
	if min_height  is not None:
		min_height  = RESTParam      ('min_height' , min_height)
		params.append (min_height)
	if colors      is not None:
		colors      = RESTParamList  ('colors'     , colors)
		params.append (colors)
	if safesearch  is not None:
		safesearch  = RESTParam      ('safesearch' , safesearch)
		params.append (safesearch)
	if order       is not None:
		order       = RESTParam      ('order'      , order)
		params.append (order)
	if page        is not None:
		page        = RESTParam      ('page'       , page)
		params.append (page)
	if per_page    is not None:
		per_page    = RESTParam      ('per_page'   , per_page)
		params.append (per_page)
	
	# 5,000 requests per hour
	# X-RateLimit-Limit     The maximum number of requests that the consumer is permitted to make in 30 minutes.
	# X-RateLimit-Remaining The number of requests remaining in the current rate limit window.
	# X-RateLimit-Reset     The remaining time in seconds after which the current rate limit window resets.
	headers = ('X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset')
	client  = IAHeaderRESTClient ('https', 'pixabay.com', 'api/', params, headers=headers, session=session)
	#client  = IAHeaderRESTClient ('https', 'pixabay.com', 'api', params, headers=headers, session=session)
	#client  = IARESTClient ('https', 'pixabay.com', 'api', params)
	r, h = client.get ()
	#r = client.get ()
	lim   = h.get ('X-RateLimit-Limit')
	rem   = h.get ('X-RateLimit-Remaining')
	reset = h.get ('X-RateLimit-Reset')
	
	total      = r['total']
	total_hits = r['totalHits']
	hits       = r['hits'] # {'id': int, 'pageURL': url, 'type': str, 'tags': strs, 'previewURL': url, 'previewWidth': int, 'previewHeight': int, 'webformatURL': url, 'webformatWidth': int, 'webformatHeight': int, 'largeImageURL': url, 'imageWidth': int, 'imageHeight': int, 'imageSize': int, 'views': int, 'downloads': int, 'favorites': int, 'likes': int, 'comments': int, 'user_id': int, 'user': str, 'userImageURL': url}
	
	#r = r[0] # most accurate
	#print ("r: %s" % (r,))
	#elevation = r['elevation']
	#print ("elevation: %s" % (elevation,))
	c = client.cred
	assert c is not None
	assert len (c) > 0
	#          0           1     2    3    4      5  6
	return total, total_hits, hits, lim, rem, reset, c
	#return total, total_hits, hits, c

from cache import memoized_key, memoized_cacher3

"""
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
"""
def pixabay_cacher (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None, session=None):
	nullify = (3, 4, 5,)
	kn      = (12,)
	#                                               0   1     2            3         4          5           6       7           8      9    10        11       12
	ret = memoized_cacher3 (nullify, kn, pixabay, key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page, session)
	#ret, cred = ret
	#ret = float (ret)
	#return ret, cred
	return ret
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None, session=None):
	key = memoized_key (pixabay)
	return pixabay_cacher (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page, session)	
	
class PixabayResults (Results):
	def __init__ (self, session=None, *args, **kwargs):
		def pixabay3 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None): return pixabay2 (qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page, session)
		Results.__init__ (self, pixabay3, 3, 200, *args, **kwargs)
		self.session = session
	def make_key (self, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None):
		qs  = tuple (qs)
		key = (qs, lang, orientation, category, min_width, min_height, colors, safesearch, order)
		return key

if __name__ == "__main__":
	import requests
	
	def main ():
		type1 = True
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
