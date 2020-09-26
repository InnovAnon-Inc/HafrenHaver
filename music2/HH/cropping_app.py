#! /usr/bin/env python3

import pygame

from app import App, ORIGIN

OPAQUE = (255, 255, 255, 255)

class CroppingApp (App):
	def __init__ (self, *args, **kwargs):
		App.__init__ (self, *args, **kwargs)
		self.bounds = None
	def draw_scene (self, temp=None):
		# 1. Draw everything on a surface with the same size as the window (background and scene).
		# 2. create the surface with the white circle.
		# 3. blit the former surface on the white circle.
		# 4. blit the whole thing on the window.
		
		if temp is None: temp = self.ss
		size = temp.get_size ()
		temp = pygame.Surface (size)
		
		self.draw_cropped_scene (temp)
		
		self.cropped_background = pygame.Surface (size, pygame.SRCALPHA)
		self.crop ()
		self.cropped_background.blit (temp, ORIGIN, special_flags=pygame.BLEND_RGBA_MIN)
		
		self.ss.blit (self.cropped_background, ORIGIN)
	def draw_cropped_scene (self, temp): App.draw_scene (self, temp)
		
	def crop (self): raise Exception ()

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = CroppingApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
