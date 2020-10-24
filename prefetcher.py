#! /usr/bin/env python3

from queue import Queue

class PrefetcherInner:                          # prefetches a result set
	def __init__ (self, res):
		self.res        = res                   # Buffer.req (**kwargs): results to prefetch
		self.is_running = True                  # whether there are more results to prefetch
		self.q          = Queue (10)            # buffer

	def req (self):                             # generator; yield results from buffer/queue
		print ("prefetcher_inner.req ()")
		while self.is_running or not self.q.empty ():
			res = self.q.get ()
			print ("res: %s" % (res,))
			yield res
		self.q.join ()
	
	def update (self):                          # prefetch if necessary
		print ("prefetcher_inner.update ()")
		if not self.is_running: return          # no more results to prefetch
		if self.q.full ():      return          # enough results have been prefetched	
		print ("prefetching next result")
		res = next (self.res)                   # prefetched result
		print ("result prefetched")
		if res is None: self.is_running = False # no more results to prefetch
		else:           self.q.put (res)
		print ("done prefetching")
			
from threading import Thread

class Prefetcher:
	def __init__ (self, buf):
		self.buf = buf
		self.pis = []
		self.thr = Thread (target=self.run)
		#self.is_running = False
		
	def __enter__ (self):
		self.is_running = True
		self.thr.start ()
		return self
	def __exit__  (self, type, value, traceback):
		self.is_running = False
		self.thr.join ()
		return False
		
	def req (self, **kwargs):
		print ("prefetcher.req (%s)" % (kwargs,))
		res = self.buf.req (**kwargs)           # result set
		print ("res: %s" % (res,))
		pi  = PrefetcherInner (res)             # prefetcher for result set
		print ("pi: %s" % (pi,))
		pi.update ()                            # fetch first result in master thread so we don't have to wait in run()
		print ("first result prefetched")
		# TODO lock
		self.pis.append (pi)                    # update this result set last in run()
		#self.pis.sort ()
		# TODO unlock
		print ("pi enqueued")
		yield from pi.req ()                    # yield from prefetched results
		print ("generator exhausted")
		#pi.q.join ()
		#print ("pi queue joined")
		# TODO lock
		#self.pis.remove (pi)                    # remove this exhausted result set
		# TODO unlock
		#print ("pi dequeued")
				
	def run (self):
		print ("prefetcher.run ()")
		while self.is_running:
			print ("prefetcher run loop")
			# TODO lock
			pis = list (self.pis)
			# TODO unlock
			print ("pis: %s" % (pis,))
			for pi in pis: pi.update ()
			print ("pis updated")
			# TODO lock
			# TODO remove exhausted result sets
			self.pis.sort ()                    # sort by most empty buffer
			# TODO unlock
			print ("pis re-sorted")
			#if len (pis) != 0: continue         # stop when all result sets are exhausted
			#self.is_running = False
			# TODO sleep until pis is non-empty
			
from buf import PixabayBuffer, PexelsBuffer

if __name__ == "__main__":
	import requests
	
	def main ():
		type1 = True
		with requests.Session () as s:
			if type1: b = PixabayBuffer (s)
			else:     b =  PexelsBuffer (s)
			with Prefetcher (b) as p:
				r  = p.req (qs=('test',))
				
				print ("r: %s" % (r,))
				print ()
				for h in r:
					print ("h: %s" % (h,))
					print ()
				
				r  = p.req (qs=('test',))
				print (len (tuple (r)))
				
				print ("time     : %s" % (p.get_time      (),))
				print ("limit    : %s" % (p.get_limit     (),))
				print ("remaining: %s" % (p.get_remaining (),))
				print ("reset    : %s" % (p.get_reset     (),))
	main ()
	quit ()
