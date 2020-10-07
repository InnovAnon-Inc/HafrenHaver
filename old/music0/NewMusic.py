# rhythm scale
# phi scale
# just scale
# equal scale
# unit circle scale

#base*(base + 7.83)
#base**2 + 7.83*base
#base**

#scale
#- key
#  - chords
#  - chord progression

from math import *

from Harmonic import *

pythagorean_scale = Harmonic.pythagorean_scale

# solfeggio to tempo
"""
for p in [147, 174, 471, 417, 714, 741, 285, 258, 852, 825, 528, 582, 396, 369, 639, 693, 963, 936]:
	print "p=",p
	for n in xrange (0, 17):
		k=pow (2, (n - log (p) / log (2)))
		#assert 2 ** n == p * k
		if k >= .5 and k <= 2:
			print "k=",k
		elif k > 2: break
"""

# tempo to brainwave

keys = {}
keys["traditional"] = 7

chords = {}
chords["triad"] = 5

progressions = {}
progressions["standard"] = 11

class Scale:
	def __init__ (self, ratios): self.ratios = ratios
	def __len__ (self): return len (self.ratios)
	def apply (self, baseFreq): return list ([baseFreq * r for r in self.ratios])

class Key:
	def __init__ (self, scaleLen, keyType):
		self.length = keyType
		#self.seq = ? (scaleLen, keyType)
	def __len__ (self): return self.length
	def apply (self, scale): return list ([scale[s] for s in self.seq])

class Chord:
	def __init__ (self, keyLen, chordType):
		self.length = chordType
		#self.seq = ? (keyLen, chordType)
	def __len__ (self): return self.length
	def apply (self, key): return list ([key[s] for s in self.seq])

class Progression:
	def __init__ (self, keyLen, progType):
		self.length = progType
		#self.seq = ? (keyLen, progType)
	def __len__ (self): return self.length
	def apply (self, key): return list ([key[s] for s in self.seq])

class Melody:
	def __init__ (self, chordLen, melodyType):
		self.length = melodyType
		#self.seq = ? (chordLen, progType)
	def __len__ (self): return self.length
	def apply (self, key): return list ([key[s] for s in self.seq])

class Measure:
	def __init__ (self, a, b):
		self.length = lcm (a, b)
		#self.seq = ? (a, b)
	def __len__ (self): return self.length

#scale = Scale (equal_temperament_scale (12))
scale = Scale (pythagorean_scale)
key   = Key (len (scale), keys["traditional"]) # TODO vary
chord = Chord (len (key), chords["triad"])
prog  = Progression (len (key), progressions["standard"]) # TODO vary

clScale = Scale (list (xrange (3, len (key) - 2)))
clKey   = Key (len (clScale), 2) # TODO vary
clProg  = Progression (len (clKey), 17) # TODO vary

melodyType = {}
melodyType[3] = 7
melodyType[4] = 9
melodyType[5] = 6
for cl in clKey:
	melody[cl] = Melody (cl, melodyType[cl])

measure = Measure (8, 5) # arbitrary

rScale = Scale (equal_rhythms_scale (10))
rKey   = Key (len (rScale), 7) # arbitrary
rChord = Chord (len (rKey), 3) # arbitrary
rProg  = Progression (len (rKey), 13) # arbitrary

rclScale = Scale (list (xrange (3, len (rKey) - 2)))
rclKey   = Key (len (rclScale), 2) # TODO vary
rclProg  = Progression (len (rclKey), 17) # TODO vary

rMelodyType = {}
rMelodyType[3] = 4
rMelodyType[4] = 5
rMelodyType[5] = 6
for rcl in rclKey:
	rMelody[rcl] = Melody (rcl, rMelodyType[rcl])

# pitch, rhythm, volume, 

# effects:
# - long notes: phasing
# - else: binaural/monaural