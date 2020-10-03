#! /usr/bin/env python3

import speech_recognition as sr                                         # import the library

from audio_gui import AudioGUI
from hallib import get_response, parse_command

import pygame

class HAL9000 (AudioGUI): # Heuristically Programmed ALgorithmic Computer
	def __init__ (self, r=None, m=None, *args, **kwargs):
		AudioGUI.__init__ (self, *args, **kwargs)
		if r is None: r = sr.Recognizer ()
		self.r = r
		if m is None: m = sr.Microphone ()
		self.m = m
			
	def run_enter (self):
		r = self.r 
		m = self.m
		print ("HAL is adjusting for ambient noise")
		# https://www.codesofinterest.com/2017/04/energy-threshold-calibration-in-speech-recognition.html
		with self.m as source: r.adjust_for_ambient_noise (source)
		r.dynamic_energy_threshold = True
		print ("HAL is online")
		
		AudioGUI.run_enter (self)
		
		# https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py
		self.stop_listening = r.listen_in_background (m, self.callback)
				
	def run_leave (self):
		self.stop_listening (wait_for_stop=False)
		AudioGUI.run_leave (self)
	
	def callback (self, recognizer, audio):
		response = get_response (recognizer, audio)
		self.handle_response (response)
	
	def handle_response (self, response):
		if not self.running: return
		
		if not response['success']:
			print ("error: %s" % (response['error'],))
			self.running = False
			return
		if response['error'] is not None:
			print ("error: %s" % (response['error'],))
			return
		
		text = response['transcription']
		print ("text: %s" % (text,))
		
		events = parse_command (text)
		if events is None: return
		for e in events: pygame.event.post (e)
	
# TODO
#import nltk
#nltk.download ()
				
if __name__ == "__main__":
	def main ():
		with HAL9000 (exit_on_close=False) as g: g.run ()
	main ()
	print ("end main")
	quit ()
