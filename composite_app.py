#! /usr/bin/env python3

from cropping_app import CroppingApp


import pygame

class CompositeApp (CroppingApp):
	def __init__ (self, child, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.child = child
	def start_running (self):
		print ("enter composite_app.start_running ()")
		CroppingApp .start_running (self)
		if self.child is not None: self.child.start_running ()
		print ("leave composite_app.start_running ()")
	def  stop_running (self):
		print ("enter composite_app.stop_running ()")
		CroppingApp .stop_running (self)
		if self.child is not None: self.child.stop_running ()
		print ("leave composite_app.stop_running ()")
	#def minsz (self):
	#	if self.child is None: k = 1
	#	else:                  k = self.child.minsz ()
	#	return CroppingApp.minsz (self) * k
	
	#def inner_rect (self): raise Exception ()
		
	#def outer_dims (self): return CroppingApp.dims (self)
	#def outer_area (self): return CroppingApp.area (self)
	
	
		"""
		dx_outer, dy_outer = self.get_outer_dims ()
		dx_inner, dy_inner = self.get_inner_dims ()
		rx, ry = dx_outer / dx_inner, dy_outer / dy_inner         # ratio of inner and outer dims
		if self.child is None: xmini, ymini = 1, 1
		else:                  xmini, ymini = self.child.minsz () # min inner dims
		xmino, ymino = xmini * rx, ymini * ry                     # outer dims := min inner dims * ratios of dims
		return xmino, ymino
		"""
	def draw_cropped_scene (self, temp):
		print ("enter composite_app.draw_cropped_scene (%s)" % (temp,))
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = temp.subsurface (rect)
		if self.child is not None:
			self.child.set_subsurface (ss2)
			self.child.draw_scene (ss2)
		print ("leave composite_app.draw_cropped_scene ()")
	def positive_space (self, is_root=True):
		print ("enter composite_app.positive_space (%s)" % (is_root,))
		if is_root: a = CroppingApp.positive_space (self)
		else:       a = 0
		a = a + self.outer_area () - self.inner_area ()
		if self.child is not None: a = a + self.child.positive_space ()
		print ("leave composite_app.positive_space ()")
		return a
	def negative_space (self, is_root=True):
		print ("enter composite_app.negative_space (%s)" % (is_root,))
		if is_root: a = CroppingApp.negative_space (self) - self.outer_area ()
		else:       a = 0
		if child is None: a = a + self.inner_area ()
		else:             a = a + self.child.negative_space ()
		print ("leave composite_app.negative_space ()")
		return a
	def is_recursable (self):
		print ("enter composite_app.is_recursable ()")
		a = self.child is None
		print ("leave composite_app.is_recursable ()")
		return a
	def set_subsurface (self, ss, second_call=False):
		print ("enter composite_app.set_subsurface (%s, %s)" % (ss, second_call))
		if not second_call: CroppingApp.set_subsurface (self, ss)
		if     second_call:
			assert ss is None
			ss = self.ss
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = ss.subsurface (rect)
		if self.child is not None: self.child.set_subsurface (ss2)
		print ("leave composite_app.set_subsurface ()")
	
	def minsz_helper (self):
		print ("enter composite_app.minsz_helper ()")
		if self.child is None: a = CroppingApp.minsz_helper ()
		else: a = self.child.minsz () # min inner dims
		print ("leave composite_app.minsz_helper ()")
		return a
	
		
	def inner_rect (self): # need to override
		print ("enter composite_app.inner_rect ()")
		if self.child is None:
			print ("inner_rect () child is None")
			a = CroppingApp.inner_rect (self)
			#raise Exception ()
		else:
			print ("inner_rect () fallback behavior")
			a = self.child.inner_rect () # fallback is to query the child
		print ("leave composite_app.inner_rect ()")
		return a
		
	#def recursion_rect (self, geom=None): # need to override: default behavior is to use square outer geometry
	# TODO if child is none then use geom, else use child geom
	# TODO if child is not none, then child's recursion rect needs to be scaled to this one
		
		
	

if __name__ == "__main__":
	from gui import GUI
	from angle_app import AngleApp
	from constants import SECONDARY_BACKGROUND
	from circled_angle import CircledAngle
	from angled_circle import AngledCircle
	from recursive_composite import RecursiveComposite
	
	def main ():
		d = None
		c = AngledCircle (d)
		b = CircledAngle (c, background=SECONDARY_BACKGROUND)
		a = RecursiveComposite (b)
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
