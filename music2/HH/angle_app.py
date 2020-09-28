#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp, OPAQUE

import pygame
import pygame.gfxdraw

from orientation import NORTH, EAST, SOUTH, WEST

from geometry import tr, coordinates_to_side_lengths, findAreaOfTriangle

class AngleApp (CroppingApp):
	def __init__ (self, orientation=NORTH, *args, **kwargs):
		CroppingApp.__init__ (self, *args, **kwargs)
		self.orientation = orientation
	def set_subsurface (self, ss):
		CroppingApp.set_subsurface (self, ss)
		size = self.ss.get_size()
		w, h = size
		orientation = self.orientation
		if orientation == NORTH:
			x = 0, h
			y = w / 2, 0
			z = w, h
			self.bounds       = x, y,      z
			self.bounds_round = x, tr (y), z
		if orientation == SOUTH:
			x = 0, 0
			y = w / 2, h
			z = w, 0
			self.bounds       = x, y,      z
			self.bounds_round = x, tr (y), z
		if orientation == EAST:
			x = 0, 0
			y = w, h / 2
			z = 0, h
			self.bounds       = x, y,      z
			self.bounds_round = x, tr (y), z
		if orientation == WEST:
			x = 0, h / 2
			y = w, 0
			z = w, h
			self.bounds       = x,      y, z
			self.bounds_round = tr (x), y, z
	def crop (self):
		x, y, z = self.bounds_round
		pygame.gfxdraw.     aatrigon (self.cropped_background, *x, *y, *z, OPAQUE)
		pygame.gfxdraw.filled_trigon (self.cropped_background, *x, *y, *z, OPAQUE)

	def minsz (self):
		w, h = CroppingApp.minsz (self)
		return w * 3, h * h
	def outer_area (self): return CroppingApp.area (self)
	def inner_area (self):
		x, y, z = self.bounds
		s21, s32, s13 = coordinates_to_side_lengths (x, y, z)
		inner_area = findAreaOfTriangle (s21, s32, s13)
		return inner_area

if __name__ == "__main__":
	from gui import GUI
	from orientation import Orientation
	
	def main ():
		for orientation in Orientation:
			a = AngleApp (orientation)
			with GUI (app=a) as g:
				#g.setApp (a)
				print ("minsz: (%s, %s)" % a.minsz ())
				print ("outer: %s"       % a.outer_area ())
				print ("inner: %s"       % a.inner_area ())
				print ("pos  : %s"       % a.positive_space ())
				print ("neg  : %s"       % a.negative_space ())
				g.run ()
	main ()
	quit ()
