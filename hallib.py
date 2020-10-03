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
		
def parse_command (text):
	text = text.lower ()        # normalize
	toks = tokenize_command (text) # tokenize
	toks = filter_stopwords (toks) # filter cruft
	#toks = stem_tokens      (toks)
	toks = lemmatize_tokens (toks) # further normalization
	# TODO handle nato here ? numbers are nightmarish in the ebnf
	#ast  = translate_tokens (toks) # translate to IR
	#evs  =   compile_tokens (ast)  # convert to pygame.Event
	evs = translate_tokens (toks) # compile to pygame.Event
	return evs
	
#from hal_parser import BAASParser
import tatsu
translate_db = {}
def translate_tokens (tokens, semantics=None):
	if semantics is None: semantics = get_semantics ()
	if (tokens, semantics) in translate_db: return translate_db[(tokens, semantics)]
	text   = " ".join (tokens)
	if not len (text): return None
	parser = get_parser ()
	#parser = BAASParser ()
	try: ast = parser.parse (text, semantics=semantics)
	except tatsu.exceptions.FailedToken as e:
		ast = None
		print (e)
	print ("ast: %s" % (ast,))
	translate_db[(tokens, semantics)] = ast
	return ast
parser_db = {}
def get_parser (ebnf='hal.ebnf'):
	if ebnf in parser_db: return parser_db[ebnf]
	with open (ebnf, 'r') as f: grammar = f.read ()
	model = tatsu.compile (grammar)
	parser_db[ebnf] = model
	return model
from hallang import HALLang
semantics_db = {}
def get_semantics (k=HALLang):
	if k in semantics_db: return semantics_db[k]
	r = k ()
	semantics_db[k] = r
	return r

"""
from itertools import chain
#compile_db = {}
def   compile_tokens (ast):
	if ast is None: return None
	ast = tuple (ast)
	#if ast in compile_db: return compile_db[ast]
	evs = map (compile_node, ast)	
	evs = tuple (evs)
	evs = chain (*evs)
	evs = tuple (evs)
	print ("events: %s" % (evs,))
	#compile_db[ast] = evs
	return evs

def compile_node (node):
	print ("compile_node (%s)" % (node,))
	if node[0] == 'terminate': return compile_terminate    (node)
	if node[0] ==    'hold':   return compile_hold_keys    (node)
	if node[0] == 'release':   return compile_release_keys (node)
	if node[0] ==   'press':   return compile_press_keys   (node)
	raise Exception ()


def compile_terminate (node): return (Event (QUIT),)

def compile_hold_keys (node):
	assert node[0] in ['hold', 'press']
	node = node[1:]
	assert len (node) == 1
	node = node[0]
	ret = map (compile_hold_key, node)
	ret = tuple (ret)
	return ret

def compile_hold_key (node): # KEYDOWN: unicode, key, mod
	print ("compile_hold_key (%s)" % (node,))
	uc = 0 # ?
	k  = 0 # ?
	m  = 0 # ?
	return Event (KEYDOWN, unicode=uc, key=k, mod=m)

def compile_release_keys (node):
	assert node[0] in ['release', 'press']
	node = node[1:]
	assert len (node) == 1
	node = node[0]
	ret = map (compile_release_key, node)
	ret = tuple (ret)
	return ret

def compile_release_key (node): # KEYUP: key, mod
	print ("compile_release_key (%s)" % (node,))
	k = 0 # ?
	m = 0 # ?
	return Event (KEYUP, key=k, mod=m)

def compile_press_keys (node):
	print ("compile_press_keys (%s)" % (node,))
	assert node[0] == 'press'
	
	
	# TODO
	#assert len (node) == 1
	#node = node[0]
	
	
	
	if node[-1] == 'multiplier':
		multiplier = compile_multiplier (node[-1])
		node       = node[:-1]
	else: multiplier = compile_multiplier (None)
	hk = compile_hold_keys    (node)
	rk = compile_release_keys (node)
	return (*hk, *rk) * multiplier
def compile_multiplier (node):
	print ("compile_multiplier (%s)" % (node,))
	if node is None: return 1
	text = node[-1]
	node = node[:-1]
	assert text in ('time', 'times')
	node = ''.join (node)
	node = int (node)
	return node
"""
	
from nltk.tokenize import word_tokenize	
def tokenize_command (text):
	print ("tokenize_command (%s)" % (text,))
	toks = word_tokenize (text)
	toks = tuple (toks)
	#print ("tokens: %s" % (toks,))
	return toks

from nltk.corpus   import stopwords	
def filter_stopwords (toks):
	print ("filter_stopwords (%s)" % (toks,))
	sw   = stopwords.words ('english')
	f    = lambda token: token not in sw
	toks = filter (f, toks)
	toks = tuple (toks)
	#print ("filtered: %s" % (toks,))
	return toks

from nltk.stem     import PorterStemmer
def stem_tokens (toks):
	print ("stem_tokens (%s)" % (toks,))
	stem = PorterStemmer()
	f    = lambda token: stem.stem (token)
	toks = map (f, toks)
	toks = tuple (toks)
	#print ("stemmed: %s" % (toks,))
	return toks
	
from nltk.stem import WordNetLemmatizer
def lemmatize_tokens (toks):
	print ("lemmatize_tokens (%s)" % (toks,))
	lemm = WordNetLemmatizer()
	f    = lambda token: lemm.lemmatize (token)
	toks = map (f, toks)
	toks = tuple (toks)
	#print ("lemmed: %s" % (toks,))
	return toks
	
# TODO
#import nltk
#nltk.download ()
				
if __name__ == "__main__":
	print (parse_command ("terminate"))
	
	print (parse_command ("hold         alpha"))
	print (parse_command ("hold    key  alpha"))
	print (parse_command ("hold         alpha sierra sierra hotel oscar lima echo"))
	print (parse_command ("hold    keys alpha sierra sierra hotel oscar lima echo"))
	
	print (parse_command ("release      sierra"))
	print (parse_command ("release key  sierra"))
	print (parse_command ("release      sierra hotel india tango bravo alpha golf"))
	print (parse_command ("release keys sierra hotel india tango bravo alpha golf"))
	
	print (parse_command ("press        whiskey"))
	print (parse_command ("press   key  whiskey"))
	print (parse_command ("press        whiskey tango foxtrot"))
	print (parse_command ("press   keys whiskey tango foxtrot"))
	
	print (parse_command ("press        whiskey repeat two"))
	print (parse_command ("press   key  whiskey repeat two"))
	print (parse_command ("press        whiskey repeat two times"))
	print (parse_command ("press   key  whiskey repeat two times"))

	print (parse_command ("press        whiskey tango foxtrot repeat two"))
	print (parse_command ("press   keys whiskey tango foxtrot repeat two"))
	print (parse_command ("press        whiskey tango foxtrot repeat two times"))
	print (parse_command ("press   keys whiskey tango foxtrot repeat two times"))
	
	# TODO multiple commands
	
	quit ()
	
