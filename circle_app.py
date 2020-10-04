#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp
from constants import OPAQUE

import pygame
import pygame.gfxdraw

from math import pi, sqrt

from geometry import tr

from constants import ORIGIN

from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_S, ANGLE_E, ANGLE_W
from orientation import NORTH, SOUTH, EAST, WEST
from geometry import inscribe_polygon, graphics_affines, scale_points, bounding_rect

class CircleApp (CroppingApp):
	def __init__ (self, *args, **kwargs): CroppingApp.__init__ (self, *args, **kwargs)
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		w, h = self.ss.get_size ()
		w, h = w / 2, h / 2
		#self.bounds_exact = w, h
		#w, h = round (w), round (h)
		self.bounds       = ORIGIN, (w, h)
	def crop (self):
		#w, h = self.ss.get_size ()
		#w, h = round (w / 2), round (h / 2)
		o, bounds = self.bounds
		bounds = tr (bounds)
		pygame.gfxdraw.     aaellipse (self.cropped_background, *bounds, *bounds, OPAQUE)
		pygame.gfxdraw.filled_ellipse (self.cropped_background, *bounds, *bounds, OPAQUE)

	def minsz_helper (self):
		w, h = CroppingApp.minsz_helper (self)
		#w, h = CroppingApp.minsz (self)
		return pi * w, pi * h
	#def outer_area (self): return CroppingApp.area (self)
	def inner_area (self):
		w, h = self.dims ()
		return pi * w / 2 * h / 2
	#def inner_rect (self): return self.outer_rect ()
	def recursion_rect (self, geom=SQUARE):
		print ("enter circle_app.recursion_rect (%s)" % (geom,))
		if geom == SQUARE:
			print ("circle_app computing recursion rect for square geometry")
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			w, h = W / sqrt (2), H / sqrt (2)
			#x, y = X + w / 2, Y + h / 2
			x, y = X + (W - w) / 2, Y + (H - h) / 2
			#x, y = X, Y
			#assert X != x
			#assert Y != y
			assert x > 0
			assert y > 0
			assert w < W
			assert h < H
			return x, y, w, h
		if geom == DIAMOND:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			#w, h = W / sqrt (2), H / sqrt (2)
			w, h = W, H
			x, y = X + (W - w) / 2, Y + (H - h) / 2
			#x, y = X - w, Y - h
			#assert x > 0
			#assert y > 0
			return x, y, w, h
		if geom == CIRCLE:
			rect = CroppingApp.recursion_rect (self, geom)
			return rect
		if geom == ANGLE_N:
			r = NORTH.radians () # direction of triangle
			pts = inscribe_polygon (3, r)
			pts = graphics_affines (pts)          # from cartesian
			pts = scale_points (pts, rect)        # scale points to ellipse dims
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			x, y, w, h = xmin, ymin, dx, dy
			assert x > 0
			assert y > 0
			return x, y, w, h
		if geom == ANGLE_E:
			r = EAST.radians () # direction of triangle
			pts = inscribe_polygon (3, r)
			pts = graphics_affines (pts)          # from cartesian
			pts = scale_points (pts, rect)        # scale points to ellipse dims
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			x, y, w, h = xmin, ymin, dx, dy
			assert x > 0
			assert y > 0
			return x, y, w, h
		if geom == ANGLE_W:
			r = WEST.radians () # direction of triangle
			pts = inscribe_polygon (3, r)
			pts = graphics_affines (pts)          # from cartesian
			pts = scale_points (pts, rect)        # scale points to ellipse dims
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			x, y, w, h = xmin, ymin, dx, dy
			assert x > 0
			assert y > 0
			return x, y, w, h
		if geom == ANGLE_S:
			r = SOUTH.radians () # direction of triangle
			pts = inscribe_polygon (3, r)
			pts = graphics_affines (pts)          # from cartesian
			pts = scale_points (pts, rect)        # scale points to ellipse dims
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			x, y, w, h = xmin, ymin, dx, dy
			assert x > 0
			assert y > 0
			return x, y, w, h
		raise Exception () # unsupported geom
			

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = CircleApp ()
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
