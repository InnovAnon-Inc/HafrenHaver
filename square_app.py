#! /usr/bin/env python3

from app import App
from geometry import tr
from cropping_app import CroppingApp
from constants import OPAQUE

from rotation import STRAIGHT, ANGLED

import pygame
import pygame.gfxdraw

class SquareApp (CroppingApp):
	def __init__ (self, rotation=STRAIGHT, parent_is_square=True, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.rotation = rotation
		self.parent_is_square = parent_is_square
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		self.bounds_exact = self.get_rect ()
		self.bounds       = self.bounds_exact
	def crop (self):
		if self.rotation == STRAIGHT:
			pygame.gfxdraw.rectangle (self.cropped_background, self.bounds, OPAQUE)
			pygame.gfxdraw.box       (self.cropped_background, self.bounds, OPAQUE)
		if self.rotation == ANGLED:
			x, y, w, h = self.bounds
			if True:
				a = 0    , h / 2
				b = w / 2, 0
				c = w    , h / 2
				d = w / 2, h
			else:
				a = 0, 0
				b = w, 0
				c = w, h
				d = 0, h
			#pts = map (tr, (a, b, c, d))
			#pts = tuple (pts)
			pts = (a, b, c, d)
			pygame.gfxdraw.     aapolygon (self.cropped_background, pts, OPAQUE)
			pygame.gfxdraw.filled_polygon (self.cropped_background, pts, OPAQUE)
			
	def minsz (self):
		w, h = CroppingApp.minsz (self)
		if self.rotation == STRAIGHT: r = 2
		if self.rotation == ANGLED:   r = 3
		return w * r, h * h
	def outer_area (self):
		x, y, w, h = self.bounds
		return w * h
	def inner_area (self):
		x, y, w, h = self.bounds
		if self.rotation == STRAIGHT: a = w * h
		if self.rotation == ANGLED:   a = w * h / 2
		assert a >= 0
		return a
	def inner_rect (self): return self.get_outer_rect ()

if __name__ == "__main__":
	from gui import GUI
	from rotation import Rotation
	
	def main ():
		for rotation in Rotation:
			a = SquareApp (rotation)
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
