#! /usr/bin/env python3

from app import App
from angle_app import tr
from cropping_app import CroppingApp, OPAQUE

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
		self.bounds_exact = self.ss.get_rect ()
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
		if self.rotation == STRAIGHT: return 2 * CroppingApp.minsz (self)
		if self.rotation == ANGLED:   return 3 * CroppingApp.minsz (self)
	def positive_space (self, is_root=True):
		x, y, w, h = self.bounds
		if self.rotation == STRAIGHT: a = w * h
		if self.rotation == ANGLED:   a = w * h / 2
		assert a >= 0
		return a
	def negative_space (self, is_root=True):
		if not is_root: return 0
		x, y, w, h = self.bounds
		if self.rotation == STRAIGHT: return 0 # TODO 1 ?
		if self.rotation == ANGLED:
			wh = w * h
			a1 = wh
			assert a1 >= 0
			a2 = wh / 2
			assert a2 >= 0
			a3 = a1 - a2
			assert a3 >= 0
			return a3
			

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = SquareApp (ANGLED)
		with GUI (app=a) as g:
			#g.setApp (a)
			print (a.positive_space ())
			print (a.negative_space ())
			g.run ()
	main ()
	quit ()
