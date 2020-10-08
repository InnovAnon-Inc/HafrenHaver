#! /usr/bin/env python3

import pygame

from circle_app import CircleApp

from polygon_app import PolygonApp
from composite_app import CompositeApp
from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_E, ANGLE_S, ANGLE_W

class PolygonedCircle (PolygonApp, CompositeApp):
	def __init__ (self, pts, child, *args, **kwargs):
		raise Exception ("fuck")
		PolygonApp   .__init__ (self, pts, *args, **kwargs)
		CompositeApp.__init__ (self, child,    *args, **kwargs)
		assert child is None or isinstance (child, CircleApp)
	def start_running (self):
		PolygonApp   .start_running (self)
		CompositeApp.start_running (self)
	def  stop_running (self):
		PolygonApp    .stop_running (self)
		CompositeApp .stop_running (self)
	def set_subsurface (self, ss):
		PolygonApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, None, True)
	def draw_cropped_scene (self, temp):
		PolygonApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_cropped_scene (self, temp)
	def positive_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def negative_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def minsz          (self):               return CompositeApp.minsz          (self)
	def outer_bounding_area (self): return PolygonApp .outer_area (self) # area of bounding box
	def outer_area          (self): return PolygonApp .inner_area (self) # area of square/diamond
	def inner_bounding_area (self):
		raise Exception ()
		x, y, w, h = self.inner_rect ()
		if self.rotation == STRAIGHT: return w * h
		assert self.rotation == ANGLED
		return w * h / 2
		return self.child.outer_area ()     # area of bounding box
	def inner_area          (self):
		raise Exception ()
		x, y, w, h = self.inner_rect ()
		w2, h2 = w / 2, h / 2
		ret = pi * w2 * h2
		return ret
		return self.child.inner_area ()     # area of circle
	def inner_rect (self):
		print ("polygoned_circle.inner_rect ()")
		raise Exception ()
		rect = self.outer_rect ()
		x, y, w, h = rect
		w2 = w / sqrt (2)
		h2 = h / sqrt (2)
		x, y = (w - w2) / 2, (h - h2) / 2
		return x, y, w2, h2
		return self.child.outer_rect ()
	def minsz_helper (self):
		raise Exception ()
		w, h = PolygonApp.minsz_helper (self) # TODO child's minsz ?
		if self.rotation == STRAIGHT: return pi * w, pi * h
		assert self.rotation == ANGLED
		return pi * sqrt (2) * w, pi * sqrt (2) * h
	def recursion_rect (self, geom=SQUARE):
		raise Exception ()
		print ("enter polygoned_circle.recursion_rect (%s)" % (geom,))
		if self.rotation == STRAIGHT: g = SQUARE
		if self.rotation == ANGLED:   g = DIAMOND
		rect =  SquareApp.recursion_rect (self, g)
		X, Y, W, H = rect
		if self.child is None:
			if self.rotation == ANGLED   and geom == DIAMOND: pass
			if self.rotation == STRAIGHT and geom == SQUARE:
				print ("polygoned_circle computing recursion_rect for square geometry")
				#w, h = W / sqrt (2), H / sqrt (2) # since the circle is empty, don't reduce size
				w, h = W, H
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == ANGLED   and geom == SQUARE:
				w, h = W / sqrt (2), H / sqrt (2) # circle's bb is smaller
				w, h = w / sqrt (2), h / sqrt (2) # square's bb is even smaller
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == STRAIGHT and geom == DIAMOND:
				w, h = W, H
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == ANGLED and geom == CIRCLE:
				w, h = W / sqrt (2), H / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == STRAIGHT and geom == CIRCLE:
				w, h = W / sqrt (2), H / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
		else:
			print ("polygoned_circle deferring to child for recursion rect")
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
		print ("leave polygoned_circle.recursion_rect ()")
		return rect
		
from polygon_app import EqualPolygonApp
from math import sqrt, cos, sin, pi
from constants import ORIGIN

def distance (a, b):
	ax, ay = a
	bx, by = b
	dx = bx - ax
	dy = by - ay
	dx = pow (dx, 2)
	dy = pow (dy, 2)
	c = sqrt (dx + dy)
	return c
def midpoint (a, b):
	ax, ay = a
	bx, by = b
	cx = ax + (bx - ax) / 2
	cy = ay + (by - ay) / 2
	c = cx, cy
	return c

class EqualPolygonedCircle (EqualPolygonApp, CompositeApp):
	def __init__ (self, n, child, *args, **kwargs):
		EqualPolygonApp   .__init__ (self, n, *args, **kwargs)
		CompositeApp.__init__ (self, child,    *args, **kwargs)
		assert child is None or isinstance (child, CircleApp)
	def start_running (self):
		EqualPolygonApp   .start_running (self)
		CompositeApp.start_running (self)
	def  stop_running (self):
		EqualPolygonApp    .stop_running (self)
		CompositeApp .stop_running (self)
	def set_subsurface (self, ss):
		EqualPolygonApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, None, True)
	def draw_cropped_scene (self, temp):
		EqualPolygonApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_cropped_scene (self, temp)
	def positive_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def negative_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def minsz          (self):               return CompositeApp.minsz          (self)
	def outer_bounding_area (self): return EqualPolygonApp .outer_area (self) # area of bounding box
	def outer_area          (self): return EqualPolygonApp .inner_area (self) # area of square/diamond
	def inner_bounding_area (self):
		raise Exception ()
		x, y, w, h = self.inner_rect ()
		if self.rotation == STRAIGHT: return w * h
		assert self.rotation == ANGLED
		return w * h / 2
		return self.child.outer_area ()     # area of bounding box
	def inner_area          (self):
		raise Exception ()
		x, y, w, h = self.inner_rect ()
		w2, h2 = w / 2, h / 2
		ret = pi * w2 * h2
		return ret
		return self.child.inner_area ()     # area of circle
	def inner_rect (self):
		print ("equal_polygoned_circle.inner_rect ()")
		if self.ss is None: return None
		rect = self.outer_rect ()
		X, Y, W, H = rect
		if self.n is None: return rect
		n = self.n
		#if self.pts is None: return rect
		#n = len (self.pts)
		#n = n * 2
		theta0 = 0 / n * 2 * pi
		theta1 = 1 / n * 2 * pi
		R = 1
		a = R * cos (theta0), R * sin (theta0)
		b = R * cos (theta1), R * sin (theta1)
		m = midpoint (a, b)
		r = distance (ORIGIN, m)
		#r = R / r		
		##W2, H2 = W / 2, H / 2
		##X2, Y2 = X + W2, Y + H2
		##w2, h2 = W / sqrt (2), H / sqrt (2)
		##w, h = w2 * 2, h2 * 2
		w, h = r * W, r * H
		x, y = X + (W - w) / 2, Y + (H - h) / 2
		rect = x, y, w, h
		return rect
		raise Exception ()
		rect = self.outer_rect ()
		if self.rotation == STRAIGHT: return rect
		assert self.rotation == ANGLED
		x, y, w, h = rect
		w2 = w / sqrt (2)
		h2 = h / sqrt (2)
		x, y = (w - w2) / 2, (h - h2) / 2
		return x, y, w2, h2
		return self.child.outer_rect ()
	def minsz_helper (self):
		raise Exception ()
		w, h = EqualPolygonApp.minsz_helper (self) # TODO child's minsz ?
		if self.rotation == STRAIGHT: return pi * w, pi * h
		assert self.rotation == ANGLED
		return pi * sqrt (2) * w, pi * sqrt (2) * h
	def recursion_rect (self, geom=SQUARE):
		raise Exception ()
		print ("enter equal_polygoned_circle.recursion_rect (%s)" % (geom,))
		if self.rotation == STRAIGHT: g = SQUARE
		if self.rotation == ANGLED:   g = DIAMOND
		rect =  SquareApp.recursion_rect (self, g)
		X, Y, W, H = rect
		if self.child is None:
			if self.rotation == ANGLED   and geom == DIAMOND: pass
			if self.rotation == STRAIGHT and geom == SQUARE:
				print ("equal_polygoned_circle computing recursion_rect for square geometry")
				#w, h = W / sqrt (2), H / sqrt (2) # since the circle is empty, don't reduce size
				w, h = W, H
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == ANGLED   and geom == SQUARE:
				w, h = W / sqrt (2), H / sqrt (2) # circle's bb is smaller
				w, h = w / sqrt (2), h / sqrt (2) # square's bb is even smaller
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == STRAIGHT and geom == DIAMOND:
				w, h = W, H
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == ANGLED and geom == CIRCLE:
				w, h = W / sqrt (2), H / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
			if self.rotation == STRAIGHT and geom == CIRCLE:
				w, h = W / sqrt (2), H / sqrt (2)
				x, y = X + (W - w) / 2, Y + (H - h) / 2
				rect = x, y, w, h
		else:
			print ("equal_polygoned_circle deferring to child for recursion rect")
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
		print ("leave equal_polygoned_circle.recursion_rect ()")
		return rect

if __name__ == "__main__":
	from hal import HAL9000
	from circled_polygon import CircledPolygon
	from constants import SECONDARY_BACKGROUND
	
	def main ():
		n = 8
		c = EqualPolygonApp (n, background=SECONDARY_BACKGROUND)
		b = CircledPolygon (c)
		n = 7
		a = EqualPolygonedCircle (n, b, background=SECONDARY_BACKGROUND)
		with HAL9000 (app=a) as g: g.run ()
	main ()
	quit ()
