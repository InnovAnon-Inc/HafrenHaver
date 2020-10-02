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


from gui import GUI

# TODO use scales to select better tick speeds
	
	

#print (reasonable_minmax_int_pitch (4, DEFAULT_SCALE, 30, 60))
#print (reasonable_minmax_int_pitch (1 / 7.83, DEFAULT_SCALE, 30, 60))
#print (reasonable_minmax_int_pitch (7.83, DEFAULT_SCALE, 1 / 30, 1 / 60))




from resize_gui import ResizeGUI

from constants import DEFAULT_BACKGROUND

class DecoratedGUI (ResizeGUI):
	def __init__ (self, title=DEFAULT_TITLE, icontitle=DEFAULT_ICONTITLE, icon=DEFAULT_ICON, running_title=RUNNING_TITLE, running_icontitle=RUNNING_ICONTITLE, closing_title=CLOSING_TITLE, closing_icontitle=CLOSING_ICONTITLE, credits=DEFAULT_CREDITS, subliminal_threshold=DEFAULT_SUBLIMINAL_THRESHOLD, crfg=IA_RED, crbg=IA_BLACK, *args, **kwargs):
		ResizeGUI.__init__ (self, *args, **kwargs)
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
		self.subliminal_threshold = subliminal_threshold
		self.ss = None
		#self.set_background_file (background)
		
	def enter0 (self):
		ResizeGUI.enter0 (self)
		self.set_title      ()
		self.set_icon       ()
	def enter1 (self):
		ResizeGUI.enter1 (self)
		self.clock.tick ()
		#self.set_fullscreen ()
		self.show_credits   ()
		#self.set_background ()
		self.clock.tick (self.subliminal_threshold)
	def exit0 (self):
		ResizeGUI.exit0 (self)
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
	"""	
	def set_background_file (self, background_file=None):
		if background_file is None: background_file = self.background_file
		else: self.background_file = background_file
		raw_background = pygame.image.load (background_file)
		self.set_raw_background (raw_background)
	def set_raw_background (self, raw_background=None):
		if raw_background is None:
			self.set_background_file ()
			raw_background = self.raw_background
		else: self.raw_background = raw_background
		if self.ss is None: return
		w = self.ss.get_width  ()
		h = self.ss.get_height ()
		background = pygame.transform.scale (raw_background.convert_alpha (), (w, h))
		self.set_background (background)
	def set_background (self, background=None):
		if background is None:
			self.set_raw_background ()
			background = self.background
		else: self.background = background
		self.ss.fill (BLACK)
		self.ss.blit (background, ORIGIN)
		pygame.display.update()
	"""
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
	
	#def set_app (self, app=None):
	#	self.set_title      ()
	#	self.set_icon       ()
	#	GUI.set_app (app)
	
	def run (self):
		self.run0 ()
		GUI.run (self)
	def run0 (self): self.set_title (self.running_title, self.running_icontitle)
		
	#def set_fullscreen (self, fullscreen=None):
	#	ResizeGUI.set_fullscreen (self, fullscreen)
	#	self.set_background ()
		
if __name__ == "__main__":
	def main ():
		with DecoratedGUI (exit_on_close=False) as g: g.run ()
	main ()
	print ("end main")
	quit ()
	sys.exit ()
