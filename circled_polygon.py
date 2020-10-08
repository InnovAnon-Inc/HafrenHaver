#! /usr/bin/env python3

import pygame

from circle_app import CircleApp
from composite_app import CompositeApp
from polygon_app import PolygonApp, EqualPolygonApp
from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_E, ANGLE_S, ANGLE_W
	
class CircledPolygon (CircleApp, CompositeApp):
	def __init__ (self, child, *args, **kwargs):
		assert child is not None
		CircleApp   .__init__ (self,        *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert child is None or isinstance (child, PolygonApp)
		#assert (child is None) != (orientation is None)
		#if child is None: self.orientation = orientation
		#else:             self.orientation = child.orientation
		assert self.child is not None
	def start_running (self):
		print ("enter circled_polygon.start_running ()")
		CircleApp   .start_running (self)
		CompositeApp.start_running (self)
		print ("enter circled_polygon.stop_running ()")
	def  stop_running (self):
		print ("enter circled_polygon.stop_running ()")
		CircleApp    .stop_running (self)
		CompositeApp .stop_running (self)
		print ("leave circled_polygon.stop_running ()")
	def set_subsurface (self, ss):
		print ("enter circled_polygon.set_subsurface (%s)", (ss,))
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, None, True)
		print ("leave circled_polygon.set_subsurface ()")
	def draw_cropped_scene (self, temp):
		print ("enter circled_polygon.draw_cropped_scene (%s)", (temp,))
		CircleApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_cropped_scene (self, temp)
		print ("leave circled_polygon.draw_cropped_scene ()")
	def positive_space (self, is_root=True):
		print ("enter circled_polygon.positive_space ()")
		a = CompositeApp.positive_space (self, is_root)
		print ("leave circled_polygon.positive_space ()")
		return a
	def negative_space (self, is_root=True):
		print ("enter circled_polygon.negative_space ()")
		a = CompositeApp.positive_space (self, is_root)
		print ("leave circled_polygon.negative_space ()")
		return a
	def minsz          (self):
		print ("enter circled_polygon.minsz ()")
		a = CompositeApp.minsz          (self)
		print ("leave circled_polygon.minsz ()")
		return a
	def outer_bounding_area (self):
		print ("enter circled_polygon.outer_bounding_area ()")
		a = CircleApp .outer_area (self) # area of bounding box
		print ("leave circled_polygon.outer_bounding_area ()")
		return a
	def outer_area          (self):
		print ("enter circled_polygon.outer_area ()")
		a = CircleApp .inner_area (self) # area of circle
		print ("leave circled_polygon.outer_area ()")
		return a
	def inner_bounding_area (self):
		raise Exception ()
		x, y, w, h = self.inner_rect ()
		return w * h
		return self.child.outer_area ()     # area of bounding box
	def inner_area          (self):
		raise Exception ()
		print ("enter circled_polygon.inner_area ()")
		x, y, w, h = self.inner_rect ()
		if self.child.rotation == STRAIGHT: a = w * h
		else:
			assert self.child.rotation == ANGLED
			a = w * h / 2
		print ("leave circled_polygon.inner_area ()")
		return a
		return self.child.inner_area ()     # area of square/diamond
		
	def set_n (self, n):
		if self.child is not None: self.child.set_n (n)
		self.n = n
	def set_pts (self, pts):
		if self.child is not None: self.child.set_pts (pts)	
		self.pts = pts
		
	def inner_rect (self):
		print ("enter circled_polygon.inner_rect ()")
		return self.outer_rect ()
		# TODO
		
		
		o, (w2, h2) = self.bounds
		if self.rotation == STRAIGHT:
			w = w2 / sqrt (2)
			h = h2 / sqrt (2)
			x, y = w2 - w, h2 - h
		if self.rotation == ANGLED:
			(x, y), (w, h) = self.bounds		
		rect = (x, y, w * 2, h * 2)
		print ("leave circled_polygon.inner_rect ()")
		return rect
		return self.child.outer_rect ()
	def minsz_helper (self):
		raise Exception ()
		print ("enter circled_polygon.minsz_helper ()")
		w, h = CircleApp.minsz_helper (self) # TODO child's minsize ?
		if self.rotation == STRAIGHT: a = pi * sqrt (2) * w, pi * sqrt (2) * h
		else:
			assert self.rotation == ANGLED
			a = pi * w, pi * h
		print ("leave circled_polygon.minsz_helper ()")
		return a
	def recursion_rect (self, geom=SQUARE):
		raise Exception ()
		print ("enter circled_polygon.recursion_rect (%s)" % (geom,))
		if self.rotation == STRAIGHT: g = SQUARE
		if self.rotation == ANGLED:   g = DIAMOND
		rect =  CircleApp.recursion_rect (self, g)
		X, Y, W, H = rect
		if self.child is None:
			if self.rotation == ANGLED   and geom == DIAMOND: pass
			if self.rotation == STRAIGHT and geom == SQUARE: pass
			if self.rotation == ANGLED   and geom == SQUARE:
				w, h = W / sqrt (2), H / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == STRAIGHT and geom == DIAMOND:
				w, h = W / sqrt (2), H / sqrt (2)
				#w, h = w / sqrt (2), h / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == ANGLED and geom == CIRCLE:
				w, h = W / sqrt (2), H / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == STRAIGHT and geom == CIRCLE:
				w, h = W, H
				#w, h = W / sqrt (2), H / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
		else:
			print ("circled_polygon deferring to child for recursion_rect")
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
		print ("leave circled_polygon.recursion_rect ()")
		return rect

if __name__ == "__main__":
	from hal import HAL9000
	from polygon_app import EqualPolygonApp
	from constants import SECONDARY_BACKGROUND
	from polygoned_circle import EqualPolygonedCircle
	
	def main ():
		c = CircleApp ()
		n = 6
		b = EqualPolygonedCircle (n, c, background=SECONDARY_BACKGROUND)
		a = CircledPolygon (b)
		with HAL9000 (app=a) as g: g.run ()
	main ()
	quit ()
