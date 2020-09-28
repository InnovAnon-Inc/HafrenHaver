#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp
from constants import OPAQUE

import pygame
import pygame.gfxdraw

from math import pi

from geometry import tr

from constants import ORIGIN

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

	def minsz (self):
		w, h = CroppingApp.minsz (self)
		return pi * w, pi * h
	def outer_area (self): return CroppingApp.area (self)
	def inner_area (self):
		w, h = self.dims ()
		return pi * w / 2 * h / 2

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = CircleApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			print ("minsz: (%s, %s)" % a.minsz ())
			print ("outer: %s"       % a.outer_area ())
			print ("inner: %s"       % a.inner_area ())
			print ("pos  : %s"       % a.positive_space ())
			print ("neg  : %s"       % a.negative_space ())
			g.run ()
	main ()
	quit ()
