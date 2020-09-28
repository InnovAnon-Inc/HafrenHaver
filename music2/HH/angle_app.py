#! /usr/bin/env python3

from app import App
from cropping_app import CroppingApp, OPAQUE

import pygame
import pygame.gfxdraw

from orientation import NORTH, EAST, SOUTH, WEST

def tr (t): return tuple (map (lambda x: round (x), t)) # tuple-round

from math import sqrt

def findSemiPerimeterOfIncircle (a, b, c):
	assert a >= 0
	assert b >= 0
	assert c >= 0
	return (a + b + c) / 2
def findAreaOfTriangle (a, b, c, p=None):
	assert a >= 0
	assert b >= 0
	assert c >= 0
	if p is None: p = findSemiPerimeterOfIncircle (a, b, c)
	n = p * (p - a) * (p - b) * (p - c)
	if n < 0: return 0
	return sqrt (n)
def findRadiusOfIncircle (a, b, c, p=None): # https://www.geeksforgeeks.org/program-to-find-the-radius-of-the-incircle-of-the-triangle/ 
	assert a >= 0 # the sides cannot be negative 
	assert b >= 0
	assert c >= 0
	if p is None: p    = findSemiPerimeterOfIncircle (a, b, c)
	area = findAreaOfTriangle          (a, b, c, p)
	return area / p

import numpy as np

def cercle_circonscrit (T):
    (x1, y1), (x2, y2), (x3, y3) = T
    A = np.array ([[x3-x1,y3-y1],[x3-x2,y3-y2]])
    Y = np.array ([(x3**2 + y3**2 - x1**2 - y1**2),(x3**2+y3**2 - x2**2-y2**2)])
    if np.linalg.det (A) == 0: return False
    Ainv = np.linalg.inv (A)
    X = 0.5 * np.dot (Ainv,Y)
    x, y = X[0], X[1]
    r = sqrt ((x-x1)**2+(y-y1)**2)
    return (x, y), r
    
def coordinates_to_deltas (x, y, z):
	(x1, y1), (x2, y2), (x3, y3) = x, y, z
	dx21, dy21 = x2 - x1, y2 - y1
	dx32, dy32 = x3 - x2, y3 - y2
	dx13, dy13 = x1 - x3, y1 - y3
	dx, dy, dz = (dx21, dy21), (dx32, dy32), (dx13, dy13)
	return dx, dy, dz
def deltas_to_side_lengths (dx, dy, dz):
	(dx21, dy21), (dx32, dy32), (dx13, dy13) = dx, dy, dz
	s21 = sqrt (pow (dx21, 2) + pow (dy21, 2))
	s32 = sqrt (pow (dx32, 2) + pow (dy32, 2))
	s13 = sqrt (pow (dx13, 2) + pow (dy13, 2))
	return s21, s32, s13
def coordinates_to_side_lengths (x, y, z):
	deltas = coordinates_to_deltas (x, y, z)
	return deltas_to_side_lengths (*deltas)
    
def cercle_inscrit (T):
	(x1, y1), (x2, y2), (x3, y3) = T
	s21, s32, s13 = coordinates_to_side_lengths (*T)
	p2  = findSemiPerimeterOfIncircle (s21, s32, s13)
	c   = findCenterOfIncircle (x1, y1, x2, y2, x3, y3, s21, s32, s13, p2)
	r   = findRadiusOfIncircle (s21, s32, s13, p2)
	return c, r
	
def findCenterOfIncircle (x1, y1, x2, y2, x3, y3, s21=None, s32=None, s13=None, p2=None):
	if s21 is None or s32 is None or s13 is None:
		assert s21 is None
		assert s32 is None
		assert s13 is None
		s21, s32, s13 = coordinates_to_side_lengths ((x1, y1), (x2, y2), (x3, y3))
	n1  = s32 * x1 + s13 * x2 + s21 * x3
	n2  = s32 * y1 + s13 * y2 + s21 * y3
	if p2 is None: p2 = findSemiPerimeterOfIncircle (s21, s32, s13)
	p  = p2 * 2
	return n1 / p, n2 / p

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
