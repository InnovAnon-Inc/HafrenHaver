#! /usr/bin/env python3

import speech_recognition as sr                                         # import the library

from audio_gui import AudioGUI

from constants import DEFAULT_EXIT_TIMEOUT

import threading
import sys
import os

class HalGUI (AudioGUI):
	def __init__ (self, r=None, mic=None, exit_mic=None, *args, **kwargs):
		AudioGUI.__init__ (self, *args, **kwargs)
		if r is None: r = sr.Recognizer () # initialize recognizer
		self.r        = r
		self.mic      = mic                               
		self.exit_mic = exit_mic
	#def run0 (self): # https://www.codesofinterest.com/2017/04/energy-threshold-calibration-in-speech-recognition.html
	#	AudioGUI.run0 (self)   
		
	def enter1 (self):
		AudioGUI.enter1 (self)

		mic = self.mic
		if mic is None:
			if self.exit_mic is None: self.exit_mic = True
			mic = sr.Microphone () # mention source it will be either Microphone or audio files.   
			mic.__enter__ ()
		self.mic = mic
		
		self.x = threading.Thread (target=self.listen)
		self.x.start ()
	
	def listen (self):
		r = self.r
		r.adjust_for_ambient_noise (self.mic, duration=5) # TODO account for exit timeout
		r.dynamic_energy_threshold = True
		
		timeout = 10 # TODO
		ptl     = 10
		while self.running:
			self.listen_loop (timeout, ptl)
		
			
	def listen_loop (self, timeout, ptl):
		print ("enter halgui.listen_loop ()")
		response = self.get_response (timeout, ptl)
		print ("response: %s" % (response,))
		
		if not response['success']:
			print ("error: %s" % (response['error'],))
			self.running = False
			return
		if response['error'] is not None:
			print ("error: %s" % (response['error'],))
			return
		
		text = response['transcription']
		print ("text: %s" % (text,))
		
		print ("leave halgui.listen_loop ()")
		
			# command process:
	# - transliterate: specify alphabet, including nato
	# - check for word matches... i.e., "shift", "hold ctrl", etc... window-resizing commands
				
	#def run_loop (self):
	#	# process hal event queue, then
	#	AudioGUI.run_loop (self)
		
		
	def get_response (self, timeout, ptl):
		r = self.r
		
		# set up the response object
		response = {
			"success"      : True,
			"error"        : None,
			"transcription": None,
		}

		# https://www.codesofinterest.com/2017/03/python-speech-recognition-pocketsphinx.html
		audio = r.listen (self.mic, timeout, phrase_time_limit=ptl)     # listen to the source
		try: response["transcription"] = r.recognize_sphinx (audio)     # try recognizing the speech in the recording
		except sr.RequestError:                                         # API was unreachable or unresponsive
			response["success"] = False
			response["error"  ] = "API unavailable/unresponsive"
		except sr.UnknownValueError:                                    # speech was unintelligible
			response["error"  ] = "Unable to recognize speech"
		except sr.WaitTimeoutError:                                     # bad params ?
			response["error"  ] = "Wait timeout"
		return response
		
	def exit0 (self, type, value, traceback):
		x = self.x
		AudioGUI.exit0 (self, type, value, traceback)
		if self.exit_on_close:
			x.join (DEFAULT_EXIT_TIMEOUT)
			if x.is_alive (): # TODO
				pass
		else: x.join ()
		if self.mic is not None and self.exit_mic: self.mic.__exit__ (type, value, traceback)
		
if __name__ == "__main__":
	def main ():
		with HalGUI (exit_on_close=True) as g: g.run ()
	main ()
	print ("end main")
	quit ()
	sys.exit ()
