#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp

from math import sqrt

class CircledSquare (CircleApp, CompositeApp):
	def __init__ (self, child, *args, **kwargs):
		CircleApp   .__init__ (self,        *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert isinstance (child, SquareApp)
		#self.child = child
	def set_subsurface (self, ss):
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		#w2, h2 = self.bounds_exact     # both center and radius
		w2, h2 = self.bounds
		w = w2 / sqrt (2)
		h = h2 / sqrt (2)
		x, y = w2 - w, h2 - h
		rect = (x, y, w * 2, h * 2)
		ss2 = ss.subsurface (rect)
		#ss2.fill ((255, 255, 255))
		
		self.inner_bounds = rect
		
		#print ("test: %s %s %s" % (rect, (w2 * 2, h2 * 2), self.background))
		self.child.set_subsurface (ss2)
		
	def draw_cropped_scene (self, temp):
		CircleApp.draw_cropped_scene (self, temp)
		w2, h2 = self.bounds
		w = w2 / sqrt (2)
		h = h2 / sqrt (2)
		x, y = w2 - w, h2 - h
		rect = (x, y, w * 2, h * 2)
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)
	
if __name__ == "__main__":
	from app import SECONDARY_BACKGROUND
	from gui import GUI
	
	def main ():
		b = SquareApp (background=SECONDARY_BACKGROUND)
		a = CircledSquare (b)
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
