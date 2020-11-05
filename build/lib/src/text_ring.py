#! /usr/bin/env python3

import pygame

from polygon_app import PolygonApp, EqualPolygonApp
from circled_polygon import CircledPolygon
from polygoned_circle import PolygonedCircle, EqualPolygonedCircle
from circle_app import CircleApp
from math import pi, sin, cos, sqrt, pow
from itertools import starmap
from constants import OPAQUE
from geometry import to_degrees

class TextRing (CircledPolygon): # circled polygon with polygon'd circle # number of sides of polygon based on text
	def __init__ (self, child, text, font=None, *args, **kwargs):
		#assert child is not None
		if not isinstance (child, PolygonedCircle) and not isinstance (child, EqualPolygonedCircle):
			assert child is None or isinstance (child, CircleApp)
			child = EqualPolygonedCircle (None, child, background=None, *args, **kwargs)
			#child = EqualPolygonedCircle (None, child, *args, **kwargs)
		#assert child is not None
		CircledPolygon.__init__ (self, child, *args, **kwargs)
		self.text = text
		self.font = font
		#assert self.child is not None
		self.th = None
	def set_subsurface (self, ss):
		CircledPolygon.set_subsurface (self, ss)
		if self.font is None:
			df        = pygame.font.get_default_font ()
			font      = pygame.font.Font (df, 8)
			self.font = font
		texts, tw, th, minn, maxn, x, y, w, h = self.compute_sizes ()
		# TODO handle change in sizes
		self.texts    = texts
		self.tw       = tw
		self.th       = th
		if self.child is not None:
			rect = self.inner_rect ()
			ss2 = ss.subsurface (rect)
			self.child.set_subsurface (ss2)
		self.minn     = minn
		self.maxn     = maxn
		self.x        = x
		self.y        = y
		self.w        = w
		self.h        = h
		#self.next_cycle ()
	def compute_sizes (self):
		text = self.text
		print ("text: %s" % (text,))
		N = len (text)
		print ("N: %s" % (N,))
		font = self.font
		
		crfg = (0, 255, 0, 255)
		f = lambda c: (font.render (c, True, crfg), *font.size (c))
		g = lambda c: str (c)
		texts = map (g, text)
		texts = map (f, texts)
		texts = tuple (texts) # image, w, h

		f = lambda iwh: iwh[1] 
		tw = max (texts, key=f)[1]
		f = lambda iwh: iwh[2]
		th = max (texts, key=f)[2]
		print ("tw: %s, th: %s" % (tw, th))
		
		# each char of text is rotated => text is a polygon, circle is inscribed
		X, Y, W, H = self.inner_rect ()                                   # outer radii
		print ("(X, Y): (%s, %s) (W: %s, H: %s)" % (X, Y, W, H))
		#w, h = W - 2 * tw, H - 2 * th                                   # make room for text aligned at axes
		x, y, w, h = X + tw / 2, Y + th / 2, W - tw, H - th # text center
		print ("w: %s, h: %s" % (w, h))
		# text is rendered between outer and inner radii
		
		minn   = 3                                                      # min number of chars that will look "arcane"
		n      = minn
		while True: # TODO if the formula doesn't work, at least use an interpolated binary search
			n      = n + 1
			i      = 0
			theta1 = (i + 0) / n * 2 * pi
			theta2 = (i + 1) / n * 2 * pi
			dx     = cos (theta2) - cos (theta1)
			dy     = sin (theta2) - sin (theta1)
			sl     = sqrt (pow (W * dx, 2) + pow (H * dy, 2))           # side length of polygon
			if sl < tw: break
		maxn = n - 1
		print ("maxn: %s" % (maxn,))
		assert maxn >= minn * (minn + 1)                                # lower bound is minn^2, and the numbers must be different
		
		return texts, tw, th, minn, maxn, x, y, w, h
	
	def transform_helper (self, text, w, h, angle):
		intermediate_alpha_surface = pygame.Surface ((w, h), flags=pygame.SRCALPHA)
		intermediate_alpha_surface.fill (pygame.Color (*OPAQUE))
		text_rect = text.get_rect ()
		text_rect.center = (w / 2, h / 2)
		intermediate_alpha_surface.blit (text, text_rect, special_flags=pygame.BLEND_RGBA_MIN)
		
		# when angle is   0    , rad is - pi / 2
		# when angle is +pi / 2, rad is 0
		# when angle is  pi    , rad is + pi / 2
		# when angle is -pi / 2, rad is 0
		#if 0 <= angle and angle <= pi: rad = angle
		#else:                          rad = angle - pi
		rad = angle	- pi / 2
		#orientation = NORTH
		
		degrees = to_degrees (rad)
		#degrees = 0
		xform = pygame.transform.rotate (intermediate_alpha_surface, degrees)
		#xform = pygame.transform.rotate (text, angle)
		return xform
	def get_transforms (self):
		texts  = self.texts # image, w, h
		angles = self.angles
		# TODO might have to blit onto a temp surface
		f = lambda text, angle: self.transform_helper (*text, angle)
		ntext  = len (texts)
		nangle = len (angles)
		#assert ntext == nangle, "ntext: %s, nangle: %s" % (ntext, nangle)
		k = zip (self.get_text_for_transforms (), angles)
		xforms = starmap (f, k)
		xforms = tuple (xforms)
		return xforms
	def get_text_for_transforms (self): return self.texts
		
	# def minsz: minsz of inner circle... + tw, th => minsz of outer
	# 3 * 4 = 12 points on polygon...  
	#def draw_foreground (self, temp):
	def draw_cropped_scene (self, temp):
		print ("circular_matrix_text.draw_foreground ()")
		#CircleApp.draw_foreground (self, temp)
		CircledPolygon.draw_cropped_scene (self, temp)
		xforms = self.xforms # image, w, h
		n      = self.n
		ndx    = self.sectioni
		pts    = self.pts
		angles = self.angles		
		print ("nsection: %s, ndx: %s" % (len (self.sections), ndx))
		#k, section = self.sections[ndx]
		section = self.sections[ndx]
		#for i in range (0, n, k):
		for i in section:
			theta = angles[i]
			xform = xforms[i]
			pt    = pts[i]

			#rect  = text.get_rect ()
			rect = xform.get_rect ()
			rect.center = (round (pt[0]), round (pt[1]))
			temp.blit (xform, rect)			
			
		#self.increment_section_index () # TODO move this to the troller

	def inner_rect (self):
		rect = self.outer_rect ()
		X, Y, W, H = rect
		th = self.th
		if th is None: return rect
		w, h = W - 2 * th, H - 2 * th
		x, y = X + (W - w) / 2, Y + (H - h) / 2
		rect = x, y, w, h
		return rect
		

if __name__ == "__main__":
	def main ():
		# TODO
		a = None
		with HAL9000 (app=a) as g: g.run ()
	main ()
	quit ()
