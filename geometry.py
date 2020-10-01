#! /usr/bin/env python3

#from numba import jit

from scipy.constants import golden

from math import log, ceil


from math import floor


def tr (t): return tuple (map (lambda x: round (x), t)) # tuple-round

from math import sqrt

##@jit
def findSemiPerimeterOfIncircle (a, b, c):
	assert a >= 0
	assert b >= 0
	assert c >= 0
	return (a + b + c) / 2
##@jit
def findAreaOfTriangle (a, b, c, p=None):
	assert a >= 0
	assert b >= 0
	assert c >= 0
	if p is None: p = findSemiPerimeterOfIncircle (a, b, c)
	n = p * (p - a) * (p - b) * (p - c)
	if n < 0: return 0
	return sqrt (n)
##@jit
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
#@jit    
def coordinates_to_deltas (x, y, z):
	(x1, y1), (x2, y2), (x3, y3) = x, y, z
	dx21, dy21 = x2 - x1, y2 - y1
	dx32, dy32 = x3 - x2, y3 - y2
	dx13, dy13 = x1 - x3, y1 - y3
	dx, dy, dz = (dx21, dy21), (dx32, dy32), (dx13, dy13)
	return dx, dy, dz
#@jit
def deltas_to_side_lengths (dx, dy, dz):
	(dx21, dy21), (dx32, dy32), (dx13, dy13) = dx, dy, dz
	s21 = sqrt (pow (dx21, 2) + pow (dy21, 2))
	s32 = sqrt (pow (dx32, 2) + pow (dy32, 2))
	s13 = sqrt (pow (dx13, 2) + pow (dy13, 2))
	return s21, s32, s13
#@jit
def coordinates_to_side_lengths (x, y, z):
	deltas = coordinates_to_deltas (x, y, z)
	return deltas_to_side_lengths (*deltas)
    
def cercle_inscrit (T):
	print ("cercle_inscrit (%s)" % (T,))
	(x1, y1), (x2, y2), (x3, y3) = T
	print ("(%s, %s) (%s, %s) (%s, %s)" % (x1, y1, x2, y2, x3, y3))
	s21, s32, s13 = coordinates_to_side_lengths (*T)
	print ("%s %s %s" % (s21, s32, s13))
	p2  = findSemiPerimeterOfIncircle (s21, s32, s13)
	print ("%s" % (p2,))
	c   = findCenterOfIncircle (x1, y1, x2, y2, x3, y3, s21, s32, s13, p2)
	print ("(%s)" % (c,))
	r   = findRadiusOfIncircle (s21, s32, s13, p2)
	print ("%s" % (r,))
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





#@jit
def trianglearea (a, b) : # https://www.geeksforgeeks.org/largest-triangle-that-can-be-inscribed-in-an-ellipse/
    # a and b cannot be negative  
    if a < 0 or b < 0 : return -1
    # area of the triangle  
    area = (3 * sqrt(3) * pow(a, 2)) / (4 * b) 
    return area 		
    
from math import sin, cos, pi

    
from constants import DEFAULT_ROTATION
##@jit
def inscribe_angles   (n):                           
	r   = range (0, n)
	f   = lambda k: k / n * 2 * pi
	tmp = map (f, r)
	if False: tmp = tuple (tmp)
	return tmp
##@jit
def   rotate_angles   (angles, dt=DEFAULT_ROTATION):
	f   = lambda t: t + dt
	tmp = map (f, angles)
	if False: tmp = tuple (tmp)
	return tmp

def  reflect_angles	  (angles):
	f = lambda t: -t
	tmp = map (f, angles)
	if False: tmp = tuple (tmp)
	return tmp

##@jit
def angles_to_polygon (angles):
	f   = lambda t: (cos (t), sin (t))
	tmp = map (f, angles)
	if False: tmp = tuple (tmp)
	return tmp
def inscribe_polygon (n, theta):
	angles = inscribe_angles   (n)
	angles =   rotate_angles   (angles, theta)
	pts    = angles_to_polygon (angles)
	return pts

#@jit	
def graphics_affine_x (x):   return (x + 1) / 2
#@jit
def graphics_affine_y (y):   return (1 - y) / 2
from itertools import chain
def graphics_affine   (pt):
	tmp = zip (pt[:-1:2], pt[1::2])
	f   = lambda xy: (graphics_affine_x (xy[0]), graphics_affine_y (xy[1]))
	tmp = map (f, tmp)
	tmp = chain (*tmp)
	if False: tmp = tuple (tmp)
	return tmp
def graphics_affines  (pts): 
	tmp = map (graphics_affine, pts)
	if False: tmp = tuple (tmp)
	return tmp

#@jit
def    scale_dim      (n,   offset, scale): return offset + scale * n
def    scale_point    (pt, origin, dims):
	nsos   = zip (pt, origin, dims)
	f      = lambda nso: scale_dim (*nso)
	ret    = map (f, nsos)
	if False: ret = tuple (ret)
	return ret
def    scale_points   (pts, rect):
	assert len (rect) % 2 == 0
	ndim = len (rect) // 2
	orig = rect[:ndim]
	dims = rect[ndim:]
	f    = lambda pt: scale_point (pt, orig, dims)
	ret  = map (f, pts)
	if False: ret = tuple (ret)
	return ret

def bounding_box (pts):
	tmp = zip (*pts)                                # array of tuples (x, y) => arrays of x's, y's and z's  
	tmp = map (lambda k: (min (*k), max (*k)), tmp) # array of tuples (minx, maxx), (miny, maxy)
	tmp = zip (*tmp)                                 # array of tuples (minx, miny), (maxx, maxy)
	if False: tmp = tuple (tmp)
	return tmp
from functools import reduce
def point_deltas (pts):
	tmp = zip (*pts)                                # array of tuples (minx, miny), (maxx, maxy) => arrays of mins, maxes
	f   = lambda k: reduce ((lambda a, b: a - b), k[::-1])
	tmp = map (f, tmp)                              # deltas (maxx - minx), (maxy - miny)
	if False: tmp = tuple (tmp)
	return tmp
def bounding_rect (pts):
	bb  = bounding_box (pts)
	bb  = tuple (bb)
	ds  = point_deltas (bb)
	return bb[0], ds   
    
    
    













#@jit
def recursive_affine (rect, dx, dy, rw, rh, n):
	x, y, w, h = rect
	for k in range (1, n + 1):
		dx, dy = dx * rw, dy * rh
		x,  y  =  x + dx,  y + dy
		w,  h  =  w * rw,  h * rh
		yield x, y, w, h
#@jit
def naffine (tgt, current, ratio): return (log (tgt) - log (current)) / log (ratio)
##@jit
def recurse_point (rect, rp, minsz):
	X, Y, W, H = rect
	x, y, w, h = rp
	assert X != x or Y != y or W != w or H != h
	#rp = x + w / 2, y + h / 2, w, h # TODO wtf
	print ("recurse_point (%s, %s, %s)" % (rect, rp, minsz))
	# get scale and offset for recursion point
	dx, dy = x - X, y - Y
	#dx, dy = dx + (W - w) / 2, dy + (H - h) / 2 # TODO wtf
	print ("dx: %s, dy: %s" % (dx, dy))
	rw, rh = w / W, h / H
	print ("rw: %s, rh: %s" % (rw, rh))
	# get number of recursions until < minsz
	xmin, ymin = minsz
	xn, yn = naffine (xmin, w, rw), naffine (ymin, h, rh)
	print ("xn: %s, yn: %s" % (xn, yn))
	n = min (xn, yn)
	print ("n: %s" % (n,))
	n = ceil (n)
	print ("n: %s" % (n,))
	# recursively apply scale and offset
	tail = recursive_affine (rp, dx, dy, rw, rh, n)
	return rp, *tail





#@jit
def octave (base_frequency, target_frequency):
	n = naffine (target_frequency, base_frequency, 2)
	return floor (n)
def pitch  (base_frequency, target_frequency=None, exponent=None):
	if exponent is None:
		assert target_frequency is not None
		exponent = octave (base_frequency, target_frequency)
	else: assert target_frequency is None
	print ("octave: %s" % (exponent,))
	return base_frequency * pow (2, exponent)
def octave_range (base_frequency, lower_bound, upper_bound):
	min_octave = octave (base_frequency, lower_bound)
	max_octave = octave (base_frequency, upper_bound)
	print ("octave range: [%s, %s]" % (min_octave, max_octave))
	return min_octave, max_octave
def pitch_range (base_frequency, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	print ("min: %s, max: %s" % (min_octave, max_octave))
	min_pitch = pitch (base_frequency, exponent=min_octave)
	max_pitch = pitch (base_frequency, exponent=max_octave)
	print ("pitch range: [%s, %s]" % (min_pitch, max_pitch))
	return min_pitch, max_pitch

def octave_triplet (base_frequency, octave, scale, degree):
	print ("scale[degree=%s]: %s, octave: %s, base_frequency: %s" % (degree, scale[degree], octave, base_frequency))
	return (octave, degree, scale[degree] * base_frequency * pow (2, octave))
def octave_triplets (base_frequency, octave, scale):
	f = lambda degree: octave_triplet (base_frequency, octave, scale, degree)
	ret = map (f, range (0, len (scale)))
	if True:
		ret = tuple (ret)
		print ("octave triplets: %s" % (ret,))
	return ret
def octave_triplets_below_helper (upper_bound, ot):
	f  = lambda octave, degree, pitch: pitch <= upper_bound
	g  = lambda odp: f (*odp)
	ot = filter (g, ot)
	if True:
		ot = tuple (ot)
		print ("octave triplets below: %s" % (ot,))
	return ot
def octave_triplets_below (base_frequency, octave, scale, upper_bound):
	ot = octave_triplets (base_frequency, octave, scale)
	return octave_triplets_below_helper (upper_bound, ot)
def octave_triplets_above_helper (lower_bound, ot):
	f  = lambda octave, degree, pitch: pitch >= lower_bound
	g  = lambda odp: f (*odp)
	ot = filter (g, ot)
	if True:
		ot = tuple (ot)
		print ("octave triplets above: %s" % (ot,))
	return ot
def octave_triplets_above (base_frequency, octave, scale, lower_bound):
	ot = octave_triplets (base_frequency, octave, scale)
	return octave_triplets_above_helper (lower_bound, ot)
def min_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave=None):
	if min_octave is None: min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	print ("min octave fuck: %s" % (min_octave,))
	mins = octave_triplets_above (base_frequency, min_octave, scale, lower_bound)
	if True:
		mins = tuple (mins)
		print ("mins: %s" % (mins,))
	mins = octave_triplets_below_helper (upper_bound, mins)
	if True:
		mins = tuple (mins)
		print ("mins: %s" % (mins,))
	return mins
def max_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave=None):
	if max_octave is None: min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	print ("max octave fuck: %s" % (max_octave,))
	maxs = octave_triplets_above (base_frequency, max_octave, scale, upper_bound)
	if True:
		maxs = tuple (maxs)
		print ("maxs: %s" % (maxs,))
	maxs = octave_triplets_below_helper (lower_bound, mins)
	if True:
		maxs = tuple (maxs)
		print ("maxs: %s" % (maxs,))
	return maxs
def minmax_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	mins = min_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave)
	maxs = min_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave)
	return mins, maxs
	

def harmonic_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
		min_pitch,  max_pitch  = pitch_range  (base_frequency, lower_bound, upper_bound, min_octave, max_octave)
	mins, maxs = minmax_pitches (base_frequency, scale, lower_bound, upper_bound, min_pitch, max_pitch)
	#min_octave = floor (min_octave)
	#max_octave = ceiling (max_octave)
	if min_octave + 1 >= max_octave: pitches = ()
	else:
		octaves = range (min_octave + 1, max_octave)
		f = lambda deg: (octave, deg, octave * deg)
		g = lambda octave: map (f, scale)
		pitches = map (g, octaves)
	ret = chain (*mins, *pitches, *maxs)
	if True:
		ret = tuple (ret)
		print ("harmonic pitches: %s" % (ret,))
	return ret
	
#print ("FUCK: %s" % (harmonic_pitches (4, (1/1, 3/2), 30, 80),))
#quit()	
	
def min_pitch (base_frequency, scale, lower_bound, upper_bound, min_octave=None):
	return min_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave)[0]
def max_pitch (base_frequency, scale, lower_bound, upper_bound, max_octave=None):
	return max_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave)[-1]
def minmax_pitch (base_frequency, scale, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	ip = min_pitch (base_frequency, scale, lower_bound, upper_bound, min_octave)
	ap = max_pitch (base_frequency, scale, lower_bound, upper_bound, max_octave)

def int_pitches (base_frequency, scale, lower_bound, upper_bound):
	pitches = harmonic_pitches (base_frequency, scale, lower_bound, upper_bound)
	f = lambda x: x == int (x)
	return filter (f, pitches)

def min_int_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave=None):
	pitches = min_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave)
	f = lambda x: x == int (x)
	return filter (f, pitches)
def max_int_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave=None):
	pitches = max_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave)
	f = lambda x: x == int (x)
	return filter (f, pitches)
def minmax_int_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	mins = min_int_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave)
	maxs = max_int_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave)
	return mins, maxs

def min_int_pitch (base_frequency, scale, lower_bound, upper_bound, min_octave=None):
	return min_int_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave)[0]
def max_int_pitch (base_frequency, scale, lower_bound, upper_bound, max_octave=None):
	return max_int_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave)[-1]
def minmax_int_pitch (base_frequency, scale, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	ip = min_int_pitch (base_frequency, scale, lower_bound, upper_bound, min_octave)
	ap = max_int_pitch (base_frequency, scale, lower_bound, upper_bound, max_octave)
	return ip, ap
	
def min_int_pitch2 (base_frequency, scale, lower_bound, upper_bound, min_octave=None):
	return int_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave)[0]
def max_int_pitch2 (base_frequency, scale, lower_bound, upper_bound, max_octave=None):
	return int_pitches (base_frequency, scale, lower_bound, upper_bound, max_octave)[-1]
def minmax_int_pitch2 (base_frequency, scale, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	ip = min_int_pitch2 (base_frequency, scale, lower_bound, upper_bound, min_octave)
	ap = max_int_pitch2 (base_frequency, scale, lower_bound, upper_bound, max_octave)
	return ip, ap
	
def error_ratio (actual, expected): return (actual - expected) / expected

def reasonable_minmax_int_pitch (base_frequency, scale, lower_bound, upper_bound, min_octave=None, max_octave=None):
	if min_octave is None or max_octave is None:
		assert min_octave is None and max_octave is None
		min_octave, max_octave = octave_range (base_frequency, lower_bound, upper_bound)
	pitches = harmonic_pitches (base_frequency, scale, lower_bound, upper_bound)
	pitches = tuple (pitches)
	ndxs    = range (0, len (pitches))
	prs     = zip (pitches, ndxs)
	f       = (lambda pitch, ndx: (error_ratio (pitch, int (pitch)), ndx)) # TODO maybe multiply by octave to cause preference for lower octaves
	prs     = map (f, prs)
	f       = lambda pi1, pi2: pi2[0] - pi1[0]
	prs     = sorted (prs, key=f)
	return round (prs[0]), round (prs[-1])
	#ers, ndxs = zip (prs) # TODO * ? chain * ?
	#return filter (f, pitches)
	#pitches = int_pitches (base_frequency, scale, lower_bound, upper_bound, min_octave, max_octave)
	# TODO if no int pitches
# TODO reasonable pitch given base freq, scale, audio bounds, graphics bounds	

	
		
		
		
def to_degrees (radians): return radians / (2 * pi) * 360
def to_radians (degrees): return degrees / 360 * (2 * pi)

def midpoint (pts):
	dims = zip (*pts)
	dims = tuple (dims)
	assert len (dims) == 2
	f    = lambda a, b: a + (b - a) / 2
	pt   = reduce (f, dims)
	if False: pt = tuple (pt)
	return pt
				
if __name__ == "__main__":
	print (DEFAULT_FRAME_RATE)
	print (DEFAULT_SAMPLE_RATE)
	print (DEFAULT_TICK_SPEED)
	# TODO
	#def main ():
	#	with GUI (exit_on_close=True) as g: g.run ()
	#main ()
	quit ()
	
