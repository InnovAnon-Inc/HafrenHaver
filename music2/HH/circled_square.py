#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp

from math import sqrt, pi

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
			o, (w2, h2) = self.bounds
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			x, y = w2 - w, h2 - h
		if self.child.rotation == ANGLED:
			(x, y), (w, h) = self.bounds
		rect = (x, y, w * 2, h * 2)
		ss2 = ss.subsurface (rect)
		#ss2.fill ((255, 255, 255))
		
		self.inner_bounds = rect
		
		#print ("test: %s %s %s" % (rect, (w2 * 2, h2 * 2), self.background))
		self.child.set_subsurface (ss2)
		
	def draw_cropped_scene (self, temp):
		CircleApp.draw_cropped_scene (self, temp)
		o, (w2, h2) = self.bounds
		if self.child.rotation == STRAIGHT:
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			x, y = w2 - w, h2 - h
		if self.child.rotation == ANGLED:
			(x, y), (w, h) = self.bounds		
		rect = (x, y, w * 2, h * 2)
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)

	def minsz (self):
		tmp = self.child.minsz () * sqrt (2)
		tmp = max (tmp, CircleApp.minsz (self))
		return tmp
		
	def positive_area (self):
		o, (w2, h2) = self.bounds		
		if self.child.rotation == STRAIGHT: # positive space of square
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			a1 = w * h
		if self.child.rotation == ANGLED: # positive space of diamond
			w, h = w2, h2
			a1 = w * h * 2
		assert a1 >= 0
		return a1
	def negative_area (self):
		o, (w2, h2) = self.bounds
		if self.child.rotation == STRAIGHT: # positive space of square
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			a1 = w * h * 2
		if self.child.rotation == ANGLED: # positive space of diamond
			w, h = w2, h2
			a1 = w * h		
		assert a1 >= 0
		a2 = w2 * h2 * 4 # negative space
		assert a2 >= 0
		a3 = a2 - self.positive_area ()
		assert a3 >= 0
		return a3
	def positive_space (self, is_root=True):
		a1 = CompositeApp.positive_space (self, is_root)
		assert a1 >= 0
		if not is_root: return a1
		a1 = a1 + CircleApp.positive_space (self, is_root)
		assert a1 >= 0
		return a1
	def negative_space (self, is_root=True):
		a1 = CompositeApp.negative_space (self, is_root)
		assert a1 >= 0
		if not is_root: return a1
		a1 = a1 + CircleApp.negative_space (self, is_root) 
		assert a1 >= 0
		return a1
	
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
			print (a.positive_space ())
			print (a.negative_space ())
			g.run ()
	main ()
	quit ()
