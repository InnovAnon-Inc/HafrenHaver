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

class  AngledCircle ( AngleApp, CompositeApp):
	def __init__ (self, child, orientation=NORTH, *args, **kwargs):
		AngleApp    .__init__ (self, orientation, *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert isinstance (child, CircleApp)
	def set_subsurface (self, ss):
		AngleApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		rect = self.bounds
		
		# TODO orientation logic
		
		ss2 = ss.subsurface (rect)
		self.inner_bounds = rect
		self.child.set_subsurface (ss2)
	def draw_cropped_scene (self, temp):
		AngleApp.draw_cropped_scene (self, temp)
		rect = self.bounds
		
		# TODO orientation logic
			
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)
	def minsz (self):
		if self.rotation == STRAIGHT: tmp = self.child.minsz ()
		if self.rotation == ANGLED:   tmp = self.child.minsz () * sqrt (2)
		tmp = max (tmp, AngleApp.minsz (self))
		return tmp
class CircledAngle  (CircleApp, CompositeApp): pass

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
	from rotation import ANGLED
	
	def main ():
		#a = SquareApp ()
		#c = CircleApp ()
		c = CircleApp (background=SECONDARY_BACKGROUND)
		b = SquaredCircle (c, rotation=ANGLED)
		#a = SquaredCircle (c)
		a = CircledSquare (b)
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
