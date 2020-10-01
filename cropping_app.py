#! /usr/bin/env python3

import pygame

from app import App
from constants import ORIGIN

from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_E, ANGLE_S, ANGLE_W


class CroppingApp (App): # https://stackoverflow.com/questions/64075338/how-to-make-circular-surface-in-pygame
	def __init__ (self, *args, **kwargs):
		App.__init__ (self, *args, **kwargs)
		self.bounds = None
	def draw_scene (self, temp=None):
		print ("enter cropping_app.draw_scene (%s)" % (temp,))
		if temp is None: temp = self.ss
		# 1. Draw everything on a surface with the same size as the window (background and scene).
		size = temp.get_size ()
		temp = pygame.Surface (size)
		self.draw_cropped_scene (temp)
		
		# 2. create the surface with the white circle.
		self.cropped_background = pygame.Surface (size, pygame.SRCALPHA)
		self.crop ()
		
		# 3. blit the former surface on the white circle.
		self.cropped_background.blit (temp, ORIGIN, special_flags=pygame.BLEND_RGBA_MIN)
		
		# 4. blit the whole thing on the window.
		self.ss.blit (self.cropped_background, ORIGIN)
		print ("leave cropping_app.draw_scene ()")
		"""
		
		
		
		
		if temp is None: temp = self.ss
		# 1. Draw everything on a surface with the same size as the window (background and scene).
		size = temp.get_size ()
		temp = pygame.Surface (size)

		self.draw_cropped_scene (temp)

		# 2. create the surface with the white circle.
		self.cropped_background = pygame.Surface (size, pygame.SRCALPHA)
		self.crop ()

		# 3. blit the former surface on the white circle.
		self.cropped_background.blit (temp, ORIGIN, special_flags=pygame.BLEND_RGBA_MIN)

		# 4. blit the whole thing on the window.
		self.ss.blit (self.cropped_background, ORIGIN)
		
		"""
		
		
		
		
		
		
		
		
		
		
		
	def draw_cropped_scene (self, temp):
		print ("enter cropping_app.draw_cropped_scene (%s)" % (temp,))
		App.draw_scene (self, temp)	
		print ("leave cropping_app.draw_cropped_scene ()")
	def crop (self): # need to override
		print ("cropping_app.crop () is abstract")
		raise Exception ()
	
	def positive_space (self, is_root=True):
		print ("enter cropping_app.positive_space (%s)" % (is_root,))
		if is_root is True: a = App.positive_space (self)
		else:               a = 0
		a = a + self.outer_area () - self.inner_area ()
		print ("leave cropping_app.positive_space ()")
		return a
	def negative_space (self, is_root=True):
		print ("enter cropping_app.negative_space (%s)" % (is_root,))
		if is_root is True: a = App.negative_space (self) - self.outer_area ()
		else:               a = 0
		print ("leave cropping_app.negative_space ()")
		return a
	def outer_area (self):
		print ("enter cropping_app.outer_area ()")
		a = App.area (self) - self.inner_area ()
		print ("leave cropping app.outer_area ()")
		return a
	def inner_area (self): # need to override
		print ("cropping app.inner_area () is abstract")
		raise Exception ()
	def outer_rect (self):
		print ("enter cropping_app.outer_rect ()")
		r = App.get_rect (self)
		print ("leave cropping_app.outer_rect ()")
		return r
	def inner_rect (self): # need to override
		print ("cropping app.inner_rect () is abstract")
		return self.outer_rect ()
		raise Exception ()
	def minsz (self):
		print ("enter cropping_app.minsz ()")
		X, Y, W, H = self.outer_rect ()
		x, y, w, h = self.inner_rect ()
		rw, rh = W / w, H / h
		minw, minh = self.minsz_helper ()
		ret = rw * minw, rh * minh
		print ("enter cropping_app.minsz ()")
		return ret
	def minsz_helper (self): # need to override
		print ("enter cropping_app.minsz_helper ()")
		a = App.minsz (self) # minsz of child
		print ("leave cropping_app.minsz_helper ()")
		return a
		
	def recursion_rect (self, geom=SQUARE): return self.inner_rect () # override
	#def recursion_rect (self, geom=SQUARE): return self.outer_rect () # override
	
	
	#def outer_bounding_area (self): raise Exception () # area of bounding box
	#def outer_area          (self): raise Exception () # area of square/diamond
	#def inner_bounding_area (self): raise Exception () # area of bounding box
	#def inner_area          (self): raise Exception () # area of circle
	
	#def recursion_rect (self, geom=SQUARE): # need to override: default behavior is to use square outer geometry
		
		

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = CroppingApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
