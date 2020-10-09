#! /usr/bin/env python3

import pygame
import pygame.gfxdraw

from orientation import NORTH, SOUTH, EAST, WEST
from circle_app import CircleApp
from geometry import inscribe_angles, rotate_angles, graphics_affines
from geometry import scale_points, angles_to_polygon, graphics_affine
from geometry import scale_point, tr
from itertools import starmap
from math import sin, cos, pi, sqrt
from constants import ORIGIN

class StatChartInner (CircleApp): # TODO need an abstract class bc this is similar to the magic circle text... nvm fuck it to death and burn it.
	# TODO axis label, value, radius
	#def __init__ (self, rads):
	def __init__ (self, rads=None, *args, **kwargs):
		CircleApp.__init__ (self, *args, **kwargs)
		self.rads = None
		if rads is not None: self.set_radii (rads)
		"""
		rads      = tuple (rads)
		self.rads = rads
		#self.lbls = lbls
		"""
	def set_radii (self, rads):
		rads = tuple (rads)
		self.rads = rads
		self.compute ()
	def compute (self):
		rads = self.rads
		n         = len (rads)
		#assert n == len (lbls)
		
		angles      = inscribe_angles (n)
		
		orientation = NORTH
		theta       = orientation.radians ()
		angles      = rotate_angles   (angles, theta)
		angles      = tuple (angles)
	    
		f           = lambda theta, radius: (radius * cos (theta), radius * sin (theta))
		pv          = zip (angles, rads)
		pts         = starmap (f, pv)
		pts         = graphics_affines (pts)
		f           = lambda k: tuple (k)
		pts         = map (f, pts)
		pts         = tuple (pts)
		self.pts    = pts
		
		axes        = angles_to_polygon (angles)
		axes        = graphics_affines (axes)
		f           = lambda k: tuple (k)
		axes        = map (f, axes)
		axes        = tuple (axes)
		self.axes   = axes
		
	def draw_background (self, temp):
		CircleApp.draw_background (self, temp)
		pts  = self.pts
		assert len (pts) > 0
		rect = temp.get_rect ()
		pts  = scale_points (pts, rect)
		f    = lambda k: tuple (k)
		pts  = map (f, pts)
		pts  = tuple (pts)
		assert len (pts) > 0
		
		color = (0, 0, 255)
		pygame.gfxdraw.     aapolygon (temp, pts, color)
		pygame.gfxdraw.filled_polygon (temp, pts, color)
		
	def draw_foreground (self, temp):
		CircleApp.draw_foreground (self, temp)
		pts  = self.axes
		assert len (pts) > 0
		rect = temp.get_rect ()
		pts  = scale_points (pts, rect)
		f    = lambda k: tr (k)
		pts  = map (f, pts)
		pts  = tuple (pts)
		assert len (pts) > 0
		
		color = (255, 0, 255)
		for a, b in zip (pts, (*pts[1:], pts[0])):
			assert len (a) == 2, "a: %s" % (a,)
			assert len (b) == 2, "b: %s" % (b,)
			pygame.gfxdraw.line (temp, *a, *b, color)
		
		o    = ORIGIN
		o    = graphics_affine (o)
		x, y, w, h = rect
		o    = scale_point (o, ORIGIN, (w, h))
		o    = tr (o)
		
		color = (255, 255, 0)
		for axis in pts:
			assert len (o)    == 2, "o:  %s" % (o,)
			assert len (axis) == 2, "pt: %s" % (axis,)
			pygame.gfxdraw.line (temp, *o, *axis, color)
			
			
			
			
			
from circled_circle import AbsoluteCircledCircle

from polygon_app import PolygonApp, EqualPolygonApp
from circled_polygon import CircledPolygon
from polygoned_circle import PolygonedCircle, EqualPolygonedCircle
from text_ring import TextRing

def inscribe (pv):
	f           = lambda theta, radius: (radius * cos (theta), radius * sin (theta))
	#pv          = zip (angles, rads)
	pts         = starmap (f, pv)
	return pts
def inscribe2 (angles, rads):
	pv = zip (angles, rads)
	return inscribe (pv)
def inscribe3 (rads):
	rads = tuple (rads)
	n = len (rads)
	angles = inscribe_angles (n)
	return inscribe2 (angles, rads)
	
from constants import SECONDARY_BACKGROUND
"""
class CircleStatChartInner (CircledPolygon): # polygon radii as a function of stats
	def __init__ (self, rads, *args, **kwargs):
		if rads is not None:
			rads = tuple (rads)
			n = len (rads)
			#child = EqualPolygonApp (n)
			#angles = inscribe_angles (n)
			#ars = zip (angles, rads)
			#pts = inscribe (ars)
			pts = inscribe3 (rads)
			f = lambda pt: tuple (pt)
			pts = map (f, pts)
			pts = tuple (pts)
		else: pts = None
		child = PolygonApp (pts, background=SECONDARY_BACKGROUND, *args, **kwargs)
		CircledPolygon.__init__ (self, child, *args, **kwargs)
	def set_radii (self, rads):
		rads = tuple (rads)
		n = len (rads)
		#child = EqualPolygonApp (n)
		#angles = inscribe_angles (n)
		#ars = zip (angles, rads)
		#pts = inscribe (ars)
		#pts = inscribe (angles, rads)
		pts = inscribe3 (rads)
		f = lambda pt: tuple (pt)
		pts = map (f, pts)
		pts = tuple (pts)
		self.child.set_pts (pts)
"""

"""
#class CircleStatChart (TextRing): # labelled stat chart inner
class CircleStatChart (AbsoluteCircledCircle):
	def __init__ (self, labels, font=None, *args, **kwargs):
		#child = StatChart (None, background=None)
		child = StatChart (None)
		#text  = ' '.join (labels)
		AbsoluteCircledCircle.__init__ (self, child, None, None, *args, **kwargs)
		self.font = font
		self.labels = labels
	def set_radii (self, rads):
		self.child.set_radii (rads)
	def set_subsurface (self, ss):
		AbsoluteCircledCircle.set_subsurface (self, ss)
		if self.font is None:
			df        = pygame.font.get_default_font ()
			font      = pygame.font.Font (df, 8)
			self.font = font
		temp = self.compute_sizes ()
		if temp is None: return
		texts, tw, th, minn, maxn, x, y, w, h = temp
		# TODO handle change in sizes
		self.texts    = texts
		self.tw       = tw
		self.th       = th
		self.minn     = minn
		self.maxn     = maxn
		self.x        = x
		self.y        = y
		self.w        = w
		self.h        = h
		#self.next_cycle ()
		if self.child is not None:
			self.xoff = self.yoff = th
		n = len (self.labels)
		self.n = maxn // n * n
		self.xforms = self.get_transforms ()
	def compute_sizes (self):
		#if self.text is None: return None
		if self.labels is None: return None
		#text = ' '.join (self.labels)
		
		#text = self.text
		#print ("text: %s" % (text,))
		#N = len (text)
		#print ("N: %s" % (N,))
		N = sum (lambda text: len (text), self.labels)
		font = self.font
		
		crfg = (0, 255, 0, 255)
		g = lambda c: str (c)
		f = lambda text: map (g, text)
		texts = map (f, self.labels)
		g = lambda c: (font.render (c, True, crfg), *font.size (c))
		f = lambda text: map (g, text)
		texts = map (f, texts)
		texts = tuple (texts) # image, w, h

		f = lambda iwh: iwh[1] 
		tw = max (texts, key=f)[1]
		f = lambda iwh: iwh[2]
		th = max (texts, key=f)[2]
		print ("tw: %s, th: %s" % (tw, th))
		
		#texts = repeat (texts)
		
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
	def draw_cropped_scene (self, temp):
		print ("circular_matrix_text.draw_foreground ()")
		#CircleApp.draw_foreground (self, temp)
		AbsoluteCircledCircle.draw_cropped_scene (self, temp)
		xforms = self.xforms # image, w, h
		n      = self.n
		#ndx    = self.sectioni
		pts    = self.pts
		#angles = self.angles		
		#print ("nsection: %s, ndx: %s" % (len (self.sections), ndx))
		#k, section = self.sections[ndx]
		#section = self.sections[ndx]
		section = self.section
		#for i in range (0, n, k):
		for i in section:
			#theta = angles[i]
			xform = xforms[i]
			pt    = pts[i]

			#rect  = text.get_rect ()
			rect = xform.get_rect ()
			rect.center = (round (pt[0]), round (pt[1]))
			temp.blit (xform, rect)			
			
		#self.increment_section_index () # TODO move this to the troller
		
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
		k = zip (cycle (texts), angles)
		xforms = starmap (f, k)
		xforms = tuple (xforms)
		return xforms
"""

from itertools import chain
from geometry import reflect_angles, to_degrees
from constants import OPAQUE
from constants import SECONDARY_BACKGROUND
from composite_app import CompositeApp

class StatChart (AbsoluteCircledCircle): # composite app, child is also circle, animated app, pos/neg space has ranges
	def __init__ (self, labels, font=None, rads=None, *args, **kwargs):
		child = StatChartInner (rads, background=None, *args, **kwargs)
		AbsoluteCircledCircle.__init__ (self, child, None, None, *args, **kwargs)

		self.labels = labels
		
		self.font = font
		
		self.n = None
		
	def set_radii (self, rads): self.child.set_radii (rads)
		
	def set_subsurface (self, ss):
		CircleApp   .set_subsurface (self, ss)
		if self.font is None:
			df        = pygame.font.get_default_font ()
			font      = pygame.font.Font (df, 8)
			self.font = font
		texts, tw, th, minn, maxn, x, y, w, h = self.compute_sizes ()
		# TODO handle change in sizes
		self.texts    = texts
		self.tw       = tw
		self.th       = th
		self.minn     = minn
		self.maxn     = maxn
		self.x        = x
		self.y        = y
		self.w        = w
		self.h        = h
		self.xoff = self.yoff = self.th
		CompositeApp.set_subsurface (self, None, True)
		self.next_cycle ()
		
	def next_cycle (self):
		#a             = self.a
		#b             = self.b
		n             = self.n
		#first_cycle   = True
		#if a is None or b is None or n is None:
		#	assert a is None
		#	assert b is None
		#	assert n is None
		#else: first_cycle = False
		n, pts, angles = self.get_polygons (n)
		#self.a        = a
		#self.b        = b
		self.n        = n
		self.pts      = pts
		self.angles   = angles
		self.sections = tuple (self.get_sections ())
		self.xforms   = self.get_transforms ()
		#self.sectioni = 0
		
	def compute_sizes (self):
		text = self.labels
		print ("text: %s" % (text,))
		N = len (text)
		print ("N: %s" % (N,))
		font = self.font
		
		crfg = (0, 255, 0, 255)
	
		texts = []
		for label in self.labels:
			Cs = []
			for c in label:
				c = str (c)
				C = font.render (c, True, crfg)
				Cw, Ch = font.size (c)
				Cs.append ((C, Cw, Ch))
			Cs = tuple (Cs)
			texts.append (Cs)
		texts = tuple (texts)
		
		
		print ("texts: %s" % (text,))

		f = lambda iwh: iwh[1] 
		tw = max (chain (*texts), key=f)[1]
		f = lambda iwh: iwh[2]
		th = max (chain (*texts), key=f)[2]
		print ("tw: %s, th: %s" % (tw, th))
		
		#texts = repeat (texts)
		
		# each char of text is rotated => text is a polygon, circle is inscribed
		X, Y, W, H = self.inner_rect ()                                   # outer radii
		print ("(X, Y): (%s, %s) (W: %s, H: %s)" % (X, Y, W, H))
		#w, h = W - 2 * tw, H - 2 * th                                   # make room for text aligned at axes
		x, y, w, h = X + tw / 2, Y + th / 2, W - tw, H - th # text center
		print ("w: %s, h: %s" % (w, h))
		# text is rendered between outer and inner radii
		
		# find max n s.t. polygon side length >= text width
		##f = lambda k: ceil (2 * pi / arccos (k))
		#f = lambda k: floor (2 * pi / acos (k))
		#maxn1 = f (1 - tw / 2)
		#maxn2 = f (1 + tw / 2)
		##maxn1 = f (1 - tw / W * tw / H / 2)
		##maxn2 = f (1 + tw / W * tw / H / 2)
		#maxn = max (maxn1, maxn2) # TODO ?
		#print ("maxn1: %s, maxn2: %s, maxn: %s" % (maxn1, maxn2, maxn))
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

	def get_polygons (self, n=None):
		texts = self.texts # image, w, h
		tw    = self.tw
		th    = self.th
		minn  = self.minn
		maxn  = self.maxn
		X, Y, W, H = self.get_rect ()
		x, y, w, h = self.x, self.y, self.w, self.h
		N = len (texts)
		n = (maxn // N) * N
		

		orientation = NORTH
		#pts = inscribe_polygon (n, orientation.radians ())
		angles = inscribe_angles   (n)
		angles =  reflect_angles   (angles)
		angles =   rotate_angles   (angles, orientation.radians ())
		#angles =  reflect_angles   (angles)
		angles = tuple (angles)
		pts    = angles_to_polygon (angles)
		pts    = graphics_affines  (pts)
		rect   = x, y, w, h # text center
		pts    = scale_points      (pts, rect)
		pts    = map (lambda pt: tuple (pt), pts)
		pts    = tuple (pts)
		print ("pts: %s" % (pts,))
		
		#while True:
		#	a = b
		#	b, n = random_relatively_prime_to (a, minn, maxn)
		#	print ("a: %s, b: %s, n: %s" % (a, b, n))
		
		return n, pts, angles
		
		
		
		
		
		
		
		
		
		
		
		
	def get_sections (self):
		n = self.n               # number of points/angles
		b = len (self.texts)     # axis labels
		assert n % b == 0
		a = n // b
		assert n % a == 0
		assert b * a == n
		
		section = []
		for k in range (0, b):   # for each label
			i = k * a            # index of point/angle
			text = self.texts[k] # current label
			#if len (text) % 2 != 0: text = text + ' '
			t = len (text) // 2  # #chars on either side of i
			for j in range (1, t + 1)[::-1]:
				J = i - j
				if J < 0: J = J + n
				T = t - j
				section.append ((J, k, T))
				print ("angles[J: %s]: %s" % (J, self.angles[J]))
				label = self.texts[k]
				print ("texts[k: %s]: %s" % (k, label))
				print ("label[T: %s]: %s" % (T, label[T]))

			#if len (text) % 2 != 0:          section.append ((i,     k, t))	# TODO even numbers have big gaping holes
			
			#for j in range (1, t + 1):
			for j in range (0, t):
				J = i + j
				if J >= n: J = J - n
				T = t + j
				section.append ((J, k, T))
				print ("angles[J: %s]: %s" % (J, self.angles[J]))
				label = self.texts[k]
				print ("texts[k: %s]: %s" % (k, label))
				assert T < len (label), "T: %s, len: %s" % (T, len (label))
				print ("label[T: %s]: %s" % (T, label[T]))
				
		#assert i == n
		#assert k * a == n, "i: %s, a: %s, b: %s, n: %s, k: %s" % (i, a, b, n, k)
		return tuple (section)

	def get_transforms (self):
		texts  = self.texts # image, w, h
		angles = self.angles
		# TODO might have to blit onto a temp surface
		f = lambda text, angle: self.transform_helper (*text, angle)
		#ntext  = len (texts)
		#nangle = len (angles)
		#assert ntext == nangle, "ntext: %s, nangle: %s" % (ntext, nangle)
		#k = zip (cycle (texts), angles)
		
		xforms = []
		for ai, li, ti in self.sections:
			angle = angles[ai]
			label = texts [li]
			text  = label [ti]
			xform = f (text, angle)
			xforms.append (xform)
		#k = zip (texts, angles)
		#xforms = starmap (f, k)
		xforms = tuple (xforms)
		return xforms
			
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
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	# def minsz: minsz of inner circle... + tw, th => minsz of outer
	# 3 * 4 = 12 points on polygon...  
	#def draw_foreground (self, temp):
	def draw_cropped_scene (self, temp):
		print ("circular_matrix_text.draw_foreground ()")
		#CircleApp.draw_foreground (self, temp)
		AbsoluteCircledCircle.draw_cropped_scene (self, temp)
		xforms = self.xforms # image, w, h
		n      = self.n
		#ndx    = self.sectioni
		pts    = self.pts
		angles = self.angles		
		#print ("nsection: %s, ndx: %s" % (len (self.sections), ndx))
		#k, section = self.sections[ndx]
		#section = self.sections[ndx]
		section = self.sections
		#for i in range (0, n, k):
		fuck = zip (xforms, section)
		for xform, s in fuck:
			ai, li, ti = s
			pt    = pts[ai]

			#rect  = text.get_rect ()
			rect = xform.get_rect ()
			rect.center = (round (pt[0]), round (pt[1]))
			temp.blit (xform, rect)			
			
		#self.increment_section_index () # TODO move this to the troller
		



		
		
if __name__ == "__main__":
	from gui import GUI, BLACK
	from hal import HAL9000
	from random import uniform, randrange
	
	def main ():	
		#n    = randrange (3, 12 + 1)
		n = 3
		assert n >= 3
		rng  = range (1, n + 1)
		rng  = tuple (rng)
		assert len (rng) == n
		f    = lambda k: uniform (0, 1)
		rads = map (f, rng)
		#a = StatChart ()
		l = ('altitude', 'pressure', 'temperature')
		a = StatChart (l)
		a.set_radii (rads)
		with HAL9000 (app=a, exit_on_close=False) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
