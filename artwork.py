#! /usr/bin/env python3



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
		if per_page is None: per_page = 20 # TODO magic numbers
		assert     page >= 1
		assert per_page >= 1
		
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
		
		assert req_min < req_max
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
			#assert vcreds == c, "c: %s, vcreds: %s" % (c, vcreds)
			assert c is None or vcreds == c, "c: %s, vcreds: %s" % (c, vcreds)
		#print ("cached: %s" % (ret,))
		
		print ("req_rng: %s" % (req_rng,))
		
		"""
		def pgpp (a, b):                                    # pp = b - a + 1 + c, s.t.
			pp = b - a + 1                                  # (pg + 0) * pp <= a, b <= (pg + 1) * pp
			pp = max (pp, self.min_page)                    # pp in [3, 200]
			while True:
				pg = a // pp + 1
				if pp * (pg + 1 - 1) >= b: break
				pp = pp + 1 # TODO reverse order to prefer larger pages => fewer requests
				if pp > self.max_page: raise Exception ()
			return (a, b, pg, pp)
		"""
		def pgpp (a, b):                                    # pp = b - a + 1 + c, s.t.
			pp = b - a + 1                                  # (pg + 0) * pp <= a, b <= (pg + 1) * pp
			pp = max (pp, self.min_page)                    # pp in [3, 200]
			PP = pp
			pp = self.max_page
			while True:
				pg = a // pp + 1
				if pp * (pg + 1 - 1) >= b: break
				pp = pp - 1 # TODO reverse order to prefer larger pages => fewer requests
				if pp < PP: raise Exception ()
			return (a, b, pg, pp)
		
		reqs = []                                           # actual ranges to request
		if len (req_rng) != 0:
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
	def get_time      (self): return self.time
	def get_limit     (self): return self.limit
	def get_remaining (self): return self.remaining
	def get_reset     (self): return self.reset

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

from cache import memoized_key, memoized_cacher2

"""
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
"""
def pixabay_cacher (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None, session=None):
	nullify = (3, 4, 5,)
	ret = memoized_cacher2 (nullify, pixabay, key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page, session)
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
		#self.session = session
	def make_key (self, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None):
		qs  = tuple (qs)
		key = (qs, lang, orientation, category, min_width, min_height, colors, safesearch, order)
		return key

































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
	ret = memoized_cacher2 (nullify, pexels, key, queries, locale, page, per_page, session)
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
		
		
		
		
		
		
		
		
		
class Buffer:
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
class PixabayBuffer (Buffer):
	def __init__ (self, session=None, *args, **kwargs):
		results = PixabayResults (session, *args, **kwargs)
		Buffer.__init__ (self, results, *args, **kwargs)
class PexelsBuffer (Buffer):
	def __init__ (self, session=None, *args, **kwargs):
		results =  PexelsResults (session, *args, **kwargs)
		Buffer.__init__ (self, results, *args, **kwargs) 






		
		
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
		type1 = True
		layer = 1
		if layer == 0:
			if type1: r = PixabayResults ()
			else:     r = PexelsResults ()
		if layer == 1:
			s = requests.Session ()
			#s = None
			if type1: r = PixabayBuffer (s)
			else:     r = PexelsBuffer (s)
		
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
