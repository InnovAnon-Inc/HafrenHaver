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

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = SquareApp (ANGLED)
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
