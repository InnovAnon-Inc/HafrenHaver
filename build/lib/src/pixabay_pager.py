#! /usr/bin/env python3
	
from pager import Pager
from pixabay_results import PixabayResults

class PixabayPager (Pager):
	def __init__ (self, session=None, *args, **kwargs):
		results = PixabayResults (session, *args, **kwargs)
		Pager.__init__ (self, results, *args, **kwargs)
	def req (self, **kwargs):
		rets    = Pager.req (self, **kwargs)
		for ret in rets:
			vtotal, vtotal_hits, res, vcreds = ret
			vcreds = set (vcreds)
			vcreds.add (res['user'])
			#res    = res['fullHDURL']
			res    = res['largeImageURL']
			ret    = vtotal, vtotal_hits, res, vcreds
			yield ret

if __name__ == "__main__":
	import requests
	
	def main ():
		type1 = True
		with requests.Session () as s:
			if type1: r = PixabayPager (s)
			else:     r =  PexelsPager (s)
		
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
