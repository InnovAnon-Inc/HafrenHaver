#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp, OPAQUE

import pygame
import pygame.gfxdraw

from math import pi

from angle_app import tr

class CircleApp (CroppingApp):
	def __init__ (self, *args, **kwargs): CroppingApp.__init__ (self, *args, **kwargs)
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		w, h = self.ss.get_size ()
		w, h = w / 2, h / 2
		self.bounds_exact = w, h
		#w, h = round (w), round (h)
		self.bounds       = w, h
	def crop (self):
		#w, h = self.ss.get_size ()
		#w, h = round (w / 2), round (h / 2)
		bounds = tr (self.bounds)
		pygame.gfxdraw.     aaellipse (self.cropped_background, *bounds, *bounds, OPAQUE)
		pygame.gfxdraw.filled_ellipse (self.cropped_background, *bounds, *bounds, OPAQUE)
	def minsz (self): return pi * CroppingApp.minsz (self)

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = CircleApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
