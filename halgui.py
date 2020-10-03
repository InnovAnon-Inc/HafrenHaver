#! /usr/bin/env python3

import speech_recognition as sr                                         # import the library

def get_response (r, audio):		
	# set up the response object
	response = {
		"success"      : True,
		"error"        : None,
		"transcription": None,
	}

	# https://www.codesofinterest.com/2017/03/python-speech-recognition-pocketsphinx.html
	try: response["transcription"] = r.recognize_sphinx (audio)     # try recognizing the speech in the recording
	except sr.RequestError:                                         # API was unreachable or unresponsive
		response["success"] = False
		response["error"  ] = "API unavailable/unresponsive"
	except sr.UnknownValueError:                                    # speech was unintelligible
		response["error"  ] = "Unable to recognize speech"
	except sr.WaitTimeoutError:                                     # bad params ?
		response["error"  ] = "Wait timeout"
	return response

from audio_gui import AudioGUI

class HalGUI (AudioGUI):
	def __init__ (self, r=None, m=None, *args, **kwargs):
		AudioGUI.__init__ (self, *args, **kwargs)
		if r is None: r = sr.Recognizer ()
		self.r = r
		if m is None: m = sr.Microphone ()
		self.m = m
			
	def run_enter (self):
		r = self.r 
		m = self.m
		# https://www.codesofinterest.com/2017/04/energy-threshold-calibration-in-speech-recognition.html
		with self.m as source: r.adjust_for_ambient_noise (source)
		r.dynamic_energy_threshold = True
		
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
		
		command = parse_command (text)
		for e in command: pygame.event.post (e)
		
def parse_command (text):
	text = text.to_lower ()        # normalize
	toks = tokenize_command (text) # tokenize
	toks = filter_stopwords (toks) # filter cruft
	#toks = stem_tokens      (toks)
	toks = lemmatize_tokens (toks) # further normalization
	toks = translate_tokens (toks) # translate to IR
	toks =   compile_tokens (toks)
	return toks
	
from hal_parser import BAASParser
def translate_tokens (tokens):
	text   = "".join (tokens)
	parser = BAASParser ()
	ast    = parser.parse (text)
	return ast
	
def   compile_tokens (ast):
	# TODO convert to pygame.Event
	
	return ast
	
from nltk.tokenize import sent_tokenize	
def tokenize_command (text):
	toks = sent_tokenize (text)
	toks = tuple (toks)
	print ("tokens: %s" % (toks,))
	return toks

from nltk.corpus   import stopwords	
def filter_stopwords (toks):
	sw   = stopwords.words ('english')
	f    = lambda token: token not in sw
	toks = filter (f, toks)
	toks = tuple (toks)
	print ("filtered: %s" % (toks,))
	return toks

from nltk.stem     import PorterStemmer
def stem_tokens (toks):
	stem = PorterStemmer()
	f    = lambda token: stem.stem (token)
	toks = map (f, toks)
	toks = tuple (toks)
	print ("stemmed: %s" % (toks,))
	return toks
	
from nltk.stem import WordNetLemmatizer
def lemmatize_tokens (toks):
	lemm = WordNetLemmatizer()
	f    = lambda token: lemm.lemmatize (token)
	toks = map (f, toks)
	toks = tuple (toks)
	print ("lemmed: %s" % (toks,))
	return toks
	
#import nltk
#nltk.download ()
				
if __name__ == "__main__":
	def main ():
		with HalGUI (exit_on_close=False) as g: g.run ()
	main ()
	print ("end main")
	quit ()
	sys.exit ()
