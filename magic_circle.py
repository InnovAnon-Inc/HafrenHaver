#! /usr/bin/env python3

import pygame
from itertools import repeat
from math import floor, acos, pi, cos, sin, sqrt, pow
from orientation import NORTH, SOUTH, EAST, WEST
from geometry import inscribe_polygon, graphics_affines, scale_points, inscribe_angles, rotate_angles, angles_to_polygon
from random_util import random_relatively_prime_pair, random_relatively_prime_to
from lc import f2lc, lc2str
from itertools import cycle, starmap
from constants import OPAQUE
from geometry import to_degrees, reflect_angles
from circle_app import CircleApp
class MagicCircle (CircleApp): # composite app, child is also circle, animated app, pos/neg space has ranges
	def __init__ (self, text=None, font=None, *args, **kwargs):
		CircleApp.__init__ (self, *args, **kwargs)

		if text is None:
			# if child is none, use own source (get subtype source), else query child for model source, else use child source
			text = f2lc   (MagicCircle)
			text = lc2str (text)
		self.text = text
		
		self.font = font
		
		self.a = None
		self.b = None
		self.n = None

	def set_subsurface (self, ss):
		CircleApp.set_subsurface (self, ss)
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
		self.next_cycle ()
		
	def next_cycle (self):
		a             = self.a
		b             = self.b
		n             = self.n
		first_cycle   = True
		if a is None or b is None or n is None:
			assert a is None
			assert b is None
			assert n is None
		else: first_cycle = False
		a, b, n, pts, angles = self.get_polygons (a, b, n)
		self.a        = a
		self.b        = b
		self.n        = n
		self.pts      = pts
		self.angles   = angles
		self.xforms   = self.get_transforms ()
		self.sections = tuple (self.get_sections (first_cycle))
		self.sectioni = 0
		
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

	def get_polygons (self, a=None, b=None, n=None):
		texts = self.texts # image, w, h
		tw    = self.tw
		th    = self.th
		minn  = self.minn
		maxn  = self.maxn
		X, Y, W, H = self.get_rect ()
		x, y, w, h = self.x, self.y, self.w, self.h
		
		if a is None or b is None or n is None:
			assert a is None
			assert b is None
			assert n is None
			a, b, n = random_relatively_prime_pair (minn, maxn)             # relatively prime pair a, b s.t. a >= minn, b >= minn, a * b <= maxn
			if a > b: # smooth out first frame
				c = a
				a = b
				b = c
		else:
			a = b
			b, n = random_relatively_prime_to (a, minn, maxn) # random number b, relatively prime to a, s.t., minn <= a * b <= maxn
		print ("a: %s, b: %s, n: %s" % (a, b, n))

		orientation = NORTH
		#pts = inscribe_polygon (n, orientation.radians ())
		angles = inscribe_angles   (n)
		angles =   rotate_angles   (angles, orientation.radians ())
		angles =  reflect_angles   (angles)
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
		
		return a, b, n, pts, angles
		
	def section_helper (self, a, b, n, rev, first_section):
		rng = range (0, n, b) # main points: render a chars, skip n / b at a time
		rng = tuple (rng)
		assert len (rng) == a
		
		nloop = b // 2 # number of chars on either side of main points until they meet
		#sections = []
		if first_section: kstart = 0
		else:             kstart = 1
		K = range (first_section, nloop)
		if rev: K = K[::-1]
		for p in K: # k chars on either side
			section = []
			P = range (0, p + 1)
			#if rev: P = P[::-1]
			for k in P:
				for base in rng: # for each of the main points
					section.append (base)
					if k == 0: continue
					section = [base - k] + section
					#section.prepend (base - k)
					#section.append  (base + k)
					section = section + [base + k]
				#sections.extend (section)
				#sections = sections + [section]
				#yield a, tuple (section)
				# TODO a or b ?
				#yield b, tuple (section)
			yield tuple (section)
			
		#f = lambda ndx: texts[ndx][0], pts[ndx]
		#sections = map (f, sections)
		#sections = tuple (sections)
		#yield a, sections
		
	def get_sections (self, first_section):
		n = self.n
		a = self.a
		b = self.b
		yield from self.section_helper (a, b, n, False, first_section) # first section starts at 0
		yield from self.section_helper (b, a, n, True,  b % 2 != 0)    # if odd, then n sections don't display long enough
		
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
		
	# def minsz: minsz of inner circle... + tw, th => minsz of outer
	# 3 * 4 = 12 points on polygon...  
	def draw_foreground (self, temp):
		print ("circular_matrix_text.draw_foreground ()")
		CircleApp.draw_foreground (self, temp)
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
			
		self.increment_section_index () # TODO move this to the troller
		
	def increment_section_index (self):
		ndx = self.sectioni + 1
		if ndx == len (self.sections):
			self.rotate_texts ()
			self.next_cycle ()
		else: self.sectioni = ndx
		
	def rotate_texts (self):
		texts = self.texts
		N = len (texts)
		n = self.n
		while n >= N: n = n - N
		self.texts = tuple (texts[n:] + texts[:n])

if __name__ == "__main__":
	from rotation import ANGLED, STRAIGHT
	from orientation import NORTH, SOUTH, EAST, WEST
	from gui import GUI
	
	def main ():
		if False:
			j = AngleApp     (orientation=NORTH)
			i = CircledAngle (j, background=SECONDARY_BACKGROUND)
			h = AngledCircle (i, orientation=WEST)
			g = CircledAngle (h, background=SECONDARY_BACKGROUND)
			f = AngledCircle (g, orientation=SOUTH)
			e = CircledAngle (f, background=SECONDARY_BACKGROUND)
			d = AngledCircle (e, orientation=EAST)
			c = CircledAngle (d, background=SECONDARY_BACKGROUND)
			b = AngledCircle (c, orientation=NORTH)
			a = CircledAngle (b, background=SECONDARY_BACKGROUND)
		elif False:
			#d = SquareApp     (background=DEFAULT_BACKGROUND)
			d = None
			c = CircledSquare (d, rotation=STRAIGHT)
			b = SquaredCircle (c, background=SECONDARY_BACKGROUND)
			a = RecursiveComposite (b)
			#a = b
		else:
			a = MagicCircle ()
		#a = RecursiveCompositeTest ()
		with GUI (app=a, exit_on_close=False) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
