#! /usr/bin/env python3

from app import App
from geometry import tr
from cropping_app import CroppingApp
from constants import OPAQUE

from rotation import STRAIGHT, ANGLED

import pygame
import pygame.gfxdraw

from math import sqrt

from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_E, ANGLE_S, ANGLE_W
from geometry import midpoint

class SquareApp (CroppingApp):
	def __init__ (self, rotation=STRAIGHT, parent_is_square=True, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.rotation = rotation
		self.parent_is_square = parent_is_square
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		self.bounds_exact = self.get_rect ()
		self.bounds       = self.bounds_exact
	def crop (self):
		if self.rotation == STRAIGHT:
			pygame.gfxdraw.rectangle (self.cropped_background, self.bounds, OPAQUE)
			pygame.gfxdraw.box       (self.cropped_background, self.bounds, OPAQUE)
		if self.rotation == ANGLED:
			x, y, w, h = self.bounds
			if True:
				a = 0    , h / 2
				b = w / 2, 0
				c = w    , h / 2
				d = w / 2, h
			else:
				a = 0, 0
				b = w, 0
				c = w, h
				d = 0, h
			#pts = map (tr, (a, b, c, d))
			#pts = tuple (pts)
			pts = (a, b, c, d)
			pygame.gfxdraw.     aapolygon (self.cropped_background, pts, OPAQUE)
			pygame.gfxdraw.filled_polygon (self.cropped_background, pts, OPAQUE)
			
	def minsz_helper (self):
		w, h = CroppingApp.minsz_helper (self)
		if self.rotation == STRAIGHT: return w * 2, h * 2
		assert self.rotation == ANGLED
		return w * sqrt (2), h * sqrt (2)
	#def outer_area (self):
	#	x, y, w, h = self.bounds
	#	return w * h
	def inner_area (self):
		x, y, w, h = self.bounds
		if self.rotation == STRAIGHT: a = w * h
		if self.rotation == ANGLED:   a = w * h / 2
		assert a >= 0
		return a
	#def inner_rect (self): return self.get_outer_rect ()
	def recursion_rect (self, geom=SQUARE):
		print ("enter square_app.recursion_rect (%s)" % (geom,))
		if self.rotation == STRAIGHT and geom == SQUARE: return CroppingApp.recursion_rect (self, geom)
		if self.rotation == ANGLED   and geom == SQUARE:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			w, h = W / sqrt (2), H / sqrt (2)
			x, y = X + w / 2, Y + h / 2
			assert x > 0
			assert y > 0
			return x, y, w, h
			
		if self.rotation == STRAIGHT and geom == DIAMOND:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			w, h = W / sqrt (2), H / sqrt (2)
			x, y = X + w / 2, Y + h / 2
			assert x > 0
			assert y > 0
			return x, y, w, h
		if self.rotation == ANGLED and geom == DIAMOND: return CroppingApp.recursion_rect (self, geom)
		
		if self.rotation == STRAIGHT and geom == CIRCLE:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			w, h = W / sqrt (2), H / sqrt (2)
			#x, y = X + w / 2, Y + h / 2
			#x, y = X + w, Y + h
			x, y = X + (W - w) / 2, Y + (H - h) / 2
			assert x > 0
			assert y > 0
			return x, y, w, h
		if self.rotation == ANGLED and geom == CIRCLE:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			#w, h = W / sqrt (2), H / sqrt (2)
			##x, y = X + w / 2, Y + h / 2
			#x, y = X + (W - w) / 2, Y + (H - h) / 2
			r = sqrt (pow (1 / 2, 2) + pow (1 / 2, 2))
			cx, cy = X + W / 2, Y + H / 2
			x, y, w, h = cx - r * W, cy - r * H, r * W * 2, r * H * 2
			assert x > 0
			assert y > 0
			return x, y, w, h
		
		if self.rotation == STRAIGHT and geom == ANGLE_N: return CroppingApp.recursion_rect (self, geom)
		if self.rotation == STRAIGHT and geom == ANGLE_E: return CroppingApp.recursion_rect (self, geom)
		if self.rotation == STRAIGHT and geom == ANGLE_S: return CroppingApp.recursion_rect (self, geom)
		if self.rotation == STRAIGHT and geom == ANGLE_W: return CroppingApp.recursion_rect (self, geom)
		if self.rotation == ANGLED   and geom == ANGLE_N:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			A = (X + W / 2, Y)
			B = (X + W    , Y + H / 2)
			C = (X + W / 2, Y + H)
			D = (X        , Y + H / 2)
			
			a = A
			b = midpoint (B, C)
			c = midpoint (C, D)
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			return (xmin, ymin, dx, dy)
		if self.rotation == ANGLED   and geom == ANGLE_E:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			A = (X + W / 2, Y)
			B = (X + W    , Y + H / 2)
			C = (X + W / 2, Y + H)
			D = (X        , Y + H / 2)
			
			a = B
			b = midpoint (C, D)
			c = midpoint (D, A)
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			return (xmin, ymin, dx, dy)
		if self.rotation == ANGLED   and geom == ANGLE_S:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			A = (X + W / 2, Y)
			B = (X + W    , Y + H / 2)
			C = (X + W / 2, Y + H)
			D = (X        , Y + H / 2)
			
			a = C
			b = midpoint (D, A)
			c = midpoint (A, B)
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			return (xmin, ymin, dx, dy)
		if self.rotation == ANGLED   and geom == ANGLE_W:
			rect = CroppingApp.recursion_rect (self, geom)
			X, Y, W, H = rect
			A = (X + W / 2, Y)
			B = (X + W    , Y + H / 2)
			C = (X + W / 2, Y + H)
			D = (X        , Y + H / 2)
			
			a = D
			b = midpoint (A, B)
			c = midpoint (B, C)
			
			o, r = bounding_rect (pts)
			xmin, ymin = o
			dx, dy = r
			return (xmin, ymin, dx, dy)
		raise Exception () # unsupported geom

if __name__ == "__main__":
	from gui import GUI
	from rotation import Rotation
	
	def main ():
		for rotation in Rotation:
			a = SquareApp (rotation)
			with GUI (app=a, exit_on_close=False) as g:
				#g.setApp (a)
				print ("minsz: (%s, %s)" % a.minsz ())
				print ("outer: %s"       % a.outer_area ())
				print ("inner: %s"       % a.inner_area ())
				print ("pos  : %s"       % a.positive_space ())
				print ("neg  : %s"       % a.negative_space ())
				g.run ()
	main ()
	quit ()
