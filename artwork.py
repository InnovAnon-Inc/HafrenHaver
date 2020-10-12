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
	url  = 'https://pixabay.com/api/'
	key  = memoized_key (use_api)
	q    = '+'.join (qs)
	lang = 'en'
	orientation = 'horizontal' # 'vertical'
	# category
	# min_width, min_height
	# colors
	# safesearch
	# order
	# page
	# per_page
	

if __name__ == "__main__":
	def main ():
		# TODO
	main ()
	quit ()
