#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp, OPAQUE

import pygame
import pygame.gfxdraw




class CircleApp (CroppingApp):
	def __init__ (self, *args, **kwargs): CroppingApp.__init__ (self, *args, **kwargs)
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		w, h = self.ss.get_size ()
		w, h = w / 2, h / 2
		self.bounds_exact = w, h
		w, h = round (w), round (h)
		self.bounds       = w, h
	def crop (self):
		#w, h = self.ss.get_size ()
		#w, h = round (w / 2), round (h / 2)
		pygame.gfxdraw.     aaellipse (self.cropped_background, *self.bounds, *self.bounds, OPAQUE)
		pygame.gfxdraw.filled_ellipse (self.cropped_background, *self.bounds, *self.bounds, OPAQUE)
	# TODO minsz = pi ?

class SquareApp (CroppingApp):
	def __init__ (self, *args, **kwargs): CroppingApp.__init__ (self, *args, **kwargs)
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		self.bounds_exact = self.ss.get_rect ()
		self.bounds       = self.bounds_exact
	def crop (self):
		pygame.gfxdraw.rectangle (self.cropped_background, self.bounds, OPAQUE)
		pygame.gfxdraw.box       (self.cropped_background, self.bounds, OPAQUE)
	# TODO minsz = 2 ?

from enum import Enum
class Orientation (Enum):
	NORTH = 0
	EAST  = 1 # "est"
	SOUTH = 2
	WEST  = 3 # "weest"
NORTH = Orientation.NORTH
EAST  = Orientation.EAST
SOUTH = Orientation.SOUTH
WEST  = Orientation.WEST

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
		a = CircleApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
