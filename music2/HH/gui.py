#! /usr/bin/env python3

#from queue import Queue
import pygame
from pygame import RESIZABLE, FULLSCREEN, VIDEORESIZE
from pygame import mixer, display

DEFAULT_TITLE     = "Hafren Haver: InnovAnon"
DEFAULT_ICONTITLE = "HH IA"
DEFAULT_ICON      = "logo.png"

RUNNING_TITLE     = "Hafren Haver: Free Code for a Free World!"
RUNNING_ICONTITLE = "HH FFF"

CLOSING_TITLE     = "Hafren Haver: Innovations Anonymous"
CLOSING_ICONTITLE = "HH InnovAnon"

DEFAULT_CREDITS   = ('InnovAnon', 'Master Faust', 'Terry A. Davis', 'Lady Severn', 'Zantedeschia')

BLACK    = (0, 0, 0)
IA_BLACK = (0,   5, 0)
IA_RED   = (247, 0, 3)

class GUI:
	def __init__ (self, title=DEFAULT_TITLE, icontitle=DEFAULT_ICONTITLE, icon=DEFAULT_ICON, running_title=RUNNING_TITLE, running_icontitle=RUNNING_ICONTITLE, closing_title=CLOSING_TITLE, closing_icontitle=CLOSING_ICONTITLE, credits=DEFAULT_CREDITS, crfg=IA_RED, crbg=IA_BLACK, fullscreen=False, app=None):
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
		#self.clock = pygame.time.Clock ()
		
	def __enter__ (self):		
		self.entered     = True
		pygame.init ()
		mixer .init ()
		self.screen_info = display.Info  () #Required to set a good resolution for the game screen
		self.clock       = pygame.time   .Clock ()
		self.set_title      ()
		self.set_icon       ()
		self.set_app        ()
		self.set_fullscreen ()
		self.show_credits   ()
		return self	
	def __exit__ (self, type, value, traceback):
		self.running = False
		self.show_credits ()
		self.set_title (self.closing_title, self.closing_icontitle)
		mixer .quit ()
		pygame.quit ()
		self.entered = False
		return False
	def show_credits (self):
		assert self.entered
		df    = pygame.font.get_default_font ()
		font  = pygame.font.Font (df, 32)
		texts = (font.render (c, True, self.crfg, self.crbg) for c in self.credits)
		w = self.ss.get_width  ()
		h = self.ss.get_height ()
		n = len (self.credits)
		self.ss.fill (self.crbg)
		for text, i in zip (texts, range (0, n)):
			rect  = text.get_rect ()
			rect.center = (round (w / 2), round (h * (i / n) + h * (1 / (2 * n))))
			self.ss.blit (text, rect)
		pygame.display.update()
		#self.clock.tick (.1)
		
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
			self.      screen = display.set_mode (self.first_screen, FULLSCREEN)
		else:
			toolbar_height = 120 # TODO
			self.first_screen = (screen_info.current_w, screen_info.current_h - toolbar_height)
			self.      screen = display.set_mode (self.first_screen, RESIZABLE)
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
		while self.running: self.run_loop ()
		if self.app is not None: self.app. stop_running ()
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
		
		if self.app is not None: self.app.run_loop (keys)
		
if __name__ == "__main__":
	def main ():
		with GUI () as g: g.run ()
	main ()
	quit ()
	
