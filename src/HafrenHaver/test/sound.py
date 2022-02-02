#! /usr/bin/env python3

#from numba  import jit

import pygame
from pygame.locals import *

import math
from math import log

from datetime import datetime

import numpy

class Sound:
	def __init__(self, audio, duration):
		self.audio     = audio
		sample_rate    = self.audio.sample_rate
		self.n_samples = int(round(duration*sample_rate))
		#self.buf       = numpy.zeros((self.n_samples, 2), dtype=numpy.float)
		self.dt        = numpy.int16
		#self.buf       = numpy.zeros((self.n_samples, 2), dtype=self.dt)
		self.buf       = numpy.zeros((self.n_samples, 2))
	def make_sound(self):
		#max_sample = numpy.iinfo(numpy.int16).max
		#buf        = (self.buf * max_sample).astype(numpy.int16)
		#print("buf: %s" % (buf,))
		buf        = self.buf
		max_sample = numpy.iinfo(self.dt).max
		buf        = numpy.int16(buf / numpy.max(numpy.abs(buf)) * max_sample)
		return pygame.sndarray.make_sound(buf)
	def play_sound(self, loops=1):
		sound = self.make_sound()
		sound.play(loops=loops)
		pygame.time.wait(int(sound.get_length() * 1000))
	def sine_wave(self, pitch, duration, volume):
		print("sine_wave(pitch=%s, duration=%s, volume=%s)" % (pitch, duration, volume,))
		sample_rate = self.audio.sample_rate
		max_sample  = numpy.iinfo(self.dt).max
		assert max_sample == 2**(self.audio.bits - 1) - 1
		volume      = volume * max_sample

		size        = int(round(sample_rate * duration))
		#temp        = numpy.arange(0, size) / sample_rate
		#temp        = numpy.linspace(0, size, size)
		temp        = numpy.linspace(0, duration, size, False)
		temp        = volume * numpy.sin(2.0 * numpy.pi * pitch * temp)
		temp        = self.dt(temp)
		#temp        = numpy.vstack((temp, temp)).reshape((-1, 2), order='F')
		temp        = numpy.repeat(temp.reshape(size, 1), 2, axis = 1)
		return temp
	def sine_waves_1(self, pitch, duration, volume):
		print("sine_waves_1(pitch=%s, duration=%s, volume=%s)" % (pitch, duration, volume,))
		sample_rate = self.audio.sample_rate
		max_sample  = numpy.iinfo(self.dt).max
		assert max_sample == 2**(self.audio.bits - 1) - 1
		#volume      = volume * max_sample
		size        = int(round(sample_rate * duration))
		return (self.sine_wave(pitch * 2**v, duration, volume / 2**v) for v in range(int(round(log(volume * max_sample)))))
		#return (self.sine_wave(pitch * 2**v, duration, volume / 2**v) for v in range(4))
	def sine_waves_2(self, pitch, duration, volume):
		print("sine_waves_1(pitch=%s, duration=%s, volume=%s)" % (pitch, duration, volume,))
		sample_rate = self.audio.sample_rate
		max_sample  = numpy.iinfo(self.dt).max
		assert max_sample == 2**(self.audio.bits - 1) - 1
		#volume      = volume * max_sample
		size        = int(round(sample_rate * duration))
		#return (self.sine_wave(pitch * 2**v, duration, volume / 2**v) for v in range(int(round(log(volume * max_sample)))))
		return (self.sine_wave(pitch * 2**v, duration, volume / (v + 1)) for v in range(int(round((log(20000 / pitch))))))

		#temp        = numpy.linspace(0, duration, size)
		#res         = numpy.zeros(size, dtype=self.dt)
		#for v in range(int(round(log(volume)))):
		#	#print("v: %s" % (2 ** v,))
		#	p       = pitch * 2**v
		#	V       = volume / 2**v
		#	t       = V * numpy.sin(2.0 * numpy.pi * p * temp)
		#	t       = self.dt(temp)
		#	res     = res + t
		#temp        = numpy.repeat(res.reshape(size, 1), 2, axis = 1)
		#return temp
	def add_wave(self, wave_func, pitch, duration, volume, offset):
		sample_rate = self.audio.sample_rate
		temp        = wave_func(pitch, duration, volume)
		start       = int(round(sample_rate *  offset))
		end         = int(round(sample_rate * (offset + duration)))
		buf         = self.buf
		#buf         = numpy.zeros((self.n_samples, 2))
		#for s in range(start, end - 1):
		for s in range(start, end):
			t = s - start
			buf[s][0] = buf[s][0] + temp[t][0]
			buf[s][1] = buf[s][1] + temp[t][1]
		max_sample  = numpy.iinfo(self.dt).max
		#self.buf = numpy.int16(buf / numpy.max(numpy.abs(buf)) * max_sample)
	def add_waves(self, wave_func, pitch, duration, volume, offset):
		sample_rate = self.audio.sample_rate
		temp        = wave_func(pitch, duration, volume)
		start       = int(round(sample_rate *  offset))
		end         = int(round(sample_rate * (offset + duration)))
		buf         = self.buf
		#buf         = numpy.zeros((self.n_samples, 2))
		for T in temp:
			for s in range(start, end - 1):
				t = s - start
				buf[s][0] = buf[s][0] + T[t][0]
				buf[s][1] = buf[s][1] + T[t][1]
		max_sample  = numpy.iinfo(self.dt).max
		#self.buf = numpy.int16(buf / numpy.max(numpy.abs(buf)) * max_sample)

