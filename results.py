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
			assert vcreds == c, "vcreds: %s, c: %s" % (vcreds, c)
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

if __name__ == "__main__":
	import requests
	
	def main ():
		# TODO
		pass
	main ()
	quit ()
