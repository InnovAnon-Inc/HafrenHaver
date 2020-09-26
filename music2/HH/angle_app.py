#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp, OPAQUE

import pygame
import pygame.gfxdraw

from orientation import NORTH, EAST, SOUTH, WEST

def tr (t): return tuple (map (lambda x: round (x), t))

class AngleApp (CroppingApp):
	def __init__ (self, orientation=NORTH, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.orientation = orientation
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		size = self.ss.get_size()
		w, h = size
		orientation = self.orientation
		if orientation == NORTH:
			x = 0, h
			y = w / 2, 0
			z = w, h
			self.bounds_exact = x, y,      z
			self.bounds       = x, tr (y), z
		if orientation == SOUTH:
			x = 0, 0
			y = w / 2, h
			z = w, 0
			self.bounds_exact = x, y,      z
			self.bounds       = x, tr (y), z
		if orientation == EAST:
			x = 0, 0
			y = w, h / 2
			z = 0, h
			self.bounds_exact = x, y,      z
			self.bounds       = x, tr (y), z
		if orientation == WEST:
			x = 0, h / 2
			y = w, 0
			z = w, h
			self.bounds_exact = x,      y, z
			self.bounds       = tr (x), y, z
	def crop (self):
		x, y, z = self.bounds
		pygame.gfxdraw.     aatrigon (self.cropped_background, *x, *y, *z, OPAQUE)
		pygame.gfxdraw.filled_trigon (self.cropped_background, *x, *y, *z, OPAQUE)

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = AngleApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
