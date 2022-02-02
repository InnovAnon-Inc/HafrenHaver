#! /usr/bin/env python3

#from numba  import jit

import pygame
from pygame.locals import *

import math
from math import log

from datetime import datetime

class Audio:
	def __init__(self, sample_rate, bits):
		pygame.mixer.pre_init(frequency=sample_rate, size=-bits, channels=2)
		pygame.init()
		self.sample_rate = sample_rate
		self.bits        = bits
	def __del__(self): pygame.quit()
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




if __name__ == "__main__":
	#from time import sleep

	def main ():
		sample_rate = 44100
		bits        = 16
		duration    = 10
		audio = Audio(sample_rate, bits)
		sound = Sound(audio, duration)

		#for k in range(duration): sound.sine_wave(432, 0.5, k)

		#buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
		#arr = stereo_sine_wave(0, n_samples, n_samples, pitch1)
		#print("arr: %s" % (arr,))
		#buf = buf + arr

		#pitch1 = 432
		#pitch2 = 7.83 / 2
		#pitch3 = 1
		sound.add_wave(sound.sine_wave, pitch2, duration, 1.0, 0)
		#sound.add_waves(sound.sine_waves_1, pitch2, duration, 1.0, 0)
		sound.add_wave(sound.sine_wave, pitch1, duration, 0.5, 0)
		#for k in range(int(round(duration * pitch1))): sound.add_waves(sound.sine_waves_1, 432.0 * 3 / 2, 0.5 / pitch1, 0.25, float(k) / pitch1)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_2, 432,           0.5 / pitch3, 0.25, float(k) / pitch3)
		#sound.add_waves(sound.sine_waves_2, pitch1, duration, 1.0, 0)
		#sound.add_waves(sound.sine_waves_1, pitch1, duration, 1.0, 0)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_1, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_2, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch3))): sound.add_wave(sound.sine_wave, pitch1, 0.5 / pitch3, 1.0, k / pitch3)

		#for k in range(int(round(duration * pitch3))): sound.add_wave(sound.sine_waves_1, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch2))): play(buf, pitch2, 0.5 / pitch2, k / pitch2)

		#sound = pygame.sndarray.make_sound(buf)
		#play once, then loop forever
		#sound.play(loops = 1)

		sound.play_sound()
		#sleep(0.1)
		#sleep(duration)
		#pygame.time.delay(1000)
		while pygame.mixer.music.get_busy(): pygame.time.Clock().tick()

		#pygame.quit()
	main ()
