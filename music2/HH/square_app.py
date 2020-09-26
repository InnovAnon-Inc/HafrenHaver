#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp, OPAQUE

import pygame
import pygame.gfxdraw

class SquareApp (CroppingApp):
	def __init__ (self, *args, **kwargs): CroppingApp.__init__ (self, *args, **kwargs)
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		self.bounds_exact = self.ss.get_rect ()
		self.bounds       = self.bounds_exact
	def crop (self):
		pygame.gfxdraw.rectangle (self.cropped_background, self.bounds, OPAQUE)
		pygame.gfxdraw.box       (self.cropped_background, self.bounds, OPAQUE)
	# TODO minsz = 2 ?

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = SquareApp ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
