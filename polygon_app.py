#! /usr/bin/env python3

import pygame
import pygame.gfxdraw

from cropping_app import CroppingApp
from constants import OPAQUE
from geometry import scale_points, tr
from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_E, ANGLE_S, ANGLE_W
from orientation import NORTH, SOUTH, EAST, WEST

class PolygonApp (CroppingApp): # divide circle into segments
	def __init__ (self, pts, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.pts = pts
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		rect = self.ss.get_rect ()
		self.compute_points (rect)
	def compute_points (self, rect):
		pts = self.pts
		pts    = scale_points      (pts, rect)
		f = lambda pt: tuple (pt)
		pts = map (f, pts)
		pts = tuple (pts)
		#print ("pts: %s" % (pts,))
		#quit ()
		self.bounds       = pts
	def crop (self):
		#w, h = self.ss.get_size ()
		#w, h = round (w / 2), round (h / 2)
		pts = self.bounds
		print ("pts: %s" % (pts,))
		pts = map (tr, pts)
		print ("pts: %s" % (pts,))
		f = lambda pt: tuple (pt)
		pts = map (f, pts)
		pts = tuple (pts)
		print ("pts: %s" % (pts,))
		pygame.gfxdraw.     aapolygon (self.cropped_background, pts, OPAQUE)
		pygame.gfxdraw.filled_polygon (self.cropped_background, pts, OPAQUE)

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
		raise Exception ()
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
	
from geometry import inscribe_graphics_polygon

class EqualPolygonApp (PolygonApp): # equal-sized angles
	def __init__ (self, n, orientation=NORTH, reflect=False, *args, **kwargs):
		pts = inscribe_graphics_polygon (n, orientation.radians (), reflect)
		PolygonApp.__init__ (self, pts, *args, **kwargs)
			 		 
if __name__ == "__main__":
	from hal import HAL9000
	
	def main ():
		a = EqualPolygonApp (5)
		with HAL9000 (app=a) as g: g.run ()
	main ()
	quit ()
