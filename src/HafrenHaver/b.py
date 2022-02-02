#! /usr/bin/env python3

LAMBDA  = (200    , 400  )
GAMMA   = ( 26    , 100  )
BETA    = ( 13    ,  32  )
ALPHA   = (  8    ,  13  )
THETA   = (  4    ,   8  )
DELTA   = (  0.500,   4  )
EPSILON = (  0.025,   0.5)

# TODO bf0, bf1, tempo, carrier frequency, harmonic complexity?, ...

import numpy
import math
import pygame
from scipy.constants import golden as phi
from math import ceil, floor, log
from random import choice

bits = 16
#the number of channels specified here is NOT 
#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels
pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
size = (1366, 720)
display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

#this sounds totally different coming out of a laptop versus coming out of headphones
sample_rate = 44100
#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
max_sample = 2**(bits - 1) - 1


def get_frequencies (base_frequency, scale):
	n1       = floor (log (base_frequency / EPSILON[0]) / log(2))
	print ("n1: %s" % (n1,))
	f1       = base_frequency / (2 ** n1)
	print ("f1: %s" % (f1,))
	pitches1 = map    (lambda p: f1 * p,                              scale)
	pitches1 = list (pitches1)
	print ("pitches1: %s" % (pitches1,))
	pitches1 = filter (lambda p: EPSILON[0] <= p and p <= EPSILON[1], pitches1)
	pitches1 = list (pitches1)
	print ("pitches1: %s" % (pitches1,))
	assert len (pitches1)
	pitch1   = choice (pitches1)

	n2       = floor (log (base_frequency / LAMBDA[0])  / log(2))
	print ("n2: %s" % (n2,))
	f2       = base_frequency / (2 ** n2)
	print ("f2: %s" % (f2,))
	pitches2 = map	  (lambda p: f2 * p,                              scale)
	pitches2 = list (pitches2)
	print ("pitches2: %s" % (pitches2,))
	pitches2 = filter (lambda p: LAMBDA[0]  <= p and p <= LAMBDA[1],  pitches2)
	pitches2 = list (pitches2)
	print ("pitches2: %s" % (pitches2,))
	assert len (pitches2)
	pitch2   = choice (pitches2)

	# TODO
	duration = 1000

	return pitch1, pitch2, duration

base_frequency = 432
scale = [1/1,  16/ 15,  9/8,  6/ 5,  5/ 4, 4/3,   45/ 32, 3/2,   8/ 5,  5/ 3,  9/5,  15/  8]

epsilon_amplitude =              phi
lambda_amplitude  = max_sample - phi

epsilon_frequency, lambda_frequency, duration = get_frequencies (base_frequency, scale)
epsilon_frequency_l = epsilon_frequency
epsilon_frequency_r = epsilon_frequency
lambda_frequency_l  = lambda_frequency
lambda_frequency_r  = lambda_frequency

n_samples = int(round(duration*sample_rate))
   
print ("creating buf")
buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
for s in range(n_samples):
	t = float(s)/sample_rate    # time in seconds

	l_tmp = 0
	r_tmp = 0

	l_tmp = l_tmp + epsilon_amplitude * math.sin (2 * math.pi * epsilon_frequency_l * t)
	r_tmp = r_tmp + epsilon_amplitude * math.sin (2 * math.pi * epsilon_frequency_r * t)

	l_tmp = l_tmp +  lambda_amplitude * math.sin (2 * math.pi *  lambda_frequency_l * t)
	r_tmp = r_tmp +  lambda_amplitude * math.sin (2 * math.pi *  lambda_frequency_r * t)

	buf[s][0] = int (round (l_tmp))
	buf[s][1] = int (round (r_tmp))
print ("done creating buf")

sound = pygame.sndarray.make_sound(buf)
#play once, then loop forever
sound.play(loops = 1)
print ("done playing")
pygame.quit()
print ("exiting")









