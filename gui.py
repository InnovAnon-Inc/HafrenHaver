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
	def __init__ (self, title=DEFAULT_TITLE, icontitle=DEFAULT_ICONTITLE, icon=DEFAULT_ICON, running_title=RUNNING_TITLE, running_icontitle=RUNNING_ICONTITLE, closing_title=CLOSING_TITLE, closing_icontitle=CLOSING_ICONTITLE, credits=DEFAULT_CREDITS, subliminal_threshold=DEFAULT_SUBLIMINAL_THRESHOLD, crfg=IA_RED, crbg=IA_BLACK, fullscreen=False, exit_on_close=True, app=None):
		self.entered           = False
		#self.running           = False
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
		self.fullscreen        = fullscreen
		self.app               = app
		self.subliminal_threshold = subliminal_threshold
		self.exit_on_close     = exit_on_close
		#self.ss = None
		#self.set_background (background)
		
	def __enter__ (self):		
		self.entered     = True
		bits = 16 #the number of channels specified here is NOT 
		          #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
		pygame.mixer.pre_init(DEFAULT_SAMPLE_RATE, -bits, 2)
		#mixer.init ()
		pygame.init ()
		mixer .init () # TODO proper order ?
		
		
		self.screen_info = display.Info  () #Required to set a good resolution for the game screen
		self.clock       = pygame.time   .Clock ()
		self.set_title      ()
		self.set_icon       ()
		self.set_app        ()
		
		self.clock.tick ()
		self.set_fullscreen ()
		self.show_credits   ()
		#self.set_background ()
		self.clock.tick (self.subliminal_threshold)
		return self	
	def __exit__ (self, type, value, traceback):
		print ("in exit")
		self.running = False
		self.clock.tick ()
		print ("after tick")
		#self.set_background ()
		self.show_credits ()
		print ("after credits")
		self.set_title (self.closing_title, self.closing_icontitle)
		print ("after title")
		#self.clock.tick (self.subliminal_threshold)
		self.clock.tick ()
		print ("after tick")
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
			x.join (DEFAULT_EXIT_TIMEOUT)
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
	def show_credits (self):
		assert self.entered
		df    = pygame.font.get_default_font ()
		font  = pygame.font.Font (df, 32)
		texts = (font.render (c, True, self.crfg, self.crbg) for c in self.credits) # TODO parallel
		w = self.ss.get_width  ()
		h = self.ss.get_height ()
		n = len (self.credits)
		self.ss.fill (self.crbg)
		for text, i in zip (texts, range (0, n)): # TODO parallel
			rect  = text.get_rect ()
			rect.center = (round (w / 2), round (h * (i / n) + h * (1 / (2 * n))))
			self.ss.blit (text, rect)
		pygame.display.update ()
		#self.clock.tick (.1)
	def set_background (self, background=None):
		if background is not None: self.raw_background = pygame.image.load (background)
		if self.ss is None: return
		w = self.ss.get_width  ()
		h = self.ss.get_height ()
		self.background = pygame.transform.scale (self.raw_background.convert_alpha (), (w, h))
		self.ss.fill (BLACK)
		self.ss.blit (self.background, ORIGIN)
		pygame.display.update()
		
	def set_title (self, title=None, icontitle=None):
		#assert title is not None or icontitle is not None
		if     title is not None: self.    title =     title
		if icontitle is not None: self.icontitle = icontitle
		if self.entered: display.set_caption (self.title, self.icontitle)
		
	def set_icon (self, icon=None):
		if icon is not None: self.icon = icon
		if not self.entered: return
		surface = pygame.image.load (self.icon)
		display.set_icon (surface)

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
		self.running = True
		self.set_title (self.running_title, self.running_icontitle)
		if self.app is not None: self.app.start_running ()
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
			self.clock.tick_busy_loop (DEFAULT_TICK_SPEED)
			#print ("after tick")
		#print ("end while")
		if self.app is not None: self.app. stop_running ()
		#print ("end run")
		#self.running = False	
	def run_loop (self):
		pygame.event.pump () 	          # process event queue
		
		for event in pygame.event.get (): # Did the user click the window close button?
			if event.type == pygame.QUIT:
				self.running = False
				return
				
			if event.type == VIDEORESIZE:
				self.ss = pygame.display.set_mode (event.dict['size'], RESIZABLE)
				if self.app is not None: self.app.set_subsurface (self.ss)
		keys = pygame.key.get_pressed ()  # It gets the states of all keyboard keys.
		if keys[ord ('q')]:
			self.running = False
			return
		if keys[ord ('f')]: self.set_fullscreen (not self.fullscreen)
		if keys[ord ('r')]: self.set_fullscreen (False)
		
		# TODO only update graphics every n ticks... audio on every tick
		if self.app is not None: self.app.run_loop (keys)
		
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
