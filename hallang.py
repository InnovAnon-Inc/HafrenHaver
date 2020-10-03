#! /usr/bin/env python3

from tatsu.ast import AST

import pygame
from pygame.event import Event
from pygame import QUIT, KEYDOWN, KEYUP

from itertools import starmap

alpha_db = {
	'backspace'         : pygame.K_BACKSPACE,
	'tab'               : pygame.K_TAB,
	'clear'             : pygame.K_CLEAR,
	'return'            : pygame.K_RETURN,
	'pause'             : pygame.K_PAUSE,
	'escape'            : pygame.K_ESCAPE,
	'space'             : pygame.K_SPACE,
	'exclaim'           : pygame.K_EXCLAIM,
	'quotedbl'          : pygame.K_QUOTEDBL,
	'hash'              : pygame.K_HASH,
	'dollar'            : pygame.K_DOLLAR,
	'ampersand'         : pygame.K_AMPERSAND,
	'quote'             : pygame.K_QUOTE,
	'left_parenthesis'  : pygame.K_LEFTPAREN,
	'right parenthesis' : pygame.K_RIGHTPAREN,
	'asterisk'          : pygame.K_ASTERISK,
	'plus'              : pygame.K_PLUS,
	'comma'             : pygame.K_COMMA,
	'minus'             : pygame.K_MINUS,
	'period'            : pygame.K_PERIOD,
	'slash'             : pygame.K_SLASH,
	0                   : pygame.K_0,
	1                   : pygame.K_1,
	2                   : pygame.K_2,
	3                   : pygame.K_3,
	4                   : pygame.K_4,
	5                   : pygame.K_5,
	6                   : pygame.K_6,
	7                   : pygame.K_7,
	8                   : pygame.K_8,
	9                   : pygame.K_9,
	'colon'             : pygame.K_COLON,
	'semicolon'         : pygame.K_SEMICOLON,
	'less than'         : pygame.K_LESS,
	'equals'            : pygame.K_EQUALS,
	'greater than'      : pygame.K_GREATER,
	'question'          : pygame.K_QUESTION,
	'at'                : pygame.K_AT,
	'left bracket'      : pygame.K_LEFTBRACKET,
	'backslash'         : pygame.K_BACKSLASH,
	'right bracket'     : pygame.K_RIGHTBRACKET,
	'caret'             : pygame.K_CARET,
	'underscore'        : pygame.K_UNDERSCORE,
	'grave'             : pygame.K_BACKQUOTE,
	'a'                 : pygame.K_a,
	'b'                 : pygame.K_b,
	'c'                 : pygame.K_c,
	'd'                 : pygame.K_d,
	'e'                 : pygame.K_e,
	'f'                 : pygame.K_f,
	'g'                 : pygame.K_g,
	'h'                 : pygame.K_h,
	'i'                 : pygame.K_i,
	'j'                 : pygame.K_j,
	'k'                 : pygame.K_k,
	'l'                 : pygame.K_l,
	'm'                 : pygame.K_m,
	'n'                 : pygame.K_n,
	'o'                 : pygame.K_o,
	'p'                 : pygame.K_p,
	'q'                 : pygame.K_q,
	'r'                 : pygame.K_r,
	's'                 : pygame.K_s,
	't'                 : pygame.K_t,
	'u'                 : pygame.K_u,
	'v'                 : pygame.K_v,
	'w'                 : pygame.K_w,
	'x'                 : pygame.K_x,
	'y'                 : pygame.K_y,
	'z'                 : pygame.K_z,
	'delete'            : pygame.K_DELETE,
	'keypad 0'          : pygame.K_KP0,
	'keypad 1'          : pygame.K_KP1,
	'keypad 2'          : pygame.K_KP2,
	'keypad 3'          : pygame.K_KP3,
	'keypad 4'          : pygame.K_KP4,
	'keypad 5'          : pygame.K_KP5,
	'keypad 6'          : pygame.K_KP6,
	'keypad 7'          : pygame.K_KP7,
	'keypad 8'          : pygame.K_KP8,
	'keypad 9'          : pygame.K_KP9,
	'keypad period'     : pygame.K_KP_PERIOD,
	'keypad divide'     : pygame.K_KP_DIVIDE,
	'keypad multiply'   : pygame.K_KP_MULTIPLY,
	'keypad minus'      : pygame.K_KP_MINUS,
	'keypad plus'       : pygame.K_KP_PLUS,
	'keypad enter'      : pygame.K_KP_ENTER,
	'keypad equals'     : pygame.K_KP_EQUALS,
	'up arrow'          : pygame.K_UP,
	'down arrow'        : pygame.K_DOWN,
	'right arrow'       : pygame.K_RIGHT,
	'left arrow'        : pygame.K_LEFT,
	'insert'            : pygame.K_INSERT,
	'home'              : pygame.K_HOME,
	'end'               : pygame.K_END,
	'page up'           : pygame.K_PAGEUP,
	'page down'         : pygame.K_PAGEDOWN,
	'f1'                : pygame.K_F1,
	'f2'                : pygame.K_F2,
	'f3'                : pygame.K_F3,
	'f4'                : pygame.K_F4,
	'f5'                : pygame.K_F5,
	'f6'                : pygame.K_F6,
	'f7'                : pygame.K_F7,
	'f8'                : pygame.K_F8,
	'f9'                : pygame.K_F9,
	'f10'               : pygame.K_F10,
	'f11'               : pygame.K_F11,
	'f12'               : pygame.K_F12,
	'f13'               : pygame.K_F13,
	'f14'               : pygame.K_F14,
	'f15'               : pygame.K_F15,
	'numlock'           : pygame.K_NUMLOCK,
	'capslock'          : pygame.K_CAPSLOCK,
	'scrollock'         : pygame.K_SCROLLOCK,
	'right shift'       : pygame.K_RSHIFT,
	'left shift'        : pygame.K_LSHIFT,
	'right control'     : pygame.K_RCTRL,
	'left control'      : pygame.K_LCTRL,
	'right alt'         : pygame.K_RALT,
	'left alt'          : pygame.K_LALT,
	'right meta'        : pygame.K_RMETA,
	'left meta'         : pygame.K_LMETA,
	'left windows key'  : pygame.K_LSUPER,
	'right windows key' : pygame.K_RSUPER,
	'mode shift'        : pygame.K_MODE,
	'help'              : pygame.K_HELP,
	'print screen'      : pygame.K_PRINT,
	'sysrq'             : pygame.K_SYSREQ,
	'break'             : pygame.K_BREAK,
	'menu'              : pygame.K_MENU,
	'power'             : pygame.K_POWER,
	'euro'              : pygame.K_EURO,
}	
	
class HALLang: # (noun, verb), sounds like "howling"
	def terminate (self, ast):
		print ("terminate (%s)" % (ast,))
		return (Event (QUIT),)
	#def hr_keys (self, ast):
	#	hr   = ast.left
	#	keys = ast.right
	#	Event (KEYDOWN, unicode=uc, key=k, mod=m)
	
	# TODO handle key modifiers
	
	def hold_keys (self, ast):
		print ("hold_keys (%s)" % (ast,))
		#f = lambda uc, k, m: Event (KEYDOWN, unicode=uc, key=k, mod=m)
		#t = starmap (f, ast.right)
		f = lambda key: Event (KEYDOWN, key=key, mod=pygame.KMOD_NONE)
		t = map (f, ast.right)
		t = tuple (t)
		return t
	def release_keys (self, ast):
		print ("release_keys (%s)" % (ast,))
		#f = lambda uc, k, m: Event (KEYUP, unicode=uc, key=k)
		#t = starmap (f, ast.right)
		f = lambda key: Event (KEYUP, key=key, mod=pygame.KMOD_NONE)
		t = map (f, ast.right)
		t = tuple (t)
		return t
		
	def keys (self, ast): return ast.right
	def alpha (self, ast):
		print ("alpha (%s)" % (ast,))
		ast = str (ast)
		#return pygame.key.key_code (ast)
		if ast in alpha_db: return alpha_db[ast]
		raise Exception ()
	def num (self, ast):
		print ("num (%s)" % (ast,))
		#ast = str (ast)
		#return pygame.key.key_code (ast)
		ast = int (ast)
		if ast in alpha_db: return alpha_db[ast]
		raise Exception ()
		
	def press_keys (self, ast):
		print ("press_keys (%s)" % (ast,))
		#keys = ast.right
		mult = ast.left
		#mult = None
		hk   = self.   hold_keys (ast)
		rk   = self.release_keys (ast)
		ks   = (*hk, *rk)
		if mult is not None: ks   = ks * mult
		ks = tuple (ks)
		return ks
		
	def multiplier (self, ast):
		print ("multiplier (%s)" % (ast,))
		return ast.right
					
if __name__ == "__main__":
	# TODO
	quit ()
	
