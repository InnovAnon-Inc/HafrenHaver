#! /usr/bin/env python3

import pygame

from hilbertcurve.hilbertcurve import HilbertCurve
from itertools import starmap
from itertools import permutations
from bjorklund import bjorklund
from square_app import SquareApp
from rotation import STRAIGHT

from lc import f2lc, lc2str

from constants import OPAQUE, ORIGIN

# TODO matrix text
def hilbjork (p, N, k, rev=False, rot=0): # p := #iteration, N := #dim, pts := useable space, k:= #pulse
	sl  = pow ( 2, p)                                                   # side length of hypercube
	sl  = int (sl)
	#npt = pow (sl, N)                                                   # number of points on hypercube
	#npt = int (npt)
	#assert npt == pow (2, N * p)
	npt = pow (2, N * p)
	npt = int (npt)
	sr  = range (0, sl)                                                 # range to iterate points in a line
	pts = permutations (sr, N)                                          # all points contained by hypercube
	pts = tuple (pts)
	#print ("pts: %s" % (pts,))
	
	hb  = HilbertCurve (p, N)                                           # map from 2-space to 1-space
	ds  = map (hb.distance_from_coordinates, pts)                       # get distances
	
	bj  = bjorklund (npt, k)                                            # evenly distribute ornaments along space-filling curve
	if rev: bj = bj[::-1]
	bj = bj[rot:] + bj[:rot]
	ds  = zip (bj, ds)
	f   = lambda t: t[0]
	ds  = filter (f, ds)                                                # sift out distances not selected by bjorklund's
	f   = lambda bj, ds: ds
	ds  = starmap (f, ds)                                               # remove bjorklund information
	
	pts = map (hb.coordinates_from_distance, ds)                        # map from 1-space to 2-space
	f   = lambda pt: tuple (pt)
	pts = map (f, pts)
	pts = tuple (pts)
	#print ("pts: %s" % (pts,))
	return pts
	
from random_util import relative_primes
from random import choice
from itertools import chain

"""
for p in range (1, 5):
	N   = 2
	npt = pow (2, N * p)
	npt = int (npt)
	ks  = relative_primes (npt)
	ks  = tuple (ks)
	k   = choice (ks)
	print (tuple (hilbjork (p, N, k)))
	"""
	
def fuck (p, N, ct, ks):
	ct = ct[::-1]
	k0 = zip ([False] * len (ks), ks)
	k1 = zip ([True]  * len (ks),  ks[::-1])
	k  = chain (k0, k1)
	k = zip (k, cycle (ct))
	for k, ct in k:
		rev, k = k
		print ("k: %s, rev: %s, ct: %s" % (k, rev, ct))
		yield hilbjork (p, N, k, rev, ct)
	"""	
	
	f = lambda k: hilbjork (p, N, k, False, ct)
	k0 = map (f, ks)
	f = lambda k: hilbjork (p, N, k, True,  ct)
	k1 = map (f, ks[::-1])
	f = lambda k: len (k) != 0
	k = chain (k0, k1)
	k = filter (f, k)
	return k
	"""
	
from math import log, floor
from itertools import cycle
class HilbjorkSquare (SquareApp):
	def __init__ (self, text=None, font=None ,*args, **kwargs):
		SquareApp.__init__ (self, *args, **kwargs)
		self.cs = True
		
		if text is None:
			# if child is none, use own source (get subtype source), else query child for model source, else use child source
			text = f2lc   (HilbjorkSquare)
			text = lc2str (text)
		self.text = text
		
		self.font = font
		
		self.a = None
		self.b = None
		self.n = None
		
	def set_subsurface (self, ss):
		SquareApp.set_subsurface (self, ss)
		self.cs = True
		#self.compute_sizes ()
		if self.font is None:
			df        = pygame.font.get_default_font ()
			font      = pygame.font.Font (df, 8)
			self.font = font
		texts, tw, th, x, y, w, h, p, N, ks = self.compute_sizes ()
		# TODO handle change in sizes
		self.texts    = texts
		self.tw       = tw
		self.th       = th
		self.x        = x
		self.y        = y
		self.w        = w
		self.h        = h
		self.p        = p
		self.N        = N
		self.ks       = ks
		self.next_cycle ()
		#self.next_screen ()
	
	
	def compute_sizes (self):
		text = self.text
		print ("text: %s" % (text,))
		N = len (text)
		print ("N: %s" % (N,))
		font = self.font
		
		crfg = (0, 255, 0, 255)
		f = lambda c: (font.render (c, True, crfg), *font.size (c))
		g = lambda c: str (c)
		texts = map (g, text)
		texts = map (f, texts)
		texts = tuple (texts) # image, w, h

		f = lambda iwh: iwh[1] 
		tw = max (texts, key=f)[1]
		f = lambda iwh: iwh[2]
		th = max (texts, key=f)[2]
		print ("tw: %s, th: %s" % (tw, th))
		
		f = lambda i, w, h: i
		texts = starmap (f, texts)
		texts = tuple (texts)
		#print ("texts: %s" % (texts,))
		
		rect = self.inner_rect ()
		X, Y, W, H = rect
		print ("(x: %s, y: %s) (W: %s, H: %s)" % (X, Y, W, H))
		
		#x, y, w, h = X + tw / 2, Y + th / 2, W - tw, H - th

		x, y = X, Y
		w = h = min (W / tw, H / th)
		w, h = int (w), int (h)
		#w = h = 10
		
		#if w % N != 0: w = h = w - 1
		print ("w: %s, h: %s" % (w, h))
		
		N   = 2
		p   = log (w * h) / (N * log (2))
		p   = floor (p)
		print ("p: %s" % (p,))
		npt = pow (2, N * p)
		npt = int (npt)
		ks  = relative_primes (npt)
		ks  = tuple (ks)
			
			
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		#self.KS = ks
		#self.ki = 0
		ks = fuck (p, N, range (0, npt), ks)
		ks = cycle (ks)
		#ks = None
		
		
		
		
		"""
		rng = range (0, npt)
		g = lambda ct: fuck (p, N, ct, ks)
		KS = map (g, rng)	
		KS = chain (KS)
		"""
		
			
		#f = lambda k, ct: hilbjork (p, N, k, False, ct)
		#k0 = starmap (f, ks0)
		#f = lambda k, ct: hilbjork (p, N, k, True,  ct)
		#k1 = starmap (f, ks[::-1])
		
		#ks = chain (k0, k1)
		#ks = cycle (ks)
		#KS = cycle (KS)
		
		#g = lambda ct: f (ct)
		#ks = map (g, count)
		#ks = chain (ks)
		
		#ks  = tuple (ks)
		#ks  = ks[:-1] + ks[::-1]
		
		return texts, tw, th, x, y, w, h, p, N, ks
		
		
	def next_screen (self):
		p   = self.p
		N   = self.N
		ks  = self.ks
		#if not ks:
		#	self.ki = self.ki + 1
		#	ks = fuck (p, N, self.ki, self.KS)
		#	self.ks = ks
		#k   = next (ks)
		#pts = hilbjork (p, N, k)
		
		pts = next (ks)
		# TODO check whether has next
		# ks = fuck (p, N, self.ki, ks)
		# self.ki ++
		self.pts = pts
		
		self.texts = list (self.texts[1:]) + list ([self.texts[0]])
		
		
		
	def next_cycle (self):
		w = self.w
		h = self.h
		"""
		N   = 2
		
		p   = log (w * h) / (N * log (2))
		p   = floor (p)
		print ("p: %s" % (p,))
		npt = pow (2, N * p)
		npt = int (npt)
		ks  = relative_primes (npt)
		ks  = tuple (ks)
		ks  = ks[:-1] + ks[::-1]
		ks  = cycle (ks)
		#ks  = iter (ks)
		"""
		#self.x   = x
		#self.y   = y
		#self.w   = W
		#self.h   = H
		self.cs  = False
		"""
		self.N   = N
		self.p   = p
		self.npt = npt
		self.ks  = ks
		"""
		self.next_screen ()
	def draw_foreground (self, temp):
		SquareApp.draw_foreground (self, temp)
		rect   = temp.get_rect ()
		x, y, W, H = rect
		assert self.x == x
		assert self.y == y
		
		tw, th = self.tw, self.th
		#assert self.w == W / self.tw
		#assert self.h == H / self.th
		#print ("(x: %s, y: %s) (W: %s, H: %s)" % (x, y, W, H))
		#w = h = min (W / 2, H / 2)
		#w = h = 10
		
		#N   = 2
		#if w % N != 0: w = h = w - 1
		#print ("w: %s, h: %s" % (w, h))
		
		#p   = log (w * h) / (N * log (2))
		#p   = floor (p)
		#print ("p: %s" % (p,))
		#npt = pow (2, N * p)
		#npt = int (npt)
		#ks  = relative_primes (npt)
		#ks  = tuple (ks)
		#k   = choice (ks)
		#pts = hilbjork (p, N, k)
		#print ("fuck: %s" % (pts,))
		##pts = tr (pts)
		
		p = self.p
		sl  = pow ( 2, p)
		sl  = int (sl)
		pts = self.pts
		
		#intermediate_alpha_surface = pygame.Surface ((W, H), flags=pygame.SRCALPHA)
		#intermediate_alpha_surface.fill (pygame.Color (*OPAQUE))
		
		texts = []
		w, h = self.w, self.h
		while len (texts) < w * h: texts = texts + list (self.texts)
		
		color  = (0, 0, 255)
		for pt in pts:
			#print ("pt: %s" % (pt,))
			x, y = pt
			i = y * w + x
			x = round (x * W / sl)
			y = round (H - y * H / sl)
			#print ("i: %s" % (i,))
			i = int (i)
			text = texts[i]
			#text, tww, thh = text
			#print ("text: %s" % (text,))
			#pt = x, y	
			#print ("pt: %s" % (pt,))
			#pygame.gfxdraw.pixel (temp, *pt, color)
			text_rect = text.get_rect ()
			text_rect.center = (x + tw / 2, y + th / 2)
			#intermediate_alpha_surface.blit (text, text_rect)
			temp.blit (text, text_rect)
			
		#temp.blit (intermediate_alpha_surface, ORIGIN, special_flags=pygame.BLEND_RGBA_MIN)
		self.next_screen ()

if __name__ == "__main__":
	from random import randrange
	#from gui import GUI
	from hal import HAL9000
	
	p   = 3
	N   = 2
	npt = pow (2, N * p)
	npt = int (npt)
	ks = relative_primes (npt)
	ks = tuple (ks)
	
	#rng = range (0, 3)
	#g = lambda ct: fuck (p, N, ct, ks)
	#KS = map (g, rng)	
	#KS = chain (KS)
	#KS = chain (*KS)
	
	#print ("fuck: %s" % list (KS))
	
	def main ():
		a = HilbjorkSquare ()
		with HAL9000 (app=a, exit_on_close=False) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
