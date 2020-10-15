#! /usr/bin/env python3

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
class Results: # keyword => result list
	def __init__ (self, result_f, min_page, max_page):
		self.time      = None # time of last request
		self.limit     = None
		self.remaining = None
		self.reset     = None
		self.cache     = {} # TODO load cache from disk
		self.result_f  = result_f
		self.min_page  = min_page
		self.max_page  = max_page
	#def req (self, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	def req (self, page=None, per_page=None, **kwargs):
		if page     is None: page     = 0 + 1
		if per_page is None: per_page = 20
		
		#key  = (qs, lang, orientation, category, min_width, min_height, colors, safesearch, order)
		key = self.make_key (**kwargs)
		if key in self.cache: vtotal, vtotal_hits, vrngs, vcreds = self.cache[key]
		else:
			vtotal = vtotal_hits = vcreds = None
			vrngs = []
		rngs = list (vrngs)
		print ("rngs: %s" % (rngs,))
		
		req_min = (page + 0 - 1) * per_page                     # lower bound requested by user
		req_max = (page + 1 - 1) * per_page                     # upper bound requested by user
		print ("req_min: %s, req_max: %s" % (req_min, req_max))
		
		req_rng = range (req_min, req_max)                  # requested range
		req_rng = list (req_rng)
		
		def result_slice (a, b, pg, pp):                    # results in [(pg + 0) * pp, (pg + 1) * pp)
			print ("result_slice (a: %s, b: %s, pg: %s, pp: %s)" % (a, b, pg, pp))
			assert a  <= b                                  
			assert pg >= 1
			assert pp >= self.min_page
			assert pp <= self.max_page
			#tmp = pixabay2 (*key, page=pg, per_page=pp)
			tmp = self.result_f (*key, page=pg, per_page=pp)
			total, total_hits, hits, lim, rem, reset, c = tmp
			tmp_min = (pg + 0 - 1) * pp
			tmp_max = (pg + 1 - 1) * pp
			a = a - tmp_min
			assert a >= 0
			b = b - tmp_min
			assert b <  tmp_max
			hits = hits[a:b + 1]                            # sliced from [a, b]
			tmp  = total, total_hits, hits, lim, rem, reset, c
			return tmp
		
		ret = []
		for rng in rngs:                                    # remove cached ranges from requested ranges
			rng_min, rng_max, pg, pp = rng
			rng = range (rng_min, rng_max + 1)
			N   = len (req_rng)
			req_rng = list (set (req_rng) - set  (rng))
			req_rng.sort ()
			n   = len (req_rng)
			if n == N: continue
			a   = max (req_min, rng_min)                    # append cached results
			b   = min (req_max, rng_max)
			print ("a: %s, b: %s, pg: %s, pp: %s" % (a, b, pg, pp))
			tmp = result_slice (a, b, pg, pp)
			total, total_hits, hits, lim, rem, reset, c = tmp
			assert lim   is None, str (lim)
			assert rem   is None, str (rem)
			assert reset is None, str (reset)
			ret.extend (hits)
			#tmp = total, total_hits, hits, c
			#ret.append (tmp)
			if vtotal is None: vtotal = total
			assert vtotal == total
			if vtotal_hits is None: vtotal_hits = total_hits
			assert vtotal_hits == total_hits
			if vcreds is None: vcreds = c
			assert vcreds == c
		#print ("cached: %s" % (ret,))
		
		print ("req_rng: %s" % (req_rng,))
		
		def pgpp (a, b):                                    # pp = b - a + 1 + c, s.t.
			pp = b - a + 1                                  # (pg + 0) * pp <= a, b <= (pg + 1) * pp
			pp = max (pp, self.min_page)                    # pp in [3, 200]
			while True:
				pg = a // pp + 1
				if pp * (pg + 1 - 1) >= b: break
				pp = pp + 1
				if pp > self.max_page: raise Exception ()
			return (a, b, pg, pp)
		
		reqs = []                                           # actual ranges to request
		a    = req_rng[0]
		for b, c in zip (req_rng[:-1], req_rng[1:]):
			if c == b + 1: continue
			tmp = pgpp (a, b)
			reqs.append (tmp)
			a   = c
		b   = req_rng[-1]
		tmp = pgpp (a, b)
		reqs.append (tmp)
		print ("reqs: %s" % (reqs,))
			
		for req in reqs:                                    # request new ranges
			req_min, req_max, pg, pp = req
			print ("req_min: %s, req_max: %s, pg: %s, pp: %s" % (req_min, req_max, pg, pp))
			tmp = result_slice (*req)
			total, total_hits, hits, lim, rem, reset, c = tmp
			ret.extend (hits)
			#tmp = total, total_hits, hits, c
			#ret.append (tmp)
			if vtotal is None: vtotal = total
			assert vtotal == total
			if vtotal_hits is None: vtotal_hits = total_hits
			assert vtotal_hits == total_hits
			if vcreds is None: vcreds = c
			assert vcreds == c
			if lim is None or rem is None or reset is None: # cached results not registered at this level
				assert lim   is None
				assert rem   is None
				assert reset is None
				continue
			self.time      = None # TODO current time
			self.limit     = lim
			self.remaining = rem
			self.reset     = reset
		#print ("ret: %s" % (ret,))
		
		# TODO fix reqs
		f = lambda val: val[0]                              # sort ranges by lower bound
		vrngs.extend (reqs)
		vrngs.sort (key=f)
		self.cache[key] = vtotal, vtotal_hits, vrngs, vcreds
		# TODO write cache to disk
		return vtotal, vtotal_hits, ret, vcreds

from rest import RESTParam, RESTParamList, RESTParamQuery, IAHeaderRESTClient
from rest import IARESTClient

def pixabay (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
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
	client  = IAHeaderRESTClient ('https', 'pixabay.com', 'api', params, headers=headers)
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
	return total, total_hits, hits, lim, rem, reset, c
	#return total, total_hits, hits, c

from cache import memoized_key, memoized_cacher2

"""
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
"""
def pixabay_cacher (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	nullify = (3, 4, 5)
	ret = memoized_cacher2 (nullify, pixabay, key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)
	#ret, cred = ret
	#ret = float (ret)
	#return ret, cred
	return ret
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay_cacher (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
	
class PixabayResults (Results):
	def __init__ (self, *args, **kwargs):
		Results.__init__ (self, pixabay2, 3, 200, *args, **kwargs)
	def make_key (self, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None):
		key = (qs, lang, orientation, category, min_width, min_height, colors, safesearch, order)
		return key

































def pexel (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
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
	client  = IAHeaderRESTClient ('https', 'pixabay.com', 'api', params, headers=headers)
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
	return total, total_hits, hits, lim, rem, reset, c
	#return total, total_hits, hits, c

from cache import memoized_key, memoized_cacher2

"""
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
"""
def pixabay_cacher (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	nullify = (3, 4, 5)
	ret = memoized_cacher2 (nullify, pixabay, key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)
	#ret, cred = ret
	#ret = float (ret)
	#return ret, cred
	return ret
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay_cacher (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
	
class PexelResults (Results):
	def __init__ (self, *args, **kwargs):
		Results.__init__ (pexel2, 1, 80, *args, **kwargs)
	def make_key (self):
		key = ()
		return key
# TODO load balancing at next level: Aggregator
# TODO recycling at next-next level: stream of unique combinations of results: Recycler
# TODO level for managing multiple streams of unique combos... for networking: OnePunch

# qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None
class Artwork: # keyword => result list => image
	def __init__ (self, results):
		self.results = results

	# TODO pagination
	# TODO cache how many results have been consumed by each consumer... when a consumer exhausts results, 
	# pages[qs, lang, orientation, category, min_width, min_height, colors, safesearch, order]


# cache name: OnePunch


if __name__ == "__main__":
	def main ():
		r = PixabayResults ()
		#print (pixabay2 (qs=('test',)))
		print ("0-19")
		p0 = r.req (qs=('test',))                      #  0-19
		print ()
		
		print ("40-59")
		p1 = r.req (qs=('test',), page=3)              # 40-59
		print ()
		
		print ("15-29")
		p2 = r.req (qs=('test',), page=2, per_page=15) # 15-29
		print ()
		
		print ("25-49")
		p3 = r.req (qs=('test',), page=2, per_page=25) # 25-49
		print ()

		for p in (p0, p1, p2, p3):
			print (p)
			print ()
		
		print ("time     : %s" % (r.time,))
		print ("limit    : %s" % (r.limit,))
		print ("remaining: %s" % (r.remaining,))
		print ("reset    : %s" % (r.reset,))
	main ()
	quit ()
