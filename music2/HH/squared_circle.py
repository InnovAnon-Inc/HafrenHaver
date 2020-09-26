#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp
from rotation import STRAIGHT, ANGLED
	
from math import sqrt, pi
	
class SquaredCircle (SquareApp, CompositeApp):
	def __init__ (self, child, rotation=STRAIGHT, *args, **kwargs):
		SquareApp   .__init__ (self, rotation, *args, **kwargs)
		CompositeApp.__init__ (self, child,    *args, **kwargs)
		assert isinstance (child, CircleApp)
	def set_subsurface (self, ss):
		SquareApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		rect = self.bounds
		
		if self.rotation == STRAIGHT: pass
		if self.rotation == ANGLED:
			x, y, w, h = rect
			w2 = w / sqrt (2)
			h2 = h / sqrt (2)
			x, y = (w - w2) / 2, (h - h2) / 2
			rect = x, y, w2, h2
		
		ss2 = ss.subsurface (rect)
		self.inner_bounds = rect
		self.child.set_subsurface (ss2)
	def draw_cropped_scene (self, temp):
		SquareApp.draw_cropped_scene (self, temp)
		rect = self.bounds
		
		if self.rotation == STRAIGHT: pass
		if self.rotation == ANGLED:
			x, y, w, h = rect
			w2 = w / sqrt (2)
			h2 = h / sqrt (2)
			x, y = (w - w2) / 2, (h - h2) / 2
			rect = x, y, w2, h2
			
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)
	def minsz (self):
		if self.rotation == STRAIGHT: tmp = self.child.minsz ()
		if self.rotation == ANGLED:   tmp = self.child.minsz () * sqrt (2)
		tmp = max (tmp, SquareApp.minsz (self))
		return tmp
	def positive_area (self):
		x, y, w, h = self.bounds
		if self.rotation == STRAIGHT:
			w2, h2 = w, h
		if self.rotation == ANGLED:	
			w2 = w / sqrt (2)
			h2 = h / sqrt (2)
		a = pi * w2 / 2 * h2 / 2
		assert a >= 0
		return a
	def negative_area (self):
		x, y, w, h = self.bounds
		if self.rotation == STRAIGHT:
			w2, h2 = w, h
			a1 = w2 * h2
		if self.rotation == ANGLED:	
			w2 = w / sqrt (2)
			h2 = h / sqrt (2)
			a1 = w2 * h2 / 2
		assert a1 >= 0
		a2 = self.positive_area ()
		assert a2 >= 0
		a3 = abs (a1 - a2) # TODO wtf
		assert a3 >= 0, "na: %s, pa: %s" % (a1, a2)
		return a3
	def positive_space (self, is_root=True):
		a1 = CompositeApp.positive_space (self, is_root)
		assert a1 >= 0
		if not is_root: return a1
		a1 = a1 + SquareApp.positive_space (self, is_root)
		assert a1 >= 0
		return a1
	def negative_space (self, is_root=True):
		a1 = CompositeApp.negative_space (self, is_root)
		assert a1 >= 0
		if not is_root: return a1
		a1 = a1 + SquareApp.negative_space (self, is_root)
		assert a1 >= 0
		return a1

if __name__ == "__main__":
	from app import SECONDARY_BACKGROUND
	from gui import GUI
	from circled_square import CircledSquare
	
	def main ():
		h = CircleApp (background=SECONDARY_BACKGROUND)
		g = SquaredCircle (h)
		f = CircledSquare (g, background=SECONDARY_BACKGROUND)
		e = SquaredCircle (f, rotation=ANGLED)
		d = CircledSquare (e, background=SECONDARY_BACKGROUND)
		c = SquaredCircle (d)
		b = CircledSquare (c, background=SECONDARY_BACKGROUND)
		a = SquaredCircle (b, rotation=ANGLED)
		with GUI (app=a) as g:
			#g.setApp (a)
			print (a.positive_space ())
			print (a.negative_space ())
			g.run ()
	main ()
	quit ()
