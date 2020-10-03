#! /usr/bin/env python3

from math import sqrt, pow, atan2, pi



import pygame

# problem: decorate a saturnalia tree

# input:
# - tree:
#   - base radius
#   - height
# - limb positions
#   - height
#   - angle
# - number of ornaments

# given (height, angle) of limb
# compute (x, y, z) of limb tip
# compute polar coordinates
# project onto 2d elliptical plane (because surface area of a cone is a 2d ellipse)
# skew from elliptical plane onto rectangular plane
# discretize
# use space-filling curve to map from discrete 2D to discrete 1D
# use bjorklund's algo to evenly distribute ornaments
# inverse mappings back to (x, y, z)
# render 3d mesh
# output pairs of (height, angle)

from math import sin, cos

def elliptical_to_rectangular (radius, t, bx, by):
	#print ("elliptical_to_rectangular (%s, %s, %s, %s)" % (radius, t, bx, by))
	#f = (1 / (pow (cos (t), 2) - pow (sin (t), 2)))
	#x = f * (+ bx * cos(t) - by * sin(t))
	#y = f * (- bx * sin(t) + by * cos(t))
	
	#x = bx / 2 * cos (t)
	x = cos (t)
	#y = by / 2 * sin (t)
	y = sin (t)
	#print ("(x: %s, y: %s" % (x, y))
	
	# find intersection of bounding box
	if t < pi / 4 or t > 7 * pi / 4: # east
		m = y / x
		#X = bx / 2
		X = 1
		Y = m * X + 0
		#print ("m: %s, X: %s, Y: %s" % (m, X, Y))
	elif t == pi / 4: # NE
		#X = +bx / 2
		#Y = +by / 2
		X = 1
		Y = 1
		#print ("X: %s, Y: %s" % (X, Y))
	elif t < 3 * pi / 4: # north
		m = y / x
		#Y = by / 2
		Y = 1
		X = Y / m
		#print ("m: %s, X: %s, Y: %s" % (m, X, Y))
	elif t == 3 * pi / 4: # NW
		#X = -bx / 2
		#Y = +by / 2
		X = -1
		Y = 1
		#print ("X: %s, Y: %s" % (X, Y))
	elif t < 5 * pi / 4: # west
		m = y / x
		#X = -bx / 2
		X = -1
		Y = m * X + 0
		#print ("m: %s, X: %s, Y: %s" % (m, X, Y))
	elif t == 5 * pi / 4: # SW
		#X = -bx / 2
		#Y = -by / 2
		X = -1
		Y = -1
		#print ("X: %s, Y: %s" % (X, Y))
	elif t < 7 * pi / 4: # south
		m = y / x
		#Y = -by / 2
		Y = -1
		X = Y / m 
		#print ("m: %s, X: %s, Y: %s" % (m, X, Y))
	elif t == 7 * pi / 4: # SE
		#X = +bx / 2
		#Y = -by / 2
		X = 1
		Y = -1
		#print ("X: %s, Y: %s" % (X, Y))
	
	# get hyp of intersection
	H = sqrt (pow (X, 2) + pow (Y, 2))
	#print ("H: %s" % (H,))
	
	# scale down hyp
	h = H * radius
	#print ("h: %s" % (h,))
	
	# compute real point
	x, y = h  * cos (t), h  * sin (t)
	#print ("(x: %s, y: %s" % (x, y))
	
	# denormalize
	x, y = ((x + 1) / 2), ((1 - y) / 2)
	x, y = bx * x, by * y
	#print ("(x: %s, y: %s" % (x, y))
	return x, y
	
def rectangular_to_elliptical (x, y, w, h): # TODO
	pass
	
from geometry import inscribe_angles, rotate_angles, graphics_affines
from geometry import scale_points, angles_to_polygon, graphics_affine
from geometry import scale_point, tr
from itertools import starmap
from constants import ORIGIN	
from rotation import STRAIGHT
from square_app import SquareApp
from orientation import NORTH
from random import uniform

class StatSquare (SquareApp): # TODO map from polygon to square
	def __init__ (self, *args, **kwargs):
		SquareApp.__init__ (self, *args, **kwargs)
		self.increment_angles (True)
	
	def set_subsurface (self, ss):
		SquareApp.set_subsurface (self, ss)
		
		
	def increment_n (self):
		n = self.n
		n = n + 1
		if n == 13: n = 3
		self.n = n
		
	def increment_angles (self, is_first=False):
		if not is_first: self.increment_n ()
		else: self.n = 3
		n = self.n
		angles      = inscribe_angles (n)
		orientation = NORTH
		radians     = orientation.radians ()
		angles      = rotate_angles (angles, radians)
		angles      = tuple (angles)
		self.angles = angles
		
	def draw_foreground (self, temp):
		print ("enter xmas_tree.draw_foreground (%s)" % (temp,))
		SquareApp.draw_foreground (self, temp)
		angles = self.angles
		assert len (self.angles) == self.n
		rect   = temp.get_rect ()
		x, y, w, h = rect
		#print ("(x: %s, y: %s) (w: %s, h: %s)" % (x, y, w, h))
		#radius = uniform (0, 1)
		radius = 1
		f      = lambda theta: elliptical_to_rectangular (radius, theta, w, h)
		pts    = map (f, angles)
		#f = lambda x, y: (x, h - y)
		#f      = lambda x, y: (x + w / 2, h - (y + h / 2))
		#pts    = starmap (f, pts)
		#f      = lambda X, Y: ((X + w / 2) / 2, (h - (Y + h / 2)) / 2)
		#pts    = starmap (f, pts)
		##pts    = graphics_affines (pts)
		##pts    = scale_points (pts, rect)
		f      = lambda pt: tr (pt)
		pts    = map (f, pts)
		pts    = tuple (pts)
		
		print ("temp: %s" % (temp,))
		color = (255, 0, 0)
		pts2 = (*pts, pts[0])
		pts2 = list (pts2)
		print ("fuck: %s" % (pts2,))
		pygame.gfxdraw.filled_polygon (temp, pts2, color)
		pygame.gfxdraw.     aapolygon (temp, pts2, color)	

		color  = (0, 255, 0)
		o = w / 2, h / 2
		o = tr (o)
		for pt in pts: pygame.gfxdraw.line (temp, *o, *pt, color)

		color  = (0, 0, 255)
		for pt in pts: pygame.gfxdraw.pixel (temp, *pt, color)
		
		print ("pts: %s" % (pts,))
		
		self.increment_angles ()
		print ("leave xmas_tree.draw_foreground ()")

	
	

def polar_to_cartesian (radius, theta): return radius * cos (theta), radius * sin (theta)
def cartesian_to_polar (x, y):
	theta  = atan2 (y, x)
	radius = sqrt (pow (x, 2) + pow (y, 2))
	return radius, theta

def ha_to_polar (height, angle, base, h): # project tree limb points on cone's surface area onto 2d polar coordinates
	c, r = base
	x, y = c
	m    = r / h                                                        # slope of cone from apex to base
	x1   = h - h1                                                       # x pos relative to apex
	y1   = m * x1                                                       # y pos as a function of x
	r1   = sqrt (pow (x1, 2) + pow (y1, 2))
	return angle, r1
def polar_to_ha (rad, theta, base, h):
	pass
def ha_to_xyz (height, angle, base, h):
	pass
def xyz_to_ha (x, y, z, base, h):
	pass
	


# TODO use annotation types and aspects to implement caching for expensive math ops... and normalize ops to enhance cacheability?

	
	
def polygonal_plane_to_grid (nvertex, nring, pts):
	# pt = ring, vertex
	pass




if __name__ == "__main__":
	from random import randrange
	from gui import GUI
	
	def main ():
		# finagellini algorithm:
		# the tree is specified with (radius, height)
		# the tree's branches are specified with (height, angle):         3D polar coordinates with respect to tree's dimensions
		# which is transformed using a 1-to-1 mapping to (x, y, z):       3D cartesian coordinates on the surface of the cone
		# which is transformed using a 1-to-1 mapping to (radius, theta): polar coordinates
		# which is discretized to radius-rings, and theta-ranges corresponding to sides on a polygon
		# which is transformed using a 1-to-1 mapping to (x, y):          2D discrete cartesian coordinates
		# which is transformed using a 1-to-1 mapping to (n,):            1D position on discrete number line
		
		a = StatSquare ()
		with GUI (app=a, exit_on_close=False) as g:
			#g.setApp (a)
			g.run ()
		
		x    = 0
		y    = 0
		c    = x, y                                                     # center of circle/cone
		r    = 10                                                       # radius of circle
		base = c, r                                                     # base   of cone
		h    = 20                                                       # height of cone
		hyp  = sqrt (pow (r, 2) + pow (h, 2))                           # hypotenuse of cone => radius of mapped circle
		
		ncoord = randrange (4, 20)
		f      = lambda k: randrange (0, h), uniform (0, 2 * pi)
		coords = range (0, ncoord)
		coords = map (f, coords)                                        # get position of tree limbs in 3-space (specified by height, angle)
		                                                                
		coords = map (ha_to_polar, coords)
		coords = tuple (coords)
		ncoord = len (coords)
		coords = starmap (polar_to_cartesian2, coords)                  # map polar coordinates to cartesian coordinates
		
		# get min d-theta
		# determine reasonable number of sides on polygon... check which number of sides causes limbs to align most closely... i.e., closer to 1/2 mark, closer to 1/3 marks, etc.
		# use theta to determine "bucket" (i.e, which side on the polygon)
		
		
		# TODO use spacing of limbs to determine p for hilbert curve ?
		# TODO use binning to discretize the continuous points?
		#npi.group_by (np.digitize (coords, bins)).mean (coords))        # map from continuous 2-space to discrete 2-space
		
		#p = ?
		N = 2
		hilbert_curve = HilbertCurve (p, N)                             # map from 2-space to 1-space
		coords = starmap (hilbert_curve.distance_from_coordinates, coords)
	
		nornament = randrange (3, ncoord)                               # get number of ornaments

		pattern = bjorklund (ncoord, nornament)                         # evenly distribute ornaments along space-filling curve
		coords  = zip (pattern, coords)
		f       = lambda t: t[0]
		coords  = filter (f, coords)
		f       = lambda t: t[1]
		coords  = map    (f, coords)
		
		coords = starmap (hilbert_curve.coordinates_from_distance, coords) # map from 1-space to 2-space

		# TODO try to fit optimal coords ^^^ onto the tree limbs

		coords = starmap (cartesian_to_polar, coords)                   # map cartesian coordinates to polar coordinates
		f      = lambda rad, theta: polar_to_ha (rad, theta, r, h)
		output = starmap (f, coords)                                    # unflatten cone's shadow from 2-space back to 3-space
		output = tuple (output)
		f      = lambda height, angle: ha_to_xyz (height, angle, r, h)
		coords = starmap (f, output)
		print (output)
		# TODO render 3D model
		# TODO get stats about ornament shapes and colors
		# TODO recursively apply bjorklund's to evenly distribute the varieties?
	main ()
	quit ()
