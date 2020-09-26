#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp

from math import sqrt

from rotation import STRAIGHT, ANGLED
from app import ORIGIN

class CircledSquare (CircleApp, CompositeApp):
	def __init__ (self, child, *args, **kwargs):
		CircleApp   .__init__ (self,        *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert isinstance (child, SquareApp)
		#self.child = child
		#self.child.parent_is_square = False
	def set_subsurface (self, ss):
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		#w2, h2 = self.bounds_exact     # both center and radius
		if self.child.rotation == STRAIGHT:
			w2, h2 = self.bounds
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			x, y = w2 - w, h2 - h
		if self.child.rotation == ANGLED:
			x, y = ORIGIN
			w, h = self.bounds
		rect = (x, y, w * 2, h * 2)
		ss2 = ss.subsurface (rect)
		#ss2.fill ((255, 255, 255))
		
		self.inner_bounds = rect
		
		#print ("test: %s %s %s" % (rect, (w2 * 2, h2 * 2), self.background))
		self.child.set_subsurface (ss2)
		
	def draw_cropped_scene (self, temp):
		CircleApp.draw_cropped_scene (self, temp)
		w2, h2 = self.bounds
		if self.child.rotation == STRAIGHT:
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			x, y = w2 - w, h2 - h
		if self.child.rotation == ANGLED:
			x, y = ORIGIN
			w, h = self.bounds		
		rect = (x, y, w * 2, h * 2)
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)

	def minsz (self):
		tmp = self.child.minsz () * sqrt (2)
		tmp = max (tmp, CircleApp.minsz (self))
		return tmp
	
if __name__ == "__main__":
	from app import SECONDARY_BACKGROUND
	from gui import GUI
	from squared_circle import SquaredCircle
	def main ():
		h = SquareApp (rotation=ANGLED, background=SECONDARY_BACKGROUND)
		g = CircledSquare (h)
		f = SquaredCircle (g, background=SECONDARY_BACKGROUND)
		e = CircledSquare (f)
		d = SquaredCircle (e, rotation=ANGLED, background=SECONDARY_BACKGROUND)
		c = CircledSquare (d)
		b = SquaredCircle (c, background=SECONDARY_BACKGROUND)
		a = CircledSquare (b)
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
