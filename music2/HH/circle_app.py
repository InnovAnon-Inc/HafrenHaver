#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp, OPAQUE

import pygame
import pygame.gfxdraw

from math import pi

from angle_app import tr

from app import ORIGIN

class CircleApp (CroppingApp):
	def __init__ (self, *args, **kwargs): CroppingApp.__init__ (self, *args, **kwargs)
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		w, h = self.ss.get_size ()
		w, h = w / 2, h / 2
		#self.bounds_exact = w, h
		#w, h = round (w), round (h)
		self.bounds       = ORIGIN, (w, h)
	def crop (self):
		#w, h = self.ss.get_size ()
		#w, h = round (w / 2), round (h / 2)
		o, bounds = self.bounds
		bounds = tr (bounds)
		pygame.gfxdraw.     aaellipse (self.cropped_background, *bounds, *bounds, OPAQUE)
		pygame.gfxdraw.filled_ellipse (self.cropped_background, *bounds, *bounds, OPAQUE)
	def minsz (self): return pi * CroppingApp.minsz (self)
	def positive_space (self, is_root=True):
		w, h = self.ss.get_size ()
		w, h = w / 2, h / 2
		a = pi * w * h
		assert a >= 0
		return a
	def negative_space (self, is_root=True):
		if not is_root: return 0
		w,  h  = self.ss.get_size ()
		w2, h2 = w / 2, h / 2
		a1 = w * h
		assert a1 >= 0
		a2 = pi * w2 * h2
		assert a2 >= 0
		a3 = a1 - a2
		assert a3 >= 0
		return a3

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = CircleApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			print (a.positive_space ())
			print (a.negative_space ())
			g.run ()
	main ()
	quit ()
