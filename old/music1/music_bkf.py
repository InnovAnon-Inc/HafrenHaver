from __future__ import division
from collections import *
from fractions import *
from functools import *
from itertools import *
from math import *
from operator import mul
from random import *
from time import sleep

from graphics import *
from play_chord import *

def pitches (freqs, base):
	return [base * freq for freq in freqs]

def harmonics (n):
	return [1 / (harmonic + 1) for harmonic in xrange (n)]
def harmonics2 (n):
	return set (harmonics20 (n) + harmonics21 (n))
def harmonics2all (n):
	return set (harmonics20 (n) + harmonics21 (n) + harmonics22 (n))
def harmonics20 (n):
	return [(harmonic + 1) / (harmonic + 2) for harmonic in xrange (n)]
def harmonics21 (n):
	return [(harmonic + 2) / (harmonic + 1) for harmonic in xrange (n)]
def harmonics22 (n):
	return [(n - harmonic) / (harmonic + 2) for harmonic in xrange (n)]
def harmonics3 (n):
	return [harmonic + 1 for harmonic in xrange (n)]
def scale4 (ns):
	return set(
		[n / n + m for n in ns for m in ns] +
		[m / n + m for n in ns for m in ns])
def harmonics4inv (n):
	return [(k + 1) * (1 / n) for k in xrange (n)]
def harmonics4inv2 (n):
	return [n / (1 + k) for k in xrange (n)]
def harmonics4 (n):
	return [k + 1 for k in xrange (n)]
def scale1 (n, m):
	return set ([(num + 1) / (den + 1) for num in xrange (n) for den in xrange (m)])
def scale2 (ns):
	#ns = {}
	#ns[2] = 20
	#ns[3] = 10
	#ns[5] =  5
	
	# every combination of every prime factor
	# by the same
	
	combos = []
	for key, value in ns:
		combos.extend ([key] * value)
	#print combos
	perms = []
	for i in xrange (len (combos)):
		perms.extend ([
			reduce (mul, p) for p in permutations (combos, i + 1)])
	perms = set (perms)
	#print perms
	return set ([p1 / p2 for p1 in perms for p2 in perms])
def scale3 (ns, E):
	perms = []
	for n in ns:
		perms.extend ([pow (n, e + 1) for e in xrange (E)])
	return set (perms)

indian_scale1 = [
	1/1, 9/8, 5/4, 4/3,
	3/2, 5/3, 15/8, 2/1]
just_scale = [
	1/1, 9/8, 5/4,
	3/2, 7/4, 2/1]
indian_scale2 = [
	1/1, 256/243, 16/15, 10/9,
	9/8, 32/27, 6/5, 5/4, 81/64, 4/3, 27/20]
pythagorean_scale = [
	1/1, 256/243, 9/8, 32/27,
	81/64, 4/3, 729/512, 3/2,
	128/81, 27/16, 16/9, 243/128, 2/1]

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
#	for e in q:
#		leaf = generatef3 (e[0], e[1], p)
#		todo.extend (generate_coprime_pairs_leaves (leaf, p))
#	return todo
def generate_coprime_pairs_leaf (m, n, p):
	return [k for k in [
		(2 * m - n, m),
		(2 * m + n, m),
		(m + 2 * n, n)]
		if k[0] <= p]
	"""leaf = []
	for k in [
		(2 * m - n, m),
		(2 * m + n, m),
		(m + 2 * n, n)]:
		if k[0] <= p:
			leaf.append (k)
	return leaf"""

#base = 100
"""print pitches (harmonics (10), base)
print pitches (scale1 (10, 10), base)
print pitches (indian_scale1, base)
print pitches (just_scale, base)
print pitches (indian_scale2, base)
print pitches (pythagorean_scale, base)"""
"""
print pitches (harmonics20 (10), base)
print pitches (harmonics21 (10), base)
print pitches (harmonics22 (10), base)
print harmonics2 (10)
print pitches (harmonics2 (10), base)
"""
"""
print pitches (scale2 ({(2, 2), (3, 2), (5, 2)}), base)
print pitches (scale2 ({(2, 3), (3, 2), (5, 1), (7, 1)}), base)
print pitches (scale2 ({(2, 1), (3, 1), (5, 1), (8, 1), (13, 1)}), base)
print pitches (scale2 ({(2, 20), (3, 20)}), base)
"""
"""
print scale2 ([(b, 1) for b in harmonics2all (1)])
print scale2 ([(b, 1) for b in harmonics2all (2)])
print scale2 ([(b, 1) for b in harmonics2all (3)])
print scale2 ([(b, 1) for b in harmonics2 (4)])
"""
"""
print scale2 ([(b, 2) for b in harmonics2all (1)])
print scale2 ([(b, 2) for b in harmonics2all (2)])
print scale2 ([(b, 2) for b in harmonics2all (3)])
print scale2 ([(b, 2) for b in harmonics2 (4)])
"""
"""
for p in xrange (3):
	for k in xrange (6):
		print sorted (scale3 (harmonics2 (k + 1), p + 1))
"""
"""
for p in xrange (3):
	for k in xrange (6):
		print sorted (scale3 (harmonics2all (k + 1), p + 1))
"""
"""
print pitches (scale2 ([(b, 1) for b in harmonics2 (3)]), base)
print pitches (scale2 ([(b, 2) for b in harmonics2 (3)]), base)
print pitches (scale2 ([(b, 1) for b in harmonics2 (4)]), base)
print pitches (scale2 ([(b, 2) for b in harmonics2 (4)]), base)
"""
"""
print pitches (sorted (scale3 ([(1 + pow (5, .5)) / 2], 6)), base)
print pitches (sorted (scale3 ([
	2/3, 3/2,
	4/5, 5/4,
	4/7, 7/4,
	5/7, 7/5,
	8/9, 9/8,
	9/10, 10/9], 3)), base)
"""
"""
print pitches (sorted (scale3 (harmonics21 (10), 1)), 100)
print pitches (sorted (scale4 (harmonics3 (4))), 100)
print pitches (sorted (harmonics4inv2 (8)), 100)
"""

"""
pick melody from "chord"
chord progression based on that
melody notes based on chords within chord progression

pick number of measures
divide that by a sequence. i.e., 2+3+2 2+3+2
generate rhythm that repeats

melody should repeat... follow A A B A song structure?

melody generating helper functions: scales + arpeggios + repetition + alternating

left hand:  | a b a a  | a b a a  |
right hand: |  c c c b |  c c c b |
third hand: |  12 1  3    12 1  3
1: |a-c|
2: |b-c|
3: |a-b|
simple repetition + alternating, trinary scale, two parts, one part is rotated by a couple notes

legato, staccato, crescendo, descendo, ritard

different musicians can play at different tempos

modulation: key siggy changes, even mid-measure

cell:
2-3 notes + rhythm + accent
^^^ a couple times => phrase (e.g., 2-3 measures)

should have intra-cell modulation?

AABA or AABB phrases => verse (e.g., 12 bar blues)

AABA or AABB verses or ABACABA or AA1BA2CA3BA4 or ABABCB => song

song + variations => song cycle ?

sections:
intro, verse, pre-chorus, chorus/refrain, bridge, outro/coda
exposition, recapitulation, conclusion, interlude

sequence:
2-4 segments
usually in one direction (e.g., going higher or lower in pitch)
continue by same interval distance

figure/motif/cell => phrase => melody/period/section

phrase ~ 4 bars
period ~ 2-4 phrases

riff vs fill
riff: often repeated
fill: played between riffs
- can be standard motifs
- can be improv'd

transformations:
- retrograde: reverse melody and/or rhythm
- transposition
- inversion?
- multiplication?

melodic motion:
- ascending
- descending
- undulating/pendulum
- tile/terrace/cascading
- rise or musical plateau

modal frame:
- floor note
- ceiling note
- central note
- upper/lower focus (i.e., skew)
"""

"""
tempo_changes["rallentando"] = gradually slowing down
tempo_changes["ritardando"] = gradually slowing down (but not as much)
tempo_changes["ritenuto"] = immediately slowing down
tempo_changes["stringendo"] = gradually speeding up (slowly)
tempo_changes["accelerando"] = gradually speeding up (quickly)

tempo_changes["allargando"] = growing broader, decreasing tempo
tempo_changes["calando"] = going slower (and usually softer)
tempo_changes["doppio movimento"] = double speed
tempo_changes["doppio piu mosso"] = double speed
tempo_changes["doppio piu lento"] = half speed
tempo_changes["lentando"] = gradual slowing and softer
tempo_changes["meno mosso"] = less movement or slower
tempo_changes["mosso"] = movement, more lively or quicker... less extreme than piu mosso
tempo_changes["piu mosso"] = more movement or faster
tempo_changes["precipitando"] = hurrying, going faster/forward
tempo_changes["rubato"] = free adjustment of tempo
tempo_changes["stretto"] = faster tempo
tempo_changes["tardando"] = slowing down gradually
"""

#euclid for rhythm pattern
#select number of notes in scale
#euclid for choosing arpeggio notes
####scale is alphabet
####create conditional probability table for bigrams (or variable length sequences)
####sequences of letters, sequence of words, sequences of sentences

# common patterns:
# fibonacci
# euclid
# alternating
# increasing/decreasing
# peaks/valleys
# cascade
# +k  (mod m)
# *k  (mod m)
# **k (mod m)
# railfence & other transposition ciphers

# how to measure entropy of music?
# keep track of current entropy level and previously played sequences
# re-use previously played sequences in order to moderate entropy
# track entropy of phrase, verse, song, etc

# other channels must track which frequencies are being played at which times
#    and remove dissonant frequencies from the scale when generating their melodies

# types of notes:
# rest
# whole (measure)
# dotted half
# half triplet
# half
# triplet
# dotted quarter
# quarter (1 beat)
# dotted eighth
# eighth
# dotted sixteenth
# sixteenth

# music divided into measures
# ...with repeats and other structure
# songs usually have a standard number of measures?
# measures divided into beats

# rhythm
# alternation, repetition, strong vs. weak beats, beats vs. rest
# predictable rhythm, possible syncopation

# melody = pitch + duration + rhythm

# time siggys - simple, compound, complex, mixed, additive, fractional, irrational

def list_to_number (l):
	s = 0
	for k in xrange (len (l)):
		s += l[k] * (10 ** (len (l) - k - 1))
	return s
def solfeggios ():
	for seq in [
		[1, 4, 7],
		[5, 2, 8],
		[3, 6, 9]]:
		for perm in permutations (seq):
			yield list_to_number (perm)
#print sorted (chain (solfeggios ()))

#hs = [harmonic + 1 for harmonic in xrange (10)]
#hs = [harmonic + 1 for harmonic in xrange (6)]
#hs = [1] + sorted ([(h + 1) / h for h in hs])
#hs = sorted ([(h + 1) / h for h in hs])
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
#for h in xrange (len (hs)):
	#for k in xrange (h):
		#for p in euclid (h, k, hs):
		#	print p
		#print "euclid (", hs[h], ",", hs[k], ")=", euclid (h, k, list (hs))
#l = []
#map (l.extend, [euclid (h, k, list (hs)) for h in xrange (len (hs)) for k in xrange (h)])
#l = sorted (set (l))		

audible_range = (20, 20000)
binaural_range = (20, 1500)
binaural_diff = (0, 40)

tempo = {}
tempo["larghissimo"] = (0, 24) # 1 ?
tempo["grave"] = (25, 45)
tempo["largo"] = (40, 60)
tempo["lento"] = (45, 60)
tempo["larghetto"] = (60, 66)
tempo["adagio"] = (66, 76)
tempo["adagietto"] = (72, 76)
tempo["andante"] = (76, 108)
tempo["andantino"] = (80, 108)
tempo["marcia moderato"] = (83, 85)
tempo["andante moderato"] = (92, 112)
tempo["moderato"] = (102, 120)
tempo["allegretto"] = (112, 120)
tempo["allegro moderato"] = (116, 120)
tempo["allegro"] = (120, 168)
tempo["vivace"] = (168, 176)
tempo["vivacissimo"] = (172, 176)
tempo["allegrissimo"] = (172, 176)
tempo["allegro vivace"] = (172, 176)
tempo["presto"] = (168, 200)
reasonable_max_tempo = 380
tempo["prestissimo"] = (200, reasonable_max_tempo)

# when notes are long enough to play offset notes or frequencies:
brainwaves = {}
brainwaves["gamma"] = (30, 50) # (40, 100)
brainwaves["beta"] = (14, 30) # (12, 40)
brainwaves["smr"] = (12.5, 15.5)
brainwaves["alpha"] = (8, 14) # (8, 12)
brainwaves["sigma"] = (12, 14)
brainwaves["mu"] = (8, 12)
brainwaves["theta"] = (4, 8) # (4, 8)
brainwaves["delta"] = (.1, 4) # (1, 4)
brainwaves["epsilon"] = (0, .1) # (0, 1)

"""
11100000
10 10 10 00
100 100 10
100 10 100 ?

abcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg
100101001001010010010100100101001001010010010100100101001001010010010100
a  d f  b  e g  c  f a  d  g b  e  a c  f  b d  g  c e  a  d f  b  e g
adfbegcfadgbeacfbdgce adfbeg

22222 10010100
21 20 20 21 20 100 ?
211 200 200 21 20
211 21 200 20 200

22222 10 01 01 00
2 10 2 01 2 01 2 00 2

2112 1200 2020 0 3333
2113 2123 0023 0
21123 12203 20203

111110000000
10 10 10 10 10 00
100 100 10 10 10
100 10 100 10 10

111112222333
12 12 12 12 13 33
123 123 12 12 13
123 12 123 12 13
123 12 13 123 12 ?

111111111111 00000000
01 01 01 01 01 01 01 01 1111
011 011 011 011 01 01 01 01
011 01 011 01 011 01 011 01

111222333444 55667788
51 51 61 62 72 72 83 83 3444
513 514 614 624 72 72 83 83
513 72 514 72 614 83 624 83 ?
"""

ranges = ["low", "med", "hi"]
chakras = ["red", "orange", "yellow", "green", "blue", "purple"]

solfeggio = {}
solfeggio["low", "red"] = 174
solfeggio["low", "orange"] = 147
solfeggio["low", "yellow"] = 285
solfeggio["low", "green"] = 369
solfeggio["low", "blue"] = 396
solfeggio["low", "purple"] = 258
solfeggio["med", "red"] = 417
solfeggio["med", "orange"] = 471
solfeggio["med", "yellow"] = 528
solfeggio["med", "green"] = 693
solfeggio["med", "blue"] = 639
solfeggio["med", "purple"] = 582
solfeggio["hi", "red"] = 741
solfeggio["hi", "orange"] = 714
solfeggio["hi", "yellow"] = 852
solfeggio["hi", "green"] = 936
solfeggio["hi", "blue"] = 963
solfeggio["hi", "purple"] = 825

def play (base, note):
	return int (round (base * note))
def chrang (chakra, rang):
	return solfeggio[rang, chakra]
def melody (scale):
	length = len (scale)
	return melody2 (length * length, scale)
def melody2 (length, scale):
	return [scale[randint (0, len (scale) - 1)] for _ in xrange (length)]

class Bjorklund:
	"""
	lengthOfSeq = -1
	pulseAmt = -1
	
	remainder = []
	count = []
	sequence = deque ()
	"""
	def __init__ (self, lengthOfSeq, pulseAmt):
		self.lengthOfSeq = lengthOfSeq
		self.pulseAmt = pulseAmt
		
		self.remainder = []
		self.count = []
		self.sequence = deque ()

	def buildSeq (self, slot):
		#lengthOfSeq = self.lengthOfSeq
		#pulseAmt = self.pulseAmt
		
		#remainder = self.remainder
		#count = self.count
		#sequence = self.sequence
		
		#print "buildSeq (", slot, sequence, ")"
		
		if slot is -1:
			self.sequence.append (0)
			#print "sequence=", sequence
		elif slot is -2:
			self.sequence.append (1)
			#print "sequence=", sequence
		else:
			i = 0
			while i < self.count[slot]:
				self.buildSeq (slot - 1)
				#print "sequence=", sequence
				i += 1
			if self.remainder[slot] is not 0:
				self.buildSeq (slot - 2)
				#print "sequence=", sequence
			#else:
			#	self.buildSeq (slot - 3)
			#	print "SEQUENCE=", sequence
		
	def bjorklund (self):
		#lengthOfSeq = self.lengthOfSeq
		#pulseAmt = self.pulseAmt
		
		#remainder = self.remainder
		#count = self.count
		#sequence = self.sequence
		
		divisor = self.lengthOfSeq - self.pulseAmt
		if divisor < 0: raise Exception ()
		
		# TODO
		#if self.lengthOfSeq is 1:
		#	self.sequence = [self.pulseAmt]
		#	return
		#print self.lengthOfSeq, self.pulseAmt, self.remainder

		self.remainder.append (self.pulseAmt)
	
		index = 0
		# TODO verify correctness of if-statement
		#if remainder[index] > 1:
		if True:
			while True:
				self.count.append (floor (divisor / self.remainder[index]))
				self.remainder.append (divisor % self.remainder[index])
				divisor = self.remainder[index]
				index += 1
				if self.remainder[index] <= 1: break
				#if remainder[index] is 0: break
		self.count.append (divisor)
		#print "divisor=", divisor
		#print "count=", count
		#print "remainder=", remainder
		#count.reverse ()
		#remainder.reverse ()
		self.buildSeq (index)
		#print "sequence=", sequence
		self.sequence.reverse ()
		#print "sequence=", sequence
	
		zeroCount = 0
		if self.sequence[0] is not 1:
			zeroCount += 1
			while self.sequence[zeroCount] is 0:
				zeroCount += 1
			self.sequence.rotate (zeroCount)
	def rotate (self, amt):
		self.sequence.rotate (amt)

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

"""for a in xrange (8):
	b = Bjorklund (8, a + 1)
	b.bjorklund ()
	print b.sequence
b = Bjorklund (13, 5)
b.bjorklund ()
print b.sequence"""

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

scale_types = [None] * 13
scale_types[12] = ["chromatic"]
scale_types[8] = ["jazz", "modern classical"]
scale_types[7] = ["modern western"]
scale_types[6] = ["western folk"]
scale_types[5] = ["oriental folk"]
scale_types[4] = ["prehistoric"]
scale_types[3] = ["prehistoric"]
scale_types[2] = ["prehistoric"]
scale_types[1] = ["liturgy", "modern art"]
scale_types[0] = None

scale_modes = [None] * 7
scale_modes[0] = "Ionian"
scale_modes[1] = "Dorian"
scale_modes[2] = "Phrygian"
scale_modes[3] = "Lydian"
scale_modes[4] = "Mixolydian"
scale_modes[5] = "Aeolian"
scale_modes[6] = "Locrian"

def harmonics6 (n):
	for i in xrange (1, n + 1):
		for j in xrange (1, i):
			yield (i + j) / i
def harmonics7 (n):
	for h in set (harmonics6 (n)):
		hh = 1
		while hh * h < 2:
			hh *= h
			yield hh
def min_max_normalize (m, i, a):
	return 1 + (m - i) / (a - i)



#display_scale (pitches ([1] + list (equal_temperament_scale (12)), 440))
"""
k = sorted ([min_max_normalize (m, 147, 963) for m in solfeggios ()])
print k
display_scale (pitches (k, 1))
"""
#h = list (harmonics5 (10))
#h2 = h.index (2)
#for i in xrange (len (h)):
#	if i != h2:
#		display_scale ([1] + euclid (h2, i, h))





#select_number_of_channels ()
# ^^^ includes harmonies/chords, other rhythms, other tempos
# select_brainwave_freq () ?
#select_tempo ()
#select_key_siggy ()
#select_time_siggy ()
#select_base_freq ()
#select_scale ()

#select_song_structure ()
#select_verse_structures ()
#select_phrase_structures ()
#select_cells ()

#choose time siggy: number of beats per 2-4 bars
#choose number of beats to go into bar of that length
#^^^ => phrase structure... need number of phrases... 2-4?... multiple types?
#^^^ => verse structure... need number of verses... 2-8?... multiple types
# chord progression?

"""
cps = generate_coprime_pairs (16)
#print cps
cp = choice (list (cps))
print cp
"""

#phrase = cp[0] * cp[1]
#print phrase
"""
b = Bjorklund (cp[0], cp[1])
b.bjorklund ()
print b.sequence
display_bjorklund (b.sequence)
"""

#display_scale (pitches ([1] + list (equal_temperament_scale (12)), 440))
#display_scale ([1] + list (harmonics5 (12)))
#sleep (30)
#exit

#b = Bjorklund (12, 7)
#b.bjorklund ()
#print b.sequence
#display_bjorklund (b.sequence)
#sleep (30)
#exit

#b = Bjorklund (8, 5)
#b.bjorklund ()
#print b.sequence
#display_bjorklund (b.sequence)
#sleep (30)
#exit

"""
for k in xrange (2, 10):
	s = sorted ([1] + list (set (harmonics7 (k))))
	print len (s)
	for v in [4, 6, 8, 12, 20]:
		if v > len (s): continue
		b = Bjorklund (len (s), v)
		b.bjorklund ()
		display_bjorklund_scale (s, b.sequence)
		sleep (2)
"""

def bjorklund_complete (n, p, r):
	b = Bjorklund (n, p)
	b.bjorklund ()
	s = b.sequence
	s.rotate (r)
	return s

class SongCycle:
	def __init__ (self, songs, pattern, mode):
		self.songs = songs
		self.seq = bjorklund_complete (len (songs), pattern, mode)
class Song:
	def __init__ (self, verses, pattern, mode):
		self.verses = verses
		self.seq = bjorklund_complete (len (verses), pattern, mode)
class Verse:
	def __init__ (self, phrases, pattern, mode):
		self.phrases = phrases
		self.seq = bjorklund_complete (len (phrases), pattern, mode)
class Phrase:
	def __init__ (self, cells, pattern, mode):
		self.cells = cells
		self.seq = bjorklund_complete (len (cells), pattern, mode)
		# need melody and "rhythm" for chord changes
class Cell:
	def __init__ (self,
		scale, key, mode,
		chord, chpattern, chmode,
		beats, pulses, bpmode):
		self.channels = 1
		self.scale = bjorklund_complete (len (scale), key, mode)
		self.chord = bjorklund_complete (key, chpattern, chmode)
		self.rhythm = bjorklund_complete (beats, pulses, bpmode)
		#TODO generate multi-order stochastic table ?
		
		# bass line         100 10 100 100 10 100
		# melody durations  3   2  3   3   2  3
		
		# hidden            10  10  100 10 10 10 10 100 10 10
		# beat pattern      1/2 1/2 1/3 1/2 ?
		
		# hidden            10 100 10 10 100 10
		# melody notes      1  3   3  2  1   1

		# hidden            100 10 100 10  100 100 10 100 10 100 100 10 100 10 100
		# number of bars    3   2  3   2   3   3   2  3   2  3   3   2  3   2  3
		# chord progression 1   4  5   1   4   5   1  4   5  1   4   5  1   4  5
		
		# hidden
		# ...some sort of rhythm of cell changes ?

# 100 10 100 100 10 100 100 10 100 100 10 100
# tff tf tff tff tf tff tff tf tff tff tf tff
# hlm hl mhl mhl mh lmh lmh lm hlm hlm hl mhl
# hhmmmlllhhhm
# now need durations

# ranges, chakras => base frequency

#0  5   10   15
#0 3 6 9  12 15

def lcm (a, b, r):
	return int (a * b / r)

def lcm_pair (a, b):
	r = gcd (a, b)
	m = lcm (a, b, r)
	#print a, b, r, m
	return (int (b / r), int (a / r), int (m / r))

class SkipIter:
	def __init__ (self, bjork, seq):
		(a, b, c) = lcm_pair (sum (bjork), len (seq))
		self.bjork = cycle (
			#repeat (
				bjork
			#, a)
		)
		self.seq = cycle (
			#repeat (
				seq
			#, b)
		)
		self.length = c
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		bj = self.bjork.next ()
		seq = self.seq.next ()
		if bj is 1: return seq
		return self.next ()
class SkipIter2:
	def __init__ (self, bjork, seq):
		self.length = sum (bjork)
		(a, b, c) = lcm_pair (self.length, len (seq))
		self.bjork = cycle (bjork)
		self.seq = cycle (seq)
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		bj = self.bjork.next ()
		seq = self.seq.next ()
		if bj is 1: return seq
		return self.next ()

#1001010010100 10010100101001001010010100
#1  3 2  3 2   3  3 2  3 2  3  3 2  3 2

class CountIter:
	def __init__ (self, bjork):
		#self.bjork = cycle (bjork)
		self.bjork = bjork.seq.__iter__ ()
		self.length = sum (bjork.seq)
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		count = 1
		while True:
			bj = self.bjork.next ()
			if bj is 1: return count
			count += 1
"""
class ChangeIter:
	def __init__ (self, bjork, seq):
		self.length = sum (bjork.seq)
		(a, b, c) = lcm_pair (self.length, len (seq))
		self.bjork = cycle (bjork)
		self.seq = cycle (seq)
		self.seq_cur = seq.next ()
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		bj = self.bjork.next ()
		ret = self.seq_cur
		if bj is 1: self.seq_cur = seq.next ()
		return ret
"""
class ZipIter:
	def __init__ (self, rangeIter, chakraIter, solfeggio):
		#print rangeIter
		#print chakraIter
		(a, b, c) = lcm_pair (len (rangeIter), len (chakraIter))
		#(a, b, c) = lcm_pair (rangeIter.length, chakraIter.length)
		self.rangeIter = cycle (
			#repeat (
				rangeIter
			#, a)
		)
		self.chakraIter = cycle (
			#repeat (
				chakraIter
			#, b)
		)
		self.solfeggio = solfeggio
		self.length = c
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		r = self.rangeIter.next ()
		c = self.chakraIter.next ()
		return self.solfeggio[r, c]

"""
class BeatChordIter:
	def __init__ (self, beats, chords

class Cell2:
	def __init__ (self, beats, rhythms, chords, chbeats):
		self.beats = beats
		self.rhythms = rhythms
		self.chords = chords
		self.chbeats = chbeats
		# get next beat(s)
		# get next chord, play for that many beats
		
		beat = self.beats.next ()
		chord = self.chords.next ()
		chbeat = self.chbeats.next ()
		
		next_beat = self.beats.next ()
		next_chord = self.chords.next ()
		next_chbeat = self.chbeats.next ()
		
		m = min (beat, chbeat)
		a = [chord] * m
		b = modulate (chord, next_chord) * (beat - i)
		c = [next_chord] * (chbeat - i)
		
		i = 0
		while i < beat and i < chbeat:
			#notes come from chord
		while i < beat:
			#notes come from modulate (chord, next_chord)
		while i < chbeat:
			#notes come from next_chord
		beat = next_beat
		chord = next_chord
		# play for beat * rhythm
		
		#10010100101001001010010100
		#  c  f g  c f  g  c f  g c
		
		#10101101101011011010110110
		#c f gc fg c fg cf g cf gc
		#  c  f g  c f  g  c f  g c

		#10010100101001001010010100
		#c f gc fg c fg cf g cf gc
		#c qfpccqg c qg pf g pf gp
		#111000000111000111000000111000111000
		#ccccccqqqfffpppccccccqqqggg
		#q=modulate(c,f)
		#p=modulate(c,g)
		
		#ccqfp ccqgg ccqgg pffgg pffgp

		#                          CFG CF GCF GCF GC FGC
		# periods of so many beats 323 23 323 323 23 323
		# divide each period by equal numbers 1/2 1/3 1/5
		# each subdivisions of the period will follow bjork pattern
"""

"""
class Cell3:
	def __init__ (self, beat, melody, rhythm, rests, volume):
		# repeat, variation, new
		# 3 beats, 1/5 rhythm, which beat*rhythms to skip
		self.beat = beat
		self.melody = melody
		self.rhythm = rhythm
		self.rests = rests
		self.volume = volume

		notes = [None] * lcm (rhythm, len (rests))
		note_duration = beat / rhythm
		for i in xrange (len (notes)):
			if not rests[i]:
				notes[i] = melody.next ()
"""

"""
class Bjorklund2 (Bjorklund):
	def __init__ (self, lengthOfSeq, pulseAmt, rotateAmt):
		Bjorklund.__init__ (self, lengthOfSeq, pulseAmt)
		#super (Bjorklund2.__class__, self).__init__ (lengthOfSeq, pulseAmt)
		self.bjorklund ()
		self.rotate (rotateAmt)
beatIter = CountIter (Bjorklund2 (13, 5, 0))
"""

class Bjorklund3:
	def __init__ (self, lengthOfSeq, pulseAmt, rotateAmt):
		bjork = Bjorklund (lengthOfSeq, pulseAmt)
		bjork.bjorklund ()
		bjork.rotate (rotateAmt)
		self.seq = bjork.sequence
		self.pulseAmt = pulseAmt
beatIter = CountIter (Bjorklund3 (13, 5, 0))

#maxRhythm = 5
#rhythms = sorted ([1] + list (set ([n / d
#	for d in xrange (1, maxRhythm)
#		for n in xrange (1, d)])))
rhythms = list (xrange (1, 10))
# TODO SkipIter should use amt relatively prime to len rhythms
#rhythmIter = SkipIter2 (Bjorklund3 (11, 3, 0).seq, rhythms)
#for k in rhythmIter: print k

rhythmIter = SkipIter2 (Bjorklund3 (len (rhythms), 3, 0).seq, rhythms)
#for k in rhythmIter: print k

class SyncopatIter:
	def __init__ (self, b):
		self.b = b
		a = list (xrange (1, b + 1))
		self.a = SkipIter2 (Bjorklund3 (len (a) + b, b, 0).seq, a)
	def __iter__ (self): return self
	def next (self):
		#return [self.a.next () for i in xrange (self.b)]
		ret = self.a.next ()
		return ret
class InterleavIter:
	def __init__ (self, interval, seq):
		self.interval = interval
		self.seq = Bjorklund3 (interval, seq, 0).seq
	def __iter__ (self): return self
	def next (self):
		return self.seq
class RhythmIter:
	def __init__ (self, ar):
		self.ar = ar
	def __iter__ (self): return self
	def next (self):
		r = self.ar.next ()
		return r, SyncopatIter (r)
rhythmIter2 = RhythmIter (rhythmIter)
"""
for r, k in rhythmIter2:
	j = 0
	for p in k:
		if j == 10: break
		j += 1
		interleavIter = InterleavIter (r, p)
		for i in xrange (5):
			print interleavIter.next ()
"""

# turns list seq into infinite cycle
class CyclIter:
	def __init__ (self, seq, length):
		self.itr = cycle (seq)
		self.length = length
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): return self.itr.next ()

"""
range iterator
chakra iterator
=> solfeggio (base freq) iterator

beat iterator

scale
key is subset of scale

noteNums length <= key length
noteNumKey is subset of noteNums

for each length in noteNumKey
	chord[length] is subset of key

rhythms
rhythmKey is subset of rhythms
rhythmProg[

silence[rhythm] is [0..rhythm]
silenceKey[rhythm] is subset of silence[rhythm]


fundyIter is subset of key
chords[noteNum] is subset of key
noteNumIter is subset of noteNumKey
rhythmIter is subset of rhythmKey
silenceIter[rhythm] is subset of rhythm

for each beat:
melodyIter[chord, noteNum, rhythm, silences] is subset of chords[noteNum] and has rhythm-silences notes
"""

class BjorklundChopper:
	def __init__ (self, bjork):
		g = gcd (len (bjork.seq), sum (bjork.seq))
		self.seq = list (bjork.seq)[:int (len (bjork.seq) / g)]
		print "c=",bjork.seq
		print "d=",self.seq
		# TODO idk wtf I'm doing
		#self.seq = list (chain.from_iterable (repeat (list (bjork.seq)[:int (len (bjork.seq) / g)], g)))
		self.length = len (bjork.seq)
	def __len__ (self): return self.length
# binary sequence bjork skips over seq

class SkipIter:
	# 00000 111
	# 01 01 01 00
	# 01 0 01 0 01
	# 01001001 01001001 01001001 01001001 01001001 | 01001001
	# abcdeabc deabcdea bcdeabcd eabcdeab cdeabcde | abcdeabc
	#  b  e  c  e  c  a  c  a  d  a  d  b  d  b  e |  b  e  c
	
	# abcdefab cdefabcd efabcdef abcdefab cdefabcd   efabcdef | abcdefab
	#  b  e  b  d  a  d  f  c  d  b  e  b  d  b  d    f  c  f |  b  e  b
	# bjork = subset (0, len (bjork) / gcd (len (bjork), sum (bjork)))
	# bjork repeats len(seq)/gcd   times
	# seq   repeats len(bjork)/gcd times
	# output is bjork.pulseAmt*len(seq)
	
	# 10010010 10010010 10010010 10010010 10010010
	# abcdefab cdefabcd efabcdef abcdefab cdefabcd
	# adacfcebe adacfc
	
	# 00001111
	# 01010101 01010101 01010101
	# abcabcab cabcabca bcabcabc
	#  b a c b  a c b a  c b a c
	# 01 01 01
	# ab ca bc
	#  b  a  c
	def __init__ (self, bjork, seq):
		#bjork = BjorklundChopper (bjork)
		#g = gcd (len (seq), len (bjork))
		g = gcd (len (seq), len (bjork.seq))
		self.bjork = chain.from_iterable (repeat (
			bjork.seq, int (len (seq)       / g)))
		self.seq   = chain.from_iterable (repeat (
			seq,       int (len (bjork.seq) / g)))
		self.length = int (sum (bjork.seq) * len (seq) / g)
		#print "e=",self.length
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		bj = self.bjork.next ()
		seq = self.seq.next ()
		if bj: return seq
		return self.next ()

# 111111100000
# 10 10 10 10 10 11
# 10 10 1 10 10 1 10
# ab cd e fg ab c de
class KeyIter:
	def __init__ (self, scale, scaleType, scaleMode):
		self.itr = SkipIter (Bjorklund3 (len (scale), scaleType, scaleMode), scale)
		self.length = len (self.itr)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		return self.itr.next ()
class ProgIter:
	def __init__ (self, key, blen, progType, progMode):
		self.itr = SkipIter (Bjorklund3 (blen, progType, progMode), key)
		self.length = len (self.itr)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		return self.itr.next ()

# 1 a 1.0
# 2 b 1.125
# 3 c 1.185185185
# 4 d 1.33333333333
# 5 e 1.5
# 6 f 1.58024691358
# 7 g 1.77777777777

#000000000111
#000100010001
#100010001000 100010001000 100010001000 100010001000 1
#abcdefgabcde fgabcdefgabc defgabcdefga bcdefgabcdef g
#a   e   b    f   c   g    d   a   e    b   f   c    g

#aebfcgd

#1000 1000 * 7
#abcd efga * 4

#0000 111

#1234567 1234567 1234567 1234567
#abcdefg abcdefg abcdefg abcdefg
#1000000 0001000 0000100 0000000
#979 979 979

#9+9=18=>20
#7+7=14=>16
#9+7=16=>18
#9+7+9=25=>28

#1001100
#abcdefg

# 1.0
# 1.33333
# 1.5

scaleType = 7
scaleMode = 0
scale = list (pythagorean_scale)
scale.remove (2)
#for k in KeyIter (scale, scaleType, scaleMode): print k
key = list (KeyIter (scale, scaleType, scaleMode))
progIter = list (ProgIter (xrange (len (key)), 29, 2, 0))

noteNums = list ([n for n in xrange (1, len (key))])
noteNumKey = list (KeyIter (noteNums, 5 % len (noteNums), 0))
noteNumProgIter = list (ProgIter (xrange (len (noteNumKey)), 41, 7, 0))

#chordIters = list ([list (KeyIter (xrange (len (key)), noteNum, 0)) for noteNum in noteNums])
#noteNumIter = list (SkipIter (Bjorklund3 (16, 5, 0), chordIters))
#for k in noteNumIter:
#	for p in k:
#		print p
#	print

chords = [None] * (max (noteNumKey) + 1)
for noteNum in noteNumKey:
	chords[noteNum] = list (
		KeyIter (xrange (len (key)), noteNum, 0))
def fundyChord (key, fundy, chord):
	return [key[(fundy + noteNum) % len (key)] for noteNum in chord]
#for b, p, n in zip (beatIter, progIter, noteNumProgIter):
#	print b, fundyChord (key, p, chords[noteNumKey[n]])
#sleep (5)

class ProdIter:
	def __init__ (self, progIter, noteNumIter):
		g = gcd (len (progIter), len (noteNumIter))
		self.progIter = chain.from_iterable (repeat (
			progIter, int (len (noteNumIter) / g)))
		self.noteNumIter = chain.from_iterable (repeat (
			noteNumIter, int (len (progIter) / g)))
		self.length = int (len (progIter) * len (noteNumIter) / g)
		#self.seq = zip (self.progIter, self.noteNumIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		#return self.seq.next ()
		return (self.progIter.next (), self.noteNumIter.next ())
class ChordIter:
	def __init__ (self, prodIter, key):
		self.prodIter = prodIter
		self.key = key
		self.length = len (prodIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		fundy, noteNums = self.prodIter.next ()
		return [key[(fundy + noteNum) % len (key)] for noteNum in noteNums]

#for k in ProdIter (progIter, noteNumIter): print k
#for k in ChordIter (ProdIter (progIter, noteNumIter), key): print k

chordProgression = list (ProdIter (progIter, noteNumProgIter))
#for (b, (p, n)) in zip (beatIter, chordProgression):
#	print b, fundyChord (key, p, chords[noteNumKey[n]])

class BaseFreqIter:
	def __init__ (self, rangeIter, chakraIter, solfeggios):
		self.prodIter = ProdIter (rangeIter, chakraIter)
		self.solfeggios = solfeggios
	def __len__ (self): return len (self.prodIter)
	def __iter__ (self): return self
	def next (self): return self.solfeggios[self.prodIter.next ()]

rangeIter = SkipIter (Bjorklund3 (10, 9, 0), ranges)
chakraIter = SkipIter (Bjorklund3 (15, 13, 0), chakras)
#for k in BaseFreqIter (rangeIter, chakraIter, solfeggio): print k

rhythmScale = list (xrange (1, 10))
rhythmScaleType = 5
rhythmKey = list (KeyIter (rhythmScale, rhythmScaleType, 0))
rhythmProgIter = list (ProgIter (xrange (len (rhythmKey)), 37, 5, 0))

rhythmNoteNums = list ([n for n in xrange (1, len (rhythmKey))])
#rhythmChordIters = list ([list (KeyIter (xrange (len (rhythmKey)), noteNum, 0)) for noteNum in rhythmNoteNums])
#rhythmNoteNumIter = list (SkipIter (Bjorklund3 (16, 5, 0), rhythmChordIters))

#rhythmNoteNums =
rhythmNoteNumKey = list (KeyIter (rhythmNoteNums, 7 - len (rhythmNoteNums), 0))
rhythmNoteNumProgIter = list (ProgIter (xrange (len (rhythmNoteNumKey)), 31, 3, 0))

rhythmChords = [None] * (max (rhythmNoteNumKey) + 1)
for noteNum in rhythmNoteNumKey:
	rhythmChords[noteNum] = list (
		KeyIter (xrange (len (rhythmKey)), noteNum, 0))
rhythmChordProgression = list (ProdIter (rhythmProgIter, rhythmNoteNumProgIter))
#for b, p, n in zip (beatIter, rhythmProgIter, rhythmNoteNumProgIter):
#for (b, (p, n)) in zip (beatIter, rhythmChordProgression):
#	print b, fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])
#sleep (5)

# shits on Bj[x,0,z]
#for k in xrange (8 + 1):
#	print Bjorklund3 (8, 8 - k, 0).seq
#print "TEST"
#print "a=",list (Bjorklund3 (8, 8, 0).seq)
#print "b=",list (SkipIter (Bjorklund3 (8, 8, 0), xrange (1,9)))
#print "END TEST"

#silenceBjork
#melodyBjork
#(melodyChord,chord)
#sort and iter rhythms
#   iter silencebjork
#      note = skiperator
#      if silence: continue
#      if melodybjork.next
#        note

silProgs = [None] * (max (rhythmKey) + 1)
#rs = [None] * (max (rhythmKey) + 1)
melodies = [None] * (max (rhythmKey) + 1)
#for k in xrange (1, max (rhythmKey) + 1):
#	melodies[k] = list (SkipIter (Bjorklund3 (max (noteNum, rhythmKey[k]), min (rhythmKey[k], noteNum), 0), chords[noteNum]))
	#print melodies[k]
for rhythm in rhythmKey:
	silScale = list (xrange (1, rhythm + 1)) #[0, rhythm]
	silScaleType = 5
	silScaleType = min (silScaleType, len (silScale))
	silScaleType = max (silScaleType, 1)
	# TODO maybe don't use subset:
	silKey = list (KeyIter (silScale, silScaleType, 0))
	silProgIter = list (ProgIter (xrange (len (silKey)), 29, 2, 0))
	silProgs[rhythm] = silProgIter
	"""
	print ("rhythm=",rhythm,
		"silScale=",list (silScale),
		"silScaleType=",silScaleType,
		"silKey=",list (silKey))
	"""
	#print len (list (SkipIter (Bjorklund3 (len (silScale), silScaleType, 0), silScale)))
	
	"""rs[rhythm] = [None] * (max (silKey) + 1)
	melodies[rhythm] = [None] * (max (silKey) + 1)
	for sil in silKey:
		rs[rhythm][sil] = Bjorklund3 (rhythm, sil, 0).seq

		melodies[rhythm][sil] = [None] * (max (noteNumKey) + 1)
		for noteNum in noteNumKey:
			melodies[rhythm][sil][noteNum] = list (SkipIter (Bjorklund3 (max (noteNum, rhythm), min (rhythm, noteNum), 0), chords[noteNum]))
			#print melodies[rhythm][sil][noteNum]
	"""
#for b, p, n in zip (beatIter, rhythmProgIter, rhythmNoteNumProgIter):
#	print b, fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])
#sleep (5)

# TODO replace rhythmProgIter with silProgIter
# ... foreach rhythm
#             /|\
#             0sil 1sil 2sil... rhythmsil
# rhythmProg * silences
#rhythmProgression = list (ProdIter (rhythmProgIter, rhythmNoteNumProgIter))
print "rhythmProgression=",rhythmChordProgression

##### 

#class BeatChordIter:
#	def __init__ (self, rhythmChordProgression):
#		self.seq = rhythmChordProgression
#		self.__len__ = 
#beatChordProgression = list ([sorted ([(k/r, 1/r) for r in rhythmChord for k in xrange (r)]) for rhythmChord in rhythmChordProgression])

chordProgression = list (ProdIter (progIter, noteNumProgIter))
# noteNum * rhythm-silence => arpeggio
print "chordProgression=", chordProgression

#print list (rhythmProgression)












#for p, n in chordProgression:
#	print fundyChord (key, p, chords[noteNumKey[n]])
#for p, n in rhythmChordProgression:
#	print fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])

class ChangeIterHelper:
	def __init__ (self, bjork, seq):
		self.length = len (bjork.seq)
		#assert sum (seq) == self.length
		self.bjork = CountIter (bjork)
		self.seq = seq.__iter__ ()
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): return [self.seq.next ()] * self.bjork.next ()
class ChangeIter:
	def __init__ (self, bjork, seq):
		helper = ChangeIterHelper (bjork, seq)
		self.length = len (helper)
		self.seq = chain.from_iterable (helper)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): return self.seq.next ()

#print list (CountIter (Bjorklund3 (7, 5, 0)))
#print "PISS=",list (CountIter (Bjorklund3 (7, 5, 0)))
#print len (ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5))))
#for k in ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5))):
#	print k
#print ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5)))
#print "SHIT=",list (ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5))))
#i = list (ChangeIter (Bjorklund3 (b, c, 0), chord))
#print "ASDFASDF"
#sleep (5)

def rhythmToBeat (r):
	for k in xrange (r):
		yield k/r
def rhythmChordToBeatChord (rc):
	return sorted (list (set (chain.from_iterable ([rhythmToBeat (r) for r in rc]))))
beatChordProgression = list ([rhythmChordToBeatChord (fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])) for p, n in rhythmChordProgression])
fundChordProgression = list ([fundyChord (key, p, chords[noteNumKey[n]]) for p, n in chordProgression])
#print fundChordProgression
#for bc in beatChordProgression: print bc

class BeatChordIterHelper:
	def __init__ (self, bcIter):
		# TODO verify correctness
		#self.length = sum ([len (bc) for dur, bc in bcIter])
		self.length = len (bcIter)
		self.bcIter = chain (bcIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): # beat as in rhythm-division... not the other kind (rhythm as in beat-division)
		#beat, ch = self.bcIter.next ()
		#prog, noteNumProg = ch
		#chord = chords[noteNumKey[noteNumProg]]
		duration, (beat, chord) = self.bcIter.next ()
		b = len (beat)
		c = len (chord)
		# TODO try >=
		if b > c:
			i = list (ChangeIter (Bjorklund3 (b, c, 0), chord))
		else:
			i = list (SkipIter (Bjorklund3 (c, b, 0), chord))
		#ret = fundyChord (key, prog, noteNumProg)
		#print (prog, zip (beat, i))
		#sleep (1)
		#return (prog, zip (beat, i))
		return (duration, zip (beat, i))
		#return zip (beat, [duration * (1 + j) for j in i])
class BeatChordIter:
	def __init__ (self, bcIter):
		helper = BeatChordIterHelper (bcIter)
		self.length = len (helper)
		#self.seq = chain.from_iterable (helper)
		self.seq = helper.__iter__ ()
	# TODO fix length
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		#return self.seq.next ()
		duration, play = self.seq.next ()
		return duration, play
"""
class BeatChordMaskIterAdapter:
	def __init__ (self, bcIter):
		self.length = sum ([len (bc) for bc in bcIter])
		print list (bcIter)
		self.bcIter = chain (bcIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): return self.bcIter.next ()
"""
"""
class MaskIter:
	def __init__ (self, bjork, seq):
		self.length = len (seq)
		self.bjork = bjork
		self.seq = seq
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		self.seq.next ()
"""	

# MUST MULTIPLY BY DURATION before EXPANDING bcIter and DROPPING notes

#bcIter = list (ProdIter (beatChordProgression, chordProgression))
#bcIter = list (ProdIter (beatChordProgression, fundChordProgression))
silBjork = Bjorklund3 (13, 5, 0)
#bcIter = list (ProdIter (beatIter, ProdIter (MaskIter (silBjork, beatChordProgression), fundChordProgression)))
#bcIter = list (ProdIter (beatIter, ProdIter (beatChordProgression, fundChordProgression))
bcIter = list (ProdIter (beatIter, ProdIter (beatChordProgression, fundChordProgression)))
#for bc in BeatChordIter (bcIter): print "bc=",bc
class ExpandBcIter:
	def __init__ (self, bcIter):
		self.bcIter = bcIter
		self.length = len (bcIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		duration, notesRhythms = self.bcIter.next ()
		for r, n in notesRhythms:
			print (r * d, n)
		# multiply each rhythm by duration
		# (rhythm := start time of note)
list (ExpandBcIter (bcIter))
		
sleep (5)
#print list (BeatChordIter (bcIter))
		
#beatChordProgression = list ([sorted ([(k/r, 1/r) for r in rhythmChord for k in xrange (r)]) for rhythmChord in rhythmChordProgression])
bcIter = ProdIter (beatChordProgression, chordProgression)
#bcIter = ProdIter (rhythmChordProgression, chordProgression)
for beat, ch in bcIter:
	prog, noteNumProg = ch
	chord = chords[noteNumKey[noteNumProg]]
	b = len (beat)
	c = len (chord)
	#print chord
	
	#print "beat=",beat
	#print "chord=", chord
	
	if b > c:
		#print Bjorklund3 (b, c, 0).seq
		i = list (ChangeIter (Bjorklund3 (b, c, 0), chord))
		#i = None
		#print "changeIter=", i
	else:
		i = list (SkipIter (Bjorklund3 (c, b, 0), chord))
		#print "skipIter=",i
	#print "i=",i
	#list (SkipIter (Bjorklund3 (max (b, c), min (c, b), 0)*, chords[noteNum]))

#for (rhythmChord, chord) in ProdIter (rhythmChordProgression, chordProgression):
#	rhythmNotes = sorted ([(k/r, 1/r) for r in rhythmChord for k in xrange (r)])

#ProdIter (beatIter, progIter, noteNumProgIter, rhythmProgIter, rhythmNoteNumProgIter)
print "DONE"

















#for k in ChordIter (ProdIter (rsProgIter, rhythmNoteNumIter), key): print k
#for k in ChordIter (ProdIter (rhythmProgIter, rhythmNoteNumIter), rhythmKey): print k
sleep (5)

# beat    beat    beat
# chord   chord   chord
# rhythms rhythms rhythms
# /|\
#rhythm   rhythm   rhythm
#silences silences silences
#melody   melody   melody
#
#for each (beat, chord, rhythmChord)
#   foreach rhythm in rhythmChord
#      nnote = bjork (rhythm, silenceIters[rhythm].next)
#      melody(chord, nnote)?


#class RhythmIter:
	
sleep (5)






class NestIter:
	def __init__ (self, itr):
		self.itr = SkipIter (itr)
		
	def __iter__ (self): return self
	def next (self): return self.itr.next ()










"""class SilenceIter:
	def __init__ (self, rang):
		self.rang = xrange (1, rang)
		self.it = SkipIter2 (Bjorklund3 (31, 23, 0).seq, self.rang)
		for i in xrange (10):
			print self.it.next ()
	def __iter__ (self):
		return self
	def next (self):
		return self.it.next ()

class ArhythmIter:
	def __init__ (self, rhythmIter):
		self.rhythmIter = rhythmIter
	def __iter__ (self):
		return self
	def next (self):
		rhythm = rhythmIter.next ()
		#print rhythm
		return rhythm, SilenceIter (rhythm)
arhythmIter = ArhythmIter (rhythmIter)
for k, p in arhythmIter:
	print k
	print list (p)

class RhythmIter:
	def __init__ (self, ar):
		self.ar = ar
	def __iter__ (self): return self
	def next (self):
		ar, se = arhythmIter.next ()
		s = se.next ()
		return Bjorklund3 (ar, s, 0).seq
rhythmIter2 = RhythmIter (arhythmIter)"""

rangeIter = SkipIter2 (Bjorklund3 (10, 9, 0).seq, ranges)
#for k in rangeIter: print k

chakraIter = SkipIter2 (Bjorklund3 (15, 13, 0).seq, chakras)
#for k in chakraIter: print k

baseFreqIter = ZipIter (rangeIter, chakraIter, solfeggio)
#for k in baseFreqIter: print k

# 4,5 - 8
scaleType = 7
scaleMode = 0
scale = list (pythagorean_scale)
scale.remove (2)
# key:
keyIter = SkipIter2 (Bjorklund3 (len (scale), scaleType, scaleMode).seq, scale)
#for k in keyIter: print k
key = list ([keyIter.next () for k in xrange (scaleType)])
#print key
progIter = SkipIter2 (Bjorklund3 (19, 15, 0).seq, xrange (len (key)))
#for k in progIter: print k

# number of notes in chord: 3 to len(keyIter) - 1
noteNums = list ([n for n in xrange (2, len (key))])
noteNumIter = SkipIter2 (Bjorklund3 (16, 5, 0).seq, noteNums)
#for k in noteNumIter: print k

# TODO rotate key by progIter.next ()
#chordBjork = Bjorklund (len (keyIter2), noteNumIter.next ())
#chordBjork.bjorklund ()
#chordBjork.rotate (0)
#chordIter = SkipIter (chordBjork.sequence, keyIter2)
#for k in chordIter: print k

class ChordIter:
	def __init__ (self, progIter, noteNumIter, key):
		self.progIter = progIter
		self.noteNumIter = noteNumIter
		self.key = key
	def __iter__ (self):
		return self
	def next (self):
		prog = self.progIter.next ()
		noteNum = self.noteNumIter.next ()
		return SkipIter2 (Bjorklund3 (len (self.key), noteNum, prog).seq, self.key)
chordIter = ChordIter (progIter, noteNumIter, key)

class CellIter:
	def __init__ (self, beatIter, arhythmIter, chordIter):
		self.beatIter = beatIter
		self.arhythmIter = arhythmIter
		self.chordIter = chordIter
	def __iter__ (self):
		return self
	def next (self):
		beat = self.beatIter.next ()
		div, arhythm = self.arhythmIter.next ()
		chordIter = self.chordIter.next ()
		
		b = beat / div
		n = arhythm
		#n = [chordIter.next () for i in xrange (div)]
		
		return (b, n)
cellIter = CellIter (beatIter, rhythmIter2, chordIter)
#for k in cellIter:
#	print k

#beatBjork = Bjorklund (13, 5)
#beatBjork.bjorklund ()
#beatBjork.rotate (0)
#beatIter = CountIter (beatBjork.sequence)
#for k in beatIter: print k

#rhythmBjork = Bjorklund (22, 13)
#rhythmBjork.bjorklund ()
#rhythmBjork.rotate (0)
#rhythms = sorted (list (set ([n / d
#	for n in xrange (1, 5)
#		for d in xrange (1, 5)])))
#print len (rhythms)
#rhythmIter = SkipIter2 (rhythmBjork.sequence, rhythms)
#for k in rhythmIter: print k

"""rhythmSelect = list ([n for n in xrange (1, len (rhythmIter))])
rhythmSelectBjork = Bjorklund (len (rhythmSelect), 3)
rhythmSelectBjork.bjorklund ()
rhythmSelectBjork.rotate (0)
rhythmSelectIter = SkipIter (rhythmSelectBjork.sequence, rhythmSelect)
print rhythmSelect
#print rhythmSelectBjork.sequence
#for k in rhythmSelectIter: print k
"""
"""
rhythmBjork2 = Bjorklund (len (rhythmIter), 3)
rhythmBjork2.bjorklund ()
rhythmBjork2.rotate (0)
rhythmIter2 = SkipIter2 (rhythmBjork2.sequence, rhythmIter)
for k in rhythmIter2: print k
"""
#rangeBjork = Bjorklund (7, 5)
#rangeBjork.bjorklund ()
#rangeBjork.rotate (0)
#rangeIter = SkipIter2 (rangeBjork.sequence, ranges)
#for k in rangeIter: print k

#chakraBjork = Bjorklund (15, 6)
#chakraBjork.bjorklund ()
#chakraBjork.rotate (0)
#chakraIter = SkipIter2 (chakraBjork.sequence, chakras)
#for k in chakraIter: print k

#baseFreqIter = ZipIter (rangeIter, chakraIter, solfeggio)
#for k in baseFreqIter: print k

# 4,5 - 8
#scaleType = 7
#scaleMode = 0
#scale = list (pythagorean_scale)
#scale.remove (2)
# key:
#scaleBjork = Bjorklund (len (scale), scaleType)
#scaleBjork.bjorklund ()
#scaleBjork.rotate (scaleMode)
#print scaleBjork.sequence
#print sum (scaleBjork.sequence)
#print len (scale)
#keyIter1 = SkipIter2 (scaleBjork.sequence, scale)
#keyIter2 = SkipIter2 (scaleBjork.sequence, scale)
#scaleIter
#for k in keyIter1: print k


def scale_key (scale, scaleType, scaleMode):
	scaleBjork = Bjorklund (scale, scaleType, scaleMode)
	scaleBjork.bjorklund ()
	scaleBjork.rotate (scaleMode)
	scaleIter = SkipIter2 (scaleBjork.sequence, scale)
	return scaleIter
"""def key_chord (key, chordType, chordPhrasing):
	chordBjork = Bjorklund (key, chordType, chordPhrasing)
	chordBjork.bjorklund ()
	chordBjork.rotate (chordPhrasing)
	chordIter = SkipIter2 (chordBjork.sequence, key)
def key_progression (key, progType, progMode):
	progBjork = Bjorklund (key, progType, progMode)
	progBjork.bjorklund ()
	progBjork.rotate (progMode)
	progIter = SkipIter2 (progBjork.sequence, key)
"""

#print scaleBjork.sequence
#print scale
#print keyIter1.length

# root progression
#progBjork = Bjorklund (len (keyIter1), 3)
#progBjork.bjorklund ()
#progBjork.rotate (0)
# clone keyIter
#progIter = SkipIter (progBjork.sequence, keyIter1)
#for k in progIter: print k

# number of notes in chord: 3 to len(keyIter) - 1
#noteNums = list ([n for n in xrange (2, len (keyIter2))])
#noteNumBjork = Bjorklund (len (noteNums), 3)
#noteNumBjork.bjorklund ()
#noteNumBjork.rotate (0)
#noteNumIter = SkipIter (noteNumBjork.sequence, noteNums)
#for k in noteNumIter: print k

# TODO rotate key by progIter.next ()
#chordBjork = Bjorklund (len (keyIter2), noteNumIter.next ())
#chordBjork.bjorklund ()
#chordBjork.rotate (0)
#chordIter = SkipIter (chordBjork.sequence, keyIter2)
#for k in chordIter: print k







print "yes"
sleep (5)
exit



key = 7
mode = 0
chord = 0
chpattern = 3
chmode = 0
beats = 8
pulses = 5
bpmode = 0

phrase_pattern = 2
phrase_mode = 0

verse_pattern = 3
verse_mode = 0

song_pattern = 2
song_mode = 0

cycle_pattern = 1
cycle_mode = 0

"""print len (scale)

def random_permutation (iterable, r=None):
	"Random selection from itertools.permutations(iterable, r)"
	pool = tuple (iterable)
	r = len (pool) if r is None else r
	return tuple (random.sample (pool, r))

sample_rate = 44100
pygame.mixer.pre_init (sample_rate, -16, 1) # 44.1kHz, 16-bit signed, mono
pygame.init ()
length = int (round (500/4))
wait = int (round (1000/4))
for s in random_permutation (solfeggios ()):
	for c in scale:
		print "s=",s,"*","c=",c,"=",s * c
		fundy = fundamental (s * c, sine_wave)
		print "fundy=", fundy
		play_for (fundy, length)
		pygame.time.delay (wait)"""
		
cells = [
	Cell (scale, key, mode, chord, chpattern, chmode, beats, pulses, bpmode),
	Cell (scale, key, mode, chord, chpattern, chmode, beats, pulses, bpmode),
	Cell (scale, key, mode, chord, chpattern, chmode, beats, pulses, bpmode)
]
phrases = [
	Phrase (cells, phrase_pattern, phrase_mode),
	Phrase (cells, phrase_pattern, phrase_mode),
	Phrase (cells, phrase_pattern, phrase_mode),
	Phrase (cells, phrase_pattern, phrase_mode)
]
verses = [
	Verse (phrases, verse_pattern, verse_mode),
	Verse (phrases, verse_pattern, verse_mode),
	Verse (phrases, verse_pattern, verse_mode)
]
songs = [
	Song (verses, song_pattern, song_mode),
	Song (verses, song_pattern, song_mode)
]
cycle = SongCycle (songs, cycle_pattern, cycle_mode)


# select scale, i.e., 12 note
# select key, 1-12 euclidean subset
# select mode, rotate key... doesn't have the same effect with equal temperament
# select chord progression
# create melody within chord progression

#print sorted ([1] + list (harmonics5 (7)))
#display_scale ([1] + list (harmonics5 (7)))
"""
for k in xrange (2, 15):
	s = sorted ([1] + list (set (harmonics6 (k))))
	print len (s)
	display_scale (s)
	sleep (1)
"""
"""
for k in xrange (2, 15):
	s = sorted ([1] + list (set (harmonics6 (k))))
	#print len (s), [(i + 1) / i for i in xrange (2, k + 1)]
	for v in [4, 6, 8, 12, 20]:
		if v > k: continue
		b = Bjorklund (len (s), v)
		b.bjorklund ()
		display_bjorklund_scale (s, b.sequence)
		sleep (1)
"""

# TODO aspects, constraint solving, mpi, opencl

sleep (30)
exit








# hz
tempo = 1
ts_top = 4 # beats per measure
ts_bottom = 4 # quarter note = 1 beat
dot = 1.5

beats = []
beats["dotted whole note"] = ts_bottom * 4 * dot
beats["whole note"] = ts_bottom * 4
beats["dotted half note"] = ts_bottom * 2 * dot
beats["half note"] = ts_bottom * 2
beats["dotted quarter note"] = ts_bottom * dot
beats["quarter note"] = ts_bottom
beats["dotted eighth note"] = ts_bottom / 2 * dot
beats["eighth note"] = ts_bottom / 2
beats["half triplet"] = ts_bottom * 4 / 3
beats["dotted triplet"] = ts_bottom * 2 / 3 * dot
beats["triplet"] = ts_bottom * 2 / 3
beats["eighth triplet"] = ts_bottom / 3
beats["fivlet"] = ts_bottom * 2 / 5

def time_signature (top, bottom):
	# TODO
	return null












ranges_scale = [(rang, note)
	for rang in ranges for note in scale]
chakras_ranges = [(chakra, rang) for chakra in chakras for rang in ranges]
chakras_scale = [(chakra, note) for chakra in chakras for note in scale]

shuffle (ranges)
shuffle (chakras)
shuffle (scale)
shuffle (ranges_scale)
shuffle (chakras_ranges)
shuffle (chakras_scale)

"""ranges_1_chakras_1_scale_1 = [(rang, chakra, note) for rang in ranges for chakra in chakras for note in scale]
ranges_1_scale_1_chakras_1 = [(rang, chakra, note) for rang in ranges for note in scale for chakra in chakras]
chakras_1_ranges_1_scale_1 = [(rang, chakra, note) for chakra in chakras for rang in ranges for note in scale]
chakras_1_scale_1_ranges_1 = [(rang, chakra, note) for chakra in chakras for note in scale for rang in ranges]
scale_1_ranges_1_chakras_1 = [(rang, chakra, note) for note in scale for rang in ranges for chakra in chakras]
scale_1_chakras_1_ranges_1 = [(rang, chakra, note) for note in scale for chakra in chakras for rang in ranges]

ranges_1_chakras_scale_2 = [(rang, chakra, note) for rang in ranges for chakra, note in chakras_scale]
chakras_1_ranges_scale_2 = [(rang, chakra, note) for chakra in chakras for rang, note in ranges_scale]
scale_1_chakras_ranges_2 = [(rang, chakra, note) for note in scale 	for chakra, rang in chakras_ranges]
chakras_scale_2_ranges_1 = [(rang, chakra, note) for chakra, note in chakras_scale for rang in ranges]
ranges_scale_2_chakras_1 = [(rang, chakra, note) for rang, note in ranges_scale for chakra in chakras]
chakras_ranges_2_scale_1 = [(rang, chakra, note) for chakra, rang in chakras_ranges for note in scale]

movements = [
	ranges_1_chakras_1_scale_1, ranges_1_scale_1_chakras_1,
	chakras_1_ranges_1_scale_1, chakras_1_scale_1_ranges_1,
	scale_1_ranges_1_chakras_1, scale_1_chakras_1_ranges_1,

	ranges_1_chakras_scale_2, chakras_1_ranges_scale_2, scale_1_chakras_ranges_2,
	chakras_scale_2_ranges_1, ranges_scale_2_chakras_1, chakras_ranges_2_scale_1]
shuffle (movements)"""

scale_melody = melody (scale)
chakras_melody = melody (chakras)
ranges_melody = melody (ranges)
chakras_scale_melody = melody (chakras_scale)
ranges_scale_melody = melody (ranges_scale)
chakras_ranges_melody = melody (chakras_ranges)

ranges_1_chakras_1_scale_1_melody = [(rang, chakra, note) for rang in ranges_melody for chakra in chakras_melody for note in scale_melody]
ranges_1_scale_1_chakras_1_melody = [(rang, chakra, note) for rang in ranges_melody for note in scale_melody for chakra in chakras_melody]
chakras_1_ranges_1_scale_1_melody = [(rang, chakra, note) for chakra in chakras_melody for rang in ranges_melody for note in scale_melody]
chakras_1_scale_1_ranges_1_melody = [(rang, chakra, note) for chakra in chakras_melody for note in scale_melody for rang in ranges_melody]
scale_1_ranges_1_chakras_1_melody = [(rang, chakra, note) for note in scale_melody for rang in ranges_melody for chakra in chakras_melody]
scale_1_chakras_1_ranges_1_melody = [(rang, chakra, note) for note in scale_melody for chakra in chakras_melody for rang in ranges_melody]

ranges_1_chakras_scale_2_melody = [(rang, chakra, note) for rang in ranges_melody for chakra, note in chakras_scale_melody]
chakras_1_ranges_scale_2_melody = [(rang, chakra, note) for chakra in chakras_melody for rang, note in ranges_scale_melody]
scale_1_chakras_ranges_2_melody = [(rang, chakra, note) for note in scale_melody 	for chakra, rang in chakras_ranges_melody]
chakras_scale_2_ranges_1_melody = [(rang, chakra, note) for chakra, note in chakras_scale_melody for rang in ranges_melody]
ranges_scale_2_chakras_1_melody = [(rang, chakra, note) for rang, note in ranges_scale_melody for chakra in chakras_melody]
chakras_ranges_2_scale_1_melody = [(rang, chakra, note) for chakra, rang in chakras_ranges_melody for note in scale_melody]

movements_melody = [
	ranges_1_chakras_1_scale_1_melody, ranges_1_scale_1_chakras_1_melody,
	chakras_1_ranges_1_scale_1_melody, chakras_1_scale_1_ranges_1_melody,
	scale_1_ranges_1_chakras_1_melody, scale_1_chakras_1_ranges_1_melody,

	ranges_1_chakras_scale_2_melody, chakras_1_ranges_scale_2_melody, scale_1_chakras_ranges_2_melody,
	chakras_scale_2_ranges_1_melody, ranges_scale_2_chakras_1_melody, chakras_ranges_2_scale_1_melody]
shuffle (movements_melody)

"""for movement in movements:
	for rang, chakra, note in movement:
		print play (chrang (chakra, rang), note), " 1"
"""
for movement in movements_melody:
	for rang, chakra, note in movement:
		print play (chrang (chakra, rang), note), " 1"