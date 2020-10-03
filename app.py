#! /usr/bin/env python3

import pygame

from constants import BLACK, ORIGIN

from constants import DEFAULT_BACKGROUND

from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_E, ANGLE_S, ANGLE_W

class App:
	def __init__ (self, background=DEFAULT_BACKGROUND):
		#self.clock = pygame.time.Clock ()
		self.ss = None
		self.set_background (background)
		self.clock = pygame.time.Clock ()
		
	def set_background (self, background=None):
		print ("enter app.set_background (%s)" % (background,))
		if background is not None: self.raw_background = pygame.image.load (background)
		if self.ss is None:
			print ("leave app.set_background ()")
			return
		w = self.ss.get_width  ()
		h = self.ss.get_height ()
		self.background = pygame.transform.scale (self.raw_background.convert_alpha (), (w, h))
		print ("leave app.set_background ()")
		
	def set_subsurface (self, ss):
		print ("enter app.set_subsurface (%s)" % (ss,))
		self.ss = ss
		self.set_background ()
		print ("leave app.set_subsurface ()")

	def start_running (self):
		print ("enter app.start_running ()")
		assert self.ss is not None
		# TODO
		print ("leave app.start_running ()")
	def  stop_running (self):
		print ("enter app.stop_running ()")
		assert self.ss is not None
		# TODO
		print ("leave app.stop_running ()")

	def run_loop      (self, events, keys):
		print ("enter app.run_loop (%s)" % (keys,))
		assert self.ss is not None
		# TODO draw bounding box
		#self.ss.fill (BLACK)
		#self.ss.blit (self.background, ORIGIN)
		#pygame.draw.rect (self.ss, color, Rect (0, 0, w, h))
		#pygame.display.flip ()
		self.draw_scene ()
		print ("leave app.run_loop ()")
		
		#pygame.display.update()  
		#self.clock.tick ()
	def draw_scene (self, temp=None):
		print ("enter app.draw_scene (%s)" % (temp,))
		if temp is None: temp = self.ss
		#self.ss.fill (BLACK)
		#self.ss.blit (self.background, ORIGIN)
		self.draw_background (temp)
		self.draw_foreground (temp)
		print ("leave app.draw_scene ()")
	def draw_background (self, temp):
		print ("enter app.draw_background (%s)" % (temp,))
		temp.fill (BLACK)
		temp.blit (self.background, ORIGIN)
		print ("leave app.draw_background ()")
	def draw_foreground (self, temp):
		print ("enter app.draw_foreground (%s)" % (temp,))
		pass
		print ("leave app.draw_foreground ()")

	def minsz (self):
		print ("app.minsz ()")
		return 1, 1 # px
	def positive_space (self, is_root=True):
		print ("app.positive_space (%s)" % (is_root,))
		return 0
	def negative_space (self, is_root=True):
		print ("enter app.negative_space (%s)" % (is_root,))
		a = self.area ()
		print ("leave app.negative_space ()")
		return a
	def area (self):
		print ("enter app.area ()")
		w, h = self.dims ()
		a    = w * h
		print ("leave app.area ()")
		return a
	def dims (self):
		print ("enter app.dims ()")
		x, y, w, h = self.get_rect ()
		print ("leave app.dims ()")
		return w, h
	def get_rect (self):
		print ("app.get_rect ()")
		return self.ss.get_rect ()
	def is_recursable (self):
		print ("app.is_recursable ()")
		return False
	def recursion_rect (self, geom=SQUARE):
		print ("enter app.recursion_rect (%s)" % (geom,))
		rect = self.get_rect ()
		print ("leave app.recursion_rect ()")
		return rect
if __name__ == "__main__":
	from gui import GUI
	
	def main ():
		a = App ()
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
