from __future__ import division
from collections import *
from fractions import *
from functools import *
from itertools import *
from math import *
from operator import *
from random import *
from time import *

from gasp import *
#from graphics import *
#from numpy import *

from Bjorklund import *
from Harmonic import *

pythagorean_scale = Harmonic.pythagorean_scale

#([0..1]*2=[0..2])-1=[-1..1]
#p * 2 - 1
def normalize_nonnegative_to_real (p, factor=1):
	return 2 * (p - Fraction (factor, 2))
#([-1..1]+1=[0..2])/2=[0..1]
#(p + 1) / 2
def normalize_real_to_nonnegative (p, factor=1):
	#hf = factor / 2.0
	hf = Fraction (factor, 2)
	return p * hf + hf

#def shift (p): return .5 * (p + 1)
def shift (n): return normalize_real_to_nonnegative (n)
def shifts (pt): return (shift (pt[0]), shift (pt[1]))
def normalize_reals_to_nonnegatives (arr):
	return [normalize_real_to_nonnegative (r) for r in arr]
def normalize_nonnegatives_to_reals (arr):
	return [normalize_nonnegative_to_real (r) for r in arr]

def accumulate (iterable, func=add):
	'Return running totals'
	# accumulate([1,2,3,4,5]) --> 1 3 6 10 15
	# accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
	it = iter (iterable)
	try: total = next (it)
	except StopIteration: return
	yield total
	for element in it:
		total = func (total, element)
		yield total
def discrete_derivative (arr): return [b - a for a, b in zip (arr, arr[1:])]
def discrete_integral (arr, c): return accumulate ([c] + arr)

def rotate (arr, amt=1):
	if len (arr) is 0: return arr
	amt = amt % len (arr) # Normalize y... even works for negative y
	return arr[amt:] + arr[:amt]

def lb (n): return log (n) / log (2)
def linearize_frequency (f): return lb (f)
def linearize_frequencies (arr): return [linearize_frequency (f) for f in arr]
def normalize_radian (r): return r * 2 * pi
def normalize_radians (arr): return [normalize_radian (r) for r in arr]
def normalize_degree (d): return d * 360
def normalize_degrees (arr): return [normalize_degree (d) for d in arr]
#def circularize (radian): return cos (radian), sin (radian)
def circularize (radian): return cos (radian), sin (radian)
def circularizes (radians): return [circularize (r) for r in radians]
def spiralize1 (r, f): return f (normalize_radian (r)) / (1 + r)
def spiralize (r): return spiralize1 (r, cos), spiralize1 (r, sin)
def inward_spiral (arr): return [spiralize (r) for r in arr]

#def equal_spacing (n): return [1.0 * h / n for h in xrange (0, n)]
def equal_spacing (n): return [Fraction (h, n) for h in xrange (0, n)]
def equal_temperament_scale (n): return [2 ** h for h in equal_spacing (n)]

def generate_coprime_pairs (p):
	return generate_coprime_pairs_leaves (
		generate_coprime_pairs_roots (p), p)
def generate_coprime_pairs_roots (p):
	return [(m, 1) for m in [2, 3] if m <= p]
def generate_coprime_pairs_leaves (q, p):
	todo = []
	todo.extend (q)
	map (todo.extend, [
		generate_coprime_pairs_leaves (
			generate_coprime_pairs_leaf (e[0], e[1], p), p)
		for e in q])
	return todo
def generate_coprime_pairs_leaf (m, n, p):
	return [k for k in [
		(2 * m - n, m),
		(2 * m + n, m),
		(m + 2 * n, n)]
		if k[0] <= p]

# TODO __pow__ for Fraction
def frac_pow (a, b):
	if isinstance (a, Fraction):
		return Fraction (
			frac_pow (a.numerator, b),
			frac_pow (a.denominator, b))
	return a ** b
#euclid_epsilon = Fraction (10, 9)
#euclid_epsilon = Fraction (2 ** 485, 3 ** 306)
euclid_epsilon = Fraction (531441, 524288)
def euclid (h, k, l):
	a = int (floor (log (l[h]) / log (l[k])))
	#b = l[h] / (l[k] ** a)
	#b = Fraction (l[h], l[k] ** a)
	b = Fraction (l[h], frac_pow (l[k], a))
	try: return euclid (k, l.index (b), l)
	except ValueError: pass
	if b < euclidepsilon: return l
	l += [b]
	return euclid (k, len (l) - 1, l)






origin = (0, 0)

class NestedWindow:
	def normalize_width  (self, x):  return x * self.W + self.wW
	def normalize_height (self, y):  return y * self.H + self.hH
	def normalize_point  (self, pt): return (
		self.normalize_width (pt[0]), self.normalize_height (pt[1]))
	def __init__ (self, W, w, H, h):
		self.w = w
		self.h = h
		self.W = W
		self.H = H
		self.wW = w * W
		self.hH = h * H
	def translate (self, pt): return self.normalize_point (shifts (pt))
	def translates (self, pts): return [self.translate (pt) for pt in pts]
	def translate2 (self, arg):
		if isinstance (arg, tuple):
			return self.translate (arg)
		if isinstance (arg, list) or isinstance (arg, iter):
			return self.translates (arg)
		raise Exception ()
	#def translates2 (self, arr):
		"""if isinstance (arg, tuple):
			return self.translate (arg)
		if isinstance (arg, list)
		or isinstance (arg, iter):
			return self.translates (arg)"""
	#	return [self.translates2 (e) for e in arr]
	def draw (self, method, arg):
		return method (*self.translate (arg))
		#arg = self.translate (arg)
		#return method (arg[0], arg[1])
	def draws (self, method, args): return method (self.translates (args))
	def draws2 (self, method, pts, center, topleft, widthheight):
		#return method (self.translates (pts),
		#	*[self.translate (arg) for arg in [center, topleft, widthheight]])
		pts = self.translates (pts)
		center = self.translate (center)
		topleft = self.translate (topleft)
		#widthheight = self.translate (widthheight)
		width, height = widthheight
		width  *= self.W
		height *= self.H
		widthheight = width, height
		#print pts
		#print center
		#print topleft
		#print widthheight
		#print
		return method (pts, center, topleft, widthheight)
			

class Scale:
	"""How to divide a circle/octave"""
	def __init__ (self, arr, mode=0):
		self.original = arr
		self.setDiffs ()
		#if mode is not 0: self.adjustMode (mode)
		diffs1 = self.diffs
		self.adjustMode (mode)
		diffs2 = self.diffs
		#print diffs1
		#print diffs2
		#assert diffs1 == diffs2
	def __len__ (self): return len (self.original)
	def __iter__ (self): return discrete_integral (self.diffs, 1)
	def setDiffs (self):
		self.diffs = discrete_derivative (self.original)
		#self.diffs = list (discrete_derivative (self.original))
	def adjustMode (self, delta_mode):
		#self.diffs = rotate (self.diffs, delta_mode)
		#self.diffs = list (rotate (self.diffs, delta_mode))
		self.diffs = rotate (list (self.diffs), delta_mode)
	def setMode (self, mode):
		setDiffs ()
		adjustMode (mode)
	def apply (self, baseFreq): return [baseFreq * e for e in self]
class Key:
	"""How to divide a scale"""
	def __init__ (self, scale_len, scale_type, mode=0):
		# TODO bjorklund bullshit (scale_len, scale_type), rotate by mode
		self.arr = list (xrange (arr_len))
		self.mode = mode
	def __len__ (self): return len (self.arr)
	def __iter__ (self): return rotate (self.arr, self.mode)
	def adjustMode (self, delta_mode):
		self.mode += delta_mode
		self.mode %= len (self)
	def setMode (self, mode): self.mode = mode
	def apply (self, scale): return [scale[k] for k in self]

"""
class ShapeSub (Shape):
	def __init__ (self, points, filled=False, color=(0, 0, 0), thickness=1):
		self.thickness = thickness
		if isinstance (points, list): self.points = points
		else: raise backend.GaspException ("points must be a list")
		x_values = []
		y_values = []    
		for point in self.points:
			if isinstance (point, tuple):
				x_values.append (point[0])
				y_values.append (point[1])
			else: raise backend.GaspException ("points for be tuples")
		#self.height = (max (y_values) - min (y_values))+self.thickness*2
		#self.width = (max(x_values) - min(x_values))+self.thickness*2
		#self.topleft = (min(x_values)-self.thickness, min(y_values)-self.thickness)
		#self.center = Point(self.width/2 + min(x_values), self.height/2 +
		#                                                      min(y_values))
		self.on_screen = False
		Shape.__init__ (self, self.center, filled, color)
		screen.action_objects.put ([["polygon",self],"new object"])
		screen.objects.append (self)    
	def __repr__(self):
		return "Polygon instance at (%i, %i)" % \
			(self.center.x , self.center.y)"""
class ShapeAbs (Polygon):
	def __init__ (self, scale, center, topleft, widthheight):
		Polygon.__init__ (self, self.initScale (scale, center))
		#Polygon.center = Point (center)
		#Polygon.topleft = topleft
		#Polygon.width, Polygon.height = widthheight
		self.center = Point (center)
		self.topleft = topleft
		self.width, self.height = widthheight
class Wheel (ShapeAbs):
#class Wheel (ShapeSub):
	def initScale (self, scale, center): return scale
	def __init__ (self, scale, center, topleft, widthheight):
		ShapeAbs.__init__ (self, scale, center, topleft, widthheight)
class Constellation (ShapeAbs):
	def initScale (self, scale, center):
		return [x for t in zip([center] * len (scale), scale) for x in t]
	def __init__ (self, scale, center, topleft, widthheight):
		ShapeAbs.__init__ (self, scale, center, topleft, widthheight)
	
class ScaleView:
	def __init__ (self, scale, nw):
		self.nw = nw
		self.initHelper (scale)
		self.scale = scale
	def remove_from_screen (self):
		remove_from_screen (self.constellation)
		remove_from_screen (self.wheel)
	def initHelper (self, scale):
		self.scale = scale
		#self.pts = circularizes (normalize_radians (linearize_frequencies (scale)))
		self.pts = inward_spiral (linearize_frequencies (scale))
		
		self.wheel = self.nw.draws2 (Wheel,
			self.pts, (0, 0), (-1, -1), (1, 1))
		self.constellation = self.nw.draws2 (Constellation,
			self.pts, (0, 0), (-1, -1), (1, 1))
	def update (self, scale):
		self.remove_from_screen ()
		self.initHelper (scale)
	def adjustMode (self, delta_mode):
		self.scale.adjustMode (delta_mode)
		self.update (self.scale)
	def setMode (self, mode):
		self.scale.setMode (mode)
		self.update (self.scale)

#For a positive odd number n,
#the n-odd-limit contains all rational numbers
#such that the largest odd number that divides either the numerator or denominator is not greater than n.
def n_odd_limit_helper (n, m):
	if n <= 0: raise Exception ()
	if n % 2 is 0: raise Exception ()
	for k in xrange (1, m + 1):
		for j in xrange (3, min (n + 1, k), 2):
			#if k / j < 2:
			#if k % j is not 0:
				#yield k / j
				yield Fraction (k, j)
	for j in xrange (3, n + 1, 2):
		for k in xrange (1, j):
			#if j / k < 2:
			#if j % k is not 0:
				#yield j / k
				yield Fraction (j, k)
def n_odd_limit (n, m):
	return sorted (set (n_odd_limit_helper (n, m)))
def is_prime (n):
	for k in xrange (2, int (pow (n, .5)) + 1):
		if n % k is 0:
			return False
	return True
def primes (n):
	for k in xrange (2, n + 1):
		if is_prime (k):
			yield k
def smooth_numbers (n, m):
	p = list (primes (n))
	return sorted (set (smooth_numbers_helper (zip (p, [0] * len (p)), m)))
def smooth_numbers_helper (ps, m):
	for i in xrange (len (ps)):
		cp = list (ps)
		b, e = cp[i]
		e += 1
		cp[i] = b, e
		ret = reduce (mul, [B ** E for B, E in cp])
		if ret > m: continue
		yield ret
		for ret in smooth_numbers_helper (cp, m):
			yield ret
def n_prime_limit_helper (n, m):
	sm = list (smooth_numbers (n, m))
	for k in sm:
		for j in sm:
			if j < k:
				#if j % k is not 0:
					#yield k / j
					yield Fraction (k, j)
def n_prime_limit (n, m):
	return sorted (set (n_prime_limit_helper (n, m)))
def consecutive_smooth_numbers (n, m):
	ns = smooth_numbers (n, m)
	return [Fraction (c, p) for p, c in zip (ns, ns[1:]) if c - 1 is p]
"""print n_odd_limit (3, 10)
print n_odd_limit (5, 10)
print n_odd_limit (7, 10)
print n_prime_limit (3, 10)
print n_prime_limit (5, 10)
print n_prime_limit (7, 10)
print consecutive_smooth_numbers (5, 20)
hs = n_odd_limit (5, 10)
l = []
map (l.extend, [euclid (h, k, list (hs)) for h in xrange (len (hs)) for k in xrange (h)])
l = sorted (set (l))
print l
sleep (3)
exit"""

# scale - wheel
# key - wheel, constellation
#class KeyView:
# chordview:
# - key - wheel
# - chord - wheel, constellation	
	
	
	#def rotate (self, scale):
	#	self.wheel.rotate (scale)
	#	self.constellation.rotate (scale)
#print equal_temperament_scale (12)
#print linearize_frequencies (equal_temperament_scale (12))
#print normalize_radians (linearize_frequencies (equal_temperament_scale (12)))
ets0 = Scale (equal_temperament_scale (12))
ets1 = Scale (equal_temperament_scale (5))
#ets2 = Scale ([n - 1 for n in [1/1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8]])
ets2 = Scale ([n - 1 for n in [Fraction (n, d) for n, d in zip ([1, 9, 5, 4, 3, 5, 15], [1, 8, 4, 3, 2, 3, 8])]])
#print list (ets)
#sleep (300)

"""print n_odd_limit (3, 10)
print n_odd_limit (5, 10)
print n_odd_limit (7, 10)
print n_prime_limit (3, 10)
print n_prime_limit (5, 10)
print n_prime_limit (7, 10)
print consecutive_smooth_numbers (5, 20)
hs = n_odd_limit (5, 10)
l = []
map (l.extend, [euclid (h, k, list (hs)) for h in xrange (len (hs)) for k in xrange (h)])
l = sorted (set (l))
print l
"""
#scale3 = sorted (list (n_odd_limit (3, 10)))
#scale3 = list ([s for s in scale3 if s < 2])	
#print scale3
scale3 = sorted (set ([
	1,
	2/1,
	3/1, 3/2,
	4/1, 4/2, 4/3,
	5/1, 5/2, 5/3, 5/4,
	6/1, 6/2, 6/3, 6/4, 6/5,
	8/1, 8/2, 8/3, 8/4, 8/5, 8/6,
	9/1, 9/2, 9/3, 9/4, 9/5, 9/6, 9/8,
	10/1, 10/2, 10/3, 10/4, 10/5, 10/6, 10/8, 10/9]))
#scale3 = list ([s for s in scale3 if s < 3])
ets3 = Scale (scale3)

W = 200
H = 200
begin_graphics (width=W, height=H)

w = 2
h = 2
nw = [[NestedWindow (Fraction (W, w), ww, Fraction (H, h), hh)
	for hh in xrange (h)] for ww in xrange (w)]

box = zip ([-1,1,1,-1],[1,1,-1,-1])
for x, y in product ([1, 0], [0, 1]):
	#pt  = nw[y][x].draw  (Point,   origin)
	b = nw[y][x].draws (Polygon, box)
	#sleep (1)

sv0 = ScaleView (ets0, nw[0][0])
#print list (ets1)
sv1 = ScaleView (ets1, nw[1][0])
sv2 = ScaleView (ets2, nw[0][1])
sv3 = ScaleView (ets3, nw[1][1])

sleep (1)

while True:
	sleep (1)
	#rotate_by (sv0.wheel, normalize_degree (1.0 / (1 + len (ets0))))
	#rotate_by (sv1.wheel, normalize_degree (1.0 / (1 + len (ets1))))
	#rotate_by (sv2.wheel, normalize_degree (1.0 / (0 + len (ets2))))
	#rotate_by (sv2.constellation, normalize_degree (1.0 / (0 + len (ets2))))
	#sv1.rotate (ets1.rotate (1))
	#ets2.adjustMode (1)
	#sv2.update (ets2)
	sv0.adjustMode (1)
	sv1.adjustMode (1)
	sv2.adjustMode (1)
	sv3.adjustMode (1)

# scale, key, prog, chord

sleep (30)

end_graphics ()

exit




# scale => key => prog
# numNotes => chords

# rhythms => rkey => rprog
# rNumNotes => rChords

# beat * chords * rChords












"""
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

""for a in xrange (8):
	b = Bjorklund (8, a + 1)
	b.bjorklund ()
	print b.sequence
b = Bjorklund (13, 5)
b.bjorklund ()
print b.sequence""

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
"""



































































"""
class NestedWindow:
	def normalize_width  (self, x):  return x * self.W + self.wW
	def normalize_height (self, y):  return y * self.H + self.hH
	def normalize_point  (self, pt): return (
		self.normalize_width (pt[0]), self.normalize_height (pt[1]))
	def __init__ (self, W, w, H, h):
		self.w = w
		self.h = h
		self.W = W
		self.H = H
		self.wW = w * W
		self.hH = h * H
		#self.origin = self.translate (origin)
		###self.objs = []
		#Plot (self.origin)
		#self.box ((0, 0), W, H)
	#def box (self, c, w, h): self.objs.append (Box (c, w, h))
	def translate (self, pt):
		return self.normalize_point (shifts (pt))
		#return ((shift (pt[0]) + self.w) * self.W, (shift (pt[1]) + self.h) * self.H)
	def draw (self, method, arg):
		arg = self.translate (arg)
		return method (arg)
	def draws (self, method, args):
		args = [self.translate (arg) for arg in args]
		return method (args)
	#def constellation (self, scale): self.objs.append (Constellation (self, scale))
	#def polygon (self, scale): self.objs.append (Polygon ([self.translate (cs) for cs in scale]))
	#def wheel (self, scale, key):
	#	self.polygon (scale)
	#	self.constellation (key)
	#	self.polygon (key)
	###def rotate (self, r):
	#	for obj in self.objs:
	#		angle = scale[len (scale) % r]
	#		rotateBy (obj, angle)
#class Constellation:
#	def __init__ (self, parent, scale):
#		self.scale = list ([Line (parent.origin, parent.translate (cs)) for cs in scale])
#class Wheel:
	
#class Wheel:
#	def __init__ (self, scale, key):


def accumulate(iterable, func=add):
    'Return running totals'
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = func(total, element)
        yield total
def discrete_derivative (arr): return [b - a for a, b in zip (arr, arr[1:])]
def discrete_integral (arr): return accumulate (arr)
	#return cumsum (self.diffs)
	
def rotate (arr, amt=1):
	if len (arr) is 0: return arr
	amt = amt % len (arr) # Normalize y... even works for negative y
	return arr[amt:] + arr[:amt]
class Scale:
	"How to divide a circle/octave"
	def __init__ (self, arr, mode=0):
		self.original = arr
		self.setDiffs ()
		self.adjustMode (mode)
	def __len__ (self): return len (self.original)
	def __iter__ (self): return discrete_integral (self.diffs)
	def setDiffs (self):
		self.diffs = discrete_derivative (self.original)
	def adjustMode (self, delta_mode):
		self.diffs = rotate (self.diffs, delta_mode)
	def setMode (self, mode):
		setDiffs ()
		adjustMode (mode)
	def apply (self, baseFreq):
		return [baseFreq * e for e in discrete_integral ()]
def lb (n): return log (n) / log (2)
def linearize_frequencies (arr): return [lb (n) for n in arr]
def normalize_radians (arr): return [n * 2 * pi for n in arr]
def circularize (radian): return cos (radian), sin (radian)
def circularizes (radians): return [circularize (r) for r in radians]
def normalize_reals_to_nonnegatives (arr):
	return [normalize_real_to_nonnegative (r) for r in arr]
def normalize_nonnegatives_to_reals (arr):
	return [normalize_nonnegative_to_real (r) for r in arr]
	"""

"""
def equal_spacing (n): return [1.0 * h / n for h in xrange (0, n)]
def equal_temperament_scale (n): return [2 ** h for h in equal_spacing (n)]
print equal_temperament_scale (12)
print linearize_frequencies (equal_temperament_scale (12))
print normalize_radians (linearize_frequencies (equal_temperament_scale (12)))
#print normalize_radians (normalize_nonnegatives_to_reals (linearize_frequencies (equal_temperament_scale (12))))
ets = Scale (equal_temperament_scale (12))

def normalize_window_point (point, win):
	x = (point[0] + 1) * win.getWidth () / 2
	y = (point[1] + 1) * win.getHeight () / 2
	return Point (x, y)
def normalize_window_polygon (pgon, win):
	return Polygon ([normalize_window_point (p, win) for p in pgon])
def display_polygon (pgon, win):
	normalize_window_polygon (pgon, win).draw (win)
def display_constellation (points, win):
	center = normalize_window_point ((0, 0), win)
	for p in points:
		pt = normalize_window_point (p, win)
		#pt.draw (win)
		l = Line (center, pt)
		l.draw (win)
		
		
def equal_spacing (n):
	for h in xrange (n):
		yield (h + 1) / n
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
	#pts = list (circularizes (normalize_radians (linearize_frequencies (scale))))
	#display_points (pts, win)
	display_constellation (pts, win)
	display_polygon (pts, win)
display_scale (ets)
sleep (300)
"""
# regular number harmonics

def euclid (h, k, l):
	#l[h] = l[k] ** a * b
	#(l[h] / b) = l[k] ** a
	#log base l[k] of (l[h] / b) = a
	#log (l[h] / b) / log l[k]) = a
	#log l[h] - log b = a log l[k]
	a = floor (log (l[h]) / log (l[k]))
	b = l[h] / (l[k] ** a)
	#print l[h], "=", l[k], "**", a, "+", b
	for i in xrange (len (l)):
		if (l[i] == b):
			#yield euclid (k, i, l)
			#break
			return euclid (k, i, l)
	epsilon = 10/9
	epsilon = (2 ** 485) / (3 ** 306)
	epsilon = 531441 / 524288
	if b < epsilon:
		return l
	l += [b]
	return euclid (k, len (l) - 1, l)
# freq = base * 2**h
# ratios: 2/1 3/1 3/2 4/1 4/2 4/3 5/1 5/2 5/3 5/4
# 1 2 3 4
# inverted: 1/1 1/2 1/3 1/4 1/5 1/6
# complement: 0 1/2 2/3 3/4 4/5 5/6
# invert:     0 2/1 3/2 4/3 5/4 6/5

pythagorean_scale = [
	1/1, 256/243, 9/8, 32/27,
	81/64, 4/3, 729/512, 3/2,
	128/81, 27/16, 16/9, 243/128, 2/1]

#for k in xrange (1,5):
#	1 - ()

#hs = [1] + sorted ([(h + 1) / h for h in hs])
#hs = sorted ([(h + 1) / h for h in hs])
#l = []
#map (l.extend, [euclid (h, k, list (hs)) for h in xrange (len (hs)) for k in xrange (h)])
#l = sorted (set (l))


# radian to color
# color to radian (needs range... assume visible spectrum)
# sound to radian (needs base freq)
# radian to sound

# 430-770 THz

# Red    FF 00 00
# Orange
# Yellow FF FF 00
# Green  00 FF 00
# Teal   00 FF FF
# Blue   00 00 FF
# Purple FF 00 FF

#     0    1     2    3   4      5      6     7
#   000  001   010  011 100    101    110   111
# black blue green teal red purple yellow white

# base freq to tempo spectrum
# base freq to color spectrum

# scale applied to base freq... equal temperament
#                  tempo...     1/1, 1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5
#                  color

# transpose audio scale to visual scale... just need len1 = len2

#def colorCircle (x, y, r):
#	for R in xrange (0, 360):
#		c = radianToColor






































# scale       class: num notes        pitch/rhythm
# key         class: num notes
# progression class: num notes
# chord       class: num notes

# need a way to change modes

# num notes (harmony complexity)
# melody:
# - distributing beats in rhythm
# - distributing arpeggio chord

#class Key (Bjorklund):
#	"""How to divide a scale"""
#	def __init__ (self):
#class Progression (Key):
#	"""How to divide a key"""
#class Chord (Key):
#	"""How to divide a key"""



# scale is radians
# key is indices in scale
# prog, chord are indices in key
Wheel (scale4, key)
Wheel (key, prog)
Wheel (key, chord)

W = 300
H = 300
begin_graphics (width=W, height=H)

w = 2
h = 2
nw = [None] * w
for ww in xrange (w):
	nw[ww] = [None] * h
	for hh in xrange (h):
		nw[ww][hh] = NestedWindow (W / w, ww, H / h, hh)

scale = pythagorean_scale
scale.remove (2)
scale2 = [log (n) / log (2) for n in scale]
scale3 = [n * 2 * pi for n in scale2]
scale4 = list ([(cos (n), sin (n)) for n in scale3])
#scale5 = list ([(translate (cs)) for cs in scale4])

key = Bjorklund.factory (len (scale), 7, 0)
key2 = [s for s,k in zip (scale, key.sequence) if k]
key4 = list ([s for s,k in zip (scale4, key.sequence) if k])
#print len (key.sequence)
#print len (key5)

prog = Bjorklund.factory (11, sum (key.sequence), 0)
prog2 = [s for s,k in zip (scale, prog.sequence) if k]
prog4 = list ([s for s,k in zip (scale4, prog.sequence) if k])
#print len (prog.sequence)
#print len (prog5)

chord = Bjorklund.factory (sum (key.sequence), 5, 0)
chord2 = [s for s,k in zip (scale, chord.sequence) if k]
chord4 = list ([s for s,k in zip (scale4, chord.sequence) if k])

nw[0][0].wheel (scale4, key4)
nw[0][1].wheel (scale4, prog4)
nw[1][0].wheel (scale4, chord4)

nw[0][0].rotate (1)
sleep (1)
nw[0][1].rotate (2)
sleep (1)
nw[1][0].rotate (3)
sleep (1)
nw[0][0].rotate (4)
sleep (1)
nw[0][1].rotate (5)
sleep (1)
nw[1][0].rotate (6)

#constellation (scale5)
#Polygon (scale5)
#constellation (key5)
#Polygon (key5)



sleep (30)

end_graphics ()