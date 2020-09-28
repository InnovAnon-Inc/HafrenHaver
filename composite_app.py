#! /usr/bin/env python3

from cropping_app import CroppingApp


import pygame

class CompositeApp (CroppingApp):
	def __init__ (self, child, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.child = child
	def start_running (self):
		CroppingApp .start_running (self)
		if self.child is not None: self.child.start_running ()
	def  stop_running (self):
		CroppingApp .stop_running (self)
		if self.child is not None: self.child.stop_running ()
	#def minsz (self):
	#	if self.child is None: k = 1
	#	else:                  k = self.child.minsz ()
	#	return CroppingApp.minsz (self) * k
	
	#def inner_rect (self): raise Exception ()
		
	def get_outer_dims (self): return CroppingApp.dims (self)
	def get_outer_area (self): return CroppingApp.area (self)
	def get_inner_dims (self):
		x, y, w, h = self.inner_rect ()
		return w, h
	def minsz (self):
		dx_outer, dy_outer = self.get_outer_dims ()
		dx_inner, dy_inner = self.get_inner_dims ()
		rx, ry = dx_outer / dx_inner, dy_outer / dy_inner         # ratio of inner and outer dims
		if self.child is None: xmini, ymini = 1, 1
		else:                  xmini, ymini = self.child.minsz () # min inner dims
		xmino, ymino = xmini * rx, ymini * ry                     # outer dims := min inner dims * ratios of dims
		return xmino, ymino

	def draw_cropped_scene (self, temp):
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = temp.subsurface (rect)
		if self.child is None: return
		self.child.set_subsurface (ss2)
		self.child.draw_scene (ss2)
		
	def positive_space (self, is_root=True):
		if is_root: a = CroppingApp.positive_space (self)
		else:       a = 0
		a = a + self.outer_area () - self.inner_area ()
		if self.child is not None: a = a + self.child.positive_space ()
		return a
	def negative_space (self, is_root=True):
		if is_root: a = CroppingApp.negative_space (self) - self.outer_area ()
		else:       a = 0
		if child is None: return a + self.inner_area ()
		return a + self.child.negative_space ()
		
	def is_recursable (self): return self.child is None
	
	def set_subsurface (self, ss, second_call=False):
		if not second_call: CroppingApp.set_subsurface (self, ss)
		if     second_call:
			assert ss is None
			ss = self.ss
		rect = self.inner_rect ()
		rect = pygame.Rect (*rect)			
		ss2 = ss.subsurface (rect)
		if self.child is not None: self.child.set_subsurface (ss2)
		
	def inner_rect (self): return self.child.inner_rect ()

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
