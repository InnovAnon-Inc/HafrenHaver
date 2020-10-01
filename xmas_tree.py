#! /usr/bin/env python3

from math import sqrt, pow, atan2, pi

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
	
from hilbertcurve.hilbertcurve import HilbertCurve
from itertools import starmap
import numpy_indexed as npi

if __name__ == "__main__":
	def main ():
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
		coords = starmap (polar_to_cartesian, coords)                   # map polar coordinates to cartesian coordinates
		# TODO use spacing of limbs to determine p for hilbert curve ?
		# TODO use binning to discretize the continuous points?
		npi.group_by (np.digitize (coords, bins)).mean (coords))        # map from continuous 2-space to discrete 2-space
		
		p = ?
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
