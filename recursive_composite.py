#! /usr/bin/env python3

import pygame
import pygame.gfxdraw

from itertools import chain

from app import App
from composite_app import CompositeApp

from geometry import tr
from constants import ORIGIN
from constants import DEFAULT_SCREEN_MODE

	
from geometry import recurse_point

class RecursiveComposite (App):
	def __init__ (self, seed, pic=None, *args, **kwargs):
		App.__init__ (self, *args, **kwargs)
		self.child = seed
		self.pic   = pic
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
	def draw_foreground (self, temp): # https://stackoverflow.com/questions/34910086/pygame-how-do-i-resize-a-surface-and-keep-all-objects-within-proportionate-to-t
		App.draw_foreground (self, temp)
		
		TR = temp.get_rect ()                            # bounding rect for parent
		X, Y, W, H = TR
		print ("TR: %s" % (TR,))
		ts = pygame.Surface ((W, H), pygame.SRCALPHA)    # get a fresh surface for working
		
		if self.pic is None: pic = temp.copy ()
		else:                pic = self.pic
		
		for rp in self.recursion_points (temp):
			x, y, w, h = rp
			print ("rp: %s" % (rp,))
			w, h = tr ((w, h))
			trans = pygame.transform.scale (pic, (w, h)) # scale fake screen to bounding rect
			ts.blit (trans, (x, y))                      # blit fake screen onto working surface
				
		temp.blit (ts, (X, Y))                           # blit working-surface onto real surface
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
			
if __name__ == "__main__":
	from rotation import ANGLED, STRAIGHT
	from orientation import NORTH, SOUTH, EAST, WEST
	from circled_square import CircledSquare
	from squared_circle import SquaredCircle
	from circled_angle import CircledAngle
	from angled_circle import AngledCircle
	from app import App
	from constants import DEFAULT_BACKGROUND, SECONDARY_BACKGROUND
	from gui import GUI
	from constants import BLACK
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
			if False:
				c = CircledSquare (d, rotation=ANGLED)
				b = SquaredCircle (c, rotation=ANGLED, background=SECONDARY_BACKGROUND)
			else:
				c = CircledAngle (d, orientation=NORTH)
				b = AngledCircle (c, orientation=NORTH, background=SECONDARY_BACKGROUND)
			a = RecursiveComposite (b)
			#a = b
		#a = RecursiveCompositeTest ()
		with GUI (app=a) as g:
			print (a.get_rect ())
			print (a.inner_rect ())
			print (a.child.outer_rect ())
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
