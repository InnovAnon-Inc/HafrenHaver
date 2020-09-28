#! /usr/bin/env python3

from math import atan, atan2, pi, sin, cos, tan, gcd, sqrt, ceil, log
from itertools import chain, product

import sys

# The line on which the orthocenter H,
# triangle centroid G,
# circumcenter O,
# de Longchamps point L,
# nine-point center N,
# and a number of other important triangle centers lie.

# TODO rotate
# TODO reflect
# TODO translate
# TODO dilate

"""
def axis (dim, ndim):
	p0   = tuple ([0] * dim + [-1] + [0] * (ndim - dim))
	p1   = tuple ([0] * dim + [+1] + [0] * (ndim - dim))
	p0   = PointND (*p0)
	p1   = PointND (*p1)
	return Line (p0, p1)
def ascension_anim (ndim=3):
	#npoint = ndim * 2
	#naxis  = ndim
	axes = tuple (axis (dim, ndim) for dim in range (0, ndim))
	# TODO how to rotate & project from ndim onto 2D
class Point3D (Point):
	def __init__ (self, x, y, z):
		Point.__init__ (self, x, y)
		self.z = z
	def shadow (self, cam):
		w,  h  = 2,     2
		cx, cy = w / 2, h / 2
		cxy = min (cx, cy) # ?

		x, y, z = self.x, self.y, self.z

		x -= cam.pos[0]
		y -= cam.pos[1]
		z -= cam.pos[2]

		x, z = rotate2d ((x, z), cam.rot[1])
		y, z = rotate2d ((y, z), cam.rot[0])

		f = cxy / z
		x, y = x * f, y * f
		#points += [(cx+int(x), cy+int(y))]
		return Point (x, y)
class PointND (Point3D):
	def __init__ (self, *xyz):
		Point3D.__init__ (self, xyz[0], xyz[1], xyz[2])
		self.xyz = xyz
	def project (self):
		# TODO
		return Point3D (x, y, z)
"""

		

class Point:
	def __init__ (self, x, y):
		self.x = x
		self.y = y
	def __repr__ (self): return "(%s, %s)" % (self.x, self.y)
	def translate (self, xOff, yOff):
		x = self.x - xOff
		y = self.y - yOff
		return Point (x, y)
	def reflectX (self, xMax):
		x = xMax - self.x
		y = self.y
		return Point (x, y)
	def reflectY (self, yMax):
		x = self.x
		y = yMax - self.y
		return Point (x, y)
	def scale (self, xscale, yscale):
		x = self.x * xscale
		y = self.y * yscale
		return Point (x, y)
	def round  (self):
		x = round (self.x)
		y = round (self.y)
		return Point (x, y)
	def unpack (self): return (self.x, self.y)
	def draw (self, screen):
		color  = (0, 0, 255)
		radius = 1
		pygame.draw.circle (screen, color, self.unpack (), radius)
	def angle (self):
		dy = self.y - 0
		dx = self.x - 0
		return atan2 (dy, dx)
	def distance (self):
		dx = self.x - 0
		x2 = dx * dx
		dy = self.y - 0
		y2 = dy * dy
		return sqrt (x2 + y2)
	def rotate (self, angle):
		a = self.angle ()
		a = a + angle
		r = self.distance ()
		x = r * cos (a)
		y = r * sin (a)
		return Point (x, y)
class Circle:
	def __init__ (self, pt, r):
		self.pt = pt
		self.r  = r
	def __repr__ (self): return "(%s, %s)" % (self.x, self.y)
	def translate (self, xOff, yOff):
		pt = self.pt.translate (xOff, yOff)
		return Circle (pt, self.r)
	def reflectX (self, xMax):
		pt = self.pt.reflectX (xMax)
		return Circle (pt, self.r)
	def reflectY (self, yMax):
		pt = self.pt.reflectY (yMax)
		return Circle (pt, self.r)
	def scale (self, xscale, yscale):
		pt = self.pt.scale (xscale, yscale)
		#r = self.r * sqrt (xscale * xscale + yscale * yscale)
		r = min (xscale, yscale)
		r = self.r * r
		return Circle (pt, r)
	def round  (self):
		pt = self.pt.round ()
		r = round (self.r)
		return Circle (pt, r)
	def unpack (self): return (self.x, self.y)
	def draw (self, screen):
		color  = (0, 0, 255)
		#pygame.draw.circle (screen, color, self.unpack (), self.r)
		left   = self.pt.x - self.r
		top    = self.pt.y - self.r
		width  = self.r * 2
		height = self.r * 2
		rect = pygame.Rect (left, top, width, height)
		pygame.draw.arc (screen, color, rect, 0, 2 * pi + 1)
class Quadrilateral:
	def __init__ (self, a, b, c, d):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.ab = Line (a, b)
		self.bc = Line (b, c)
		self.cd = Line (c, d)
		self.da = Line (d, a)
	#def __repr__ (self): return "(%s, %s)" % (self.a, self.b)
	def translate (self, xOff, yOff):
		pts = self.points ()
		pts = [pt.translate (xOff, yOff) for pt in pts]
		return Quadrilateral (*pts)
	def reflectX (self, xMax):
		pts = self.points ()
		pts = [pt.reflectX (xMax) for pt in pts]
		return Quadrilateral (*pts)
	def reflectY (self, yMax):
		pts = self.points ()
		pts = [pt.reflectY (yMax) for pt in pts]
		return Quadrilateral (*pts)
	def scale (self, xscale, yscale):
		pts = self.points ()
		pts = [pt.scale (xscale, yscale) for pt in pts]
		return Quadrilateral (*pts)
	def round  (self):
		pts = self.points ()
		pts = [pt.round () for pt in pts]
		return Quadrilateral (*pts)
	def lines  (self): return [self.ab, self.bc, self.cd, self.da]
	def points (self): return [self.a,  self.b,  self.c,  self.d]
	def draw (self, screen):
		for line in self.lines (): line.draw (screen)
	def tlwh (self):
		lines = self.lines ()
		tl     = lines[0].a
		for line in lines[1:]:
			if line.a.x <= tl.x and line.a.y >= tl.y: tl = line.a
		for line in lines:
			if line.b.x <= tl.x and line.b.y >= tl.y: tl = line.b
		br     = lines[0].a
		for line in lines[1:]:
			if line.a.x >= br.x and line.a.y <= br.y: br = line.a
		for line in lines:
			if line.b.x >= br.x and line.b.y <= br.y: br = line.b
		left   = tl.x
		top    = tl.y
		width  = br.x - tl.x
		height = tl.y - br.y
		return top, left, width, height
	def rotate (self, angle):
		abcd = (pt.rotate (angle) for pt in (self.a, self.b, self.c, self.d))
		return Quadrilateral (*abcd)
class Line: # connects points
	def __init__ (self, a, b):
		self.a  = a
		self.b  = b
		self.dx = b.x - a.x
		self.dy = b.y - a.y
	def translate (self, xOff, yOff):
		a = self.a.translate (xOff, yOff)
		b = self.b.translate (xOff, yOff)
		return Line (a, b)
	def reflectX (self, xMax):
		a = self.a.reflectX (xMax)
		b = self.b.reflectX (xMax)
		return Line (a, b)
	def reflectY (self, yMax):
		a = self.a.reflectY (yMax)
		b = self.b.reflectY (yMax)
		return Line (a, b)
	def scale (self, xscale, yscale):
		a = self.a.scale (xscale, yscale)
		b = self.b.scale (xscale, yscale)
		return Line (a, b)
	def round  (self):
		a = self.a.round ()
		b = self.b.round ()
		return Line (a, b)
	def slope_intercept_form (self): return self.slope (), self.y_intercept () # m, b      where y      = mx + b
	def other_form           (self): return self.a.y, self.slope (), self.a.x  # y1, m, x1 where y - y1 = m(x - x1)
	def standard_form        (self):
		m = self.slope ()
		return -m, 1, self.a.y - m * self.a.x                                  # a, b, c where ax + by = c
	def __repr__ (self): return "%s-%s" % (self.a, self.b)
	def slope (self):
		if self.is_vertical (): return None
		return self.dy / self.dx
	def x_intercept (self):
		if self.is_horizontal ():
			if self.a.y == 0: return 0
			return None
		return - self.y_intercept () / self.slope ()
	def y_intercept (self):
		if self.is_vertical ():
			if self.a.x == 0: return 0
			return None
		return self.slope () * self.a.x + self.a.y
	def distance (self):
		dx  = self.dx
		dy  = self.dy
		dx2 = dx * dx
		dy2 = dy * dy
		return sqrt (dx2 + dy2)
	def midpoint (self):
		x2 = self.a.x + self.dx / 2
		y2 = self.a.y + self.dy / 2
		return Point (x2, y2)
	def bisector (self, pt):
		p = self.midpoint ()
		return Line (pt, p)
	#def is_vertical   (self): return self.a.y == self.b.y
	#def is_horizontal (self): return self.a.x == self.b.x
	def is_vertical   (self): return self.dx == 0
	def is_horizontal (self): return self.dy == 0
	def contains (self, pt):
		m = self.slope ()
		b = self.y_intercept ()
		l1 = Line (self.a, pt)
		m1 = l1.slope ()
		l2 = Line (self.b, pt)
		b1 = l2.y_intercept ()
		if m1 != m: return False
		if b1 != b: return False
		m2 = l2.slope ()
		b2 = l2.y_intercept ()
		if m2 != m: return False
		if b2 != b: return False
		return True
	def perpendicular_bisector (self, pt):
		mid = self.midpoint ()
		if self.is_vertical ():
			#x = mid.x
			x = pt.x
			#y = pt.y
			y = mid.y
			p = Point (x, y)
			return Line (mid, p)
		if self.is_horizontal ():
			#x = pt.x
			x = mid.x
			#y = mid.y
			y = pt.y
			p = Point (x, y)
			return Line (mid, p)
		m1 = self.slope ()
		#b1 = self.y_intercept ()
		# parallel to this line, passing through given point
		m2 = m1
		#b2 = pt.y - m2 * pt.x
		# perpendicular to previous line, passing through midpoint
		m3 = -1 / m1
		b3 = mid.y - m3 * mid.x
		# intersection of parallel line and perpendicular line
		#xn = m1 * pt.x - pt.y + mid.y
		#xn = m1 * xn + mid.x
		#xd = 1 + m1 * m1
		xn = m3 * mid.x - mid.y - m2 * pt.x + pt.y
		xd = m3 - m2
		x  = xn / xd
		y  = m3 * x + b3
		p  = Point (x, y)
		return Line (mid, p)
	#def perpendicular_distance (self, pt):
	#	A =
	#	B =
	#	C =
	#	num = abs (A * pt.x + B * pt.y + C)
	#	den = sqrt (A * A + B * B)
	#	return num / den
	# https://stackoverflow.com/questions/39840030/distance-between-point-and-a-line-from-two-points
	#def perpendicular_distance (self, pt):
	#	coef = (self.m (), self.b ())
	#	return abs((coef[0]*point[0])-point[1]+coef[1])/math.sqrt((coef[0]*coef[0])+1)
	#def parallel (self, pt):
	#def perpendicular0 (self, pt):
	#	if self.is_vertical ():
	#		x = self.a.x
	#		y = pt.y
	#		p = Point (x, y)
	#		return Line (pt, p)
	#	if self.is_horizontal ():
	#		x = pt.x
	#		y = self.a.y
	#		p = Point (x, y)
	#		return Line (pt, p)
	#	m1 = self.m ()
	#	m2 = -1 / m1
	#	b1 = self.a.y - m1 * self.a.x
	#	b2 =     pt.y - m2 *     pt.x
	#	x = (b2 - b1) / (m1 - m2)
	#	y = m1 * x + b1
	#	p = Point (x, y)
	#	return Line (pt, p)
	#def parallel (self, pt): # parallel to this line and passing through the given point
	#	dx = 
	#	dy = 
	#	a  = self.a.translate (dx, dy)
	#	b  = self.b.translate (dx, dy)
	#	return Line (a, b)
	#def perpendicular_bisector (self, line): # perpendicular to this line and passing through the given parallel line
	#	mid = self.midpoint ()
	#	m1  = -1 / self.m ()
	#	m2  = line.m ()
	#	b1  =    mid.y - m1 *    mid.x
	#	b2  = line.a.y - m2 * line.a.x
	#	x   = (b2 - b1) / (m1 - m2)
	#	y   = m1 * x + b1
	#	p   = Point (x, y)
	#	return Line (mid, p)
	def angle (self): return atan2 (self.dy, self.dx)
	def draw0 (self, screen):
		color = (0, 255, 0)
		width = 1
		pygame.draw.line (screen, color, self.a.unpack (), self.b.unpack (), width)
	def draw (self, screen):
		self.draw0 (screen)
		self.a.draw (screen)
		self.b.draw (screen)
	def intersection (self, line):
		m1, b1 = self.slope_intercept_form ()
		m2, b2 = line.slope_intercept_form ()
		if m1 is None and m2 is None: return None
		if m1 is None:
			x = self.a.x
			y = m2 * x + b2
			return Point (x, y)
		if m2 is None:
			x = line.a.x
			y = m1 * x + b1
			return Point (x, y)
		num    = b2 - b1
		den    = m1 - m2
		if den == 0: return None # parallel
		x      = num / den
		y      = m1 * x + b1
		#assert y == m2 * x + b2, "%s, %s" % (y, m2 * x + b2)
		return Point (x, y)
	def rotate (self, angle):
		a = self.a.rotate (angle)
		b = self.b.rotate (angle)
		return Line (a, b)
class Angle: # connects lines
	def __init__ (self, a, b, c):
		self.a  = a
		self.b  = b
		self.c  = c
		self.ab = Line (a, b)
		self.bc = Line (b, c)
	def translate (self, xOff, yOff):
		a = self.a.translate (xOff, yOff)
		b = self.b.translate (xOff, yOff)
		c = self.c.translate (xOff, yOff)
		return Angle (a, b, c)
	def reflectX (self, xMax):
		a = self.a.reflectX (xMax)
		b = self.b.reflectX (xMax)
		c = self.c.reflectX (xMax)
		return Angle (a, b, c)
	def reflectY (self, yMax):
		a = self.a.reflectY (yMax)
		b = self.b.reflectY (yMax)
		c = self.c.reflectY (yMax)
		return Angle (a, b, c)
	def scale (self, xscale, yscale):
		a = self.a.scale (xscale, yscale)
		b = self.b.scale (xscale, yscale)
		c = self.c.scale (xscale, yscale)
		return Angle (a, b, c)
	def round  (self):
		a = self.a.round ()
		b = self.b.round ()
		c = self.c.round ()
		return Angle (a, b, c)
	def bisector (self, line):
		# TODO return line that bisects this angle
		# and passes through the given line
		ab_theta = self.ab.angle ()
		bc_theta = self.bc.angle ()
		theta    = bc_theta - ab_theta
		theta2   = theta / 2
		theta3   = ab_theta + theta2
		m1       = tan (theta3)
		b1       = self.b.y - m1 * self.b.x
		m2       = line.slope ()
		b2       = line.y_intercept ()
		xn = m2 * line.a.x - line.a.y - m1 * self.b.x - self.b.y
		xd = m2 - m1
		x  = xn / xd
		y  = m2 * x + b2
		p  = Point (x, y)
		return Line (self.b, p)
	def __repr__ (self): return "Angle [%s-%s-%s, ab=%s, bc=%s]" % (self.a, self.b, self.c, self.ab, self.bc)
	def angle (self):
		#if perpendicular (self.ab, self.bc):
		#	# TODO
		#	return ???
		m1   = self.ab.m ()
		m2   = self.bc.m ()
		dm   = m2 - m1
		den  = 1 + m1 * m2
		tant = abs (dm / den)
		return atan (tant)
class Triangle:
	def __init__ (self, a, b, c):
		self.a   = a
		self.b   = b
		self.c   = c
		self.ab  = Line  (a, b)
		self.bc  = Line  (b, c)
		self.ca  = Line  (c, a)
		self.abc = Angle (a, b, c)
		self.bca = Angle (b, c, a)
		self.cab = Angle (c, a, b)
	def translate (self, xOff, yOff):
		a = self.a.translate (xOff, yOff)
		b = self.b.translate (xOff, yOff)
		c = self.c.translate (xOff, yOff)
		return Triangle (a, b, c)
	def reflectX (self, xMax):
		a = self.a.reflectX (xMax)
		b = self.b.reflectX (xMax)
		c = self.c.reflectX (xMax)
		return Triangle (a, b, c)
	def reflectY (self, yMax):
		a = self.a.reflectY (yMax)
		b = self.b.reflectY (yMax)
		c = self.c.reflectY (yMax)
		return Triangle (a, b, c)
	def scale (self, xscale, yscale):
		a = self.a.scale (xscale, yscale)
		b = self.b.scale (xscale, yscale)
		c = self.c.scale (xscale, yscale)
		return Triangle (a, b, c)
	def round  (self):
		a = self.a.round ()
		b = self.b.round ()
		c = self.c.round ()
		return Triangle (a, b, c)
	def perimeter (self): return sum (line.distance () for line in (self.ab, self.bc, self.ca))
	# TODO def area (self): return ???
	def linear_bisectors (self):
		a = self.ab.bisector (self.c)
		b = self.bc.bisector (self.a)
		c = self.ca.bisector (self.b)
		return (a, b, c)
	def angular_bisectors (self):
		a = self.abc.bisector (self.ca)
		b = self.bca.bisector (self.ab)
		c = self.cab.bisector (self.bc)
		return (a, b, c)
	#def perpendicular_bisectors (self):
	#	pa = self.ab.parallel (self.c)
	#	pb = self.bc.parallel (self.a)
	#	pc = self.ca.parallel (self.b)
	#	a  = self.ab.perpendicular_bisector (pa)
	#	b  = self.bc.perpendicular_bisector (pb)
	#	c  = self.ca.perpendicular_bisector (pc)
	#	return (a, b, c)
	def perpendicular_bisectors (self):
		a  = self.ab.perpendicular_bisector (self.c)
		b  = self.bc.perpendicular_bisector (self.a)
		c  = self.ca.perpendicular_bisector (self.b)
		return (a, b, c)
	def __repr__ (self): return "Triangle [%s-%s-%s, abc=%s, bca=%s, cab=%s]" % (self.a, self.b, self.c, self.abc, self.bca, self.cab)
	def angles (self): return (ang.angle () for ang in (self.abc, self.bca, self.cab))
	def unpack (self): return (pt.unpack () for pt  in (self.a,   self.b,   self.c))
	def draw0 (self, screen):
		color = (255, 0, 0)
		width = 1
		pygame.draw.polygon (screen, color, list (self.unpack ()), width)
	def draw (self, screen):
		self.draw0 (screen)
		for line in (self.ab, self.bc, self.ca): line.draw0 (screen)
		for pt   in (self.a,  self.b,  self.c):  pt  .draw  (screen)





def color_section (theta):
	sections = [(k, k * 2 * pi / 6) for k in range (0, 6)]
	for k, start in sections[::-1]:
		if theta >= start: return k
	raise Exception (theta)
def angle_color (theta, r):
	while theta <= 0:      theta = theta + 2 * pi
	while theta >  2 * pi: theta = theta - 2 * pi
	section = color_section (theta)
	#print (section)
	s_theta = 2 * pi / 6
	if   section == 0:
		red   = int (r * 255)
		temp  = (theta - s_theta * 0) / s_theta
		green = int (temp * 255)
		blue  = 0
	elif section == 1:
		temp  = (theta - s_theta * 1) / s_theta
		temp  = 1 - temp
		red   = int (temp * 255)
		green = int (r * 255)
		blue  = 0
	elif section == 2:
		red   = 0
		green = int (r * 255)
		temp  = (theta - s_theta * 2) / s_theta
		blue  = int (temp * 255)
	elif section == 3:
		red   = 0
		temp  = (theta - s_theta * 3) / s_theta
		temp  = 1 - temp
		green = int (temp * 255)
		blue  = int (r * 255)
	elif section == 4:
		temp  = (theta - s_theta * 4) / s_theta
		red   = int (temp * 255)
		green = 0
		blue  = int (r * 255)
	elif section == 5:
		red   = int (r * 255)
		green = 0
		temp  = (theta - s_theta * 5) / s_theta
		temp  = 1 - temp
		blue  = int (temp * 255)
	else: raise Exception (section)
	return (red, green, blue)



from random import randrange, uniform

def random_point (xymin, xymax, pts=None):
	xmin, ymin = xymin
	xmax, ymax = xymax
	x = randrange (xmin, xmax)
	y = randrange (ymin, ymax)
	while True:
		pt = Point (x, y)
		if pts is None: break
		if pt in pts: continue
		if len (pts) <= 2: break
		for a, b in zip (pts[:-1], pts[1:]):
			line = Line (a, b)
			if line.contains (pt): continue
	return pt
def random_points (xymin, xymax, n):
	pts = []
	for k in range (0, n):
		pt = random_point (xymin, xymax, pts)
		pts = pts + [pt]
	return pts
def random_line     (xymin, xymax): return Line     (*random_points (xymin, xymax, 2))
def random_angle    (xymin, xymax): return Angle    (*random_points (xymin, xymax, 3))
def random_triangle (xymin, xymax): return Triangle (*random_points (xymin, xymax, 3))
	



def pentagram (npoint, d):
	#r = 10
	r = 1
	thetas = [point / npoint * 2 * pi for point in range (0, npoint)]
	points = [Point (r * cos (theta), r * sin (theta)) for theta in thetas]
	#a = 0
	#b = 0 + d
	lines = []
	#for k in range (0, npoint % d + 1):
	print ("npoint=%s, d=%s, gcd=%s" % (npoint, d, gcd (npoint, d)))
	div = gcd (npoint, d)
	for k in range (0, div):
		a = k
		b = k + d
		#lines = []
		#for p in range (0, ceil (npoint / d)):
		for p in range (0, npoint // div):
	#for k in range (0, len (points)):
		#p = k + d
		#while p >= len (points): p = p - len (points)
			while a >= len (points): a = a - len (points)
			while b >= len (points): b = b - len (points)
			A = points[a]
			B = points[b]
			lines = lines + [Line (A, B)]
			a = a + d
			b = b + d
		#all_lines = all_lines + lines
	return lines
		
#def pentagrams (npoint):
#	ds = [d for d in range (2, npoint - 1) if gcd (npoint, d) == 1]
#	# TODO filter similar stars
#	for d in ds:
#		yield pentagram (npoint, d)
#def pentagrams2 ():
#	npoint = 5
#	while npoint <= 31:
#		yield pentagrams (npoint)
#		npoint = npoint + 1
#def intersection (line1, line2):
#	a1, b1, c1 = line1.standard_form ()
#	a2, b2, c2 = line2.standard_form ()
#	determinant = a1 * b2 - a2 * b1
#	if determinant == 0: return None # parallel
#	x = c1 * b2 - c2 * b1
#	x = x / determinant
#	y = a1 * c2 - a2 *c1
#	y = y / determinant
#	pt = Point (x, y)
#	if not line1.contains (pt): return None
#	if not line2.contains (pt): return None
#	return pt
class Pentagram:
	def __init__ (self, star):
		assert len (star) > 0
		#assert len (star) >= 5
		self.star = star
		self.dist = self.distance ()
		#assert self.dist > 0
		assert self.dist >= 0
	def inside_pts (self):
		pts = []
		for line1, line2 in product (self.star, self.star):
			#if line1 == line2: continue
			#pt = intersection (line1, line2)
			pt = line1.intersection (line2)
			if pt is None: continue
			#if not line1.contains (pt): continue
			#assert not line2.contains (pt)
			#if pt in pts: continue
			flag = 1
			for p in pts:
				if p.x == pt.x and p.y == pt.y: flag = 0
				#if pt.x < -1 or pt.x > 1: flag = 0
				#if pt.y < -1 or pt.y > 1: flag = 0
			if flag: pts = pts + [pt]
		return pts
	def inside_lines (self):
		pts = self.inside_pts ()
		assert len (pts) > 0
		print ("pts=%s" % len (pts))
		return (Line (a, b) for a, b in zip (pts[:-1], pts[1:]))
	#def inside_mids (self): return (line.midpoint () for line in self.inside_lines ())
	def inside_mids (self): return (line.midpoint () for line in self.star)
	def distances (self):
		origin = Point (0, 0)
		return (Line (origin, pt).distance () for pt in self.inside_mids ())
	def distance (self): return min (self.distances ())
	def translate (self, xmin, ymin): return Pentagram ([s.translate (xmin,   ymin)   for s in self.star])
	def reflectX (self, xdiff):       return Pentagram ([s.reflectX  (xdiff)          for s in self.star])
	def reflectY (self, ydiff):       return Pentagram ([s.reflectY  (ydiff)          for s in self.star])
	def scale (self, xscale, yscale): return Pentagram ([s.scale     (xscale, yscale) for s in self.star])
	def round (self):                 return Pentagram ([s.round ()                   for s in self.star])
	def draw (self, screen):
		#for s in self.il: s.draw (screen) # TODO
		for s in self.star: s.draw (screen)
pentagrams_cache = {}
def pentagram0  (npoint, d):
	if (npoint, d) in pentagrams_cache: return pentagrams_cache[(npoint, d)]
	p = Pentagram (list (pentagram (npoint, d)))
	#assert len (list (p.inside_pts ())) == npoint
	pentagrams_cache[(npoint, d)] = p
	return p
def rotate (pentagram, angle):
	star = [pt.rotate (angle) for pt in pentagram.star]
	return Pentagram (star)
def pentagrams0_rec (outside, npds, inv=True):
	if len (npds) == 0: return []
	npd0 = npds[0]
	#npd0 = next (npds)
	npoint, d = npd0
	npds = npds[1:]
	inside  = pentagram0 (npoint, d)
	dist    = outside.distance ()
	if npoint == len (outside.star):
		# TODO
		xscale, yscale = dist, dist
	else: xscale, yscale = dist, dist
	if inv:
		if npoint % 2 == 0:
			angle = 2 * pi / npoint
			angle = angle / 2
			inside = rotate (inside, angle)
		else:  inside = inside.reflectX (0)
	inside  = inside.scale (xscale, yscale)
	return chain ([inside], pentagrams0_rec (inside, npds, not inv))
def pentagrams0 (npds):
	npd0 = npds[0]
	#npd0 = next (npds)
	npoint, d = npd0
	npds = npds[1:]
	outside = pentagram0 (npoint, d)
	return chain ([outside], pentagrams0_rec (outside, npds))
#	inside  = pentagram0 (npoint, d)
#	dist    = outside.distance ()
#	#xscale  = (1 - dist) / 1
#	#yscale  = (1 - dist) / 1
#	xscale, yscale = dist, dist
#	print ("dist=%s" % dist)
#	#xscale  = 1 / (1 - dist)
#	#yscale  = 1 / (1 - dist)
#	inside  = inside.reflectX (0)
#	inside  = inside.scale (xscale, yscale)
#	return [outside, inside]
#	#return [outside]

def pentagrams1 ():
#	npds = generate_coprime_pairs (5, 32)
#	npds = filter (lambda x: x[1] <= 31 and x[1] >= 5, npds)
#	for npd in npds: print (npd)
#	npds = ((npoint, d) for d, npoint in npds)
#	while True:
#		temp = (next (npds) for _ in range (0, 4))
#		yield pentagrams0 (temp)
	min_n = 4
	max_n = 17
	npds0 = list (generate_coprime_pairs (8, 31, False))
	npds1 = list (generate_coprime_pairs (7, 29, True))
	npds2 = list (generate_coprime_pairs (6, 23, False))
	npds3 = list (generate_coprime_pairs (5, 19, True))
	npds4 = list (generate_coprime_pairs (4, 17, False))
	npds5 = list (generate_coprime_pairs (3, 13, True))
	#npds = list (generate_coprime_pairs (5, 10))
	#npds = product (npds, npds, npds, npds)
	npds = product (npds0, npds1, npds2, npds3, npds4, npds5)
	#npds = product (npds5, npds4, npds3, npds2, npds1, npds0)
	npds = (npd[::-1] for npd in npds)
	#npds = pentagrams1_helper (npds)
	for npd in npds: yield pentagrams0 (npd)
#def pentagrams1_helper (npds):
#	return (npd[::-1] for npd in product (npds, npds, npds, npds, npds, npds))
#	#for npd0 in npds:
#	#	for npd1 in npds:
#	#		for npd2 in npds:
#	#			for npd3 in npds:
#	#				#yield (npd0, npd1, npd2, npd3)
#	#				yield (npd3, npd2, npd1, npd0)
def generate_coprime_pairs (min_n, max_n, INV):
	inv = INV
	for npoint in range (min_n, max_n + 1):
		#ds = [d for d in range (2, npoint // 2 + 1) if gcd (npoint, d) == 1]
		#ds = [d for d in range (2, npoint // 2)]
		#ds = [d for d in range (2, ceil (npoint / 2))]
		#ds = [d for d in range (1, ceil (npoint / 2))]
		ds = [d for d in range (2, ceil (npoint / 2))]
		if len (ds) == 0: ds = [1]
		d_mod = {}
		for d in ds:
			mod = npoint % d
			if mod in d_mod: continue
			d_mod[mod] = d
		ds = list (d_mod.values ())
		if inv: ds = ds[::-1]
		inv = not inv
		for d in ds: yield npoint, d
		# TODO yield ds in order but reverse order for every other layer
		#while len (ds) > 1:
		#	d  = ds[0]
		#	yield npoint, d
		#	d  = ds[-1]
		#	yield npoint, d
		#	ds = ds[1:-1]
		#if len (ds) == 1: yield npoint, ds[0]
#def generate_coprime_pairs (p):
#	return generate_coprime_pairs_leaves (
#		generate_coprime_pairs_roots (p), p)
#def generate_coprime_pairs_roots (p):
#	return [(m, 1) for m in [2, 3] if m <= p]
#def generate_coprime_pairs_leaves (q, p):
#	todo = []
#	todo.extend (q)
#	map (todo.extend, [
#		generate_coprime_pairs_leaves (
#			generate_coprime_pairs_leaf (e[0], e[1], p), p)
#		for e in q])
#	return todo
#def generate_coprime_pairs_leaf (m, n, p):
#	return [k for k in [
#		(2 * m - n, m),
#		(2 * m + n, m),
#		(m + 2 * n, n)]
#		if k[0] <= p]

position_db = {
	"aleph1" : (0,  0), # e
	"mem"    : (0,  1),
	"sin"    : (0,  2),
	"peh"    : (1,  0),
	"resh"   : (1,  1),
	"bet"    : (1,  2),
	"dalet"  : (1,  3),
	"gimel"  : (1,  4),
	"tet"    : (1,  5), # thet
	"kaf"    : (1,  6),
	"he"     : (2,  0),
	"vav"    : (2,  1),
	"zayin"  : (2,  2),
	"chet"   : (2,  3),
	"tet"    : (2,  4),
	"yod"    : (2,  5),
	"lamed"  : (2,  6),
	"nun"    : (2,  7),
	"sin"    : (2,  8),
	"aleph2" : (2,  9), # o
	"tsadeh" : (2, 10), # ayin
	"qof"    : (2, 11),
}
ringsz_db = {
	0 : 3,
	1 : 7,
	2 : 12,
}
transliteration_db = {
	"A"  : "aleph2",
	"O"  : "aleph2",
	"E"  : "aleph1",
	"B"  : "bet",
	"V"  : "bet",
	"G"  : "gimel",
	"Gh" : "gimel",
	"D"  : "dalet",
	"Dh" : "dalet",
	"H"  : "he",
	"W"  : "vav",
	"U"  : "vav",
	"Z"  : "zayin",
	"H"  : "chet",
	"T"  : "tet",
	"Th" : "tet",
	"Y"  : "yod",
	"I"  : "yod",
	"J"  : "yod",
	"K"  : "kaf",
	"Kh" : "kaf",
	"C"  : "kaf",
	"L"  : "lamed",
	"M"  : "mem",
	"N"  : "nun",
	"S"  : "samech",
	#"ayin",
	"P"  : "peh",
	"Ph" : "peh",
	"F"  : "peh",
	"Ts" : "tsadeh",
	"Q"  : "qof",
	"R"  : "resh",
	"Rh" : "resh",
	"S"  : "sin",
	"Sh" : "sin",
	"T"  : "tav",
}
def polar (ring, index):
	nring  = len (ringsz_db)
	radius = (1 + ring) / (nring + 1)
	ringsz = ringsz_db[ring]
	segsz  = index / ringsz
	angle  = segsz * 2 * pi
	if ring % 2: angle = angle + segsz / 2
	angle  = angle + pi / 2
	return angle, radius
def perpendicular (slope):
	if slope is None: return 0
	if slope == 0:    return None
	return 1 / slope
def cartesian (angle, radius):
	x = radius * cos (angle)
	y = radius * sin (angle)
	return (x, y)
def sigil (string, width, height):
	if len (string) <= 1: raise Exception ()
	string = string.upper ()                                             # normalize
	# TODO kh, ph, sh, ts
	string = (transliteration_db [char]  for char in string)             # transliterate; directionality of the script is irrelevant
	string = (position_db        [char]  for char in string)             # positions on diagram
	string = (polar     (*char)          for char in string)             # polar     coordinates
	string = (cartesian (*char)          for char in string)             # cartesian coordinates
	string = [Point     (*char)          for char in string]
	string = [Line (p0, p1) for p0, p1 in zip (string[:-1], string[1:])] # relative coordinates for sigil
	string = [line.scale (width, height) for line in string]             # absolute coordinates for sigil
	#for line in string:
	#	assert line.a.x >
	
	first  = string[ 0]                                                  # first line
	start  = first.a                                                     # start point
	angle  = first.angle ()
	radius = 1
	dx, dy = cos (angle), sin (angle)
	#dx, dy =      1 - dx,      1 - dy
	dx, dy = radius * dx, radius * dy
	x,  y  = start.x + dx,         start.y + dy
	new_a  = Point (x, y)                                                # adjust for circle
	assert new_a != first.a
	assert new_a.x != first.a.x or new_a.y != first.a.y
	first  = Line (new_a, first.b)                                       # shortened first line
	string[0] = first                                                    # replace first line
	circle = Circle (start, radius)                           # path start indicator
	
	last   = string[-1]                                                  # last line
	end    = last.b                                                      # end point
	angle  = last.angle ()
	angle  = angle + pi / 2
	radius = 1
	dx, dy = radius * cos (angle), radius * sin (angle)
	ax, ay = end.x - dx,           end.y - dy
	bx, by = end.x + dx,           end.y + dy
	a      = Point (ax, ay)                                              # end point's perpendicular's start point
	b      = Point (bx, by)                                              # end point's perpendicular's end   point
	dash   = Line (a, b)                                                 # path end indicator
	
	return Sigil ([circle] + string + [dash])                            # completed sigil
class Sigil:
	def __init__ (self, sigil): self.sigil = sigil
	def translate (self, xmin, ymin): return Sigil ([s.translate (xmin,   ymin)   for s in self.sigil])
	def reflectX (self, xdiff):       return Sigil ([s.reflectX  (xdiff)          for s in self.sigil])
	def reflectY (self, ydiff):       return Sigil ([s.reflectY  (ydiff)          for s in self.sigil])
	def scale (self, xscale, yscale): return Sigil ([s.scale     (xscale, yscale) for s in self.sigil])
	def round (self):                 return Sigil ([s.round ()                   for s in self.sigil])
	def draw (self, screen):
		for s in self.sigil: s.draw (screen)
	

class Text:
	def __init__ (self, text): self.text = text
	def draw (self, screen):
		width  = screen.get_width  ()
		height = screen.get_height ()
		font  = pygame.font.Font ('freesansbold.ttf', 32)
		red   = (255, 0, 0)
		black = (  0, 3, 0)
		text  = font.render (self.text, True, red, black)
		rect  = text.get_rect ()
		rect.center = (width / 2, height / 2)
		screen.blit (text, rect) 
def text (string, delay1=3, delay2=5):
	#texts = [[]] * delay1
	texts = []
	for k in range (0, len (string)):
		text  = string[:k]
		text  = Text (text)
		texts = texts + [[text]]
	texts = texts + [[Text (string)]] * delay2
	return texts





def animation0_helper (sigil_txt, width, height, gen):
	#print ("sigil txt: %s" % sigil_txt)
	sigil_obj = sigil (sigil_txt, width, height)
	sigil_obj = sigil_obj.scale (1 / width, 1 / height)
	#print ("sigil len: %s" % len (sigil_obj.sigil))
	#assert len (sigil_txt) == len (sigil_obj.sigil)
	
	circle = sigil_obj.sigil[0]
	radius = circle.r
	scale  = radius
	dx     = circle.pt.x
	dy     = circle.pt.y
	
	#lines = []
	lines = animation3a (width, height, gen)
	
	# move circle from origin to location
	R = min (width, height)
	for k in range (0, int (R)):
		k = (k + 1) / R
		x = dx * k
		y = dy * k
		#c = circle.translate (x, y)
		#p = Point (x, y)
		#c = Circle (p, circle.r)
		penta = next (gen)
		penta = [k.scale (scale, scale) for k in penta]
		penta = [k.translate (-x, -y) for k in penta]
		lines = lines + [penta]
	
	for k in range (1, len (sigil_obj.sigil) + 1):
		line  = sigil_obj.sigil[:k]
		penta = next (gen)
		#penta = [k.scale (scale, scale) for k in penta]
		#penta = [k.translate (-dx, -dy) for k in penta]
		#lines = lines + [penta + line]
		lines = lines + [line]
	line = sigil_obj.sigil
	for k in range (0, 7):	
		penta = next (gen)
		#penta = [k.scale (scale, scale) for k in penta]
		#penta = [k.translate (-dx, -dy) for k in penta]
		#lines = lines + [penta + line]
		lines = lines + [line]
		
	for k in range (0, int (R)):
		k = (R - k) / R
		x = dx * k
		y = dy * k
		#p = Point (x, y)
		#c = Circle (p, circle.r)
		penta = next (gen)
		penta = [k.scale (scale, scale) for k in penta]
		penta = [k.translate (-x, -y) for k in penta]
		lines = lines + [penta]
		
	lines = lines + animation3a_rev (width, height, gen)
	
	#lines = lines + [sigil_obj.sigil] * 7
	#print ("lines=%s" % lines)
	return lines
def animation0a (width, height, gen): # InnovAnon
	sigil_txt = "InouvAnon"
	#return animation0_helper (sigil_txt, width, height)
	display   = text ("InnovAnon")
	return display + animation0_helper (sigil_txt, width, height, gen)
def animation0b (width, height, gen): # Innovations
	sigil_txt = "Inouveisuns"
	display   = text ("Innovations")
	return display + animation0_helper (sigil_txt, width, height, gen)
def animation0c (width, height, gen): # Anonymous
	sigil_txt = "Anonoumus"
	display   = text ("Anonymous")
	return display + animation0_helper (sigil_txt, width, height, gen)
def animation0d (width, height, gen): # Free Code
	sigil_txt = "FriCoud"
	display   = text ("Free Code")
	return display + animation0_helper (sigil_txt, width, height, gen)
def animation0e (width, height, gen, delay1=1): # Free World
	sigil_txt = "FriWorld"
	display   = text ("Free World", delay1)
	return display + animation0_helper (sigil_txt, width, height, gen)
def animation0 (width, height, gen): return animation0a (width, height, gen) + animation0b (width, height, gen) + animation0c (width, height, gen) + animation0d (width, height, gen) + text ("for a", 1, 2) + animation0e (width, height, gen)
	
def animation1a (r): # 0d to 1d; point to line
	origin = Point (0, 0)
	lines = [[origin]]
	#for x in chain (range (0, int (r)), [r] * 5):
	for x in range (0, int (1 * r)):
		x = x / r
		other = Point (x, 0)
		line  = Line (origin, other)
		lines = lines + [[line]]
	x     = r
	other = Point (x, 0)
	line  = Line (origin, other)
	lines = lines + [[line]] * 5
	return lines
def animation1b (ntheta): # 1d to 2d; line to circle
	origin = Point (0, 0)
	#lines = [[origin]]
	lines = []
	for theta_i in range (0, int (ntheta)):
		theta = theta_i / ntheta * 2 * pi
		x     = cos (theta)
		y     = sin (theta)
		other = Point (x, y)
		line  = Line (origin, other)
		#arc   = Arc (0 - 1, 0 + 1, 1, 1, 0, theta)
		#arc   = Arc (-1/2, 1.5, 1, 1, 0, theta)
		arc   = Arc (origin, 1, 1, 0, theta)
		lines = lines + [[line, arc]]
	theta = 0
	x     = cos (theta)
	y     = sin (theta)
	other = Point (x, y)
	line  = Line (origin, other)
	arc   = Circle (origin, 1)
	lines = lines + [[line, arc]] * 3
	
	for x in range (0, int (1 * ntheta) + 1):
		x = x / ntheta
		x = 1 - x
		other = Point (x, 0)
		line  = Line (origin, other)
		lines = lines + [[line, arc]]

	lines = lines + [[arc, origin]] * 2
	return lines
def animation1c_helper (line, pt, radius):
	angle  = line.angle ()
	angle  = angle + pi / 2
	dx, dy = radius * cos (angle), radius * sin (angle)
	ax, ay = pt.x - dx,            pt.y - dy
	bx, by = pt.x + dx,            pt.y + dy
	a      = Point (ax, ay)                                              # end point's perpendicular's start point
	b      = Point (bx, by)                                              # end point's perpendicular's end   point
	dash   = Line (a, b)                                                 # path end indicator
	return dash
def animation2c (width, height, gen): # point to circle
	r = min (width, height)
	origin = Point (0, 0)
	lines = [[origin]]
	for x in range (0, int (r)):
		x = (x + 1) / r
		circle = Circle (origin, x)
		penta  = [k.scale (x, x) for k in next (gen)]
		lines = lines + [[circle] + penta]
	return lines
	
def animation2a (r): # add axes, shrink circle (some), expand end points for four-corners sigil
	origin = Point (0, 0)
	lines = [[origin, Circle (origin, 1)]]
	for x in range (0, int (1 * r)):
		x      = x / r
		a      = Point (-x,  0)
		b      = Point (+x,  0)
		c      = Point ( 0, -x)
		d      = Point ( 0, +x)
		x_axis = Line  ( a,  b)
		y_axis = Line  ( c,  d)
		arc    = Circle (origin, 1 - (1 + x) / r)
		lines = lines + [[x_axis, y_axis, arc]]
	a      = Point (-1,  0)
	b      = Point (+1,  0)
	c      = Point ( 0, -1)
	d      = Point ( 0, +1)
	x_axis = Line  ( a,  b)
	y_axis = Line  ( c,  d)
	arc    = Circle (origin, 1 - (1 + 1) / r)
	lines = lines + [[x_axis, y_axis, arc]]
	#for x in range (0, int (pi * r)):
	for x in range (0, int (1 * r)):
		x = x / r
		#x = x / r
		x = x * pi / r
		e = animation1c_helper (x_axis, a, x)
		f = animation1c_helper (x_axis, b, x)
		g = animation1c_helper (y_axis, c, x)
		h = animation1c_helper (y_axis, d, x)
		lines = lines + [[x_axis, y_axis, arc, e, f, g, h]]
	x = pi
	x = x / r
	e = animation1c_helper (x_axis, a, x)
	f = animation1c_helper (x_axis, b, x)
	g = animation1c_helper (y_axis, c, x)
	h = animation1c_helper (y_axis, d, x)
	#lines = lines + [[x_axis, y_axis, arc, e, f, g, h]] * 5
	lines = lines + [[x_axis, y_axis, arc, e, f, g, h]]
	return lines
	
	
	
	
	
	
	
	
	
def animation2aa (r, gen): # four corners; scale-down-cross in circle; scale-down-point in circle; scale-down-hollow four corners with scale-up-penta; hollow four corners with scale-down-penta; cross; four corners
	origin = Point (0, 0)
	
	a      = Point (-1,  0)
	b      = Point (+1,  0)
	c      = Point ( 0, -1)
	d      = Point ( 0, +1)
	x_axis = Line  ( a,  b)
	y_axis = Line  ( c,  d)
	
	x = pi
	x = x / r
	X = x
	e = animation1c_helper (x_axis, a, x)
	f = animation1c_helper (x_axis, b, x)
	g = animation1c_helper (y_axis, c, x)
	h = animation1c_helper (y_axis, d, x)
	
	cross = [x_axis, y_axis, e, f, g, h]
	max_r = 1
	min_r = 1 - (1 + 1) / r
	arc   = Circle (origin, min_r)
	#four_corners = cross + [arc]
	
	max_w = 2
	min_w = 2 * min_r
	d_w   = pow (min_w / max_w, 1 / int (r))
	d_r   = pow (max_r / min_r, 1 / int (r))
	
	#lines = [[cross + [arc]]
	lines = []
	for x in range (0, int (r)):
		cross = [shape.scale (d_w, d_w) for shape in cross]
		arc   = arc.scale (d_r, d_r)
		lines = lines + [cross + [arc]]
	
	d_r   = pow (min_r / max_r, 1 / int (r))
	
	max_w = min_w
	min_w = 2 / r / r
	d_w   = pow (min_w / max_w, 1 / int (r))
	for x in range (0, int (r)):
		cross = [shape.scale (d_w, d_w) for shape in cross]
		arc   = arc.scale (d_r, d_r)
		
		#a      = Point (-1,  0)
		#b      = Point (+1,  0)
		#c      = Point ( 0, -1)
		#d      = Point ( 0, +1)
		k = max_r - (x + 1) * (max_r - min_r) / r
		a1     = Point (-k,  0)
		b1     = Point (+k,  0)
		c1     = Point ( 0, -k)
		d1     = Point ( 0, +k)
		#x_axis = Line  ( a,  b)
		#y_axis = Line  ( c,  d)
		x_axis1 = Line (a,  a1)
		x_axis2 = Line (b1, b)
		y_axis1 = Line (c,  c1)
		y_axis2 = Line (d1, d)
		w = (x / r) * (pi / r)
		e = animation1c_helper (x_axis1, a, w)
		f = animation1c_helper (x_axis2, b, w)
		g = animation1c_helper (y_axis1, c, w)
		h = animation1c_helper (y_axis2, d, w)
		cross2 = [x_axis1, e, x_axis2, f, y_axis1, g, y_axis2, h]
		lines = lines + [cross + [arc] + cross2]
		
		
		
	max_r = min_r
	min_r = 1 / r / r
	d_r   = pow (min_r / max_r, 1 / int (r))
	for x in range (0, int (r)):
		#cross = [shape.scale (d_w, d_w) for shape in cross]
		arc   = arc.scale (d_r, d_r)
		
		#dp = ((x + 1) / r) * (max_r)
		#dp = ((x + 1) / r) * (max_r - min_r)
		#dp = pow (d_r, x + 1)
		#dp = dp * arc.r
		#dp = arc.r
		#dp = log (x) / log (r)
		#dpr = pow (1 / min_r, 1 / int (r))
		#dpr = arc.r
		#dp = pow (dpr, (x + 1) / r)
		#xx = x / r
		#dp = (x + 1) * pow (1 / r, x + 1)
		#dp = (x + 1) / r
		#dp = pow (d_r, (x + 1) / r)
		#dp = pow (1 / d_r, x + 1)
		#dp = pow (d_r, r - x - 1)
		#dp = pow (1 / d_r, (x + 1) / r)
		#dp = min_r * dp
		#dp = pow (r, (x + 1) / r) / r
		#dp = (log (1) - log (r)) / log (r)
		#dp = arc.r
		#dp = (x + 1) / r
		#dp = (1 - min_r) * pow (dp, (x + 1) / r)
		#dp = pow (arc.r / min_r, 1 / r)
		#dp = pow (1 / (1 - min_r), 1 / r)
		#dp = pow ((1 - min_r) / min_r, 1 / r)
		#dp = pow ((1 - min_r) / r, 1 / r)
		#dp = 1 / min_r
		#dp = (1 - min_r)
		#dp = 1 / dp
		#dp = dp / r
		#dp = 1 / r
		#dp = 1 / dp
		#dp = pow (min_r / (1 - min_r), 1 / r)
		#dp = pow (r, x + 1) / pow (r, r)
		#dp = pow (dp, r - x)
		#dp = (r - x) / r
		dp = (x + 1) / r # fuck it
		#dp = r / (x + 1)
		#dp = pow ((1 - min_r) / min_r, 1 / r)
		#dp = pow (dp, x + 1)
		#dp = dp * (1 - min_r)
		#dp = pow (x + 1, 1 / r) / pow (r, 1 / r)
		#dp = pow (1 / min_r, 1 / r)
		#dp = pow (1 / min_r, 1 / r)
		#dp = pow (dp, x + 1)
		#dp = 1
		dp = dp * arc.r
		penta = [shape.scale (dp, dp) for shape in next (gen)]
		
		#a      = Point (-1,  0)
		#b      = Point (+1,  0)
		#c      = Point ( 0, -1)
		#d      = Point ( 0, +1)
		#k = max_r - (x) * (max_r - min_r) / r
		k = arc.r
		a1     = Point (-k,  0)
		b1     = Point (+k,  0)
		c1     = Point ( 0, -k)
		d1     = Point ( 0, +k)
		#x_axis = Line  ( a,  b)
		#y_axis = Line  ( c,  d)
		x_axis1 = Line (a,  a1)
		x_axis2 = Line (b1, b)
		y_axis1 = Line (c,  c1)
		y_axis2 = Line (d1, d)
		#w = (x / r) * (pi / r)
		e = animation1c_helper (x_axis1, a, X)
		f = animation1c_helper (x_axis2, b, X)
		g = animation1c_helper (y_axis1, c, X)
		h = animation1c_helper (y_axis2, d, X)
		cross2 = [x_axis1, e, x_axis2, f, y_axis1, g, y_axis2, h]
		lines = lines + [penta + [arc] + cross2]
	
	a      = Point (-1,  0)
	b      = Point (+1,  0)
	c      = Point ( 0, -1)
	d      = Point ( 0, +1)
	x_axis = Line  ( a,  b)
	y_axis = Line  ( c,  d)
	
	x = pi
	x = x / r
	X = x
	e = animation1c_helper (x_axis, a, x)
	f = animation1c_helper (x_axis, b, x)
	g = animation1c_helper (y_axis, c, x)
	h = animation1c_helper (y_axis, d, x)
	
	cross = [x_axis, y_axis, e, f, g, h]
	min_r = 1 / r / r
	max_r = 1 - (1 + 1) / r
	arc   = Circle (origin, min_r)
	d_r   = pow (max_r / min_r, 1 / int (r))
	for x in range (0, int (r)):
		arc   = arc.scale (d_r, d_r)
		lines = lines + [cross + [arc]]
	return lines	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
def animation2ab_helper (line, pt, radius, theta):
	angle  = line.angle ()
	angle  = angle + pi / 2
	angle1 = angle - theta
	angle2 = angle + theta
	dx1, dy1 = radius * cos (angle1), radius * sin (angle1)
	dx2, dy2 = radius * cos (angle2), radius * sin (angle2)
	ax1, ay1 = pt.x - dx1,            pt.y - dy1
	#bx1, by1 = pt.x + dx1,            pt.y + dy1
	#ax2, ay2 = pt.x - dx2,            pt.y - dy2
	bx2, by2 = pt.x + dx2,            pt.y + dy2
	a1      = Point (ax1, ay1)                                              # end point's perpendicular's start point
	#b1      = Point (bx1, by1)                                              # end point's perpendicular's end   point
	#a2      = Point (ax2, ay2)                                              # end point's perpendicular's start point
	b2      = Point (bx2, by2)                                              # end point's perpendicular's end   point
	dash1   = Line (pt, a1)                                                 # path end indicator
	dash2   = Line (pt, b2)                                                 # path end indicator
	return dash1, dash2
def animation2ab (r): # rotate and mirror cross, midway through the rotaton, the lines should be arrows of length 1, and the circle shrinks
	origin = Point (0, 0)
	
	a      = Point (-1,  0)
	b      = Point (+1,  0)
	c      = Point ( 0, -1)
	d      = Point ( 0, +1)
	x_axis = Line  ( a,  b)
	y_axis = Line  ( c,  d)
	
	# radius of circle
	max_r = 1 - (1 + 1) / r
	min_r = 1 / r / r
	dr    = (max_r - min_r) / (r * 2)
	
	# length of arrows
	max_x = pi / r
	min_x = 1 / r
	dx    = (max_x - min_x) / r
	
	# rotation of axes
	max_theta = pi / 2
	min_theta = 0
	dtheta    = (max_theta - min_theta) / r
		
	# rotation of arrows
	max_theta2 = pi / 4
	min_theta2 = 0
	dtheta2    = (max_theta2 - min_theta2) / r
	
	max_w = 1
	min_w = 1 / r / r
	dw    = (max_w - min_w) / r
	
	lines = []
	for X in range (0, int (r * 1)): # perpendiculars to arrows and rotate axes
		print ("X=%s" % X)
		theta  = min_theta  + X * dtheta
		#R      = max_r      - X * dr
		w      = min_w      + X * dw
		x      = max_x      - X * dx
		theta2 = min_theta2 + X * dtheta2
		if X < r: # [0, r)
			X2 = X
		else:     # [r, 0)
			X2 = X - r
		R      = max_r      - X2 * dr
		print ("R=%s" % R)
		print ("x=%s" % x)
		print ("theta1=%s" % theta)
		print ("theta2=%s" % theta2)
		
		x_axis1 = x_axis.rotate ( theta)
		y_axis1 = y_axis.rotate ( theta)
		e1, e2 = animation2ab_helper (x_axis1, x_axis1.a, x, -theta2)
		f1, f2 = animation2ab_helper (x_axis1, x_axis1.b, x,  theta2)
		g1, g2 = animation2ab_helper (y_axis1, y_axis1.a, x, -theta2)
		h1, h2 = animation2ab_helper (y_axis1, y_axis1.b, x,  theta2)
		shape1 = [x_axis1, y_axis1, e1, e2, f1, f2, g1, g2, h1, h2]
		
		x_axis2 = x_axis.rotate (-theta)
		y_axis2 = y_axis.rotate (-theta)
		e1, e2 = animation2ab_helper (x_axis2, x_axis2.a, x, -theta2)
		f1, f2 = animation2ab_helper (x_axis2, x_axis2.b, x,  theta2)
		g1, g2 = animation2ab_helper (y_axis2, y_axis2.a, x, -theta2)
		h1, h2 = animation2ab_helper (y_axis2, y_axis2.b, x,  theta2)
		shape2 = [x_axis2, y_axis2, e1, e2, f1, f2, g1, g2, h1, h2]
		
		e1, e2 = animation2ab_helper (x_axis, x_axis.a, min_x, -max_theta2)
		f1, f2 = animation2ab_helper (x_axis, x_axis.b, min_x,  max_theta2)
		g1, g2 = animation2ab_helper (y_axis, y_axis.a, min_x, -max_theta2)
		h1, h2 = animation2ab_helper (y_axis, y_axis.b, min_x,  max_theta2)
		shape3  = [x_axis, y_axis, e1, e2, f1, f2, g1, g2, h1, h2]
		shape3  = [shape.scale (w, w) for shape in shape3]
		
		arc = Circle (origin, R)
		
		lines = lines + [[arc] + shape1 + shape2 + shape3]
		#lines = lines + [shape1]
		#lines = lines + [shape2]
		
	max_theta = pi / 4
	min_theta = 0
	dtheta    = (max_theta - min_theta) / r
		
	for X in range (0, int (r * 1)):
		print ("X=%s" % X)
		theta  = min_theta  + X * dtheta
		#R      = max_r      - X * dr
		w      = min_w      + X * dw
		#x      = max_x      - X * dx
		x = min_x
		#theta2 = min_theta2 + X * dtheta2
		theta2 = max_theta2
		if X < r: # [0, r)
			X2 = r + X
		else:     # [r, 0)
			X2 = X
		R      = max_r      - X2 * dr
		print ("R=%s" % R)
		print ("x=%s" % x)
		print ("theta1=%s" % theta)
		print ("theta2=%s" % theta2)
		
		x_axis1 = x_axis.rotate ( theta)
		y_axis1 = y_axis.rotate ( theta)
		e1, e2 = animation2ab_helper (x_axis1, x_axis1.a, x, -theta2)
		f1, f2 = animation2ab_helper (x_axis1, x_axis1.b, x,  theta2)
		g1, g2 = animation2ab_helper (y_axis1, y_axis1.a, x, -theta2)
		h1, h2 = animation2ab_helper (y_axis1, y_axis1.b, x,  theta2)
		shape1 = [x_axis1, y_axis1, e1, e2, f1, f2, g1, g2, h1, h2]
		
		x_axis2 = x_axis.rotate (-theta)
		y_axis2 = y_axis.rotate (-theta)
		e1, e2 = animation2ab_helper (x_axis2, x_axis2.a, x, -theta2)
		f1, f2 = animation2ab_helper (x_axis2, x_axis2.b, x,  theta2)
		g1, g2 = animation2ab_helper (y_axis2, y_axis2.a, x, -theta2)
		h1, h2 = animation2ab_helper (y_axis2, y_axis2.b, x,  theta2)
		shape2 = [x_axis2, y_axis2, e1, e2, f1, f2, g1, g2, h1, h2]

		e1, e2 = animation2ab_helper (x_axis, x_axis.a, min_x, -max_theta2)
		f1, f2 = animation2ab_helper (x_axis, x_axis.b, min_x,  max_theta2)
		g1, g2 = animation2ab_helper (y_axis, y_axis.a, min_x, -max_theta2)
		h1, h2 = animation2ab_helper (y_axis, y_axis.b, min_x,  max_theta2)
		shape3  = [x_axis, y_axis, e1, e2, f1, f2, g1, g2, h1, h2]
		#shape3  = [shape.scale (w, w) for shape in shape3]

		x_axis3 = x_axis.rotate (pi / 4)
		y_axis3 = y_axis.rotate (pi / 4)
		e1, e2 = animation2ab_helper (x_axis3, x_axis3.a, min_x, -max_theta2)
		f1, f2 = animation2ab_helper (x_axis3, x_axis3.b, min_x,  max_theta2)
		g1, g2 = animation2ab_helper (y_axis3, y_axis3.a, min_x, -max_theta2)
		h1, h2 = animation2ab_helper (y_axis3, y_axis3.b, min_x,  max_theta2)
		shape4  = [x_axis3, y_axis3, e1, e2, f1, f2, g1, g2, h1, h2]
		shape4  = [shape.scale (w, w) for shape in shape4]
		
		arc = Circle (origin, R)
		
		lines = lines + [[arc] + shape1 + shape2 + shape3 + shape4]

	max_r = 1
	dr    = (max_r - min_r) / (r * 1)
	
	max_theta = pi / 4
	min_theta = 0
	dtheta    = (max_theta - min_theta) / r

	for flag in [0, 1, 2, 3]:
		for X in range (0, int (r * 1)):
			print ("X=%s" % X)
			theta  = min_theta  + X * dtheta
			#if flag: R = max_r
			if   flag == 1: R = max_r
			elif flag == 2: R = max_r - X * dr
			else:           R = min_r      + X * dr
			w      = min_w      + X * dw
			#x      = max_x      - X * dx
			x = min_x
			#theta2 = min_theta2 + X * dtheta2
			theta2 = max_theta2
			if X < r: # [0, r)
				X2 = r + X
			else:     # [r, 0)
				X2 = X
			#R      = max_r      - X2 * dr
			print ("R=%s" % R)
			print ("x=%s" % x)
			print ("theta1=%s" % theta)
			print ("theta2=%s" % theta2)
			
			x_axis1 = x_axis.rotate ( theta)
			y_axis1 = y_axis.rotate ( theta)
			e1, e2 = animation2ab_helper (x_axis1, x_axis1.a, x, -theta2)
			f1, f2 = animation2ab_helper (x_axis1, x_axis1.b, x,  theta2)
			g1, g2 = animation2ab_helper (y_axis1, y_axis1.a, x, -theta2)
			h1, h2 = animation2ab_helper (y_axis1, y_axis1.b, x,  theta2)
			shape1 = [x_axis1, y_axis1, e1, e2, f1, f2, g1, g2, h1, h2]
			if flag > 1: shape1  = [shape.scale (R, R) for shape in shape1]
			
			x_axis2 = x_axis.rotate (-theta)
			y_axis2 = y_axis.rotate (-theta)
			e1, e2 = animation2ab_helper (x_axis2, x_axis2.a, x, -theta2)
			f1, f2 = animation2ab_helper (x_axis2, x_axis2.b, x,  theta2)
			g1, g2 = animation2ab_helper (y_axis2, y_axis2.a, x, -theta2)
			h1, h2 = animation2ab_helper (y_axis2, y_axis2.b, x,  theta2)
			shape2 = [x_axis2, y_axis2, e1, e2, f1, f2, g1, g2, h1, h2]
			if flag > 1: shape2  = [shape.scale (R, R) for shape in shape2]
			
			x_axis1 = x_axis.rotate (pi / 4 + theta)
			y_axis1 = y_axis.rotate (pi / 4 + theta)
			e1, e2 = animation2ab_helper (x_axis1, x_axis1.a, x, -theta2)
			f1, f2 = animation2ab_helper (x_axis1, x_axis1.b, x,  theta2)
			g1, g2 = animation2ab_helper (y_axis1, y_axis1.a, x, -theta2)
			h1, h2 = animation2ab_helper (y_axis1, y_axis1.b, x,  theta2)
			shape3 = [x_axis1, y_axis1, e1, e2, f1, f2, g1, g2, h1, h2]
			if flag > 1: shape3  = [shape.scale (R, R) for shape in shape3]
			
			x_axis2 = x_axis.rotate (pi / 4 -theta)
			y_axis2 = y_axis.rotate (pi / 4 -theta)
			e1, e2 = animation2ab_helper (x_axis2, x_axis2.a, x, -theta2)
			f1, f2 = animation2ab_helper (x_axis2, x_axis2.b, x,  theta2)
			g1, g2 = animation2ab_helper (y_axis2, y_axis2.a, x, -theta2)
			h1, h2 = animation2ab_helper (y_axis2, y_axis2.b, x,  theta2)
			shape4 = [x_axis2, y_axis2, e1, e2, f1, f2, g1, g2, h1, h2]
			if flag > 1: shape4  = [shape.scale (R, R) for shape in shape4]
			#shape4 = []

			e1, e2 = animation2ab_helper (x_axis, x_axis.a, min_x, -max_theta2)
			f1, f2 = animation2ab_helper (x_axis, x_axis.b, min_x,  max_theta2)
			g1, g2 = animation2ab_helper (y_axis, y_axis.a, min_x, -max_theta2)
			h1, h2 = animation2ab_helper (y_axis, y_axis.b, min_x,  max_theta2)
			shape5  = [x_axis, y_axis, e1, e2, f1, f2, g1, g2, h1, h2]
			#shape3  = [shape.scale (w, w) for shape in shape3]

			x_axis3 = x_axis.rotate (pi / 4)
			y_axis3 = y_axis.rotate (pi / 4)
			e1, e2 = animation2ab_helper (x_axis3, x_axis3.a, min_x, -max_theta2)
			f1, f2 = animation2ab_helper (x_axis3, x_axis3.b, min_x,  max_theta2)
			g1, g2 = animation2ab_helper (y_axis3, y_axis3.a, min_x, -max_theta2)
			h1, h2 = animation2ab_helper (y_axis3, y_axis3.b, min_x,  max_theta2)
			shape6  = [x_axis3, y_axis3, e1, e2, f1, f2, g1, g2, h1, h2]
			
			arc = Circle (origin, R)
			
			lines = lines + [[arc] + shape1 + shape2 + shape3 + shape4 + shape5 + shape6]
		#lines = lines + [[arc] + shape3 + shape4 + shape5 + shape6]
			
	# primary axes morph into cross
	# diag axes shrink to point
	# 4 diag spinning
	# circle shrinks to cross
	
	# radius of circle
	min_r = 1 - (1 + 1) / r
	max_r = 1
	dr    = (max_r - min_r) / (r * 1)
	
	# length of arrows
	max_x = pi / r
	min_x = 1 / r
	dx    = (max_x - min_x) / r
	
	# rotation of axes
	max_theta = pi / 4
	min_theta = 0
	dtheta    = (max_theta - min_theta) / r
		
	# rotation of arrows
	max_theta2 = pi / 4
	min_theta2 = 0
	dtheta2    = (max_theta2 - min_theta2) / r
	
	max_w = 1
	min_w = 1 / r / r
	dw    = (max_w - min_w) / r
	
	for flag in [0, 1]:
		for X in range (0, int (r * 1)):
			print ("X=%s" % X)
			theta  = min_theta  + X * dtheta
			if flag: R = min_r
			else:    R      = max_r      - X * dr
			w      = max_w      - X * dw
			#x      = max_x      - X * dx
			if flag: x2 = max_x
			else:    x2      = min_x      + X * dx
			x = min_x
			#theta2 = min_theta2 + X * dtheta2
			if flag: theta3 = min_theta2
			else:    theta3 = max_theta2 - X * dtheta2
			theta2 = max_theta2
			print ("R=%s" % R)
			print ("x=%s" % x)
			print ("theta1=%s" % theta)
			print ("theta2=%s" % theta2)
			
			x_axis1 = x_axis.rotate ( theta)
			y_axis1 = y_axis.rotate ( theta)
			e1, e2 = animation2ab_helper (x_axis1, x_axis1.a, x, -theta2)
			f1, f2 = animation2ab_helper (x_axis1, x_axis1.b, x,  theta2)
			g1, g2 = animation2ab_helper (y_axis1, y_axis1.a, x, -theta2)
			h1, h2 = animation2ab_helper (y_axis1, y_axis1.b, x,  theta2)
			shape1 = [x_axis1, y_axis1, e1, e2, f1, f2, g1, g2, h1, h2]
			shape1 = [shape.scale (R, R) for shape in shape1]
			#if flag == 2: shape1 = [shape.scale (w, w) for shape in shape1]
			if flag == 1: shape1 = []
			
			x_axis2 = x_axis.rotate (-theta)
			y_axis2 = y_axis.rotate (-theta)
			e1, e2 = animation2ab_helper (x_axis2, x_axis2.a, x, -theta2)
			f1, f2 = animation2ab_helper (x_axis2, x_axis2.b, x,  theta2)
			g1, g2 = animation2ab_helper (y_axis2, y_axis2.a, x, -theta2)
			h1, h2 = animation2ab_helper (y_axis2, y_axis2.b, x,  theta2)
			shape2 = [x_axis2, y_axis2, e1, e2, f1, f2, g1, g2, h1, h2]
			shape2 = [shape.scale (R, R) for shape in shape2]
			#if flag == 2: shape2 = [shape.scale (w, w) for shape in shape2]
			if flag == 1: shape2 = []
			
			e1, e2 = animation2ab_helper (x_axis, x_axis.a, x2, -theta3)
			f1, f2 = animation2ab_helper (x_axis, x_axis.b, x2,  theta3)
			g1, g2 = animation2ab_helper (y_axis, y_axis.a, x2, -theta3)
			h1, h2 = animation2ab_helper (y_axis, y_axis.b, x2,  theta3)
			shape3  = [x_axis, y_axis, e1, e2, f1, f2, g1, g2, h1, h2]
			#shape3  = [shape.scale (R, R) for shape in shape3]

			x_axis3 = x_axis.rotate (pi / 4)
			y_axis3 = y_axis.rotate (pi / 4)
			e1, e2 = animation2ab_helper (x_axis3, x_axis3.a, min_x, -max_theta2)
			f1, f2 = animation2ab_helper (x_axis3, x_axis3.b, min_x,  max_theta2)
			g1, g2 = animation2ab_helper (y_axis3, y_axis3.a, min_x, -max_theta2)
			h1, h2 = animation2ab_helper (y_axis3, y_axis3.b, min_x,  max_theta2)
			shape4  = [x_axis3, y_axis3, e1, e2, f1, f2, g1, g2, h1, h2]
			shape4  = [shape.scale (R, R) for shape in shape4]
			shape4  = [shape.scale (w, w) for shape in shape4]
			
			arc = Circle (origin, R)
			
			lines = lines + [[arc] + shape1 + shape2 + shape3 + shape4]
		
	return lines
	
	
	
def animation2b (r): # shrink circle (completely), shrink and remove end points of sigil, leaving only axes, then shrink axes to 0d
	origin = Point ( 0 , 0)
	a      = Point (-1,  0)
	b      = Point (+1,  0)
	c      = Point ( 0, -1)
	d      = Point ( 0, +1)
	x_axis = Line  ( a,  b)
	y_axis = Line  ( c,  d)
	lines = []
	max_r = 1 - (1 + 1) / r
	#dr    = (max_r - 0) / r
	dr    = max_r
	for x in range (0, int (1 * r)):
		x = x / r
		#x = x / r
		l = 1 - x
		l = pi / r * l
		e = animation1c_helper (x_axis, a, l)
		f = animation1c_helper (x_axis, b, l)
		g = animation1c_helper (y_axis, c, l)
		h = animation1c_helper (y_axis, d, l)
		#arc   = Circle (origin, max_r - dr * x)
		arc   = Circle (origin, max_r - dr * x)
		lines = lines + [[x_axis, y_axis, arc, e, f, g, h]]
	#lines = lines + [[x_axis, y_axis]]
	for x in range (0, int (1 * r)):
		x = x /r
		x = 1 - x
		a      = Point (-x,  0)
		b      = Point (+x,  0)
		c      = Point ( 0, -x)
		d      = Point ( 0, +x)
		x_axis = Line  ( a,  b)
		y_axis = Line  ( c,  d)
		lines = lines + [[x_axis, y_axis]]
	origin = Point (0, 0)
	lines = lines + [[origin]]
	return lines
def animation1 (width, height):
	r = min (width, height)
	#return animation1a (r) + animation1b (r) + animation1c (r) + animation1d (r)
	return animation1a (r) + animation1b (r)
	#return animation1c (r) + animation1d (r)
	#return animation1d (r)
def animation2 (width, height, gen):
	r = min (width, height)
	return animation2a (r) + animation2aa (r, gen) + animation2ab (r) + animation2b (r)
	#return animation2ab (r)
def animation3a (width, height, gen):
	R = min (width, height)
	
	origin = Point (0, 0)
	lines  = [[origin]]
		
	r = 1 / R
	for k in range (0, int (R)):
		k = (k + 1) / R * r
		circle = Circle (origin, k)
		penta  = [K.scale (k, k) for K in next (gen)]
		lines = lines + [[circle] + penta]
	
	circle = Circle (origin, r)
	temp   = [circle]
	penta  = [k.scale (r, r) for k in next (gen)]
	lines  = lines + [temp + penta]
	return lines
def animation3a_rev (width, height, gen):
	R = min (width, height)
	
	origin = Point (0, 0)
	lines  = []
		
	r = 1 / R
	for k in range (0, int (R)):
		k = (R - k) / R * r
		circle = Circle (origin, k)
		penta  = [K.scale (k, k) for K in next (gen)]
		lines = lines + [[circle] + penta]
	
	#circle = Circle (origin, r)
	temp   = [origin]
	#penta  = [k.scale (r, r) for k in next (gen)]
	#lines  = lines + [temp + penta]
	#lines = lines + [temp + [origin]]
	lines = lines + [temp]
	return lines

def animation3 (width, height, gen): # circling the square
	R = min (width, height)
	
	origin = Point (0, 0)
	#lines  = [[origin]]
	#lines = animation3a (width, height, gen)
	intro = animation3a (width, height, gen)
	lines = []
		
	r = 1 / R
	#for k in range (0, int (R)):
	#	k = (k + 1) / R * r
	#	circle = Circle (origin, k)
	#	penta  = [K.scale (k, k) for K in next (gen)]
	#	lines = lines + [[circle] + penta]
	
	#arck = 2 * log (R) / log (2)
	#arck = int (arck)
	arck = int (R)
	
	draw_arcs = True # TODO testing
	if draw_arcs:	
		for kk in range (0, arck):
			#tt = kk / R * pi / 2
			tt = kk / arck * pi / 2
			#TT = (R - kk) / R * pi / 4
			TT = (arck - kk) / arck * pi / 4
			#rr = r * pow (sc, K)
			rr = r
			aa = Arc (origin, rr, rr, TT, TT + tt)
			bb = aa.rotate (pi / 2)
			cc = bb.rotate (pi / 2)
			dd = cc.rotate (pi / 2)
			temp = [aa, bb, cc, dd]
			
			#ss = kk / R * r
			ss = kk /arck * r
			aa = Line (Point (-r, -ss), Point (-r, +ss))
			bb = Line (Point (+r, -ss), Point (+r, +ss))
			cc = Line (Point (-ss, -r), Point (+ss, -r))
			dd = Line (Point (-ss, +r), Point (+ss, +r))
			temp = temp + [aa, bb, cc, dd]
			#try:
			if len (intro) == 0: penta  = [k.scale (r, r) for k in next (gen)]
			else:
				penta = intro[0]
				intro = intro[1:]
			#except:
			#intro_done = True
			lines = lines + [temp + penta]
			
	"""	
	if draw_arcs and False:
		#for kk in range (0, int (R)):
		for kk in range (0, arck):
			#ss = kk / R * r
			ss = kk /arck * r
			aa = Line (Point (-r, -ss), Point (-r, +ss))
			bb = Line (Point (+r, -ss), Point (+r, +ss))
			cc = Line (Point (-ss, -r), Point (+ss, -r))
			dd = Line (Point (-ss, +r), Point (+ss, +r))
			penta  = [k.scale (r, r) for k in next (gen)]
			lines = lines + [temp + [aa, bb, cc, dd] + penta]
	"""	
	circle = Circle (origin, r)
	temp   = [circle]
	#penta  = [k.scale (r, r) for k in next (gen)]
	#lines  = lines + [temp + penta]
	#lines = [temp]
	
	
	#lines = animation3a (width, height, gen)
	
	a      = Point (-r, -r)
	b      = Point (-r, +r)
	c      = Point (+r, +r)
	d      = Point (+r, -r)
	square = Quadrilateral (a, b, c, d)
	if len (intro) == 0: penta  = [k.scale (r, r) for k in next (gen)]
	else:
		#try
		penta = intro[0]
		intro = intro[1:]
		#except
		#intro_done = True
	temp   = temp + [square]
	lines  = lines + [temp + penta]
	
	# TODO while True ?
	#for k in range (0, int (R)):
	K = 0
	while True:
		k = (K + 1) * r
		K = K + 1
		sc = sqrt (2)
		
		lines_tempa = []
		if draw_arcs:
			#for kk in range (0, int (R)):
			for kk in range (0, arck):
				#tt = kk / R * pi / 2
				tt = kk / arck * pi / 2
				#TT = (R - kk) / R * pi / 4
				TT = (arck - kk) / arck * pi / 4
				rr = r * pow (sc, K)
				aa = Arc (origin, rr, rr, TT, TT + tt)
				bb = aa.rotate (pi / 2)
				cc = bb.rotate (pi / 2)
				dd = cc.rotate (pi / 2)
				penta  = [k.scale (r, r) for k in next (gen)]
				#lines = lines + [temp + [aa, bb, cc, dd] + penta]
				lines_tempa = lines_tempa + [temp + [aa, bb, cc, dd] + penta]
		
		circle = circle.scale (sc, sc)
		if circle.r > 1:
			lines = lines + lines_tempa
			break
		#if circle.r > sqrt (2): break
		
		
		square = square.scale (sc, sc)
		top, left, width, height = square.tlwh ()
		if width > R * 2:
			#penta  = [k.scale (r, r) for k in next (gen)]
			#lines = lines + [temp + penta] + lines_tempa
			lines = lines + lines_tempa
			temp   = temp + [circle]
			break
		

		lines_tempb = []
		if draw_arcs:
			#for kk in range (0, int (R)):
			for kk in range (0, arck):
				rr = r * pow (sc, K)
				#ss = kk / R * rr
				ss = kk / arck * rr
				aa = Line (Point (-rr, -ss), Point (-rr, +ss))
				bb = Line (Point (+rr, -ss), Point (+rr, +ss))
				cc = Line (Point (-ss, -rr), Point (+ss, -rr))
				dd = Line (Point (-ss, +rr), Point (+ss, +rr))
				#penta  = [k.scale (r, r) for k in next (gen)]
				#lines = lines + [temp + [aa, bb, cc, dd] + penta]
				lines_tempb = lines_tempb + [temp + [aa, bb, cc, dd]]
		lines_temp = [aaa + bbb for aaa, bbb in zip (lines_tempa, lines_tempb)]
		lines = lines + lines_temp
		#temp   = temp + [[circle], [circle, square]]	
		#temp   = temp + [circle]
		#penta  = [k.scale (r, r) for k in next (gen)]
		#lines  = lines + [temp + penta]
		temp   = temp + [circle]
		temp   = temp + [square]
		#penta  = [k.scale (r, r) for k in next (gen)]
		#lines  = lines + [temp + penta]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	top, left, width, height = square.tlwh ()
	assert width  > 0
	assert height > 0
	#sc = pow (2 / width, 1 / R)
	#sc = pow (2 * sqrt (2) / width, 1 / R)
	#sc = pow (2 / width, 1 / R)
	sc = pow (1 / temp[0].r, 1 / R / (len (temp) // 2))
	assert sc > 1, sc
	SC = r * sc
	dthetas = []
	kkk = 0
	squares = list (filter (lambda shape: type (shape) is Quadrilateral, temp))
	for square in squares:
		#dtheta  = kkk + 1
		#dtheta  = len (squares) - kkk # shape number
		#print ("nrot: %s" % dtheta)
		#dtheta = dtheta / len (squares) # rotation frequency
		#dtheta  = 1 / dtheta          # number of rotations
		#print (" rot: %s" % dtheta)
		
		#dtheta = dtheta * len (squares)
		
		#dtheta = 1 / len (squares)
		#dtheta = (len (squares) - kkk) * dtheta # outer squares rotate more quickly
		#dtheta = (kkk + 1) * dtheta
		#dtheta = len (squares) / (kkk + 1)
		#dtheta = len (squares) / (len (squares) - kkk)
		#dtheta = len (squares) / (len (squares) - kkk)
		#dtheta = (len (squares) - kkk) / len (squares)
		#dtheta = (kkk + 1) / len (squares)
		# [1, 1/2, 1/3, 1/4]
		dtheta = 1 / (kkk + 1)
		
		#rrr = R - 1
		rrr = R
		#rrr = R + 1
		#rrr     = log (1 / r) / log (sc) - 1
		#rrr     = log (1 / temp[0].r) / log (sc) 
		#rrr     = log (sc) / (log (1) - log (r)) + 1
		print ("nani: %s" % rrr)
		dtheta  = dtheta / rrr      # animation increments
		#dtheta  = dtheta * rrr
		print ("anim: %s" % dtheta)
		
		
		#dtheta  = dtheta * (pi)   # number of radians
		dtheta  = dtheta * (pi / 2)   # number of radians
		print ("nrad: %s" % dtheta)
		if kkk % 2 != 0: dtheta = -dtheta # reverse direction
		dthetas = dthetas + [dtheta]
		kkk = kkk + 1
	#dthetas = dthetas[::-1]
	assert kkk == len (squares)
	print ("dthetas=%s" % dthetas)
	RRR = 0
	while len (temp) > 0:
		RR = 0
		while type (temp[-1]) is Circle and temp[-1].r <= sqrt (2) or type (temp[-1]) is Quadrilateral and temp[-1].tlwh ()[2] <= 2:
		#while type (temp[-1]) is Circle and temp[-1].r <= 1 or type (temp[-1]) is Quadrilateral and temp[-1].tlwh ()[2] <= 2:
			kkk = 0
			temp2 = []
			for shape in temp:
				if type (shape) is Quadrilateral:
					shape = shape.rotate (dthetas[kkk])
					#print ("shape=%s" % shape)
					kkk = kkk + 1
				temp2 = temp2 + [shape]
			assert kkk == len (dthetas)
			temp = temp2
			#k  = width + (k + 1) / R * dw
			#sc = k / width
			temp = [t.scale (sc, sc) for t in temp]
			if temp[0].r > 1: break
			penta  = [K.scale (SC, SC) for K in next (gen)]
			lines = lines + [temp + penta]
			SC = SC * sc
			RR = RR + 1
		print ("RR: %s" % RR)
		if len (temp) > 0:
			if type (temp[-1]) is Circle: temp = temp[:-2]
			else:                         temp = temp[:-1]
			dthetas = dthetas[:-1]
		RRR = RRR + 1
		#assert RR == R, "RR: %s, R: %s" % (RR, R)
	#assert RRR == R, "RRR: %s, R: %s" % (RRR, R)
	print ("RRR: %s" % RRR)
		#if temp[0].r > 1: break
	if len (temp) > 0 and type (temp[-1]) is Quadrilateral: temp = temp[:-1]
	if len (temp) == 0: temp = [Circle (origin, 1)]
	penta = list (next (gen))
	lines = lines + [temp + penta]
	
	assert len (temp) == 1
	circle = temp[0]
	r      = circle.r / sqrt (2)
	a      = Point (-r, -r)
	b      = Point (-r, +r)
	c      = Point (+r, +r)
	d      = Point (+r, -r)
	square = Quadrilateral (a, b, c, d)
	penta  = [k.scale (r, r) for k in next (gen)]
	temp   = temp + [square]
	lines  = lines + [temp + penta]
	
	K = 0
	while True:
		k = (K + 1) * r
		sc = 1 / sqrt (2)
		circle = circle.scale (sc, sc)
		#if circle.r > 1: break
		if circle.r < 1 / R: break
		#temp   = temp + [[circle], [circle, square]]
		temp   = temp + [circle]
		SC = r * pow (sc, K + 0)
		penta  = [k.scale (SC, SC) for k in next (gen)]
		lines  = lines + [temp + penta]
		
		square = square.scale (sc, sc)
		temp   = temp + [square]
		SC = r * pow (sc, K + 1)
		penta  = [k.scale (SC, SC) for k in next (gen)]
		lines  = lines + [temp + penta]
		K = K + 1
		
	#square = temp[1]
	#top, left, width, height = square.tlwh ()
	#assert width  > 0
	#assert height > 0
	#sc = pow (2 / width, 1 / R)
	#sc = pow (width / 2 / sqrt (2), 1 / R)
	#sc = pow (2 * sqrt (2) / width, 1 / R)
	#assert sc > 1, sc
	sc = pow (2 * sqrt (2) / width, 1 / R)
	r = 1 / R
	#SC = r / sc
	k = 1
	while len (temp) > 0:
		while type (temp[-1]) is Circle and temp[-1].r >= 1 / R or type (temp[-1]) is Quadrilateral and temp[-1].tlwh ()[2] >= 2 / R:
			#k  = width + (k + 1) / R * dw
			#sc = k / width
			temp = [t.scale (1 / sc, 1 / sc) for t in temp]
			if type (temp[-1]) is Circle: SC = temp[-1].r / 1
			else:                        SC = temp[-1].tlwh ()[2] / 2
			#SC = pow (SC, k)
			#SC = 1 / SC
			k = k + 1
			penta  = [K.scale (SC, SC) for K in next (gen)]
			#if temp[-1].r < 1: break
			lines = lines + [temp + penta]
			#lines = lines + [temp]
			#SC = SC / sc
		if len (temp) > 0:
			if type (temp[-1]) is Circle: temp = temp[:-1]
			else:                         temp = temp[:-1]
		#if temp[0].r < 1: break
	#if len (temp) > 0 and type (temp[-1]) is Quadrilateral: temp = temp[:-1]
	#SC = temp[-1].r / 2
	#penta  = [K.scale (SC, SC) for K in next (gen)]
	#lines = lines + [temp + penta]
	temp = []
	for t in animation3a_rev (width, height, gen):
		t = [T.scale (SC, SC) for T in t]
		temp = temp + [t]
	lines = lines + temp	
	return lines
def animation4 (r): # trinity
	pass
def animations (width, height, gen):
	return chain (animation0 (width, height, gen), animation1 (width, height))
def animations_repeat_helper (width, height, gen):
	return chain (animation2 (width, height, gen), animation3 (width, height, gen))
	#return (k for k in animation3 (width, height, gen))
	#return (k for k in animation2 (width, height, gen))
def animations_repeat (width, height, gen):
	return chain (animation2c (width, height, gen), animations_repeat_helper (width, height, gen))
	#return animations_repeat_helper (width, height, gen)
def animations_repeat0 (width, height, gen):
	return chain (animations (width, height, gen), animations_repeat_helper (width, height, gen))
	#return animations_repeat_helper (width, height, gen)
	
	
	

class Arc:
	def __init__ (self, pt, width, height, start_angle, stop_angle):
		self.pt          = pt
		self.width       = width
		self.height      = height
		self.start_angle = start_angle
		self.stop_angle  = stop_angle
		#print ("(%s, %s) [%s, %s]" % (left, top, width, height))
		#self.lines ()
	def lines (self):
		left   = self.left
		top    = self.top
		width  = self.width
		height = self.height
		a  = Point (left,         top)
		b  = Point (left + width, top)
		c  = Point (left + width, top - height)
		d  = Point (left,         top - height)
		ab = Line (a, b)
		bc = Line (b, c)
		cd = Line (c, d)
		da = Line (d, a)
		lines = [ab, bc, cd, da]
		print ("lines=%s" % lines)
		return lines
	def tlbr (self, lines):
		tl     = lines[0].a
		for line in lines[1:]:
			if line.a.x <= tl.x and line.a.y >= tl.y: tl = line.a
		for line in lines:
			if line.b.x <= tl.x and line.b.y >= tl.y: tl = line.b
		br     = lines[0].a
		for line in lines[1:]:
			if line.a.x >= br.x and line.a.y <= br.y: br = line.a
		for line in lines:
			if line.b.x >= br.x and line.b.y <= br.y: br = line.b
		left   = tl.x
		top    = tl.y
		width  = br.x - tl.x
		height = tl.y - br.y
		return top, left, width, height
	def translate (self, xmin, ymin):
		pt = self.pt.translate (xmin, ymin)
		return Arc (pt, self.width, self.height, self.start_angle, self.stop_angle)
	def reflectX (self, xdiff):
		pt = self.pt.reflectX (xdiff)
		return Arc (pt, self.width, self.height, self.start_angle, self.stop_angle)
	def reflectY (self, ydiff):
		pt = self.pt.reflectY (ydiff)
		return Arc (pt, self.width, self.height, self.start_angle, self.stop_angle)
	def scale (self, xscale, yscale):
		pt     = self.pt.scale (xscale, yscale)
		width  = self.width  * xscale
		height = self.height * yscale
		return Arc (pt, width, height, self.start_angle, self.stop_angle)
	def round (self):
		pt     = self.pt.round ()
		width  = round (self.width)
		height = round (self.height)
		return Arc (pt, width, height, self.start_angle, self.stop_angle)
	def draw (self, screen):
		color = (0, 0, 255)
		left   = self.pt.x - self.width
		top    = self.pt.y - self.height
		width  = self.width  * 2
		height = self.height * 2
		rect = pygame.Rect (left, top, width, height)
		pygame.draw.arc (screen, color, rect, self.start_angle, self.stop_angle)
	def rotate (self, angle):
		pt          = self.pt.rotate (angle)
		start_angle = self.start_angle + angle
		stop_angle  = self. stop_angle + angle
		return Arc (pt, self.width, self.height, start_angle, stop_angle)
"""
class Eye:
	def __init__ (self, arcs, lines):
		self.arcs  = arcs
		self.lines = lines
def eye ():
	x     = 1/2
	theta = acos (x)
	y     =  sin (theta)
	# arc x = 0, 1/2; y = 0, sin(acos(1/2))
	# 
"""








# Import and initialize the pygame library
import pygame

def main ():
	pygame.init ()

	# Set up the drawing window
	#pygame.display.set_icon (surface)
	title     = "Free Code for a Free World!"
	icontitle = "InnovAnon, Inc."
	width     = 500
	height    = 500
	pygame.display.set_caption (title, icontitle)
	screen = pygame.display.set_mode ([width + 1, height + 1])
	rect   = screen.get_rect ()
	ss     = screen.subsurface (rect)
	#ss     = pygame.transform.flip (ss, False, True)
	xmin,   ymin   = -10, -10
	xmax,   ymax   =  10,  10
	xdiff,  ydiff  = xmax - xmin, ymax - ymin
	#ss     = pygame.transform.scale (ss, (xdiff, ydiff))
	xscale, yscale = width / xdiff, height / ydiff
	
	clock = pygame.time.Clock ()
	
	#pentagrams = chain (*pentagrams2 ())
	#pentagrams = (list (p) for p in pentagrams)
	#shapes_gen = pentagrams1 ()
	penta_gen = pentagrams1 ()
	#shapes_gen = animations (xdiff / 2, ydiff / 2, penta_gen)
	#shapes_gen = chain (shapes_gen, animations_repeat0 (xdiff / 2, ydiff / 2, penta_gen))
	
	shapes_gen = animations_repeat0 (xdiff / 2, ydiff / 2, penta_gen)
	#shapes_gen = animations_repeat (xdiff / 2, ydiff / 2, penta_gen)
	# TODO smooth transitions between sigils
	#shapes_gen = chain (shapes_gen, animations_repeat (xdiff / 2, ydiff / 2, penta_gen))
	repeat = True
	
	#shapes = [
	#	sigil ("InouvAnon",   xdiff / 2, ydiff / 2), # InnovAnon
	#	sigil ("Inouveisuns", xdiff / 2, ydiff / 2), # Innovations
	#	sigil ("Anonoumus",   xdiff / 2, ydiff / 2), # Anonymous
	#	sigil ("FriCoud",     xdiff / 2, ydiff / 2), # Free Code (for a)
	#	sigil ("FriWorld",    xdiff / 2, ydiff / 2), # Free World
	#]
	#shape_ndx = 0

	# Run until the user asks to quit
	running = True
	while running:
		# Did the user click the window close button?
		for event in pygame.event.get ():
			if event.type == pygame.QUIT: running = False

		# Fill the background with white
		##screen.fill ((255, 255, 255))
		##angle  = random_angle ()
		##angle  = angle.angle ()
		#angle  = uniform (-2 * pi, 2 * pi)
		#radius = uniform (0, 1)
		#color  = angle_color (angle, radius)
		#print (color)
		color = (0, 0, 0)
		ss.fill (color)
		
		# color wheel
		#for theta in range (0, 360):
		#	theta = theta / 360 * 2 * pi
		#	cost  = cos (theta)
		#	sint  = sin (theta)
		#	for radius in range (0, 256):
		#		radius = radius / 255
		#		color  = angle_color (theta, radius)
		#		x      = radius * cost
		#		y      = radius * sint
		#		w2     = width  / 2
		#		h2     = height / 2
		#		x      = int (w2 * x + w2)
		#		y      = int (h2 * y + h2)
		#		pygame.draw.circle (screen, color, (x, y), 1)
		# star
		#p = next (pentagrams)
		##p  = next (ps)
		#for shape in p:
		#	print (shape)
		#	shape = shape.translate (xmin,   ymin)
		#	print (shape)
		#	shape = shape.reflectY  (ydiff)
		#	print (shape)
		#	shape = shape.scale     (xscale, yscale)
		#	print (shape)
		#	shape = shape.round     ()
		#	print (shape)
		#	print ()
		#	shape.draw (ss)
		# Draw a solid blue circle in the center
		if True:
			shapes = [random_triangle ((xmin, ymin), (xmax, ymax))]
			from time_app import cercle_circonscrit, cercle_inscrit
			for shape in shapes:
				if isinstance (shape, Triangle):
					for f in (cercle_inscrit, cercle_circonscrit):
						res = f (((shape.a.x, shape.a.y), (shape.b.x, shape.b.y), (shape.c.x, shape.c.y)))
						if not res: continue
						(x, y), r = res
						if r <= 0: continue
						pt   = Point  (x, y)
						temp = Circle (pt, r)
						shapes.append (temp)
		#shapes = pentagrams0 ([(5, 2)] * 4)
		else:
			shapes = next (shapes_gen, None)
			if shapes is None:
				if repeat: shapes_gen = animations_repeat (xdiff / 2, ydiff / 2, penta_gen)
				else:      running    = False
				continue
			#shapes  = [shape.scale (xdiff / 2, ydiff / 2) for shape in shapes]
			shapes2 = []
			for shape in shapes:
				if type (shape) is not Text:
					shape   = shape.scale (xdiff / 2, ydiff / 2)
				shapes2 = shapes2 + [shape]
			shapes = shapes2
		#if type (shapes) is Text: s = shapes
		#else:
		#s = shapes.scale (xdiff / 2, ydiff / 2)
		#shapes = shapes + list (shapes[0].inside_pts ())
		#sys.exit (0)
		#shapes = sigil ("Mikel", xdiff / 2, ydiff / 2)
		#s         = shapes[shape_ndx]
		#shape_ndx = shape_ndx + 1
		#if shape_ndx == len (shapes): shape_ndx = 0
		#if True:
		for s in shapes:
			#print (s)
			if type (s) is Text: shape = s
			if type (s) is not Text:
				shape = s.translate (xmin,   ymin)
				#print (shape)
				shape = shape.reflectY  (ydiff)
				#print (shape)
				shape = shape.scale     (xscale, yscale)
				#print (shape)
				shape = shape.round     ()
				#print (shape)
			#print ()
			shape.draw (ss)
		#	for shape in s.linear_bisectors ():
		#		print (shape)
		#		shape = shape.translate (xmin,   ymin)
		#		print (shape)
		#		shape = shape.reflectY  (ydiff)
		#		print (shape)
		#		shape = shape.scale     (xscale, yscale)
		#		print (shape)
		#		shape = shape.round     ()
		#		print (shape)
		#		print ()
		#		shape.draw (ss)
		#	for shape in s.perpendicular_bisectors ():
		#		print (shape)
		#		shape = shape.translate (xmin,   ymin)
		#		print (shape)
		#		shape = shape.reflectY  (ydiff)
		#		print (shape)
		#		shape = shape.scale     (xscale, yscale)
		#		print (shape)
		#		shape = shape.round     ()
		#		print (shape)
		#		print ()
		#		shape.draw (ss)
		#	for shape in s.angular_bisectors ():
		#		print (shape)
		#		shape = shape.translate (xmin,   ymin)
		#		print (shape)
		#		shape = shape.reflectY  (ydiff)
		#		print (shape)
		#		shape = shape.scale     (xscale, yscale)
		#		print (shape)
		#		shape = shape.round     ()
		#		print (shape)
		#		print ()
		#		shape.draw (ss)
		#pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

		# Flip the display
		pygame.display.flip ()
		#clock.tick (.1)
		#clock.tick (1)
		#clock.tick (3)
		#clock.tick (10)
		#clock.tick (60)
		clock.tick (7.83)
	# Done! Time to quit.
	pygame.quit ()




if __name__ == "__main__":
	#abc = random_triangle ()
	#print (abc)
	#for ang in abc.angles ():
	#	print (ang)
	#main ([abc])
	main ()
	quit ()
