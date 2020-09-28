#! /usr/bin/env python3

import pygame
import pygame.gfxdraw

from composite_app import CompositeApp
from circle_app import CircleApp
from angle_app import AngleApp

from orientation import NORTH, SOUTH, EAST, WEST
from geometry import cercle_circonscrit, cercle_inscrit
	
	

class  AngledCircle (AngleApp, CompositeApp):
	def __init__ (self, child, orientation=NORTH, *args, **kwargs):
		AngleApp    .__init__ (self, orientation, *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert child is None or isinstance (child, CircleApp)
		assert (child is None) != (orientation is None)
		if child is None: self.orientation = orientation
		else:             self.orientation = self.child.orientation
	def start_running (self):
		AngleApp   .start_running (self)
		CompositeApp.start_running (self)
	def  stop_running (self):
		AngleApp    .stop_running (self)
		CompositeApp .stop_running (self)
	def set_subsurface (self, ss):
		AngleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, None, True)
		"""
		ss = self.ss
		
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = ss.subsurface (rect)
		self.child.set_subsurface (ss2)
		"""
		"""
		x1, y1, z1 = self.bounds
		(x, y), r  = cercle_inscrit ((x1, y1, z1))
		x2, y2 = x - r, y - r
		w = h = 2 * r
		rect = pygame.Rect (x2, y2, w, h)
		print ((x1, y1, z1))
		print ((x, y))
		print (r)
		print ((x2, y2))
		print ((w))
		
		ss2 = ss.subsurface (rect)
		self.inner_bounds = (x, y), (r, r)
		self.child.set_subsurface (ss2)
		"""
	def draw_cropped_scene (self, temp):
		AngleApp.draw_cropped_scene (self, temp)
		CompositeApp.draw_cropped_scene (self, temp)
		"""
		x1, y1, z1 = self.bounds
		(x, y), r  = cercle_inscrit ((x1, y1, z1))
		x2, y2 = x - r, y - r
		w = h = 2 * r
		rect = pygame.Rect (x2, y2, w, h)
			
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)
		"""
	"""
	def minsz (self):
		# TODO determine scale factor from current radius to min radius
		raise Exception ()
		tmp = self.child.minsz () * foo
		tmp = max (tmp, AngleApp.minsz (self))
		return tmp
	def positive_area (self):
		x, y, z = self.bounds
		(x1, y1), (x2, y2), (x3, y3) = x, y, z
		dx21, dy21 = x2 - x1, y2 - y1
		dx32, dy32 = x3 - x2, y3 - y2
		dx13, dy13 = x1 - x3, y1 - y3
		s21 = sqrt (pow (dx21, 2) + pow (dy21, 2))
		s32 = sqrt (pow (dx32, 2) + pow (dy32, 2))
		s13 = sqrt (pow (dx13, 2) + pow (dy13, 2))
		a1 = findAreaOfTriangle (s21, s32, s13)
		assert a1 >= 0
		return a1
	def negative_area (self):
		size = self.ss.get_size()
		w, h = size
		w, h = w / 2, h / 2
		a1 = pi * w * h
		assert a1 >= 0
		a2   = self.positive_space ()
		assert a2 >= 0
		a3 = a1 - a2
		assert a3 >= 0
		return a3
	def positive_space (self, is_root=True):
		a1 = CompositeApp.positive_space (self, is_root)
		assert a1 >= 0
		if not is_root: return a1
		a1 = a1 + AngleApp.positive_space (self, is_root)
		assert a1 >= 0
		return a1
	def negative_space (self, is_root=True):
		a1 = CompositeApp.negative_space (self, is_root)
		assert a1 >= 0
		if not is_root: return a1
		a1 = a1 + AngleApp.negative_space (self, is_root) 
		assert a1 >= 0
		return a1
	"""
	def positive_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def negative_space (self, is_root=True): return CompositeApp.positive_space (self, is_root)
	def minsz          (self):               return CompositeApp.minsz          (self)
	def outer_bounding_area (self): return AngleApp .outer_area (self) # area of bounding box
	def outer_area          (self): return AngleApp .inner_area (self) # area of triangle
	def inner_bounding_area (self): return self.child.outer_area ()    # area of bounding box
	def inner_area          (self): return self.child.inner_area ()    # area of circle
	def inner_rect (self):
		x1, y1, z1 = self.bounds
		(x, y), r  = cercle_inscrit ((x1, y1, z1))
		x2, y2 = x - r, y - r
		w = h = 2 * r
		return (x2, y2, w, h)
		return self.child.outer_rect ()

if __name__ == "__main__":
	from rotation import ANGLED, STRAIGHT
	from orientation import Orientation
	from app import App
	from constants import DEFAULT_BACKGROUND, SECONDARY_BACKGROUND
	from gui import GUI
	#from circled_angle import CircledAngle
	
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
			b = CircleApp ()
			a = AngledCircle (b, orientation=NORTH)
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
