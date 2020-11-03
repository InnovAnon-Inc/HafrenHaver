#! /usr/bin/env python3

from play import random_audio
from draw import Graphics

class AV:
	def __init__ (self, audio, graphics):
		self.audio    = audio
		self.graphics = graphics
	def append_audio (self, bar):
		r = self.audio.rest
		d = bar * (r * 2) - r
		self.audio.append_sinewave (duration_milliseconds=d)
		self.audio.append_silence  (duration_milliseconds=r)
	def append_graphics (self, bar):
		r = self.audio.rest
		D = bar * (r * 2)
		self.graphics.append (duration_milliseconds=D)
	def append (self, bar):
		self.append_audio    (bar)
		self.append_graphics (bar)
	def save (self):
		afname = "test.wav"
		gfname = "test.gif"
		fname  = "test.mp4"
		self.audio.save_wav (afname)
		self.graphics.save  (gfname)
		# TODO merge results
def random_av (a=None, a_args=(), g=None, g_args=()):
	if a is None: a = random_audio (*a_args)
	if g is None: g = Graphics     (*g_args)
	return AV (a, g)
