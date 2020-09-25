#! /usr/bin/env python3

import pygame

from gui import GUI, BLACK

DEFAULT_BACKGROUND = "background.png"

ORIGIN = (0, 0)

class App:
	def __init__ (self, background=DEFAULT_BACKGROUND):
		#self.clock = pygame.time.Clock ()
		self.ss = None
		self.set_background (background)
		
	def set_background (self, background=None):
		if background is not None: self.raw_background = pygame.image.load (background)
		if self.ss is None: return
		w = self.ss.get_width  ()
		h = self.ss.get_height ()
		self.background = pygame.transform.scale (self.raw_background, (w, h))
		
	def set_subsurface (self, ss):
		self.ss = ss
		self.set_background ()

	def start_running (self):
		assert self.ss is not None
		# TODO
	def  stop_running (self):
		assert self.ss is not None
		# TODO

	def run_loop      (self, keys):
		assert self.ss is not None
		# TODO draw bounding box
		self.ss.fill (BLACK)
		self.ss.blit (self.background, ORIGIN)
		#pygame.draw.rect (self.ss, color, Rect (0, 0, w, h))
		#pygame.display.flip ()
		pygame.display.update()  
		#self.clock.tick (7.83)

"""
class CenteredApp (App):
	def __init__ (self):
		App.__init__ (self)
	def set_subsurface (self, ss):
		App.set_subsurface (self, ss)
		# TODO compute center
	def run_loop (self, keys):
		App.run_loop (self, keys)
		# TODO draw centered point
"""
"""
class CircularApp (App):
	def __init__ (self):
		CenteredApp.__init__ (self)
	def set_subsurface (self, ss):
		CenteredApp.set_subsurface (self, ss)
		# TODO check for square children
	def run_loop (self, keys):
		CenteredApp.run_loop (self, keys)
		# TODO draw bounding circle

class SquareApp (App):
	def __init__ (self):
		CenteredApp.__init__ (self)
	def set_subsurface (self, ss):
		CenteredApp.set_subsurface (self, ss)
		# TODO check for circular parents
	def run_loop (self, keys):
		CenteredApp.run_loop (self, keys)
		# TODO

class TimeApp (CenteredApp):
	def __init__ (self):
		CenteredApp.__init__ (self)
	def run_loop (self, keys):
		#CenteredApp.run_loop (self, keys)
		pass
"""
# day/night indicator
# wheel of the year
# moon phases
# day of week indicator
# classical time		
# countdown clock / alarm that can trigger by the stars

if __name__ == "__main__":
	def main ():
		a = App ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
