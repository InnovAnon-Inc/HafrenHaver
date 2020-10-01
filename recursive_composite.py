#! /usr/bin/env python3

import pygame
import pygame.gfxdraw

from itertools import chain

from app import App
from composite_app import CompositeApp

from geometry import tr
from constants import ORIGIN
from constants import DEFAULT_SCREEN_MODE

from cropping_app import CroppingApp

	
from geometry import recurse_point

class RecursiveComposite (App):
	def __init__ (self, seed, pic=None, *args, **kwargs):
		App.__init__ (self, *args, **kwargs)
		self.child = seed
		assert seed is not None
		assert isinstance (seed, CompositeApp)
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
		print ("test a")
		if self.pic is None: pic = temp.copy ()
		else:                pic = self.pic
		print ("test b")
		for rp in self.recursion_points (temp):
			print ("test c: recursive_composite.draw_foreground () in for-loop: %s" % (rp,))
			x, y, w, h = rp # x, y is at origin bc relative rects. need to get abs rect
			print ("rp: %s" % (rp,))
			w, h = tr ((w, h))
			print ("test d")
			trans = pygame.transform.scale (pic, (w, h)) # scale fake screen to bounding rect
			print ("test e")
			ts.blit (trans, (x, y))                      # blit fake screen onto working surface
			print ("test f")
		print ("test g")
		temp.blit (ts, (X, Y))                           # blit working-surface onto real surface
	def recursion_points_helper (self):
		print ("enter recursive_composite.recursion points helper ()")
		node = self.child
		while True:
			# TODO inner_rect() is not right: need an inner inner rect
			if not isinstance (node, CompositeApp):
				#print ("unexpected node type")
				#raise Exception ()
				print ("test a")
				if isinstance (node, CroppingApp): r = node.inner_rect ()
				else: r = node.get_rect ()
				#ret = (node.get_rect (), node.minsz ())
				#ret = (node.inner_rect (), node.minsz ())
				ret = (r, node.minsz ())
				print ("test b")
				break
			if node.is_recursable ():
				print ("test c: get inner rect from node: %s %s" % (type (node), node))
				temp_a = node.inner_rect ()
				print ("test d")
				temp_b = node.minsz ()
				print ("test e")
				ret = (temp_a, temp_b)
				#ret = (node.inner_rect (temp), node.minsz ())
				print ("test f")
				break
			print ("test g")
			node = node.child
			print ("test h")
		#assert False
		print ("test i")
		print ("leave recursive_composite.recursion points helper ()")
		return (ret,)
	
	def recursion_points (self, temp):
		print ("enter recursive_composite.recursion points (%s)" % (temp,))
		rect = temp.get_rect ()
		print ("test a")
		rps = self.recursion_points_helper ()
		if True:
			for rp in rps: yield from recurse_point (rect, *rp)
		else:
			print ("test b")
			f = lambda args: recurse_point (rect, *args)
			print ("test c")
			ret = map (f, rps)
			print ("test d")
			ret=tuple(ret)
			print ("test dd")
			ret = chain (*ret)
			print ("test ddd")
			ret=tuple(ret)
			print ("test e")
			return ret
		print ("leave recursive_composite.recursion_points ()")
			
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
	from square_app import SquareApp
	
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
			k = 0
			if k == -1:
				d = SquareApp (background=SECONDARY_BACKGROUND)
				c = CircledSquare (d)
				b = SquaredCircle (c, background=SECONDARY_BACKGROUND)
			if k == 0:
				# TODO need to get inner inner rect, given a specified geometry
				# shapeApp.get_inner_inner_rect (outer_geometry=square)
				# 
				r = ANGLED
				if False:
					d = SquareApp (rotation=r, background=SECONDARY_BACKGROUND)
					c = CircledSquare (d)
				elif True:
					c = CircledSquare (d, rotation=r)
				else:
					c = CircledSquare (d, rotation=STRAIGHT)
				b = SquaredCircle (c, rotation=r, background=SECONDARY_BACKGROUND)
			if k == 1:
				r = STRAIGHT
				c = SquaredCircle (d, rotation=r)
				b = CircledSquare (c, background=SECONDARY_BACKGROUND)
			if k == 2:
				c = CircledAngle (d, orientation=NORTH)
				b = AngledCircle (c, orientation=NORTH, background=SECONDARY_BACKGROUND)
			if k == 3:
				c = AngledCircle (d, orientation=NORTH)
				b = CircledAngle (c, orientation=NORTH, background=SECONDARY_BACKGROUND)
				
			if k == 4:
				r = STRAIGHT
				c = CircledSquare (d, rotation=r)
				b = SquaredCircle (c, rotation=r, background=SECONDARY_BACKGROUND)
				
			a = RecursiveComposite (b)
			#a = b
		#a = RecursiveCompositeTest ()
		with GUI (app=a) as g:
			#print (a.get_rect ())
			#print (a.inner_rect ())
			#print (a.child.outer_rect ())
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
