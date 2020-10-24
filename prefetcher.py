#! /usr/bin/env python3

from queue import Queue, Empty

class PrefetcherInner:                          # prefetches a result set
	def __init__ (self, res):
		self.res        = res                   # Buffer.req (**kwargs): results to prefetch
		self.is_running = True                  # whether there are more results to prefetch
		self.q          = Queue (10)            # buffer

	def req (self):                             # generator; yield results from buffer/queue
		#print ("prefetcher_inner.req ()")
		while self.is_running or not self.q.empty ():
			#print ("prefetcher_inner req loop: %s %s" % (self.is_running, self.q.qsize (),))
			#res = self.q.get (block=(self.is_running or not self.q.empty ()))
			#res = self.q.get ()
			while True:
				try:
					res = self.q.get_nowait ()
					break
				except Empty:
					if not self.is_running and self.q.empty ():
						#self.q.join ()
						return
					continue
			#if res is None: break
			#print ("res: %s" % (res,))
			assert res is not None
			assert len (res) != 0
			yield res
			#print ("prefetcher_inner req loop done")
		#print ("prefetcher_inner req done")
		#return
		#self.q.join ()
		#return
	
	def update (self):                          # prefetch if necessary
		#print ("prefetcher_inner.update ()")
		if not self.is_running: return         # no more results to prefetch
		if self.q.full ():      return          # enough results have been prefetched	
		#print ("prefetching next result")
		#res = next (self.res)
		#if res is not None: self.q.put (res)
		#else: self.is_running = False
		#return
		try:
			res = next (self.res)                   # prefetched result
			tmp = (res is not None)
			#print ("result prefetched: %s" % (res,))
		except StopIteration: tmp = False
		if tmp:
			#print ("result enqueued")
			self.q.put (res)
		else:
			#print ("result not enqueued")
			self.is_running = False # no more results to prefetch
		#print ("done prefetching")
		#return tmp
			
from threading import Thread, Lock

class Prefetcher:
	def __init__ (self, buf):
		self.buf = buf
		self.pis = []
		self.thr = Thread (target=self.run)
		self.l   = Lock ()
		
	def __enter__ (self):
		self.is_running = True
		self.thr.start ()
		return self
	def __exit__  (self, type, value, traceback):
		self.is_running = False
		# TODO set each pi to not running
		self.thr.join ()
		return False
		
	def req (self, **kwargs):
		#print ("prefetcher.req (%s)" % (kwargs,))
		res = self.buf.req (**kwargs)           # result set
		#print ("res: %s" % (res,))
		pi  = PrefetcherInner (res)             # prefetcher for result set
		#print ("pi: %s" % (pi,))
		pi.update ()                            # fetch first result in master thread so we don't have to wait in run()
		#print ("first result prefetched")
		self.l.acquire ()
		self.pis.append (pi)                    # update this result set last in run()
		#self.pis.sort ()
		self.l.release ()
		#print ("pi enqueued")
		#yield from pi.req ()                    # yield from prefetched results
		for k in pi.req ():
			assert k is not None
			assert len (k) != 0
			#print ("k: %s" % (k,))
			yield k
		#return pi.req ()
		self.l.acquire ()
		self.pis.remove (pi)
		self.l.release ()
		#print ("generator exhausted")
		#return
		#pi.q.join ()
		#print ("pi queue joined")
		# TODO lock
		#self.pis.remove (pi)                    # remove this exhausted result set
		# TODO unlock
		#print ("pi dequeued")
				
	def run (self):
		#print ("prefetcher.run ()")
		while self.is_running:
			#print ("prefetcher run loop")
			self.l.acquire ()
			pis = list (self.pis)
			self.l.release ()
			if not self.is_running: break
			#if pis.empty (): continue # TODO maybe sleep ?
			#print ("pis: %s" % (pis,))
			for pi in pis:
				if not self.is_running: break
				pi.update () # TODO rate-limit ?
			#print ("pis updated")
			if not self.is_running: break
			self.l.acquire ()
			#for pi in self.pis:                  # filter non-running
			#	if pi.is_running: continue
			#	if not pi.q.empty (): continue
			#	self.pis.remove (pi)
			self.pis.sort ()                    # sort by most empty buffer
			self.l.release ()
			#print ("pis re-sorted")
			##if len (pis) != 0: continue         # stop when all result sets are exhausted
			##self.is_running = False
			## TODO sleep until pis is non-empty
			
	def convert       (self, **kwargs): return self.buf.convert       (**kwargs)
	def get_time      (self):           return self.buf.get_time      ()
	def get_limit     (self):           return self.buf.get_limit     ()
	def get_remaining (self):           return self.buf.get_remaining ()
	def get_reset     (self):           return self.buf.get_reset     ()
from buf import PixabayBuffer

class PixabayPrefetcher (Prefetcher):
	def __init__ (self, session=None, *args, **kwargs):
		buf = PixabayBuffer (session,   *args, **kwargs)
		Prefetcher.__init__ (self, buf, *args, **kwargs)

from buf import PexelsBuffer

class PexelsPrefetcher (Prefetcher):
	def __init__ (self, session=None, *args, **kwargs):
		buf = PexelsBuffer  (session,   *args, **kwargs)
		Prefetcher.__init__ (self, buf, *args, **kwargs)
		
if __name__ == "__main__":
	import requests
	
	def main ():
		type1 = False
		with requests.Session () as s:
			if type1:
				with PixabayPrefetcher (s) as p:
					r  = p.req (qs=('test',))
					print ("r: %s" % (r,))
					print ()
					for h in r:
						print ("h: %s" % (h,))
						print ("time     : %s" % (p.get_time      (),))
						print ("limit    : %s" % (p.get_limit     (),))
						print ("remaining: %s" % (p.get_remaining (),))
						print ("reset    : %s" % (p.get_reset     (),))
						print ()
					
					#r  = p.req (qs=('test',))
					#print (len (tuple (r)))
					#
					#print ("time     : %s" % (p.get_time      (),))
					#print ("limit    : %s" % (p.get_limit     (),))
					#print ("remaining: %s" % (p.get_remaining (),))
					#print ("reset    : %s" % (p.get_reset     (),))
			else:
				with  PexelsPrefetcher (s) as p:
					r  = p.req (queries=('test',))
					print ("r: %s" % (r,))
					print ()
					for h in r:
						print ("h: %s" % (h,))
						print ("time     : %s" % (p.get_time      (),))
						print ("limit    : %s" % (p.get_limit     (),))
						print ("remaining: %s" % (p.get_remaining (),))
						print ("reset    : %s" % (p.get_reset     (),))
						print ()
					
					r  = p.req (queries=('test',))
					print (len (tuple (r)))
					
					print ("time     : %s" % (p.get_time      (),))
					print ("limit    : %s" % (p.get_limit     (),))
					print ("remaining: %s" % (p.get_remaining (),))
					print ("reset    : %s" % (p.get_reset     (),))
			#if type1: b = PixabayBuffer (s)
			#else:     b =  PexelsBuffer (s)
			#with Prefetcher (b) as p:
			#	if type1: r  = p.req (qs=('test',))
			#	else:     r  = p.req (queries=('test',))
			#	
			#	print ("r: %s" % (r,))
			#	print ()
			#	for h in r:
			#		print ("h: %s" % (h,))
			#		print ()
			#	
			#	if type1: r  = p.req (qs=('test',))
			#	else:     r  = p.req (queries=('test',))
			#	print (len (tuple (r)))
			#	
			#	print ("time     : %s" % (p.get_time      (),))
			#	print ("limit    : %s" % (p.get_limit     (),))
			#	print ("remaining: %s" % (p.get_remaining (),))
			#	print ("reset    : %s" % (p.get_reset     (),))
	main ()
	quit ()
