#! /usr/bin/env python3

import os
from pathlib import Path
import requests
import shutil

def download_file (url, session=requests): # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    assert url
    index = -1
    while True:
        local_filename = url.split ('/')[index] # TODO use entire url for filename
        if local_filename: break
        index = index - 1
    assert local_filename, "url: %s" % (url,)
    newdir         = "cache"                                            # create directory for cached images
    p              = Path (newdir)
    if not p.is_dir (): os.makedirs (newdir, 0o0777)
    local_filename = "%s/%s" % (newdir, local_filename,)                # put file in directory
    p              = Path (local_filename)
    if p.is_file (): return local_filename, None, None, None            # don't redownload
    
    with session.get (url, stream=True) as r:
        h     = r.headers
        lim   = h.get ('X-RateLimit-Limit')
        rem   = h.get ('X-RateLimit-Remaining')
        reset = h.get ('X-RateLimit-Reset')
        with open (local_filename, 'wb') as f: shutil.copyfileobj (r.raw, f)

    # TODO validate downloaded file
	
    return local_filename, lim, rem, reset
    
class Buffer: # fetch / prefetch results
	def __init__ (self, pager): self.pager = pager
	def req (self, **kwargs):
		pager = self.pager
		rets  = pager.req (**kwargs)
		# TODO might need to lock session
		# TODO prefetch first result in bg thread
		for ret in rets:
			# TODO join bg thread
			# TODO prefetch next result in bg thread
			vtotal, vtotal_hits, res, vcreds = ret
			# TODO fetch results: get session from pager's results... need to store session there
			session = self.pager.results.get_session ()
			res = download_file (res, session)
			res, limit, remaining, reset = res
			if limit     is not None: self.pager.results.limit     = limit
			if remaining is not None: self.pager.results.remaining = remaining
			if reset     is not None: self.pager.results.reset     = reset
			#print ("limit: %s, remaining: %s, reset: %s" % (limit, remaining, reset))
			ret = vtotal, vtotal_hits, res, vcreds
			yield ret
	def get_time      (self): return self.pager.get_time      ()
	def get_limit     (self): return self.pager.get_limit     ()
	def get_remaining (self): return self.pager.get_remaining ()
	def get_reset     (self): return self.pager.get_reset     ()
    
from pixabay_pager import PixabayPager

class PixabayBuffer (Buffer):
	def __init__ (self, session=None, *args, **kwargs):
		pager = PixabayPager (session)
		Buffer.__init__ (self, pager, *args, **kwargs)
	def convert (self, **kwargs):
		queries = kwargs.get ('queries')
		del kwargs['queries']
		kwargs['qs'] = queries
		return kwargs
		
from  pexels_pager import  PexelsPager

class PexelsBuffer (Buffer):
	def __init__ (self, session=None, *args, **kwargs):
		pager = PexelsPager (session)
		Buffer.__init__ (self, pager, *args, **kwargs)
	def convert (self, **kwargs):
		locale = kwargs.get ('lang')
		del kwargs['lang']
		kwargs['locale'] = locale
		return kwargs
		
if __name__ == "__main__":
	import requests
	
	def main ():
		type1 = False
		with requests.Session () as s:
			if type1: r = PixabayBuffer (s)
			else:     r =  PexelsBuffer (s)
			
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
