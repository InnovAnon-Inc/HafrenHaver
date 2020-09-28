#! /usr/bin/env python3

import pygame

from app import App, ORIGIN

class CroppingApp (App): # https://stackoverflow.com/questions/64075338/how-to-make-circular-surface-in-pygame
	def __init__ (self, *args, **kwargs):
		App.__init__ (self, *args, **kwargs)
		self.bounds = None
	def draw_scene (self, temp=None):
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
	def draw_cropped_scene (self, temp): App.draw_scene (self, temp)	
	def crop (self): raise Exception ()
	
	def positive_space (self, is_root=True):
		if is_root is True: a = App.positive_space (self)
		else:               a = 0
		return a + self.outer_area () - self.inner_area ()
	def negative_space (self, is_root=True):
		if is_root is True: a = App.negative_space (self) - self.outer_area ()
		else:               a = 0
		return a
	def outer_area (self): raise Exception ()
	def inner_area (self): raise Exception ()
	def outer_rect (self): return App.get_rect (self)
	def inner_rect (self): raise Exception ()

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = CroppingApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
