#! /usr/bin/env python3

import speech_recognition as sr                                         # import the library

from audio_gui import AudioGUI

class HalGUI (AudioGUI):
	def __init__ (self, mic, *args, **kwargs):
		GUI.__init__ (self, *args, **kwargs)
		self.mic = mic
		
	def run0 (self): # https://www.codesofinterest.com/2017/04/energy-threshold-calibration-in-speech-recognition.html
		AudioGUI.run0 (self)
		r.adjust_for_ambient_noise (source, duration=5)
		r.dynamic_energy_threshold = True   
		
	def run_enter (self):
		AudioGUI.run_enter (self)
		# TODO setup loop:
		print ("Speak Anything :")
		audio = r.listen (source)                                           # listen to the source
		try: # https://www.codesofinterest.com/2017/03/python-speech-recognition-pocketsphinx.html
			text = r.recognize_sphinx (audio)                               # use recognizer to convert our audio into text part.
			print ("You said : {}".format (text))
		except: print ("Sorry could not recognize your voice")              # In case of voice not recognized  clearly
				
	def run_leave (self):
		AudioGUI.run_leave (self)
		
	# command process:
	# - transliterate: specify alphabet, including nato
	# - check for word matches... i.e., "shift", "hold ctrl", etc
				
	#def run_loop (self):
	#	# process hal event queue, then
	#	AudioGUI.run_loop (self)
		
if __name__ == "__main__":
	def main ():
		r = sr.Recognizer ()                                            # initialize recognizer
		with sr.Microphone () as mic:                                   # mention source it will be either Microphone or audio files.
			with HalGUI (mic, exit_on_close=False) as g: g.run ()
	main ()
	print ("end main")
	quit ()
	sys.exit ()
