#! /usr/bin/env python3

from cropping_app import CroppingApp


import pygame

class CompositeApp (CroppingApp): # TODO SO creds
	def __init__ (self, child, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.child = child
	def start_running (self):
		CroppingApp .start_running (self)
		self.child.start_running ()
	def  stop_running (self):
		CroppingApp .stop_running (self)
		self.child.stop_running ()
	def minsz (self): return CroppingApp.minsz (self) * self.child.minsz ()
	#ef positive_space (self): return CroppingApp.positive_space (self) + self.child.positive_space ()
	def positive_space (self, is_root=True):
		a11 = self.positive_area ()
		assert a11 >= 0
		a12 = self.child.negative_space (False)
		assert a12 >= 0
		a1 = abs (a11 - a12) # TODO wtf
		assert a1 >= 0
		if not is_root: return a1
		a1 = a1 + CroppingApp.positive_space (self, is_root)
		assert a1 >= 0
		return a1
	def negative_space (self, is_root=True):
		a11 = self.negative_area ()
		assert a11 >= 0
		a12 = self.child.positive_space (False)
		assert a12 >= 0
		#a1 = a11 - a12
		a1 = abs (a12 - a11) # TODO wtf
		assert a1 >= 0, "na: %s, ps: %s" % (a11, a12)
		if not is_root: return a1
		a1 = a1 + CroppingApp.negative_space (self, is_root)
		assert a1 >= 0
		return a1

if __name__ == "__main__":
	from gui import GUI
	from angle_app import AngleApp
	
	def main ():
		b = AngleApp ()
		a = CompositeApp (b)
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
