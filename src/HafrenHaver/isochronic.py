#! /usr/bin/env python3

from enum   import Enum
#from numba  import jit
from random import choice

import pygame
from pygame.locals import *

import numpy
import math
from math import log

from chromatic import ratios_db

from datetime import datetime

# base frequency of water
# scale/chord intervals
# isochronic frequency

# subliminal_frequency = base_frequency * ratio * pow (2, octave)

# valid chords: reduce (lambda a, b: a * b, ratios + subliminal_frequency) <= subliminal_frequency




def isochronic ():
	bits = 16
	#the number of channels specified here is NOT 
	#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

	pygame.mixer.pre_init(44100, -bits, 2)
	pygame.init()
	
	duration = 10.0          # in seconds
	#freqency for the left speaker
	#frequency_l = 440
	#frequency for the right speaker
	#frequency_r = 550

	#this sounds totally different coming out of a laptop versus coming out of headphones
	sample_rate = 44100

	#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
	max_sample = 2**(bits - 1) - 1

	def play (pitch, duration):
		frequency_l = pitch
		frequency_r = pitch
		n_samples   = int(round(duration*sample_rate))
		buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
		for s in range(n_samples):
			t = float(s)/sample_rate    # time in seconds

			#grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
			buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
			buf[s][1] = int(round(max_sample*math.sin(2*math.pi*frequency_r*t)))    # right

		sound = pygame.sndarray.make_sound(buf)
		#play once, then loop forever
		sound.play(loops = 1)

	scale   = ratios_db[5][0]
	max_hz  = 12
	carrier = 432
	octave  = - int (log (carrier / max_hz) / log (2)) - 1
	rem     = 0
	
	while True:
		print ("octave: %s" % (octave,))
		for degree in range (len (scale))[::-1]:
			#print ("test: %s" % (carrier * pow (2, octave),))
			pitch  = carrier * scale[degree] * pow (2, octave)
			print ("pitch: %s" % (pitch,))
			print (datetime.utcnow ())
			time   = 1 / pitch
			assert time <= duration
			d      = duration + rem
			pulses = round (d * pitch)
			#print ("pulses: %s" % (pulses,))
			for k in range (pulses): play (carrier, time)
			rem    = duration - pulses * time
			#print ("rem: %s" % (rem,))
		octave = octave - 1
	
	pygame.quit()


if __name__ == "__main__":
	def main ():
		isochronic ()
	main ()
	
