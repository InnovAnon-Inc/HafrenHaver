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
		if pts is None: self.pts = None
		else:
			f = lambda pt: tuple (pt)
			pts = map (f, pts)
			self.pts = tuple (pts)
	def set_pts (self, pts):
		f = lambda pt: tuple (pt)
		pts = map (f, pts)
		pts = tuple (pts)
		self.pts = pts
		self.set_subsurface (None)
	def set_subsurface (self, ss):
		print ("enter polygon_app.set_subsurface (%s)" % (ss,))
		CroppingApp.set_subsurface (self, ss)
		if self.ss is not None:
			rect = self.ss.get_rect ()
			self.compute_points (rect)
		print ("leave polygon_app.set_subsurface ()")
	def compute_points (self, rect):
		print ("enter polygon_app.compute_points (%s)" % (rect,))
		pts = self.pts
		if pts is None: return
		assert len (pts) >= 3
		pts    = scale_points      (pts, rect)
		f = lambda pt: tuple (pt)
		pts = map (f, pts)
		pts = tuple (pts)
		#print ("pts: %s" % (pts,))
		#quit ()
		self.bounds       = pts
		print ("leave polygon_app.compute_points ()")
	def crop (self):
		print ("enter polygon_app.crop ()")
		#w, h = self.ss.get_size ()
		#w, h = round (w / 2), round (h / 2)
		pts = self.bounds
		#if len (pts) == 0:
		#	self.compute_points (self.outer_rect ())
		#	pts = self.bounds
		#if len (pts) == 0: return
		print ("pts: %s" % (pts,))
		pts = map (tr, pts)
		print ("pts: %s" % (pts,))
		f = lambda pt: tuple (pt)
		pts = map (f, pts)
		pts = tuple (pts)
		print ("pts: %s" % (pts,))
		pygame.gfxdraw.     aapolygon (self.cropped_background, pts, OPAQUE)
		pygame.gfxdraw.filled_polygon (self.cropped_background, pts, OPAQUE)
		print ("leave polygon_app.crop ()")
		
	def minsz_helper (self):
		print ("enter polygon_app.minsz_helper ()")
		w, h = CroppingApp.minsz_helper (self)
		#w, h = CroppingApp.minsz (self)
		a = pi * w, pi * h
		print ("leave polygon_app.minsz_helper ()")
		return a
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
		if n is None: pts = None
		else: pts = inscribe_graphics_polygon (n, orientation.radians (), reflect)
		PolygonApp.__init__ (self, pts, *args, **kwargs)
		self.n = n
		self.orientation = orientation
		self.reflect = reflect
	def set_n (self, n):
		self.n = n
		orientation = self.orientation
		reflect = self.reflect
		pts = inscribe_graphics_polygon (n, orientation.radians (), reflect)
		PolygonApp.set_pts (self, pts)
			 		 
if __name__ == "__main__":
	from hal import HAL9000
	
	def main ():
		n = 5
		a = EqualPolygonApp (n)
		#a = EqualPolygonApp (None)
		#a.set_n (n)
		with HAL9000 (app=a) as g: g.run ()
	main ()
	quit ()
