#! /usr/bin/env python3

import pygame

from hilbertcurve.hilbertcurve import HilbertCurve
from itertools import starmap
from itertools import permutations
from bjorklund import bjorklund
from square_app import SquareApp
from rotation import STRAIGHT

# TODO matrix text
def hilbjork (p, N, k): # p := #iteration, N := #dim, pts := useable space, k:= #pulse
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
	print ("pts: %s" % (pts,))
	
	hb  = HilbertCurve (p, N)                                           # map from 2-space to 1-space
	ds  = map (hb.distance_from_coordinates, pts)                       # get distances
	
	bj  = bjorklund (npt, k)                                            # evenly distribute ornaments along space-filling curve
	ds  = zip (bj, ds)
	f   = lambda t: t[0]
	ds  = filter (f, ds)                                                # sift out distances not selected by bjorklund's
	f   = lambda bj, ds: ds
	ds  = starmap (f, ds)                                               # remove bjorklund information
	
	pts = map (hb.coordinates_from_distance, ds)                        # map from 1-space to 2-space
	f   = lambda pt: tuple (pt)
	pts = map (f, pts)
	pts = tuple (pts)
	print ("pts: %s" % (pts,))
	return pts
	
from random_util import relative_primes
from random import choice

for p in range (1, 5):
	N   = 2
	npt = pow (2, N * p)
	npt = int (npt)
	ks  = relative_primes (npt)
	ks  = tuple (ks)
	k   = choice (ks)
	print (tuple (hilbjork (p, N, k)))
	
from math import log, floor
from itertools import cycle
class HilbjorkSquare (SquareApp):
	def __init__ (self, *args, **kwargs):
		SquareApp.__init__ (self, *args, **kwargs)
		self.cs = True
	def set_subsurface (self, ss):
		SquareApp.set_subsurface (self, ss)
		self.cs = True
		self.compute_sizes ()
	def next_screen (self):
		p   = self.p
		N   = self.N
		ks  = self.ks
		k   = next (ks)
		pts = hilbjork (p, N, k)
		self.pts = pts
	def compute_sizes (self):
		rect = self.inner_rect ()
		x, y, W, H = rect
		print ("(x: %s, y: %s) (W: %s, H: %s)" % (x, y, W, H))
		w = h = min (W / 2, H / 2)
		#w = h = 10
		
		N   = 2
		if w % N != 0: w = h = w - 1
		print ("w: %s, h: %s" % (w, h))
		
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
		
		self.x   = x
		self.y   = y
		self.w   = W
		self.h   = H
		self.cs  = False
		self.N   = N
		self.p   = p
		self.npt = npt
		self.ks  = ks
		self.next_screen ()
	def draw_foreground (self, temp):
		SquareApp.draw_foreground (self, temp)
		rect   = temp.get_rect ()
		x, y, W, H = rect
		assert self.x == x
		assert self.y == y
		assert self.w == W
		assert self.h == H
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
		
		color  = (0, 0, 255)
		for pt in pts:
			print ("pt: %s" % (pt,))
			x, y = pt
			x = round (x * W / sl)
			y = round (H - y * H / sl)
			pt = x, y
			print ("pt: %s" % (pt,))
			pygame.gfxdraw.pixel (temp, *pt, color)
		self.next_screen ()

if __name__ == "__main__":
	from random import randrange
	from gui import GUI
	
	def main ():
		a = HilbjorkSquare ()
		with GUI (app=a, exit_on_close=False) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
