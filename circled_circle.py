#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp

from math import sqrt, pi

from constants import ORIGIN

import pygame
from geom import SQUARE, DIAMOND, CIRCLE

class CircledCircle (CircleApp, CompositeApp):
	#def __init__ (self, child, inner_bounds=None, *args, **kwargs):
	def __init__ (self, child, *args, **kwargs):
		CircleApp   .__init__ (self,        *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert child is None or isinstance (child, CircleApp)
		#assert (child is None) != (inner_bounds is None)
		#if child is None: self.inner_bounds = inner_bounds
		#else:             self.inner_bounds = child.bounds
	def start_running (self):
		print ("enter circled_circle.start_running ()")
		CircleApp   .start_running (self)
		CompositeApp.start_running (self)
		print ("enter circled_circle.stop_running ()")
	def  stop_running (self):
		print ("enter circled_circle.stop_running ()")
		CircleApp    .stop_running (self)
		CompositeApp .stop_running (self)
		print ("leave circled_circle.stop_running ()")
	def set_subsurface (self, ss):
		print ("enter circled_circle.set_subsurface (%s)", (ss,))
		#(X, Y), (W2, H2) = self.bounds
		#(x, y), (w2, h2) = self.inner_bounds
		#rw, rh = W2 / w2, H2 / h2
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, None, True)
		#if child is not None: self.inner_bounds = child.bounds
		#else:
		#	(X, Y), (W2, H2) = self.bounds
		#	w2, h2 = rw * W2, rh * H2
		#	self.inner_bounds = ORIGIN, (w2, h2)
		#self.set_inner_bounds (ss)
		print ("leave circled_circle.set_subsurface ()")
	def draw_cropped_scene (self, temp):
		print ("enter circled_circle.draw_cropped_scene (%s)", (temp,))
		CircleApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_cropped_scene (self, temp)
		print ("leave circled_cricle.draw_cropped_scene ()")
	def positive_space (self, is_root=True):
		print ("enter circled_circle.positive_space ()")
		a = CompositeApp.positive_space (self, is_root)
		print ("leave circled_circle.positive_space ()")
		return a
	def negative_space (self, is_root=True):
		print ("enter circled_circle.negative_space ()")
		a = CompositeApp.positive_space (self, is_root)
		print ("leave circled_circle.negative_space ()")
		return a
	def minsz          (self):
		print ("enter circled_circle.minsz ()")
		a = CompositeApp.minsz          (self)
		print ("leave circled_circle.minsz ()")
		return a
	def outer_bounding_area (self):
		print ("enter circled_circle.outer_bounding_area ()")
		a = CircleApp .outer_area (self) # area of bounding box
		print ("leave circled_circle.outer_bounding_area ()")
		return a
	def outer_area          (self):
		print ("enter circled_circle.outer_area ()")
		a = CircleApp .inner_area (self) # area of circle
		print ("leave circled_circle.outer_area ()")
		return a
	def inner_bounding_area (self):
		x, y, w, h = self.inner_rect ()
		return w * h
		return self.child.outer_area ()     # area of bounding box
	def inner_area          (self):
		print ("enter circled_circle.inner_area ()")
		#c, (w2, h2) = self.inner_bounds () # self.child.bounds
		x, y, w, h = self.inner_rect ()
		w2, h2 = w / 2, h / 2
		a = pi * w2 * h2
		print ("leave circled_circle.inner_area ()")
		return a
	#def inner_rect (self):
	#	print ("enter circled_circle.inner_rect ()")
	#	(X, Y), (w2, h2) = self.inner_bounds ()# self.child.bounds
	#	x = X - w2
	#	y = Y - h2
	#	w = w2 * 2
	#	h = h2 * 2
	#	rect = x, y, w, h
	#	print ("rect: %s" % (rect,))
	#	print ("leave circled_circle.inner_rect ()")
	#	return rect
	#	return self.child.outer_rect ()
	def minsz_helper (self):
		print ("enter circled_circle.minsz_helper ()")
		if self.child is not None: return self.child.minsz ()
		w, h = CircleApp.minsz_helper (self)
		a = w, h
		print ("leave circled_circle.minsz_helper ()")
		return a
	def recursion_rect (self, geom=SQUARE):
		print ("enter circled_circle.recursion_rect (%s)" % (geom,))
		rect =  CircleApp.recursion_rect (self, CIRCLE)
		X, Y, W, H = rect
		if self.child is None:
			x, y, w, h = self.inner_rect ()
			if geom == SQUARE:
				w, h = w / sqrt (2), h / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if geom == DIAMOND:
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if geom == CIRCLE:
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
		else:
			print ("circled_circle deferring to child for recursion_rect")
			rect = self.child.recursion_rect (geom)
			x, y, w, h = rect
			
			assert X >= 0
			assert Y >= 0
			assert W > 0
			assert H > 0
			assert x >= 0
			assert y >= 0
			#assert w <= W
			#assert h <= H
			#rect = (X + x, Y + y, W / w, H / h)
			#rect = X + x, Y + y, w, h
			rect = X + (W - w) / 2, Y + (H - h) / 2, w, h
		print ("leave circled_circle.recursion_rect ()")
		return rect
		
class RelativeCircledCircle (CircledCircle):
	def __init__ (self, child, rw, rh, *args, **kwargs):
		CircledCircle.__init__ (self, child, *args, **kwargs)
		self.rw = rw
		self.rh = rh
	def inner_rect (self):
		X, Y, W, H = self.outer_rect ()
		rw, rh = self.rw, self.rh
		w, h = W * rw, H * rh
		x, y = X + (W - w) / 2, Y + (H - h) / 2
		return x, y, w, h
class AbsoluteCircledCircle (CircledCircle):
	def __init__ (self, child, xoff, yoff, *args, **kwargs):
		CircledCircle.__init__ (self, child, *args, **kwargs)
		self.xoff = xoff
		self.yoff = yoff
	def inner_rect (self):
		X, Y, W, H = self.outer_rect ()
		dw, dh = self.xoff, self.yoff
		dw, dh = dw * 2, dh * 2
		w, h = W - dw, H - dh
		x, y = X + (W - w) / 2, Y + (H - h) / 2
		return x, y, w, h
		
if __name__ == "__main__":
	from constants import SECONDARY_BACKGROUND
	from gui import GUI
	from hal import HAL9000
	from recursive_composite import RecursiveComposite
	
	def main ():
		c = CircleApp ()
		if False: b = RelativeCircledCircle (c, 9 / 10, 1 / 2, background=SECONDARY_BACKGROUND)
		else:     b = AbsoluteCircledCircle (c, 10, 20, background=SECONDARY_BACKGROUND)
		a = RecursiveComposite (b)
		#a = b
		with HAL9000 (app=a) as g:
			#g.setApp (a)
			#print ("minsz: (%s, %s)" % a.minsz ())
			#print ("outer: %s"       % a.outer_area ())
			#print ("inner: %s"       % a.inner_area ())
			#print ("pos  : %s"       % a.positive_space ())
			#print ("neg  : %s"       % a.negative_space ())
			g.run ()
	main ()
	quit ()
