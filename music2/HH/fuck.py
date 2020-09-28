DEFAULT_ROTATION = pi / 2
def inscribe_angles   (n):                           
	r   = range (0, n)
	f   = lambda k: k / n * pi
	tmp = map (f, r)
	tmp=tuple(tmp)
	print("inscribed angles: %s" % (tmp,))
	return tuple (tmp)
def   rotate_angles   (angles, dt=DEFAULT_ROTATION):
	f   = lambda t: t + dt
	tmp = map (f, angles)
	return tuple (tmp)
def angles_to_polygon (angles):
	f   = lambda t: (cos (t), sin (t))
	tmp = map (f, angles)
	tmp=tuple(tmp)
	print("polygon: %s" % (tmp,))
	return tuple (tmp)
def inscribe_polygon (n):
	angles = inscribe_angles   (n)
	angles =   rotate_angles   (angles)
	pts    = angles_to_polygon (angles)
	return tuple (pts)

def graphics_affine_x (x):   return (x + 1) / 2
def graphics_affine_y (y):   return (1 - y) / 2
from itertools import chain
def graphics_affine   (pt):
	tmp = zip (pt[:-1:2], pt[1::2])
	tmp=tuple (tmp)
	print(tmp)
	f   = lambda xy: (graphics_affine_x (xy[0]), graphics_affine_y (xy[1]))
	tmp = map (f, tmp)
	tmp = chain (*tmp) # TODO ?
	tmp=tuple (tmp)
	print("graphics affine: %s" % (tmp,))
	return tuple (tmp)
def graphics_affines  (pts): 
	tmp = map (graphics_affine, pts)
	tmp=tuple(tmp)
	print ("graphics affines: %s" % (tmp,))
	return tmp

def    scale_dim      (n,   scale, offset):
	print ("n: %s" % (n,))
	print ("s: %s" % (scale,))
	print ("o: %s" % (offset,))
	return offset + scale * n
def    scale_point    (pt, origin, dims):
	nsos   = zip (pt, origin, dims)
	nsos=tuple(nsos)
	print("nsos: %s" % (nsos,))
	f      = lambda nso: scale_dim (*nso)
	ret    = map (f, nsos)
	ret=tuple(ret)
	print(ret)
	#ret = zip (*ret) # TODO ?
	print("scaled point: %s" % (ret,))
	return tuple (ret)	
def    scale_points   (pts, rect):
	assert len (rect) % 2 == 0
	ndim = len (rect) // 2
	orig = rect[:ndim]
	dims = rect[ndim:]
	print (pts)
	print (orig)
	print (dims)
	f    = lambda pt: scale_point (pt, orig, dims)
	ret  = map (f, pts)
	ret=tuple(ret)
	print ("scaled points: %s" % (ret,))
	return tuple (ret)
	
def bounding_box (pts):
	tmp = zip (*pts)                                # array of tuples (x, y) => arrays of x's, y's and z's  
	tmp = map (lambda k: (min (*k), max (*k)), tmp) # array of tuples (minx, maxx), (miny, maxy)
	tmp = zip (tmp)                                 # array of tuples (minx, miny), (maxx, maxy)
	tmp=tuple(tmp)
	print("bounding box: %s" % (tmp,))
	return tuple (tmp)
from itertools import accumulate
def point_deltas (pts):
	tmp = zip (*pts)                                # array of tuples (minx, miny), (maxx, maxy) => arrays of mins, maxes
	f   = lambda k: accumulate (lambda a, b: a - b, k[::-1])
	tmp = map (f, tmp)                              # deltas (maxx - minx), (maxy - miny)
	tmp=tuple(tmp)
	print ("deltas: %s" % (tmp,))
	return tuple (tmp)
def bounding_rect (pts):
	bb  = bounding_box (pts)
	ds  = point_deltas (bb)
	return bb[0], ds
