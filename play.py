# https://stackoverflow.com/questions/33879523/python-how-can-i-generate-a-wav-file-with-beeps

import math
from math import pi
import wave
import struct
from pygame import mixer

from solfeggio import random_solfeggio

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in 
# memory.
class Audio:
	def __init__ (self, solfeggio, sample_rate=44100.0, rest=500):
		self.audio       = []
		self.sample_rate = sample_rate
		self.rest        = rest
		self.solfeggio   = solfeggio
		self.fname       = None
	def append_silence (self, duration_milliseconds=None):
		if duration_milliseconds is None: duration_milliseconds = self.rest
		"""
		Adding silence is easy - we add zeros to the end of our array
		"""
		num_samples = duration_milliseconds * (self.sample_rate / 1000.0)
		for x in range (int (num_samples)): self.audio.append (0.0)	
		self.fname = None
	def append_sinewave (self, freq=None, duration_milliseconds=None, volume=1.0):
		if freq is None: freq = self.solfeggio.base_frequency
		if duration_milliseconds is None: duration_milliseconds = self.rest
		"""
		The sine wave generated here is the standard beep.  If you want something
		more aggresive you could try a square or saw tooth waveform.   Though there
		are some rather complicated issues with making high quality square and
		sawtooth waves... which we won't address here :) 
		""" 
		num_samples = duration_milliseconds * (self.sample_rate / 1000.0)
		for x in range (int (num_samples)): self.audio.append (volume * math.sin (2 * math.pi * freq * (x / self.sample_rate)))
		self.fname = None
	def save_wav (self, file_name="test.wav"):
		# Open up a wav file
		with wave.open (file_name, "w") as wav_file:
			# wav params
			nchannels = 1
			sampwidth = 2

			# 44100 is the industry standard sample rate - CD quality.  If you need to
			# save on file size you can adjust it downwards. The stanard for low quality
			# is 8000 or 8kHz.
			nframes = len (self.audio)
			comptype = "NONE"
			compname = "not compressed"
			wav_file.setparams ((nchannels, sampwidth, self.sample_rate, nframes, comptype, compname))

			# WAV files here are using short, 16 bit, signed integers for the 
			# sample size.  So we multiply the floating point data we have by 32767, the
			# maximum value for a short integer.  NOTE: It is theortically possible to
			# use the floating point -1.0 to 1.0 data directly in a WAV file but not
			# obvious how to do that using the wave module in python.
			for sample in self.audio: wav_file.writeframes (struct.pack ('h', int (sample * 32767.0)))

		#wav_file.close()
		self.fname = file_name
	def play (self):
		if self.fname is None: self.save_wav ()
		fname = self.fname
		
		# Starting the mixer 
		mixer.init ()

		# Loading the song 
		mixer.music.load (fname) 

		# Setting the volume 
		mixer.music.set_volume (0.7) 

		# Start playing the song 
		mixer.music.play () 

		"""
		# infinite loop 
		while True: 
			
			print("Press 'p' to pause, 'r' to resume") 
			print("Press 'e' to exit the program") 
			query = input(" ") 
			
			if query == 'p': 

				# Pausing the music 
				mixer.music.pause()	 
			elif query == 'r': 

				# Resuming the music 
				mixer.music.unpause() 
			elif query == 'e': 

				# Stop the mixer 
				mixer.music.stop() 
				break
		"""

def random_audio (s=None):
	if s is None: s = random_solfeggio ()
	return Audio (s)
