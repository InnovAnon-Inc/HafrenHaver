#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp

from math import sqrt, pi

from rotation import STRAIGHT, ANGLED
from constants import ORIGIN

import pygame

class CircledSquare (CircleApp, CompositeApp):
	def __init__ (self, child, rotation=None, *args, **kwargs):
		CircleApp   .__init__ (self,        *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert child is None or isinstance (child, SquareApp)
		assert (child is None) != (rotation is None)
		if child is None: self.rotation = rotation
		else:             self.rotation = child.rotation
	def start_running (self):
		CircleApp   .start_running (self)
		CompositeApp.start_running (self)
	def  stop_running (self):
		CircleApp    .stop_running (self)
		CompositeApp .stop_running (self)
	def set_subsurface (self, ss):
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, None, True)
		"""
		ss = self.ss
		
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = ss.subsurface (rect)
		self.child.set_subsurface (ss2)
		"""
		"""
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
		"""
	def draw_cropped_scene (self, temp):
		CircleApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_cropped_scene (self, temp)
		"""
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
		"""
	"""
	def minsz (self):
		tmp = self.child.minsz () * sqrt (2)
		tmp = max (tmp, CircleApp.minsz (self))
		return tmp
	"""
	"""
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
	"""
	def positive_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def negative_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def minsz          (self):               return CompositeApp.minsz          (self)
	def outer_bounding_area (self): return CircleApp .outer_area (self) # area of bounding box
	def outer_area          (self): return CircleApp .inner_area (self) # area of circle
	def inner_bounding_area (self):
		x, y, w, h = self.inner_rect ()
		return w * h
		return self.child.outer_area ()     # area of bounding box
	def inner_area          (self):
		x, y, w, h = self.inner_rect ()
		if self.child.rotation == STRAIGHT: return w * h
		assert self.child.rotation == ANGLED
		return w * h / 2
		return self.child.inner_area ()     # area of square/diamond
	def inner_rect (self):
		o, (w2, h2) = self.bounds
		if self.rotation == STRAIGHT:
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			x, y = w2 - w, h2 - h
		if self.rotation == ANGLED:
			(x, y), (w, h) = self.bounds		
		rect = (x, y, w * 2, h * 2)
		return rect
		return self.child.outer_rect ()
	
if __name__ == "__main__":
	from constants import SECONDARY_BACKGROUND
	from gui import GUI
	from squared_circle import SquaredCircle
	def main ():
		if False:
			h = SquareApp (rotation=ANGLED, background=SECONDARY_BACKGROUND)
			g = CircledSquare (h)
			f = SquaredCircle (g, background=SECONDARY_BACKGROUND)
			e = CircledSquare (f)
			d = SquaredCircle (e, rotation=ANGLED, background=SECONDARY_BACKGROUND)
			c = CircledSquare (d)
		else: c = None
		b = SquaredCircle (c, background=SECONDARY_BACKGROUND)
		a = CircledSquare (b)
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
