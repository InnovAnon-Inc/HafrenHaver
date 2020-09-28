#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp
from rotation import STRAIGHT, ANGLED
	
from math import sqrt, pi
import pygame

class SquaredCircle (SquareApp, CompositeApp):
	def __init__ (self, child, rotation=STRAIGHT, *args, **kwargs):
		SquareApp   .__init__ (self, rotation, *args, **kwargs)
		CompositeApp.__init__ (self, child,    *args, **kwargs)
		assert child is None or isinstance (child, CircleApp)
	def start_running (self):
		SquareApp   .start_running (self)
		CompositeApp.start_running (self)
	def  stop_running (self):
		SquareApp    .stop_running (self)
		CompositeApp .stop_running (self)
	
	def set_subsurface (self, ss):
		SquareApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, None, True)
	"""
		ss = self.ss
		
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = ss.subsurface (rect)
		self.child.set_subsurface (ss2)
	"""
	def draw_cropped_scene (self, temp):
		SquareApp.draw_cropped_scene (self, temp)
		#rect = self.bounds
		
		#if self.rotation == STRAIGHT: pass
		#if self.rotation == ANGLED:
		#	x, y, w, h = rect
		#	w2 = w / sqrt (2)
		#	h2 = h / sqrt (2)
		#	x, y = (w - w2) / 2, (h - h2) / 2
		#	rect = x, y, w2, h2
		
		CompositeApp.draw_cropped_scene (self, temp)
			
		#ss2 = temp.subsurface (rect)
		#self.child.set_subsurface (ss2)
		##self.child.draw_cropped_scene (ss2)
		#self.child.draw_scene (ss2)
		
	def positive_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def negative_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def minsz          (self):               return CompositeApp.minsz          (self)
	def outer_bounding_area (self): return SquareApp .outer_area (self) # area of bounding box
	def outer_area          (self): return SquareApp .inner_area (self) # area of square/diamond
	def inner_bounding_area (self):
		x, y, w, h = self.inner_rect ()
		if self.rotation == STRAIGHT: return w * h
		assert self.rotation == ANGLED
		return w * h / 2
		return self.child.outer_area ()     # area of bounding box
	def inner_area          (self):
		x, y, w, h = self.inner_rect ()
		w2, h2 = w / 2, h / 2
		ret = pi * w2 * h2
		return ret
		return self.child.inner_area ()     # area of circle
	def inner_rect (self):
		rect = self.outer_rect ()
		if self.rotation == STRAIGHT: return rect
		assert self.rotation == ANGLED
		x, y, w, h = rect
		w2 = w / sqrt (2)
		h2 = h / sqrt (2)
		x, y = (w - w2) / 2, (h - h2) / 2
		return x, y, w2, h2
		return self.child.outer_rect ()

if __name__ == "__main__":
	from app import SECONDARY_BACKGROUND
	from gui import GUI
	from circled_square import CircledSquare
	
	def main ():
		if True:
			h = CircleApp (background=SECONDARY_BACKGROUND)
			g = SquaredCircle (h, rotation=ANGLED)
			f = CircledSquare (g, background=SECONDARY_BACKGROUND)
			e = SquaredCircle (f, rotation=STRAIGHT)
			d = CircledSquare (e, background=SECONDARY_BACKGROUND)
			c = SquaredCircle (d, rotation=ANGLED)
			b = CircledSquare (c, background=SECONDARY_BACKGROUND)
		else:
			b = CircleApp (background=SECONDARY_BACKGROUND)
		#a = SquaredCircle (b, rotation=STRAIGHT)
		a = SquaredCircle (None, rotation=ANGLED)
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
