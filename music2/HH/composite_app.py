#! /usr/bin/env python3

from cropping_app import CroppingApp


import pygame

class CompositeApp (CroppingApp):
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
