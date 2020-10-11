#! /usr/bin/env python3

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
class Results: # keyword => result list
	def __ init__ (self):
		pass


class Artwork: # keyword => result list => image
	def __init__ (self, results):
		self.results = results

if __name__ == "__main__":
	def main ():
		# TODO
	main ()
	quit ()
