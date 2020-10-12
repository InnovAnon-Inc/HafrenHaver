#! /usr/bin/env python3

# map keywords => [(image, credits), ...]
# TODO how to decide when to pull more images

# db1[keywords] = [(image, credits), ...]

# db2[caller] = [keywords, ...]
# check whether caller has used these keywords
# if so, pull more images ?

# TODO
ARTWORK_CREDITS = ('https://pixabay.com',)


# count distinct pairs of caller, keywords
# record time of last call to web service
# if sufficient time has passed, select a keyword pair

# don't update cache until result list is exhausted, account for artwork's timeout
class Results: # keyword => result list
	def __init__ (self):
		pass


class Artwork: # keyword => result list => image
	def __init__ (self, results):
		self.results = results



		

		

# cache name: OnePunch


from rest import RESTParam, RESTParamList, RESTParamQuery, IAHeaderRESTClient

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
	r, lim, rem, reset = client.get ()
	
	#r = r[0] # most accurate
	#print ("r: %s" % (r,))
	#elevation = r['elevation']
	#print ("elevation: %s" % (elevation,))
	return r, lim, rem, reset, client.cred

from cache import memoized_key

def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
	
"""
def pixabay_cacher (key, qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	ret = memoized_cacher (pixabay, key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)
	ret, cred = ret
	#ret = float (ret)
	return ret, cred
def pixabay2 (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key = memoized_key (pixabay)
	return pixabay_cacher (key, qs, lang, orientation, category, min_width, min_height, colors, safesearch, order, page, per_page)	
"""	

if __name__ == "__main__":
	def main ():
		print (pixabay2 ())
	main ()
	quit ()
