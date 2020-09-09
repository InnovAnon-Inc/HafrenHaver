#! /usr/bin/env python

from itertools import chain, permutations, repeat, product
#from numba     import jit
from random import choice

from scale       import random_scale, init_scale_inversion_db, init_scales_db, init_scale_db
from random_util import random_index, rotate

# TODO scale inversions
# TODO scale rotations
"""
scale_inversion_db = {}
def init_scale_inversion_db (intervals):
	assert type (intervals) is tuple
	if intervals in scale_inversion_db: return scale_inversion_db[intervals]
	rev = tuple (intervals[::-1])
	scale_inversion_db[intervals] = rev
	scale_inversion_db[rev]       = intervals
scale_rotation_db = {}
def init_scale_rotation_db  (intervals):
	assert type (intervals) is tuple
	if intervals in scale_rotation_db:  return scale_rotation_db[intervals]
	inverse = init_scale_inversion_db (intervals)
	
	
	temp = {}
	
		if mode1 in temp: continue
		if mode2 in temp: continue
		rot1 = rotate (intervals, mode1)
		rot1 = tuple (rot1)
		rot2 = rotate (intervals, mode2)
		rot2 = rot2[::-1]
		rot2 = tuple (rot2)
		if rot1 != rot2: continue
		if mode1 in temp:
			if mode2 not in temp[mode1]: temp[mode1] = temp[mode1] + [mode2]
		else: temp[mode1] = [mode2]
		if mode2 in temp:
			if mode1 not in temp[mode2]: temp[mode2] = temp[mode2] + [mode1]
		else: temp[mode2] = [mode1]
	scale_inversion_db[intervals] = temp
	#if tuple (intervals[::-1]) not in scale_inversion_db:
	#	scale_inversion_db[tuple (intervals[::-1])] = temp
	print ("temp=%s" % temp)
	return temp

scale_inversion_db = {}
def init_scale_inversion_db (intervals):
	assert type (intervals) is tuple
	if intervals in scale_inversion_db: return scale_inversion_db[intervals]
	temp = {}
	for mode1, mode2 in product (range (0, len (intervals)), range (0, len (intervals))):
		if mode1 in temp: continue
		if mode2 in temp: continue
		rot1 = rotate (intervals, mode1)
		rot1 = tuple (rot1)
		rot2 = rotate (intervals, mode2)
		rot2 = rot2[::-1]
		rot2 = tuple (rot2)
		if rot1 != rot2: continue
		if mode1 in temp:
			if mode2 not in temp[mode1]: temp[mode1] = temp[mode1] + [mode2]
		else: temp[mode1] = [mode2]
		if mode2 in temp:
			if mode1 not in temp[mode2]: temp[mode2] = temp[mode2] + [mode1]
		else: temp[mode2] = [mode1]
	scale_inversion_db[intervals] = temp
	#if tuple (intervals[::-1]) not in scale_inversion_db:
	#	scale_inversion_db[tuple (intervals[::-1])] = temp
	print ("temp=%s" % temp)
	return temp
"""
#@jit
class Mode:
	def __init__ (self, scale, mode):
		self.scale = scale
		self.mode  = mode
	def __repr__ (self): return str ("Mode=[%s, mode=%s]" % (self.scale, self.mode))
	def adjust (self, index):
		slen   = len (self.scale.intervals)
		index  = index + self.mode
		octave = 0
		while index >= slen:
			index  = index - slen
			octave = octave + 1
		while index < 0:
			index  = index + slen
			octave = octave - 1
		return (index, octave)
	def ratio (self, index, octave):
		(index, doctave) = self.adjust (index)
		octave = octave + doctave
		return self.scale.ratio (index, octave)
	def pitch (self, index, octave):
		(index, doctave) = self.adjust (index)
		octave = octave + doctave
		return self.scale.pitch (index, octave)
	def function (self, index):
		#(index, doctave) = self.adjust (index)
		#return self.scale.function (index)
		return self.scale.function (index)
	def interval (self, index):
		(index, doctave) = self.adjust (index)
		return self.scale.interval (index)
	def degree (self, index):
		(index, doctave) = self.adjust (index)
		return self.scale.degree (index)
	def degrees (self):
		for index in range (0, len (self.scale.intervals)):
			#function = self.function (index)
			index    = self.degree (index) 
			#yield (index, function)
			yield index
	def increment_key (self, dkey=1): # c major => c# major
		scale, doctave = self.scale.increment_key (dkey)
		return (Mode (scale, self.mode), doctave)
	def decrement_key (self, dkey=1): # c major => b major
		scale, doctave = self.scale.decrement_key (dkey)
		return (Mode (scale, self.mode), doctave)
	def increment_scale (self, ddegree=1): # c major => d major
		index, doctave1 = self.adjust (ddegree)
		#print ("index=%s" % index)
		scale, doctave2 = self.scale.increment (index)
		doctave = doctave1 + doctave2
		return (Mode (scale, self.mode), doctave)
		#scale, doctave = self.scale.increment (ddegree)
		#return Mode (scale, self.mode), doctave
	def decrement_scale (self, ddegree=1): # c major => b major
		#index, doctave1 = self.adjust (-ddegree)
		#print ("index=%s" % index)
		#scale, doctave2 = self.scale.decrement (index)
		#doctave = doctave1 + doctave2
		#return Mode (scale, self.mode), doctave
		index, doctave1 = self.adjust (-ddegree)
		#print ("index=%s" % index)
		scale, doctave2 = self.scale.decrement (index)
		doctave = doctave1 + doctave2
		return (Mode (scale, self.mode), doctave)
	def increment (self, dmode=1): # c major => d dorian
		index, doctave = self.adjust (dmode)
		#index, doctave1 = self.adjust (dmode)
		#if   doctave1 < 0: scale, doctave2 = self.scale.decrement_key ()
		#elif doctave1 > 0: scale, doctave2 = self.scale.increment_key ()
		#else:              scale, doctave2 = self.scale, 0
		return (Mode (self.scale, index), doctave)
		#doctave = doctave1 + doctave2
		#return (Mode (scale, index), doctave)
	# c major => b locrian
	def decrement (self, dmode=1): return self.increment (-dmode)
	def brighter_key (self): # c major => g major
		scale, doctave = self.scale.brighter_key ()
		return (Mode (scale, self.mode), doctave)
	def darker_key (self): # c major => f major
		scale, doctave = self.scale.darker_key ()
		return (Mode (scale, self.mode), doctave)
	
	def brighter_scale (self):
		raise Exception ()
		ddegree           = len (self.scale.intervals)
		ddegree           = ddegree - ddegree // 2
		#ddegree           = ddegree - ddegree // 2 + self.mode
		scale, doctave = self.scale.brighter (ddegree)
		#ddegree, doctave1 = self.adjust (ddegree)
		#scale, doctave2 = self.scale.brighter (ddegree)
		#doctave = doctave1 + doctave2
		
		##ddegree, doctave1 = self.adjust (ddegree)
		##scale,   doctave2 = self.scale.increment (ddegree)
		##doctave           = doctave1 + doctave2
		return (Mode (scale, self.mode), doctave)
	def darker_scale (self):
		raise Exception ()
		ddegree           = len (self.scale.intervals)
		ddegree           = ddegree // 2
		#ddegree           = ddegree - ddegree // 2
		#ddegree           = ddegree - ddegree // 2 + self.mode
		scale, doctave = self.scale.darker (ddegree)
		#ddegree, doctave1 = self.adjust (ddegree)
		#scale, doctave2 = self.scale.darker (ddegree)
		#doctave = doctave1 + doctave2
		
		##ddegree           = len (self.scale.intervals)
		##ddegree           = ddegree - ddegree // 2
		##ddegree, doctave1 = self.adjust (-ddegree)
		##scale,   doctave2 = self.scale.decrement (ddegree)
		##doctave           = doctave1 + doctave2
		return (Mode (scale, self.mode), doctave)
	
	def brighter (self): # c major => f lydian
		ndegree           = len (self.scale.intervals)
		ddegree           = ndegree // 2
		#ddegree           = ndegree - ndegree // 2
		return self.increment (ddegree)
		#if self.mode == ddegree: # increment, f lydian => c locrian
	def darker (self): # c major => g mixolydian
		ndegree           = len (self.scale.intervals)
		ddegree           = ndegree // 2
		#ddegree           = ndegree - ndegree // 2
		return self.decrement (ddegree)
		#if self.mode == ndegree: # decrement, b locrian => Bb lydian
		
	"""
	def parallel_key (self, dmode):
		#dmode = self.mode - mode
		if dmode == 0: return self
		if dmode <  0:
			temp,  doctave1 = self.increment_scale (-dmode)
			scale, doctave2 = temp.decrement       (-dmode)
		if dmode >  0:
			temp,  doctave1 = self.decrement_scale ( dmode)
			scale, doctave2 = temp.increment       ( dmode)
		doctave = doctave1 + doctave2
		return scale, doctave
	"""
	def parallel_key (self, dmode):
		if dmode == 0: return (self, 0)
		mode, doctave1 = self.adjust (dmode)
		if dmode <  0: scale, doctave2 = self.scale.darker   (dmode)
		if dmode >  0: scale, doctave2 = self.scale.brighter (dmode)
		doctave = doctave1 + doctave2
		return (Mode (scale, mode), doctave)
		
		#mode,  doctave1 = self.brighter () # c major to f lydian
		##scale, doctave2 = mode.increment_scale (mode.mode)
		#scale, doctave2 = mode.decrement_scale (mode.mode)
		#doctave         = doctave1 + doctave2
		#return scale, doctave
	def parallel_mode_brighter (self):
		ddegree           = len (self.scale.intervals)
		ddegree           = ddegree // 2
		# TODO handle lydian
		return self.parallel_key (ddegree)
	def parallel_mode_darker (self):
		ddegree           = len (self.scale.intervals)
		ddegree           = ddegree - ddegree // 2
		# TODO handle locrian
		return self.parallel_key (ddegree)
	"""
	def invert_mode1 (self):
		#inversions = init_scale_inversion_db (self.scale.intervals2)
		#modes = inversions[self.mode]
		#assert len (modes) == 1
		#mode  = modes[0]
		#dmode = self.mode - mode
		#ret   = self.parallel_key (dmode)
		##print ("%s" % type (ret))
		##assert type (ret) is tuple
		#return ret
		lr         = len (self.scale.key.chromatic.ratios)
		inversions = init_scale_inversion_db (lr)
		inversion  = inversions[self.scale.intervals2]
		scales     = init_scales_db (lr)
		modes      = scales[inversion]
		temp       = choice (modes)
		scale, mode = temp
		temp       = init_scale_db (lr)
		l_tetra, r_tetra = temp[mode]
		scale      = Scale (self.scale.key, l_tetra, r_tetra)
		return (Mode (scale, mode), doctave)
	def invert_mode2 (self):
		modes = scale_inversion_db[self.mode]
		assert len (modes) == 1
		mode  = modes[0]
		dmode = self.mode - mode
		if dmode == 0: return self
		if dmode <  0: return self.decrement (-dmode)
		if dmode >  0: return self.increment ( dmode)
		
		#mode,  doctave1 = self.darker ()
		##scale, doctave2 = self.decrement_scale (mode.mode)
		#scale, doctave2 = self.increment_scale (mode.mode)
		#doctave         = doctave1 + doctave2
		#return scale, doctave
	"""
	#def build_chords (self):
	#	degrees = list (self.degrees ())
	#	chords = {}
	#	for i in range (0, len (degrees)):
	#		a = degrees[i]
	#		for j in range (i + 1, len (degrees)):
	#			b = degrees[j]
	#			for k in range (j + 1, len (degrees)):
	#				c = degrees[k]
	#				chord = [a, b, c]
	#				if chord not in chord_db: continue
	#				if i not in chords: chords[i] = [chord]
	#				else:               chords[i] = chords[i] + [chord]
	#	return chords



#interval_db = [
#	1, # m2
#	2, # M2
#	3, # m3
#	4, # M3
#	5, # P4
#]
#interval_db = [
#	[4, 3], # major
#	[3, 4], # minor
#	[1, 6], # sus2
#	[2, 5], # sus2
#	[5, 2], # sus4
#	[3, 3], # dim
#	[4, 4], # aug
#]

# TODO generate chord db using entire scales (for extended notes)
# at chromatic layer
chord_db = [
	[0, 4, 7], # major chord, consonant
	[0, 3, 7], # minor chord, consonant
	[0, 1, 7], # sus2 (m2),   dissonant, chord[1]-- or chord[1]++
	[0, 2, 7], # sus2 (M2),   dissonant, chord[1]-- or chord[1]++
	[0, 5, 7], # sus4,        dissonant, chord[1]-- or chord[1]++
	[0, 3, 6], # dim,         dissonant, TT
	[0, 4, 8], # aug,         dissonant, chord[2]-- or chord[2]++
]

# at key layer
chords_db = {}
#@jit
def init_chords_db (chromatic):
	if chromatic in chords_db: return chords_db[chromatic]
	temp = []
	for chord in chord_db:
		for root in range (0, len (chromatic.ratios)):
			t = [root + note for note in chord]
			temp = temp + [t]
	chords_db[chromatic] = temp
	return temp

# mode layer

tonic_chords_db = {}
#@jit
def adjust (chromatic, index):
	rlen   = len (chromatic.ratios)
	octave = 0
	while index >= rlen:
		octave = octave + 1
		index  = index  - rlen
	while index < 0:
		octave = octave - 1
		index  = index  + rlen
	return (index, octave)
#@jit
def tonic_chord (chord, mode):
	degrees = mode.degrees ()
	for note in chord:
		note, doctave = adjust (mode.scale.key.chromatic, note)
		if note not in degrees: return False
	return True
#@jit
def init_tonic_chords_db (mode):
	if mode in tonic_chords_db: return tonic_chords_db[mode]
	chords = init_chords_db (mode.scale.key.chromatic)
	temp = [chord for chord in chords if tonic_chord (chord, mode)]
	tonic_chords_db[mode] = temp
	return temp

tonic_chord_inversions_db = {}
#@jit
def increasing (chord, chromatic):
	interval0 = chord[0]
	yield interval0
	for interval in chord[1:]:
		while interval < interval0: interval = interval + len (chromatic.ratios)
		interval0 = interval
		yield interval0
def chord_inversions (chord, chromatic):
	for permutation in permutations (chord): yield list (increasing (permutation, chromatic))
def init_tonic_chord_inversions_db (mode):
	if mode in tonic_chord_inversions_db: return tonic_chord_inversions_db[mode]
	tonic_chords = init_tonic_chords_db (mode)
	temp = []
	for chord in tonic_chords:
		t = list (chord_inversions (chord, mode.scale.key.chromatic))
		temp = temp + t
	tonic_chord_inversions_db[mode] = temp
	return temp

chord_root_db = {}
def init_chord_root_db (mode):
	if mode in chord_root_db: return chord_root_db[mode]
	chords = init_tonic_chord_inversions_db (mode)
	#temp = []
	temp = {}
	for root in mode.degrees ():
		temp_temp = []
		for chord in chords:
			root0 = chord[0]
			root0, octave = adjust (mode.scale.key.chromatic, root0)
			if root == root0: temp_temp = temp_temp + [chord]
		#temp = temp + [temp_temp]
		temp[root] = temp_temp
	chord_root_db[mode] = temp
	return temp
	
chord_function_db = {}
def init_chord_function_db (mode):
	if mode in chord_function_db: return chord_function_db[mode]
	chords = init_chord_root_db (mode)
	temp = []
	for function in range (0, 3):
		roots = [mode.degree (root) for root in range (0, len (mode.scale.intervals)) if mode.function (root) == function]
		temp_temp = [chords[root] for root in roots]
		temp = temp + [temp_temp]
	chord_function_db[mode] = temp
	return temp
	
perfect_consonance_db   = [0, 5, 7]
imperfect_consonance_db = [2, 3, 4, 8, 9, 10]
perfect_dissonance_db   = [1, 6, 11]
imperfect_dissonance_db = []
#@jit
def   perfect_consonance (interval): return interval in   perfect_consonance_db
#@jit
def imperfect_consonance (interval): return interval in imperfect_consonance_db
#@jit
def   perfect_dissonance (interval): return interval in   perfect_dissonance_db
#@jit
def imperfect_dissonance (interval): return interval in imperfect_dissonance_db
#@jit
def consonant (chord):
	for interval1 in chord:
		for interval2 in chord:
			interval = abs (interval2 - interval1)
			if imperfect_dissonance (interval) or perfect_dissonance (interval): return False
	return True
#@jit
def dissonant (chord):
	for interval1 in chord:
		for interval2 in chord:
			interval = abs (interval2 - interval1)
			if imperfect_dissonance (interval) or   perfect_dissonance (interval): return True
	return False

consonant_chord_db = {}
dissonant_chord_db = {}
def init_consonant_chord_db (mode):
	if mode in consonant_chord_db: return consonant_chord_db[mode]
	chords  = init_chord_function_db (mode)
	chords0 = chords[0]
	chords0 = chain (*chords0)
	temp    = [chord for chord in chords0 if consonant (chord)]
	consonant_chord_db[mode] = temp
	return temp
def init_dissonant_chord_db (mode):
	if mode in dissonant_chord_db: return dissonant_chord_db[mode]
	chords  = init_chord_function_db (mode)
	chords0 = chords[0]
	chords0 = chain (*chords0)
	chords0 = [chord for chord in chords0 if dissonant (chord)]
	temp    = chords0 + chords[1] + chords[2]
	dissonant_chord_db[mode] = temp
	return temp
	
# TODO parallel  key+mode
# TODO relative  key+mode
# TODO chromatic key
# TODO negative  key+mode
# TODO secondary key+mode <= relative+parallel

# TODO modulations

# TODO borrow from parallel  key+mode
# TODO borrow from chromatic key
# TODO borrow from secondary key+mode

# TODO voice leading




#def chords (root, chromatic):
#	for chord0 in chords_db:
#		for root2 in range (0, len (chromatic.ratios)):
#			chord = [root2 + note for note in chord0]				
#			if root not in chord: continue
#			chord.remove (root)
#			for permutation in permutations (chord):
#				intervals = [root] + permutation
#				yield increasing (intervals)
#class Chord:
#	def __init__ (self, intervals, root):
#		self.intervals = intervals
#		self.root      = root
# TODO
#def random_chord (): pass
		
		
def random_mode (scale=None, key=None, chromatic=None, solfeggio=None, lower_tetrachord=None, upper_tetrachord=None):
	if not scale: scale = random_scale (key, chromatic, solfeggio, lower_tetrachord, upper_tetrachord)
	mode = random_index (scale.intervals)
	return Mode (scale, mode)

if __name__ == "__main__":
	def main ():
		mode = random_mode ()
		print (mode)
		for degree in mode.degrees (): print (degree)
		#tonic_chords = init_chord_root_db (mode)
		#tonic_chords = init_chord_function_db (mode)
		#for tonic_chord in tonic_chords: print (tonic_chord)
		consonant_chords = init_consonant_chord_db (mode)
		dissonant_chords = init_dissonant_chord_db (mode)
		for chord in consonant_chords: print (chord)
		print ()
		for chord in dissonant_chords: print (chord)
		print ()
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 12):
			temp_mode = mode
			mode, doctave = mode.increment_key ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ()
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 12):
			temp_mode = mode
			mode, doctave = mode.decrement_key ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ("\n\n")
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.increment_scale ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ()
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.decrement_scale ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ("\n\n")
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.increment ()
			print (mode)
			assert temp_mode.mode != mode.mode
		#assert old_mode == mode
		print ()
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.decrement ()
			print (mode)
			assert temp_mode.mode != mode.mode
		#assert old_mode == mode
		print ("\n\n")
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 12):
			temp_mode = mode
			mode, doctave = mode.brighter_key ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ()
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 12):
			temp_mode = mode
			mode, doctave = mode.darker_key ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ("\n\n")
		
		
		"""
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.brighter_scale ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ()
		
		old_mode = mode
		print (mode)
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.darker_scale ()
			print (mode)
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ("\n\n")
		"""
		
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.brighter ()
			print (mode)
			assert temp_mode.mode != mode.mode
		#assert old_mode == mode
		print ()
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.darker ()
			print (mode)
			assert temp_mode.mode != mode.mode
		#assert old_mode == mode
		print ("\n\n")
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.parallel_mode_brighter ()
			print (mode)
			assert temp_mode.mode != mode.mode
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ()
		
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.parallel_mode_darker ()
			print (mode)
			assert temp_mode.mode != mode.mode
			assert temp_mode.scale.key.key != mode.scale.key.key
		#assert old_mode == mode
		print ("\n\n")
		"""
		old_mode = mode
		print (mode)
		print ()
		for _ in range (0, 7):
			temp_mode = mode
			mode, doctave = mode.increment ()
			print (mode)
			assert temp_mode.mode != mode.mode
			
			temp_mode = mode
			mode, doctave = mode.invert_mode1 ()
			#mode = mode.invert_mode1 ()
			print (mode)
		print ("\n\n")
			"""
		#assert old_mode == mode
		print ()
		
	main ()
