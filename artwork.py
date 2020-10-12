#! /usr/bin/env python3

# map keywords => [(image, credits), ...]
# TODO how to decide when to pull more images

# db1[keywords] = [(image, credits), ...]

# db2[caller] = [keywords, ...]
# check whether caller has used these keywords
# if so, pull more images ?

# TODO
ARTWORK_CREDITS = ('https://pixabay.com',)

# 5,000 requests per hour
# X-RateLimit-Limit     The maximum number of requests that the consumer is permitted to make in 30 minutes.
# X-RateLimit-Remaining The number of requests remaining in the current rate limit window.
# X-RateLimit-Reset     The remaining time in seconds after which the current rate limit window resets.

# count distinct pairs of caller, keywords
# record time of last call to web service
# if sufficient time has passed, select a keyword pair

# don't update cache until result list is exhausted, account for artwork's timeout
class Results: # keyword => result list
	def __ init__ (self):
		pass


class Artwork: # keyword => result list => image
	def __init__ (self, results):
		self.results = results



		

		

# cache name: OnePunch


def use_api (qs=None, lang=None, orientation=None, category=None, min_width=None, min_height=None, colors=None, safesearch=None, order=None, page=None, per_page=None):
	key    = memoized_key (use_api)
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
	
	client = IARESTClient ('https', 'pixabay.com', 'api', params)
	r      = client.post ()
	
	
	

if __name__ == "__main__":
	def main ():
		# TODO
	main ()
	quit ()
