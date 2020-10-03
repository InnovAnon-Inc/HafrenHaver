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










import threading
import sys
import os

class GUI:
	def __init__ (self, fullscreen=False, exit_on_close=False, app=None, busy_wait=False):
		self.entered           = False
		#self.running           = False
		"""
		self.        title     =         title
		self.        icontitle =         icontitle
		self.        icon      =         icon
		self.running_title     = running_title
		self.running_icontitle = running_icontitle
		self.closing_title     = closing_title
		self.closing_icontitle = closing_icontitle
		self.credits           = credits
		self.crfg              = crfg
		self.crbg              = crbg
		"""
		self.fullscreen        = fullscreen
		self.app               = app
		#self.subliminal_threshold = subliminal_threshold
		self.exit_on_close     = exit_on_close
		self.busy_wait         = busy_wait
		#self.ss = None
		#self.set_background (background)
		
	def __enter__ (self):		
		self.entered     = True
		#bits = 16 #the number of channels specified here is NOT 
		          #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
		# TODO
		#pygame.mixer.pre_init(DEFAULT_SAMPLE_RATE, -bits, 2)
		##mixer.init ()
		pygame.init ()
		#mixer .init () # TODO proper order ?
		
		
		self.screen_info = display.Info  () #Required to set a good resolution for the game screen
		self.clock       = pygame.time   .Clock ()
		#self.set_title      ()
		#self.set_icon       ()
		self.enter0 ()
		self.set_app        ()
		
		#self.clock.tick ()
		self.set_fullscreen ()
		#self.show_credits   ()
		##self.set_background ()
		#self.clock.tick (self.subliminal_threshold)
		self.enter1 ()
		return self
	
	def enter0 (self): pass
	def enter1 (self): pass 
	def  exit0 (self, type, value, traceback): pass
	def __exit__ (self, type, value, traceback):
		print ("in exit")
		self.running = False
		#self.clock.tick ()
		#print ("after tick")
		##self.set_background ()
		#self.show_credits ()
		#print ("after credits")
		#self.set_title (self.closing_title, self.closing_icontitle)
		#print ("after title")
		##self.clock.tick (self.subliminal_threshold)
		#self.clock.tick ()
		#print ("after tick")
		self.exit0 (type, value, traceback)
		def f ():
			pygame.display.quit ()
			print ("after display quit")
			mixer.quit ()
			print ("after pygame quit")
			pygame.quit ()
			#print ("after pygame quit")
			#mixer .quit () # TODO proper order ?
			print ("after mixer quit")
			mixer.quit ()
			print ("after mixer quit")
		if True:
			x = threading.Thread (target=f)
			print ("thread created")
			x.start ()
			print ("thread started")
			if self.exit_on_close:
				x.join (DEFAULT_EXIT_TIMEOUT)
				if x.is_alive (): # TODO
					pass
			else: x.join ()
			print ("thread joined")
			res = 0 # TODO
		else:
			f ()
			res = 0
		self.entered = False
		#if self.exit_on_close: sys.exit ()
		if self.exit_on_close: os._exit (res)
		print ("exit_on_close disabled")
		return False

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
	
	def set_app (self, app=None):
		if app is not None: self.app = app
		if not self.entered: return
		if app is None: return
		if self.ss is not None: self.app.set_subsurface (self.ss)
	
	def run (self):
		self.run_enter ()
		self.clock.tick ()
		while self.running:
			#print ("in while")
			self.run_loop ()
			if not self.running: break
			#print ("before update")
			pygame.display.update ()
			#print ("after update")
			if not self.running: break
			#print ("before tick")
			# TODO get tick speed from app
			self.do_tick ()
			#print ("after tick")
		#print ("end while")
		if self.app is not None: self.app.stop_running ()
		self.run_leave ()
		self.clock.tick ()
	def run_enter (self):
		self.running = True
#		self.set_title (self.running_title, self.running_icontitle)
		if self.app is not None: self.app.start_running ()
		
	def run_leave (self):
		#print ("end run")
		self.running = False
		
	def do_tick (self):
		if self.busy_wait: f = self.clock.tick_busy_loop	
		else:              f = self.clock.tick
		f (DEFAULT_TICK_SPEED)
	def run_loop (self):
		pygame.event.pump () 	          # process event queue
		
		for event in pygame.event.get (): # Did the user click the window close button?
			if event.type == pygame.QUIT:
				self.running = False
				return
				
#			if event.type == VIDEORESIZE:
#				self.ss = pygame.display.set_mode (event.dict['size'], RESIZABLE)
#				if self.app is not None: self.app.set_subsurface (self.ss)				
			self.handle_event (event)
		keys = pygame.key.get_pressed ()  # It gets the states of all keyboard keys.
		if keys[ord ('q')]:
			self.running = False
			return
#		if keys[ord ('f')]: self.set_fullscreen (not self.fullscreen)
#		if keys[ord ('r')]: self.set_fullscreen (False)
		self.handle_keys (keys)
		
		# TODO only update graphics every n ticks... audio on every tick
		if self.app is not None: self.app.run_loop (keys)
		
	def handle_event (self, event): pass
	def handle_keys  (self, keys):  pass
		
if __name__ == "__main__":
	print (DEFAULT_FRAME_RATE)
	print (DEFAULT_SAMPLE_RATE)
	print (DEFAULT_TICK_SPEED)
	def main ():
		with GUI (exit_on_close=True) as g: g.run ()
	main ()
	print ("end main")
	quit ()
	sys.exit ()
