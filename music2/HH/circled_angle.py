#! /usr/bin/env python3

import pygame
import pygame.gfxdraw

from composite_app import CompositeApp
from circle_app import CircleApp
from angle_app import AngleApp

#from angled_circle import AngledCircle
		
def trianglearea (a, b) : # https://www.geeksforgeeks.org/largest-triangle-that-can-be-inscribed-in-an-ellipse/
    # a and b cannot be negative  
    if a < 0 or b < 0 : return -1
    # area of the triangle  
    area = (3 * sqrt(3) * pow(a, 2)) / (4 * b) 
    return area 		
				
from math import sin, cos, pi

DEFAULT_ROTATION = pi / 2
def inscribe_angles   (n):                           
	r   = range (0, n)
	f   = lambda k: k / n * 2 * pi
	tmp = map (f, r)
	if False: tmp = tuple (tmp)
	return tmp
def   rotate_angles   (angles, dt=DEFAULT_ROTATION):
	f   = lambda t: t + dt
	tmp = map (f, angles)
	if False: tmp = tuple (tmp)
	return tmp
def angles_to_polygon (angles):
	f   = lambda t: (cos (t), sin (t))
	tmp = map (f, angles)
	if False: tmp = tuple (tmp)
	return tmp
def inscribe_polygon (n, theta):
	angles = inscribe_angles   (n)
	angles =   rotate_angles   (angles, theta)
	pts    = angles_to_polygon (angles)
	return pts
	
def graphics_affine_x (x):   return (x + 1) / 2
def graphics_affine_y (y):   return (1 - y) / 2
from itertools import chain
def graphics_affine   (pt):
	tmp = zip (pt[:-1:2], pt[1::2])
	f   = lambda xy: (graphics_affine_x (xy[0]), graphics_affine_y (xy[1]))
	tmp = map (f, tmp)
	tmp = chain (*tmp)
	if False: tmp = tuple (tmp)
	return tmp
def graphics_affines  (pts): 
	tmp = map (graphics_affine, pts)
	if False: tmp = tuple (tmp)
	return tmp

def    scale_dim      (n,   offset, scale): return offset + scale * n
def    scale_point    (pt, origin, dims):
	nsos   = zip (pt, origin, dims)
	f      = lambda nso: scale_dim (*nso)
	ret    = map (f, nsos)
	if False: ret = tuple (ret)
	return ret
def    scale_points   (pts, rect):
	assert len (rect) % 2 == 0
	ndim = len (rect) // 2
	orig = rect[:ndim]
	dims = rect[ndim:]
	f    = lambda pt: scale_point (pt, orig, dims)
	ret  = map (f, pts)
	if False: ret = tuple (ret)
	return ret

def bounding_box (pts):
	tmp = zip (*pts)                                # array of tuples (x, y) => arrays of x's, y's and z's  
	tmp = map (lambda k: (min (*k), max (*k)), tmp) # array of tuples (minx, maxx), (miny, maxy)
	tmp = zip (*tmp)                                 # array of tuples (minx, miny), (maxx, maxy)
	if False: tmp = tuple (tmp)
	return tmp
from functools import reduce
def point_deltas (pts):
	tmp = zip (*pts)                                # array of tuples (minx, miny), (maxx, maxy) => arrays of mins, maxes
	f   = lambda k: reduce ((lambda a, b: a - b), k[::-1])
	tmp = map (f, tmp)                              # deltas (maxx - minx), (maxy - miny)
	if False: tmp = tuple (tmp)
	return tmp
def bounding_rect (pts):
	bb  = bounding_box (pts)
	bb  = tuple (bb)
	ds  = point_deltas (bb)
	return bb[0], ds

class CircledAngle  (CircleApp, CompositeApp): # https://stackoverflow.com/questions/64089260/find-coordinates-of-isosceles-triangle-with-maximum-area-bounded-by-ellipse
	def __init__ (self, child, *args, **kwargs):
		CircleApp   .__init__ (self, *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert isinstance (child, AngleApp)
	def start_running (self):
		CircleApp   .start_running (self)
		CompositeApp.start_running (self)
	def  stop_running (self):
		CircleApp    .stop_running (self)
		CompositeApp .stop_running (self)
	def set_subsurface (self, ss):
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = ss.subsurface (rect)
		self.child.set_subsurface (ss2)	
	def draw_cropped_scene (self, temp):
		CircleApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_cropped_scene (self, temp)
	def positive_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def negative_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def minsz          (self):               return CompositeApp.minsz          (self)
	def outer_bounding_area (self): return CircleApp .outer_area (self) # area of bounding box
	def outer_area          (self): return CircleApp .inner_area (self) # area of triangle
	def inner_bounding_area (self): return self.child.outer_area ()    # area of bounding box
	def inner_area          (self): return self.child.inner_area ()    # area of circle
	def inner_rect (self):
		rect = self.outer_rect ()             # bounding box of ellipse
		x, y, w, h = rect

		r = self.child.orientation.radians () # direction of triangle
		pts = inscribe_polygon (3, r)
		pts = graphics_affines (pts)          # from cartesian
		pts = scale_points (pts, rect)        # scale points to ellipse dims
		
		o, r = bounding_rect (pts)
		xmin, ymin = o
		dx, dy = r
		return (xmin, ymin, dx, dy)
		return self.child.outer_rect ()
			
		
	"""
	def set_inner_bounds (self):
		w, h = self.get_outer_dims ()
		
		# coordinates of inscribed triangle
		top       = (w/2, 0)  # this one does not change
		xmin = w/2 - w * cos (pi/6) / 2
		xmax = w/2 + w * cos (pi/6) / 2
		ymax = h/2 + h * sin (pi/6) / 2
		bot_left  = (xmin, ymax)
		bot_right = (xmax, ymax)
		self.inner_bounds = top, bot_left, bot_right
		self.inner_rect   = rect = (*ORIGIN, xmax, ymax)
		
	def get_outer_dims (self):
		x, y, w, h = self.ss.get_rect ()
		return w, h
	def get_inner_dims (self):
		x, y, w, h = self.get_inner_rect
		return w, h
	def set_subsurface (self, ss):
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		self.set_inner_bounds ()
		
		ss = self.ss
		rect = self.get_inner_rect ()
		rect = pygame.Rect (*rect)	
		ss2 = ss.subsurface (rect)
		self.inner_bounds = (top, bot_left, bot_right)
		self.child.set_subsurface (ss2)
	def draw_cropped_scene (self, temp):
		CircleApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_scene (self)
		#rect = self.inner_rect ()
		#rect = pygame.Rect (*rect)			
		#ss2 = temp.subsurface (rect)
		#self.child.set_subsurface (ss2)
		#self.child.draw_scene (ss2)
	"""
		
if __name__ == "__main__":
	from rotation import ANGLED, STRAIGHT
	from orientation import NORTH, SOUTH, EAST, WEST
	from gui import GUI
	
	def main ():
		if False:
			j = AngleApp     (orientation=NORTH)
			i = CircledAngle (j)
			h = AngledCircle (i, orientation=WEST)
			g = CircledAngle (h)
			f = AngledCircle (g, orientation=SOUTH)
			e = CircledAngle (f)
			d = AngledCircle (e, orientation=EAST)
			c = CircledAngle (d)
			b = AngledCircle (c, orientation=NORTH)
			a = CircledAngle (b)
		else:
			b = AngleApp (orientation=NORTH)
			a = CircledAngle (b)
		#a = RecursiveCompositeTest ()
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
