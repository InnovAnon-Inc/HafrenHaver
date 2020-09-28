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
from angled_circle import AngledCircle
from circled_angle import CircledAngle

from orientation import NORTH, SOUTH, EAST, WEST



from angle_app import cercle_circonscrit, cercle_inscrit
	
	

		


class  AngledSquare ( AngleApp, CompositeApp): pass
class SquaredAngle  (SquareApp, CompositeApp): pass








from angle_app import tr
from app import ORIGIN

from math import log, ceil

def recursive_affine (rect, dx, dy, rw, rh, n):
	x, y, w, h = rect
	for k in range (1, n + 1):
		dx, dy = dx * rw, dy * rh
		x,  y  =  x + dx,  y + dy
		w,  h  =  w * rw,  h * rh
		yield x, y, w, h
def recurse_point (rect, rp, minsz):
	X, Y, W, H = rect
	x, y, w, h = rp
	# get scale and offset for recursion point
	dx, dy = x - X, y - Y
	rw, rh = w / W, h / H
	# get number of recursions until < minsz
	f = lambda a, b, c: (log (a) - log (b)) / log (c)
	xmin, ymin = minsz
	xn, yn = f (xmin, w, rw), f (ymin, h, rh)
	n = min (xn, yn)
	n = ceil (n) # TODO off by one ?
	# recursively apply scale and offset
	tail = recursive_affine (rp, dx, dy, rw, rh, n)
	return rp, *tail

from itertools import chain

class RecursiveComposite (App):
	def __init__ (self, seed, *args, **kwargs):
		App.__init__ (self, *args, **kwargs)
		self.child = seed
	def get_outer_dims (self): return self.child.dims ()
	def get_outer_area (self): return self.child.outer_area ()
	def get_inner_dims (self): return self.child.inner_dims ()
	def minsz (self): return self.child.minsz ()	
	# TODO fractal space ?
	def positive_space (self, is_root=True): return self.child.positive_space (is_root)
	def negative_space (self, is_root=True): return self.child.negative_space (is_root)
	def inner_rect (self): return self.child.inner_rect ()
	def set_subsurface (self, ss):
		self.child.set_subsurface (ss) # SquareApp   .set_subsurface (self, ss)
		App.set_subsurface (self, self.child.ss)
	
	def draw_background (self, temp):
		App.draw_background (self, temp)
		self.child.draw_scene (temp)	
	def draw_foreground (self, temp):
		TR = temp.get_rect ()                                           # bounding rect for parent
		X, Y, W, H = TR
		ts = pygame.Surface ((W, H), pygame.SRCALPHA)                   # get a fresh surface for working
		
		pic = temp.copy ()
		#fake_screen = temp.copy ()                                     # fake screen same size as parent
		#fake_screen.blit (pic, (W, H))                                 # blit recursive image onto fake screen
		
		for rp in self.recursion_points (temp):
			x, y, w, h = rp
			w, h = tr ((w, h))
			trans = pygame.transform.scale (pic, (w, h))                # scale fake screen to bounding rect
			ts.blit (trans, (x, y))                                     # blit fake screen onto working surface
			
		# TODO more than one level of recursion depth
			
		temp.blit (ts, (X, Y))     # blit working-surface onto real surface
	def recursion_points_helper (self):
		node = self.child
		while True:
			if not isinstance (node, CompositeApp):
				ret = (node.get_rect (), node.minsz ())
				break
			if node.is_recursable ():
				ret = (node.inner_rect (), node.minsz ())
				break
			node = node.child
		#assert False
		return (ret,)
	
	def recursion_points (self, temp):
		rect = temp.get_rect ()
		rps = self.recursion_points_helper ()
		f = lambda args: recurse_point (rect, *args)
		ret = map (f, rps)
		return chain (*ret)
			


# using poetic cadences, grammar models, synonym dictionaries => wizard swears (take colorful input and produce musical output)			

		
# how to manage concentrations of positive vs negative space ?

# need subclasses of main connector apps for providing recursion points and reducing negative space


	
	
	
	
		
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
# need to account for ratios of positive space vs. negative space







from pyephem_sunpath.sunpath import sunpos
from datetime import datetime

thetime = datetime (2018, 5, 23, 13)
lat = 28.6
lon = 77.2
tz = 0

alt, azm = sunpos (thetime, lat, lon, tz, dst=False)



from skyfield import api

timescale = api.load.timescale ()
class PointInTime:
	def __init__ (self, observer, datetime):
		self.observer = observer
		self.datetime = datetime
	def get_position_of_sun (self):
		pass
	def get_position_of_sun  (self, datetime=None): # position of sun relative to earth
		dt = self.get_datetime (datetime)
		
	# get position of sun  in sky ?
	# get position of moon in sky ?
		
	def get_position_of_moon (self, datetime=None): pass 
	def get_wheel            (self, datetime=None): pass # wheel of the year, only update computations when time has passed
	def get_time_of_day      (self, datetime=None): pass # day, night, twilight
	def get_day_of_week      (self, datetime=None): pass # beginning after sundown ?
	def get_moon_phase       (self, datetime=None): pass #
	def get_length_of_day    (self, datetime=None): pass # length of day/night in seconds
	def get_second_of_day    (self, datetime=None): pass

class TimeModel:
	def __init__ (self, observer, datetime=None):
		self.observer = some_gps_voodoo # position of user (lat, lon, alt), either from client or server
	def get_datetime (self, datetime=None):
		if datetime is None: datetime = timescale.now ()
		else:                datetime = timescale.from_datetime (datetime)
		return datetime
	def get_observer (self): pass
	def get_model (self, datetime=None):
		observer = self.get_observer ()
		datetime = self.get_datetime ()
		return PointInTime (observer, datetime)
		
		
	

class TimeController: # tells the app when to update, based on isochronic pulses + frame rate + audio sample rate
	def get_tick (self): return 7.83 # TODO

# TODO use flatlib for horoscopes/astrology... bitches love sun signs, and computing entire charts for entire congregrations on the daily... well... there might be some possibilities in that


# has-a pos_of_sun + woy, pos_of_moon + moonphase, dow, clock, timer, tod
class TimeApp (CircleApp): # gets data from model, renders it on screen
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
		if False:
			j = AngleApp     (orientation=NORTH)
			i = CircledAngle (j, background=SECONDARY_BACKGROUND)
			h = AngledCircle (i, orientation=WEST)
			g = CircledAngle (h, background=SECONDARY_BACKGROUND)
			f = AngledCircle (g, orientation=SOUTH)
			e = CircledAngle (f, background=SECONDARY_BACKGROUND)
			d = AngledCircle (e, orientation=EAST)
			c = CircledAngle (d, background=SECONDARY_BACKGROUND)
			b = AngledCircle (c, orientation=NORTH)
			a = CircledAngle (b, background=SECONDARY_BACKGROUND)
		else:
			#d = SquareApp     (background=DEFAULT_BACKGROUND)
			d = None
			c = CircledSquare (d, rotation=STRAIGHT)
			b = SquaredCircle (c, background=SECONDARY_BACKGROUND)
			a = RecursiveComposite (b)
			#a = b
		#a = RecursiveCompositeTest ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
