#! /usr/bin/env python3

import pygame

import matplotlib
matplotlib.use ("Agg")

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt

from app import App
from constants import ORIGIN

# https://stackoverflow.com/questions/13714454/specifying-and-saving-a-figure-with-exact-size-in-pixels
def pygame2matplotlib (w, h): return { 'figsize' : (w, h), 'dpi' : 1 }

# TODO some projections are circular...
class PyGamePlotLib (App): # integrates matplotlib with pygame
	def set_subsurface (self, ss=None, second_run=False): # TODO apps should pre render images here
		print ("enter pygame_plotlib.set_subsurface (%s)" % (ss,))
		if second_run: assert ss is None
		else: App.set_subsurface (self, ss)
		self.compute ()
		print ("leave pygame_plotlib.set_subsurface ()")
	def compute (self):
		print ("enter pygame_plotlib.compute ()")
		ss = self.ss
		if ss is None: return
		
		rect = ss.get_rect ()
		x, y, w, h = rect
		dims = pygame2matplotlib (w, h)
		
		fig = plt.figure (**dims, facecolor='none', edgecolor='none')
		fig.patch.set_visible (False)
		
		self.compute_helper (fig)
		fig.tight_layout () # https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
		
		canvas = agg.FigureCanvasAgg (fig) # https://stackoverflow.com/questions/48093361/using-matplotlib-in-pygame
		canvas.draw ()		
		renderer = canvas.get_renderer ()
		raw_data = renderer.buffer_rgba () # tricky
		self.raw_data = raw_data
		self.size     = canvas.get_width_height ()
		W, H = self.size
		assert w == W
		assert h == H
		print ("leave pygame_plotlib.compute ()")
	def compute_helper (self, fig): pass # override: draw stuff here
	def draw_foreground (self, temp): # TODO apps should merely blit pre rendered images here
		print ("enter pygame_plotlib.draw_foreground (%s)" % (temp,))
		App.draw_foreground (self, temp)
	#def draw_scene (self, temp=None): # TODO apps should merely blit pre rendered images here
	#	print ("enter pygame_plotlib.draw_scene (%s)" % (temp,))
	#	App.draw_scene (self, temp)
		if temp is None: temp = self.ss
		raw_data = self.raw_data
		size     = self.size
		x, y, w, h = temp.get_rect ()
		W, H = self.size
		assert w == W
		assert h == H
		surf = pygame.image.frombuffer (raw_data, size, "RGBA")
		temp.blit (surf, ORIGIN) 
		#x, y, w, h = temp.get_rect ()
		#picture = pygame.transform.scale (surf, (w, h))
		#temp.blit (picture, ORIGIN)
		print ("leave pygame_plotlib.draw_foreground ()")
		 		 
if __name__ == "__main__":
	from hal import HAL9000
	
	def main ():
		a = PyGamePlotLib ()
		with HAL9000 (app=a) as g: g.run ()
	main ()
	quit ()
