#! /usr/bin/env python3

import pygame
from pygame import mixer

from constants import DEFAULT_SAMPLE_RATE

from decorated_gui import DecoratedGUI

class AudioGUI (DecoratedGUI):
	def __init__ (self, sample_rate=DEFAULT_SAMPLE_RATE, *args, **kwargs):
		DecoratedGUI.__init__ (self, *args, **kwargs)
		self.sample_rate = sample_rate
		
	def __enter__ (self):		
		bits = 16 #the number of channels specified here is NOT 
		          #the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
		sr   = self.sample_rate
		pygame.mixer.pre_init (sr, -bits, 2)
		##mixer.init ()
		#pygame.init ()
		#mixer .init () # TODO proper order ?
		return DecoratedGUI.__enter__ (self)	
	# TODO handle keys for volume ?
		
if __name__ == "__main__":
	def main ():
		with AudioGUI (exit_on_close=False) as g: g.run ()
	main ()
	print ("end main")
	quit ()
	sys.exit ()
