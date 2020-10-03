#! /usr/bin/env python3

#from queue import Queue
import pygame
from pygame import RESIZABLE, FULLSCREEN, VIDEORESIZE
from pygame import mixer, display

from scipy.constants import golden

from constants import DEFAULT_TITLE, DEFAULT_ICONTITLE, DEFAULT_ICON
from constants import RUNNING_TITLE, RUNNING_ICONTITLE, CLOSING_TITLE
from constants import CLOSING_ICONTITLE, DEFAULT_CREDITS
from constants import DEFAULT_SUBLIMINAL_THRESHOLD, BLACK, IA_BLACK
from constants import IA_RED, DEFAULT_SCREEN_MODE, DEFAULT_ISOCHRONIC
from constants import DEFAULT_SCALE, DEFAULT_SAMPLE_RATE
from constants import DEFAULT_FRAME_RATE, DEFAULT_TICK_SPEED
from constants import DEFAULT_EXIT_TIMEOUT, ORIGIN




# TODO use scales to select better tick speeds
	
	

#print (reasonable_minmax_int_pitch (4, DEFAULT_SCALE, 30, 60))
#print (reasonable_minmax_int_pitch (1 / 7.83, DEFAULT_SCALE, 30, 60))
#print (reasonable_minmax_int_pitch (7.83, DEFAULT_SCALE, 1 / 30, 1 / 60))




from gui import GUI





import threading
import sys
import os

class ResizeGUI (GUI):
	def __init__ (self, fullscreen=False, *args, **kwargs):
		GUI.__init__ (self, *args, **kwargs)
		self.fullscreen        = fullscreen
	"""	
	def set_fullscreen (self, fullscreen=None):
		assert self.entered
		if fullscreen is not None: self.fullscreen = fullscreen
		screen_info     = self.screen_info
		if fullscreen:
			self.first_screen = (screen_info.current_w, screen_info.current_h)
			self.      screen = display.set_mode (self.first_screen, FULLSCREEN | DEFAULT_SCREEN_MODE)
		else:
			w, h = screen_info.current_w, screen_info.current_h
			if w == h: self.first_screen = (w,                  h                 )
			if w >  h: self.first_screen = (w,                  round (h / golden))
			if w <  h: self.first_screen = (round (w / golden), h                 )
			#toolbar_height = 120 # TODO
			#self.first_screen = (screen_info.current_w, screen_info.current_h - toolbar_height)
			self.      screen = display.set_mode (self.first_screen, RESIZABLE | DEFAULT_SCREEN_MODE)
		self.rect = self.screen.get_rect   ()
		self.ss   = self.screen.subsurface (self.rect)
		if self.app is not None: self.app.set_subsurface (self.ss)
		"""		
	def handle_event (self, event):
		if event.type == VIDEORESIZE:
			self.ss = pygame.display.set_mode (event.dict['size'], RESIZABLE)
			if self.app is not None: self.app.set_subsurface (self.ss)
		GUI.handle_event (self, event)
	def handle_keys  (self, keys):
		if keys[ord ('f')]: self.set_fullscreen (not self.fullscreen)
		if keys[ord ('r')]: self.set_fullscreen (False)
		GUI.handle_keys (self, keys)
		
if __name__ == "__main__":
	def main ():
		with ResizeGUI (exit_on_close=False) as g: g.run ()
	main ()
	print ("end main")
	quit ()
	sys.exit ()
