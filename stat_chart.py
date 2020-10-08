#! /usr/bin/env python3

import pygame
import pygame.gfxdraw

from orientation import NORTH, SOUTH, EAST, WEST
from circle_app import CircleApp
from geometry import inscribe_angles, rotate_angles, graphics_affines
from geometry import scale_points, angles_to_polygon, graphics_affine
from geometry import scale_point, tr
from itertools import starmap
from math import sin, cos
from constants import ORIGIN

class StatChart (CircleApp): # TODO need an abstract class bc this is similar to the magic circle text
	# TODO axis label, value, radius
	#def __init__ (self, rads):
	def __init__ (self):
		CircleApp.__init__ (self)
		self.rads = None
		"""
		rads      = tuple (rads)
		self.rads = rads
		#self.lbls = lbls
		"""
	def set_radii (self, rads):
		rads = tuple (rads)
		self.rads = rads
		self.compute ()
	def compute (self):
		rads = self.rads
		n         = len (rads)
		#assert n == len (lbls)
		
		angles      = inscribe_angles (n)
		
		orientation = NORTH
		theta       = orientation.radians ()
		angles      = rotate_angles   (angles, theta)
		angles      = tuple (angles)
	    
		f           = lambda theta, radius: (radius * cos (theta), radius * sin (theta))
		pv          = zip (angles, rads)
		pts         = starmap (f, pv)
		pts         = graphics_affines (pts)
		f           = lambda k: tuple (k)
		pts         = map (f, pts)
		pts         = tuple (pts)
		self.pts    = pts
		
		axes        = angles_to_polygon (angles)
		axes        = graphics_affines (axes)
		f           = lambda k: tuple (k)
		axes        = map (f, axes)
		axes        = tuple (axes)
		self.axes   = axes
		
	def draw_background (self, temp):
		CircleApp.draw_background (self, temp)
		pts  = self.pts
		assert len (pts) > 0
		rect = temp.get_rect ()
		pts  = scale_points (pts, rect)
		f    = lambda k: tuple (k)
		pts  = map (f, pts)
		pts  = tuple (pts)
		assert len (pts) > 0
		
		color = (0, 0, 255)
		pygame.gfxdraw.     aapolygon (temp, pts, color)
		pygame.gfxdraw.filled_polygon (temp, pts, color)
		
	def draw_foreground (self, temp):
		CircleApp.draw_foreground (self, temp)
		pts  = self.axes
		assert len (pts) > 0
		rect = temp.get_rect ()
		pts  = scale_points (pts, rect)
		f    = lambda k: tr (k)
		pts  = map (f, pts)
		pts  = tuple (pts)
		assert len (pts) > 0
		
		color = (255, 0, 255)
		for a, b in zip (pts, (*pts[1:], pts[0])):
			assert len (a) == 2, "a: %s" % (a,)
			assert len (b) == 2, "b: %s" % (b,)
			pygame.gfxdraw.line (temp, *a, *b, color)
		
		o    = ORIGIN
		o    = graphics_affine (o)
		x, y, w, h = rect
		o    = scale_point (o, ORIGIN, (w, h))
		o    = tr (o)
		
		color = (255, 255, 0)
		for axis in pts:
			assert len (o)    == 2, "o:  %s" % (o,)
			assert len (axis) == 2, "pt: %s" % (axis,)
			pygame.gfxdraw.line (temp, *o, *axis, color)
			
			
			
			
			
from circled_circle import AbsoluteCircledCircle

from polygon_app import PolygonApp, EqualPolygonApp
from circled_polygon import CircledPolygon
from polygoned_circle import PolygonedCircle, EqualPolygonedCircle
from text_ring import TextRing

def inscribe (pv):
	f           = lambda theta, radius: (radius * cos (theta), radius * sin (theta))
	#pv          = zip (angles, rads)
	pts         = starmap (f, pv)
	return pts
def inscribe2 (angles, rads):
	pv = zip (angles, rads)
	return inscribe (pv)
def inscribe3 (rads):
	rads = tuple (rads)
	n = len (rads)
	angles = inscribe_angles (n)
	return inscribe2 (angles, rads)
	
from constants import SECONDARY_BACKGROUND
"""
class CircleStatChartInner (CircledPolygon): # polygon radii as a function of stats
	def __init__ (self, rads, *args, **kwargs):
		if rads is not None:
			rads = tuple (rads)
			n = len (rads)
			#child = EqualPolygonApp (n)
			#angles = inscribe_angles (n)
			#ars = zip (angles, rads)
			#pts = inscribe (ars)
			pts = inscribe3 (rads)
			f = lambda pt: tuple (pt)
			pts = map (f, pts)
			pts = tuple (pts)
		else: pts = None
		child = PolygonApp (pts, background=SECONDARY_BACKGROUND, *args, **kwargs)
		CircledPolygon.__init__ (self, child, *args, **kwargs)
	def set_radii (self, rads):
		rads = tuple (rads)
		n = len (rads)
		#child = EqualPolygonApp (n)
		#angles = inscribe_angles (n)
		#ars = zip (angles, rads)
		#pts = inscribe (ars)
		#pts = inscribe (angles, rads)
		pts = inscribe3 (rads)
		f = lambda pt: tuple (pt)
		pts = map (f, pts)
		pts = tuple (pts)
		self.child.set_pts (pts)
"""

#class CircleStatChart (TextRing): # labelled stat chart inner
class CircleStatChart (AbsoluteCircledCircle):
	def __init__ (self, labels, font=None):
		child = StatChart (None)
		text  = ' '.join (labels)
		TextRing.__init__ (self, child, text, font)
	def set_radii (self, rads):
		self.child.set_radii (rads)

if __name__ == "__main__":
	from gui import GUI, BLACK
	from hal import HAL9000
	from random import uniform, randrange
	
	def main ():	
		n    = randrange (3, 12 + 1)
		assert n >= 3
		rng  = range (1, n + 1)
		rng  = tuple (rng)
		assert len (rng) == n
		f    = lambda k: uniform (0, 1)
		rads = map (f, rng)
		#a = StatChart ()
		a = CircleStatChart ()
		a.set_radii (rads)
		with HAL9000 (app=a, exit_on_close=False) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
