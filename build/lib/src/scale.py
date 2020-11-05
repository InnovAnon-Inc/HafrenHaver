#! /usr/bin/env python3

from itertools import accumulate, product
##from numba     import jit
from random    import choice
from key       import random_key

from random_util import rotate

western_lower_tetrachords_db = [
	[2, 2, 1], # Major
	[2, 1, 2], # Minor
	[1, 3, 1], # Harmonic
	[1, 2, 2], # Upper Minor
]
western_upper_tetrachords_db = [
	[2, 2, 1], # Major
	[1, 3, 1], # Harmonic
	[1, 2, 2], # Upper Minor
]
non_western_lower_tetrachords_db = [
	[3, 1, 1],
	[2, 2, 1],
	[1, 3, 1],
	[2, 1, 2],
	[1, 2, 2],
	[1, 1, 3],
]
non_western_upper_tetrachords_db = [
 	[3, 1, 1],
 	[2, 2, 1],
 	[1, 3, 1],
 	[2, 1, 2],
 	[1, 2, 2],
 	[1, 1, 3],
]
indian_lower_tetrachords_db = [
	[3, 2, 1],
	[3, 1, 2],
	[2, 2, 2],
	[1, 3, 2],
	[2, 1, 3],
	[1, 2, 3],
]
indian_upper_tetrachords_db = [
	[3, 1, 1],
	[2, 2, 1],
	[1, 3, 1],
	[2, 1, 2],
	[1, 2, 2],
	[1, 1, 3],
]
"""
def init_db (db, lr, lower_tetrachords, upper_tetrachords):
	if lr in db: return db[lr]
	db[lr] = tuple (filter (lambda tetras: sum (tetras[0] + tetras[1]) < lr, product (lower_tetrachord, upper_tetrachord)))
	return db[lr]
western_scales_db = {}
def init_western_scales_db (lr):
	return init_db (western_scales_db, lr, western_lower_tetrachords_db, western_upper_tetrachords_db)
non_western_scales_db = {}
def init_non_western_scales_db (lr):
	return init_db (non_western_scales_db, lr, non_western_lower_tetrachords_db, non_western_upper_tetrachords_db)
indian_scales_db = {}
def init_indian_scales_db (lr):
	return init_db (indian_scales_db, lr, indian_lower_tetrachords_db, indian_upper_tetrachords_db)
# TODO japanese_scales_db = {}
western_scales_rotations_db = {}
def init_western_scales_rotations_db (lr):
	scale_rots = {}
	for scale in western_scales_db:
		temp = []
		for rot in range (0, len (scale)):
			scale_rot = rotate (scale, rot)
			temp = temp + [scale_rot]
		scale_rots[scale] = temp
	return scale_rots
"""
#def init_western_scale_rotation_mappings_db (lr):
	# determine scales which are rotations/modes of another scale
# select scale region
# select scale from that region
# create mapping from scales to inversion/rotations for all scales across all regions


# TODO trichords
# TODO pentatonic scales
# TODO map pentatonics scales to septatonic scales
	

# the natural modes can be computed using bjorklund's
# but the more archaic tetrachord theory yields more exotic results
tetrachords_db = [
	[2, 2, 1], # major
	[2, 1, 2], # minor
	[1, 3, 1], # harmonic
	[1, 2, 2], # upper minor
	
	# non-western, lower tetrachords
	[3, 1, 1],
	[1, 1, 3],
	
	# indian, lower tetrachord
	[3, 2, 1],
	[3, 1, 2],
	[2, 2, 2],
	[1, 3, 2],
	[2, 1, 3],
	[1, 2, 3],
]
#class Tetrachord:
def random_tetrachord (): return choice (tetrachords_db)

scale_db = {}
def init_scale_db (lr):
	if lr not in scale_db: scale_db[lr] = tuple (filter (lambda tetras: sum (tetras[0] + tetras[1]) < lr, product (tetrachords_db, tetrachords_db)))
	return scale_db[lr]

##@jit
class Scale:
	# given 2 tetrachords, create a scale that can be indexed to get ratios
	@staticmethod
	#def make_scale (lr=12, lower_tetrachord, upper_tetrachord):
	def make_scale (lr, lower_tetrachord, upper_tetrachord):
		lower_sum = sum (lower_tetrachord)
		upper_sum = sum (upper_tetrachord)
		mid       = lr - lower_sum - upper_sum
		if mid == 0: raise Error ()
		return tuple (lower_tetrachord + [mid] + upper_tetrachord)
	@staticmethod
	def make_scale2 (intervals):
		intervals = accumulate (intervals)
		return tuple (intervals)
	def __init__ (self, key, lower_tetrachord, upper_tetrachord):
		self.key              = key
		self.lower_tetrachord = lower_tetrachord
		self.upper_tetrachord = upper_tetrachord
		self.intervals2       = Scale.make_scale (len (key.chromatic.ratios), lower_tetrachord, upper_tetrachord)
		self.intervals        = Scale.make_scale2 ([0] + list (self.intervals2[:-1]))
		intervals = tuple (list (self.intervals) + [len (key.chromatic.ratios)])
		self.intervals3       = [y - x for x, y in zip (intervals[:-1:], intervals[1::])]
		#self.intervals2 = self.intervals2[1:]
		#self.intervals2 = self.intervals2[1:] + [self.intervals2[0]]
		
		#self.intervals2 = self.intervals2[1:]
		#assert sum ([0] + lower_tetrachord + [mid] + upper_tetrachord) == len (ratios)
		assert sum (self.intervals2) == len (key.chromatic.ratios)
	def __repr__ (self): return str ("Scale=[%s, lower tetrachord=%s, upper tetrachord=%s, intervals=%s]" % (self.key, self.lower_tetrachord, self.upper_tetrachord, self.intervals))
	def ratio (self, degree, octave):
		index = self.intervals[degree]
		return self.key.ratio (index, octave)
	def pitch (self, degree, octave):
		index = self.intervals[degree]
		return self.key.pitch (index, octave)
	def function (self, degree): return self.key.function (self.intervals[degree])
	def interval (self, degree): return self.intervals[degree]
	def degree (self, degree):
		index = self.interval (degree)
		return self.key.degree (index)
	def increment_key (self, dkey=1):
		key, doctave = self.key.increment (dkey)
		return Scale (key, self.lower_tetrachord, self.upper_tetrachord), doctave
	def decrement_key (self, dkey=1):
		key, doctave = self.key.decrement (dkey)
		return Scale (key, self.lower_tetrachord, self.upper_tetrachord), doctave
	def increment (self, degree):
		#  TODO fuck
		#print ("degree=%s" % degree)
		#key = self.interval (degree) - self.interval (0)
		#key = self.interval (degree) - self.interval (degree - 1)
		#if degree == len (self.intervals2) - 1: degree = 0
		#if degree == 0: key = self.intervals2[0]
		#else:           key = self.intervals2[1:][degree - 1]
		#assert degree != 0
		print ("degree=%s, %s" % (degree, self.intervals2))
		key = self.intervals2[degree - 1]
		#print ("dkey=%s" % key)
		return self.increment_key (key)
	def decrement (self, degree):
		#  TODO fuck
		#key = self.interval (-degree) - self.interval (0)
		#key = len (self.key.chromatic.ratios) - self.interval (-degree)
		#a = self.interval (-degree + 1)
		#b = len (self.key.chromatic.ratios)
		#if degree == 1: degree
		#key = self.interval (-degree + 1) - self.interval (-degree)
		#assert degree != 0
		print ("degree=%s, %s" % (degree, self.intervals3))
		#if degree == 0: key = self.intervals3[0]
		#key = self.intervals3[-degree]
		key = self.intervals3[degree]
		#key = self.intervals2[-degree]
		print ("dkey=%s" % key)
		return self.decrement_key (key)
	def brighter_key (self):
		key, doctave = self.key.brighter ()
		return Scale (key, self.lower_tetrachord, self.upper_tetrachord), doctave
	def darker_key (self):
		key, doctave = self.key.darker ()
		return Scale (key, self.lower_tetrachord, self.upper_tetrachord), doctave
	def brighter (self, ddegree):
		#ddegree = len (self.intervals)
		#ddegree = ddegree - ddegree // 2
		key = sum (self.intervals2[:ddegree])
		return self.increment_key (key)
		##return self.increment (ddegree)
	def darker (self, ddegree):
		#ddegree = len (self.intervals)
		#ddegree = ddegree // 2
		##ddegree = ddegree - ddegree // 2
		##return self.decrement (ddegree)
		key = sum (self.intervals3[:ddegree + 1])
		return self.decrement_key (key)
	#def parallel (self, degree):




def init_scale (lr, l_tetra, r_tetra):
	s = sum (l_tetra + r_tetra)
	if s >= lr: raise Exception ()
	mid = lr - s
	return tuple (l_tetra + [mid] + r_tetra)
scale_db = {}
def init_scale_db (lr):
	if lr in scale_db: return scale_db[lr]
	temp = {}
	for l_tetra, r_tetra in product (tetrachords_db, tetrachords_db):
		if sum (l_tetra + r_tetra) >= lr: continue
		scale        = init_scale (lr, l_tetra, r_tetra)
		if  scale in temp: continue
		temp[scale]  = (l_tetra, r_tetra)

		il_tetra     = r_tetra[::-1]
		ir_tetra     = l_tetra[::-1]
		iscale       = init_scale (lr, il_tetra, ir_tetra)
		if iscale in temp: continue
		temp[iscale] = (il_tetra, ir_tetra)
	scale_db[lr] = temp
	return temp
scale_inversion_db = {}
def init_scale_inversion_db (lr):
	if lr in scale_inversion_db: return scale_inversion_db[lr]
	scales = init_scale_db (lr)
	temp   = {}
	for scale, tetras in scales.items ():
		l_tetra, r_tetra = tetras
		if scale in temp: continue
		inversion       = tuple (scale[::-1])
		assert inversion not in temp
		assert inversion     in scales
		temp[scale]     = inversion
		temp[inversion] = scale
	scale_inversion_db[lr] = temp
	return temp
scale_rotation_db = {}
def init_scale_rotation_db (lr):
	if lr in scale_rotation_db: return scale_rotation_db[lr]
	scales = init_scale_inversion_db (lr)
	temp   = {}
	for scale in scales:
		for r in range (0, len (scale)):
			#temp2[r] = tuple (rotate (scale, r))
			rot = tuple (rotate (scale, r))
			temp[rot] = (scale, r)
		#temp[scale] = temp2
	scale_rotation_db[lr] = temp
	return temp
scales_db = {}
def init_scales_db (lr):
	if lr in scales_db: return scales_db[lr]
	rotations = init_scale_rotation_db (lr)
	temp = {}
	for mode, value in rotations.items ():
		scale, r = value
		for scale2, value in rotations.items ():
			mode2, r2 = value
			#if scale == scale2 and mode == mode2: continue
			if mode2 == mode:
				if mode in temp: temp[mode] = temp[mode] + [(scale2, r2)]
				else:            temp[mode] = [(scale2, r2)]
	scales_db[lr] = temp
	return temp
# TODO db of unique tuples on top of scales_db ?
	
	

	#def degrees (self):
	#	for index in range (0, len (self.intervals)):
	#		function = self.function (index)
	#		index    = self.degree   (index) 
	#		yield (index, function)
def random_scale (key=None, chromatic=None, solfeggio=None, lower_tetrachord=None, upper_tetrachord=None):
	if not key: key = random_key (chromatic, solfeggio)
	#scales = init_scale_db (len (key.chromatic.ratios))
	lr = len (key.chromatic.ratios)
	scales = init_scales_db (lr)
	#lower_tetrachord, upper_tetrachord = choice (scales)
	scale, mode = choice ([(key, value) for key, value in scales.items ()])
	scales = init_scale_db (lr)
	lower_tetrachord, upper_tetrachord = scales[scale]
	return Scale (key, lower_tetrachord, upper_tetrachord)
	"""
	if lower_tetrachord is None and upper_tetrachord is None: lower_tetrachord = random_tetrachord ()
	if lower_tetrachord is None:
		while True:
			lower_tetrachord = random_tetrachord ()
			if (sum (lower_tetrachord) + sum (upper_tetrachord) < len (key.chromatic.ratios)): break
	if upper_tetrachord is None:
		while True:
			upper_tetrachord = random_tetrachord ()
			if (sum (lower_tetrachord) + sum (upper_tetrachord) < len (key.chromatic.ratios)): break
	return Scale (key, lower_tetrachord, upper_tetrachord)
	"""
if __name__ == "__main__":
	def main ():
		scale = random_scale ()
		print (scale)
	main ()
