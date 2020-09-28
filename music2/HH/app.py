#! /usr/bin/env python3

import pygame

from gui import BLACK

DEFAULT_BACKGROUND   = "background.png"
SECONDARY_BACKGROUND = "shiva.png"

ORIGIN = (0, 0)

class App:
	def __init__ (self, background=DEFAULT_BACKGROUND):
		#self.clock = pygame.time.Clock ()
		self.ss = None
		self.set_background (background)
		self.clock = pygame.time.Clock ()
		
	def set_background (self, background=None):
		if background is not None: self.raw_background = pygame.image.load (background)
		if self.ss is None: return
		w = self.ss.get_width  ()
		h = self.ss.get_height ()
		self.background = pygame.transform.scale (self.raw_background.convert_alpha (), (w, h))
		
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
		#self.ss.fill (BLACK)
		#self.ss.blit (self.background, ORIGIN)
		#pygame.draw.rect (self.ss, color, Rect (0, 0, w, h))
		#pygame.display.flip ()
		
		self.draw_scene ()
		
		#pygame.display.update()  
		#self.clock.tick ()
	def draw_scene (self, temp=None):
		if temp is None: temp = self.ss
		#self.ss.fill (BLACK)
		#self.ss.blit (self.background, ORIGIN)
		self.draw_background (temp)
		self.draw_foreground (temp)
	def draw_background (self, temp):
		temp.fill (BLACK)
		temp.blit (self.background, ORIGIN)
	def draw_foreground (self, temp): pass

	def minsz (self): return 1, 1 # px
	def positive_space (self, is_root=True): return 0
	def negative_space (self, is_root=True): return self.area ()
	def area (self):
		w, h = self.dims ()
		return w * h
	def dims (self):
		x, y, w, h = self.get_rect ()
		return w, h
	def get_rect (self): return self.ss.get_rect ()
	def is_recursable (self): return False

if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = App ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
