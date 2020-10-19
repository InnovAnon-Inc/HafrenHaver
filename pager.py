#! /usr/bin/env python3
		
class Pager: # iterate results / pages
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
	
if __name__ == "__main__":
	import requests
	
	def main ():
		# TODO
		pass
	main ()
	quit ()
