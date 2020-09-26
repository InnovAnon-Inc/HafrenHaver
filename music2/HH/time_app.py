#! /usr/bin/env python3

from app import App, DEFAULT_BACKGROUND, SECONDARY_BACKGROUND
from cropping_app import CroppingApp, OPAQUE


import pygame

from gui import GUI, BLACK


import pygame
import pygame.gfxdraw


from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp
from angle_app import AngleApp

from circled_square import CircledSquare
from squared_circle import SquaredCircle

from orientation import NORTH, SOUTH, EAST, WEST



from angle_app import cercle_circonscrit, cercle_inscrit
	
	

class  AngledCircle ( AngleApp, CompositeApp):
	def __init__ (self, child, orientation=NORTH, *args, **kwargs):
		AngleApp    .__init__ (self, orientation, *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert isinstance (child, CircleApp)
	def set_subsurface (self, ss):
		AngleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		
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
	def draw_cropped_scene (self, temp):
		AngleApp.draw_cropped_scene (self, temp)
		
		x1, y1, z1 = self.bounds
		(x, y), r  = cercle_inscrit ((x1, y1, z1))
		x2, y2 = x - r, y - r
		w = h = 2 * r
		rect = pygame.Rect (x2, y2, w, h)
			
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)
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
		
		
		
def trianglearea (a, b) : # https://www.geeksforgeeks.org/largest-triangle-that-can-be-inscribed-in-an-ellipse/
    # a and b cannot be negative  
    if a < 0 or b < 0 : return -1
    # area of the triangle  
    area = (3 * sqrt(3) * pow(a, 2)) / (4 * b) 
    return area 		
		
class CircledAngle  (CircleApp, CompositeApp):
	def __init__ (self, child, *args, **kwargs):
		CircleApp   .__init__ (self, *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert isinstance (child, AngleApp)
	def set_subsurface (self, ss):
		CircleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		
		# TODO circumscribed triangle... need triangle bounds relative to circle
		
		
		
		
		(x, y), (w, h) = self.bounds
		print ((x, y, w, h))
		
		A = 3 * sqrt (3) / 4 * w * h
		
		
		#b = c
		#p = a + b + c = a + 2 * b
		#A = sqrt (p * (p - a) * (p - b) * (p - c)) = sqrt (p * (p - a)) * (p - b)
		
		# pow (x / w, 2) + pow (y / h, 2) = 1
		
		# TODO arcane sources hint at using orthogonal projections for this, but nobody has actually done it and written about it
		
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
	def draw_cropped_scene (self, temp):
		CircleApp.draw_cropped_scene (self, temp)
		
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
			
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)
	def minsz (self):
		# TODO determine scale factor from current radius to min radius
		raise Exception ()
		tmp = self.child.minsz () * foo
		tmp = max (tmp, CircleApp.minsz (self))
		return tmp

class  AngledSquare ( AngleApp, CompositeApp): pass
class SquaredAngle  (SquareApp, CompositeApp): pass

		
# perfect varieties of squares and circles, for compositing

# compositing:
# circles in circle (ring, cluster)
# circles in square
# squares in circle
# squares in square (grid, lines)

# nested apps should recurse with copies of themselves in used slots... need pixel-perfect minsz... copies need to not be clickable

# aesthetic composites:
# golden ratio ? for square layouts with main section et al
# golden ratio ? for circle in circle containers
		
# TODO circular container:
#      has inner & outer radii,
#      handles sizes of square   children
# TODO square   container:
#      has inner & outer rects,
#      handles sizes of circular parents

# animated containers...
# jiggle back and forth / up and down (1 pixel)
# jiggle rotation back and forth (1 degree ?)
# pulse (scale down by 1 pixel, then back up)
# fading (alpha)

# some sort of hilbert curve + cadence => how to vary animations of all containers on screen

class TimeApp (CircleApp):
	def __init__ (self):
		CircleApp.__init__ (self)
	def run_loop (self, keys):
		#CenteredApp.run_loop (self, keys)
		pass

# show splash text re: lovecraftian stars aligning
# day/night indicator... red during sunriset, no blue during night, bright during day (greenish?), dark at night
# wheel of the year... can indicate position of sun in sky ?
# moon phases... can indicate position of moon in sky ?
# day of week indicator... switch symbols at sundown
# classical time... analog clock with a hand for the procession of the equinox (i.e., eon hand) ?		
# countdown clock / alarm that can trigger by the stars

if __name__ == "__main__":
	from rotation import ANGLED, STRAIGHT
	from orientation import NORTH, SOUTH, EAST, WEST
	
	def main ():
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
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
