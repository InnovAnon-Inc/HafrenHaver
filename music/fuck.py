from __future__ import division
from collections import *
from fractions import *
from functools import *
from itertools import *
from math import *
from operator import mul
from random import *
from time import sleep

from graphics import *

#def pitches (freqs, base):
#	return [base * freq for freq in freqs]


def equal_spacing (n):
	for h in xrange (n):
		yield (h + 1) / n

def normalize_window_point (point, win):
	x = (point[0] + 1) * win.getWidth () / 2
	y = (point[1] + 1) * win.getHeight () / 2
	return Point (x, y)
def normalize_window_polygon (pgon, win):
	return Polygon ([normalize_window_point (p, win) for p in pgon])
def display_points (points, win):
	for p in points:
		pt = normalize_window_point (p, win)
		pt.draw (win)

def bjorklund_polygon (scale, points):
	for sp in zip (scale, points):
		(s, p) = sp
		if s is not 0: yield p
def display_polygon (pgon, win):
	normalize_window_polygon (pgon, win).draw (win)
def display_constellation (points, win):
	center = normalize_window_point ((0, 0), win)
	for p in points:
		pt = normalize_window_point (p, win)
		#pt.draw (win)
		l = Line (center, pt)
		l.draw (win)
def display_bjorklund (scale):
	win = GraphWin ()
	pts = list (points (normalize_radians (
		equal_spacing (len (scale)))))
	#display_points (pts, win)
	display_constellation (pts, win)
	pgon = list (bjorklund_polygon (scale, pts))
	display_constellation (pgon, win)
	display_polygon (pgon, win)
	#win.promptClose ()
def display_bjorklund_scale (scale, bjork):
	win = GraphWin ()
	pts = list (points (normalize_radians (
		normalize_frequency (normalize_octave (scale)))))
	#display_constellation (pts, win)
	display_polygon (pts, win)
	pgon = list (bjorklund_polygon (bjork, pts))
	display_constellation (pgon, win)
	display_polygon (pgon, win)
	#win.promptClose ()

"""for a in xrange (8):
	b = Bjorklund (8, a + 1)
	b.bjorklund ()
	print b.sequence
b = Bjorklund (13, 5)
b.bjorklund ()
print b.sequence"""

def harmonics5 (n):
	for h in xrange (n):
		yield (h + 2) / (h + 1)
def harmonics5base (n):
	return [1] + sorted (harmonics5 (n))
def normalize_octave (ss):
	for s in ss:
		yield 1 + (s - 1) / (2 - 1)
def normalize_frequency (ss):
	for s in ss:
		yield log (s) / log (2)
def normalize_radians (ss):
	for s in ss:
		yield s * 2 * pi
def points (ss):
	for s in ss:
		yield (cos (s), sin (s))
def equal_temperament_scale (n):
	return [2 ** h for h in equal_spacing (n)]
	#for h in xrange (n):
	#	yield 2 ** ((h + 1) / n)
def display_scale (scale):
	win = GraphWin ()
	pts = list (points (normalize_radians (
		normalize_frequency (normalize_octave (scale)))))
	#display_points (pts, win)
	display_constellation (pts, win)
	display_polygon (pts, win)
	#win.promptClose ()
	#win.close ()



#display_scale (pitches ([1] + list (equal_temperament_scale (12)), 440))
display_scale ([1] + list (equal_temperament_scale (12)))


sleep (5)