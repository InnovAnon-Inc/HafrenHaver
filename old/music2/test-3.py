#! /usr/bin/env python

import math
from itertools import accumulate




song_structure_db = [
	# pop song structures
	   [0, 0,    1, 0,    1, 2, 1],    #   V1 V2   C V3   C B C
	[3, 0, 0,    1, 0,    1, 2, 1],    # I V1 V2   C V3   C B C
	   [0, 0,    1, 0,    1, 2, 1, 4], #   V1 V2   C V3   C B C O
	[3, 0, 0,    1, 0,    1, 2, 1, 4], # I V1 V2   C V3   C B C O
	   [0, 0, 5, 1, 0, 5, 1, 2, 1],    #   V1 V2 P C V3 P C B C
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1],    # I V1 V2 P C V3 P C B C
	   [0, 0, 5, 1, 0, 5, 1, 2, 1, 4], #   V1 V2 P C V3 P C B C O
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1, 4], # I V1 V2 P C V3 P C B C O
	#
	#   [0, 0,    1, 0,    1, 2, 1],          #   V1 V2   C B C V3   C C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    #   V1 V2   C B C V3   C B C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], #   V1 V2   C B C V3   C B C C

	#   [0, 0,    1, 0,    1, 2, 1],          #   V1 V2 P C B C V3 P C C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    #   V1 V2 P C B C V3 P C B C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], #   V1 V2 P C B C V3 P C B C C

	#   [0, 0,    1, 0,    1, 2, 1],          # I V1 V2   C B C V3   C C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    # I V1 V2   C B C V3   C B C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], # I V1 V2   C B C V3   C B C C

	#   [0, 0,    1, 0,    1, 2, 1],          # I V1 V2 P C B C V3 P C C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    # I V1 V2 P C B C V3 P C B C
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], # I V1 V2 P C B C V3 P C B C C

	#   [0, 0,    1, 0,    1, 2, 1],          #   V1 V2   C B C V3   C C     O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    #   V1 V2   C B C V3   C B C   O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], #   V1 V2   C B C V3   C B C C O

	#   [0, 0,    1, 0,    1, 2, 1],          #   V1 V2 P C B C V3 P C C     O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    #   V1 V2 P C B C V3 P C B C   O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], #   V1 V2 P C B C V3 P C B C C O

	#   [0, 0,    1, 0,    1, 2, 1],          # I V1 V2   C B C V3   C C     O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    # I V1 V2   C B C V3   C B C   O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], # I V1 V2   C B C V3   C B C C O

	#   [0, 0,    1, 0,    1, 2, 1],          # I V1 V2 P C B C V3 P C C     O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1],    # I V1 V2 P C B C V3 P C B C   O
	#   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1], # I V1 V2 P C B C V3 P C B C C O

	# TODO I O P for ^^^
	# folk song structures
	   [0, 1,    0, 1,    0, 1, 0, 1],
	   [0, 1,    0, 1,    0, 1, 1],
]


verse_structure_db = [
	0, # by verse       => 1X measures
	1, # by phrase      => 2X measures
	2, # by semi-phrase => 4X measures
	3, # by measure     => 8X measures
]

def verseStructure (vs):
	measure_min = 2
	measure_max = 7
	if vs == 3: # by measure
		# n measure in [1, 2]
		measure_length_0 = ?
		return [measure_length_0] * 8
	if vs == 2: # by semi-phrase
		# n measure in [1, 4]
		# measure length in ???
		measure_length_0 = ?
		measure_length_1 = ?
		return [measure_length_0, measure_length_1] * 4
	if vs == 1: # by phrase
		# n measure in [1, 8]
		measure_length_0 = ?
		measure_length_1 = ?
		measure_length_2 = ?
		measure_length_3 = ?
		return [measure_length_0, measure_length_1,
		        measure_length_2, measure_length_3] * 2
	# by verse
	# n measure in [1, 16]
	measure_length_0 = ?
	measure_length_1 = ?
	measure_length_2 = ?
	measure_length_3 = ?
	measure_length_4 = ?
	measure_length_5 = ?
	measure_length_6 = ?
	measure_length_7 = ?
	return [measure_length_0, measure_length_1,
	        measure_length_2, measure_length_3,
	        measure_length_4, measure_length_5,
	        measure_length_6, measure_length_7]

# TODO rotate measures by fractional length (e.g., pickup notes) ?

def varyVerseStructure (vs, verse_structure):
	# TODO trucate, append  measure length array
	# TODO rotate           measure length array
	# TODO dilate, contract measure length elements
	# TODO reverse, invert? measure length array
	pass

# length of chord progression ?
# by song? by verse? by phrase? by measure?
# modulate after each chord progression ?

#chords_db = [
#	[0, ], // major
#]

# TODO chord_progression = T-T,
# T-D(-T), T-S(-T),
# T-S-D(-T), T-D-S(-T),
# T-S-D-S(-T), T-D-S-D(-T), T-S-S-D(-T), T-D-S-S(-T)
# I-vii-iii-vi-IV-ii-V => T-S-D-T-S-S-D(-T)
chord_progression_db = [
	[0],          # T(-T)
	[0, 1],       # T-D(-T)
	[0, 2],       # T-S(-T)
	[0, 2, 1],    # T-S-D(-T)
	[0, 1, 2],    # T-D-S(-T)
	[0, 2, 2],    # T-S-S(-T)
	[0, 1, 1],    # T-D-D(-T)
	[0, 2, 2, 1], # T-S-S-D(-T)
	[0, 2, 1, 2], # T-S-D-S(-T)
	[0, 1, 2, 2], # T-D-S-S(-T)
]

# Python program to print all subsets with given sum 

# The vector v stores current subset. 
def printAllSubsetsRec (arr, n, v, sum):

	# If remaining sum is 0, then print all
	# elements of current subset.
	if sum == 0:
		for value in v:
			print (value, end=" ")
		print()
		return

	# If no remaining elements,
	if n == 0: return

	# We consider two cases for every element.
	# a) We do not include last element.
	# b) We include last element in current subset.
	printAllSubsetsRec (arr, n - 1, v, sum)
	v1 = [] + v
	v1.append (arr[n - 1])
	printAllSubsetsRec (arr, n - 1, v1, sum - arr[n - 1])


# Wrapper over printAllSubsetsRec()
def printAllSubsets (arr, n, sum):
	v = []
	printAllSubsetsRec (arr, n, v, sum)

# This code is contributed by ihritik 

# TODO handle chorus and/or song end

def chordProgressionHelper (nc):
	# TODO get uniq lengths from chord_progression_db
	arr = [1, 2, 3, 4]
	progressions = printAllSubsets (arr, len(arr), nc)
	# TODO select random subset
	# TODO select random chord progression segments for each subset
	# TODO modulations
	# TODO borrow chords... now or per verse?
	
def chordProgression (verse_structures, cp):
	if cp == 4: # by measure (chord progression for verse)
		for verse_structure in verse_structures:
			nc = len (verse_structure)
			yield chordProgressionHelper (nc)
	if cp == 3: # by semi-phrase (chord progression for verse)
		for verse_structure in verse_structures:
			# TODO extract semi-phrases
	if cp == 2: # by phrase (one chord per phrase => chord progression for song)
		for verse_structure in verse_structures:
			# TODO extract phrases
	if cp == 1:  # by verse (one chord for whole verse => chord progression for song)
		nc = len (verse_structures)
		return chordProgressionHelper (nc)
	# by song (one chord for whole song)
	return [0]

# repetition patterns:
# - repetition
# - variation
# - contrast
#
# nphrase in [2, 3]
#
# 1 phrase
# 2 repeat/contrast/variation
# (3)
#
# 1 phrase_a                   r/c/v          (r/c/v)
# 2 r/c/v                      r/c/v          (r/c/v)
# (3)
#
# 1 phrase_aa r/c/v            r/c/v r/c/v    (r/c/v)
# 2 r/c/v     r/c/v            r/c/v r/c/v    (r/c/v)
# (3)

class Meter:
	def __init__ (self, lengths): self.lengths = lengths
	def getLength  (self): return sum (self.lengths)
	def getLengths (self): return self.lengths # TODO freeze
class MeterByMeasure    (Meter):
	def __init__ (self):
		lengths = random_array ()
		nparts  = random_range (2, 3)
		self.phrase1a = lengths
class MeterBySemiPhrase (Meter):
	def __init__ (self):
		lengths = random_array ()
		nparts  = random_range (2, 3)
		# TODO
		self.phrase1a = lengths
		self.phrase1b = lengths
		self.phrase2a = lengths
		self.phrase2b = lengths
	def getLengths (self): return [self.a] + self.phrase1a + [self.b] + self.phrase1b + [self.c] + self.phrase2a + [self.d] + self.phrase2b + [self.e]
class MeterByPhrase     (Meter):
	def __init__ (self):
		lengths = random_array ()
		Meter.__init__ (self, lengths)
		lengths = Meter.getLengths (self)
		self.phrase1 = lengths
		self.phrase2 = lengths
	def getLengths (self): return [self.a] + self.phrase1 + [self.b] + self.phrase2 + [self.c]
class MeterByVerse      (Meter):
	def __init__ (self):
		lengths = random_array ()
		Meter.__init__ (self, lengths)

	measure_min = 2
	measure_max = 7
	if vs == 3: # by measure
		# n measure in [1, 2]
		measure_length_0 = ?
		return [measure_length_0] * 8
	if vs == 2: # by semi-phrase
		# n measure in [1, 4]
		# measure length in ???
		measure_length_0 = ?
		measure_length_1 = ?
		return [measure_length_0, measure_length_1] * 4
	if vs == 1: # by phrase
		# n measure in [1, 8]
		measure_length_0 = ?
		measure_length_1 = ?
		measure_length_2 = ?
		measure_length_3 = ?
		return [measure_length_0, measure_length_1,
		        measure_length_2, measure_length_3] * 2
	# by verse
	# n measure in [1, 16]
	measure_length_0 = ?
	measure_length_1 = ?
	measure_length_2 = ?
	measure_length_3 = ?
	measure_length_4 = ?
	measure_length_5 = ?
	measure_length_6 = ?
	measure_length_7 = ?
	return [measure_length_0, measure_length_1,
	        measure_length_2, measure_length_3,
	        measure_length_4, measure_length_5,
	        measure_length_6, measure_length_7]
class Bar:
	def __init__ (self, nbeat):
		# TODO
class Segment:
	def __init__ (self, bars): self.bars = bars
	def getRepeatableBars (bar):
		# TODO
class Phrase:
	def __init__ (self, segments):
		self.segments = segments
	def getRepeatableSegments (segment):
		# TODO
	def getSegments (segment):
		repeatable = []
		for s in self.segments:
			if segment == s:
				repeatable = repeatable + [s]
		return repeatable
	def getAllBars  ():
		ret = []
		for s in self.segments:
			ret = ret + [s.getBars()]
		return ret
	def getBars     (bar):
		repeatable = []
		for s in self.segments:
			for b in s.getBars ():
				if b == bar:
					repeatable = repeatable + [b]
		return repeatable

def random_phrase ():
	# TODO






meter_db = [
	[[0]],

	[[0, 0]],
	[[0, 1]],
	[[0, 0, 0]],
	[[0, 0, 1]],
	[[0, 1, 2]],

	[[0, 1], [0, 1]],
	[[0, 1], [0, 1], [0]],
	[[0, 1], [0, 1], [1]],
	[[0, 1], [0, 1], [2]],
	[[0, 1], [0], [0, 1]],
	[[0, 1], [1], [0, 1]],
	[[0, 1], [2], [0, 1]],
	[[0], [0, 1], [0, 1]],
	[[1], [0, 1], [0, 1]],
	[[2], [0, 1], [0, 1]],

	[[0, 1], [0, 2]],
	[[0, 1], [0, 2], [0]],
	[[0, 1], [0, 2], [1]],
	[[0, 1], [0, 2], [2]],
	[[0, 1], [0], [0, 2]],
	[[0, 1], [1], [0, 2]],
	[[0, 1], [2], [0, 2]],
	[[0], [0, 1], [0, 2]],
	[[1], [0, 1], [0, 2]],
	[[2], [0, 1], [0, 2]],

	[[0, 0], [0, 1]],
	[[0, 0], [0, 1], [0]],
	[[0, 0], [0, 1], [1]],
	[[0, 0], [0, 1], [2]],
	[[0, 0], [0], [0, 1]],
	[[0, 0], [1], [0, 1]],
	[[0, 0], [2], [0, 1]],
	[[0], [0, 0], [0, 1]],
	[[1], [0, 0], [0, 1]],
	[[2], [0, 0], [0, 1]],

	[[0, 1], [0, 1], [0, 1]],
	[[0, 1], [0, 1], [0, 2]],

	[[0, 1], [0, 2], [0, 2]],
	[[0, 1], [0, 2], [1, 2]],

	[[0, 1], [2, 1], [0, 1]],
	[[0, 1], [2, 1], [2, 1]],
]
		
class Phrase0 (Phrase):
	def __init__ (self):
		bars = [random_range (13, 23)]
		bars = [Bar (nbeat) for nbeat in bars]
		bars = [Segment (bars)]
		Phrase.__init__ (self, bars)
class Phrase1 (Phrase):
	def __init__ (self):
		nbar = random_range (2, 3)
		segments = []
		for bar in nbar:
			nbeats = random_range (5, 13)
			for nbeat in nbeats:
				bars = Bar (nbeat)
				segments = segments + [Segment (bars)]
class Phrase2 (Phrase):
	def __init__ (self):
		nsegment = random_range (2, 3)
		segments = []
		for segment in nsegment:
			nbars = random_range (1, 3)
			bars = []
			for bar in nbars:
				nbeat = random_range (1, 5)
				bars = bars + [nbeat]
			segments = segments + [Segment (bars)]
	# bars:
	# - by phrase => (bars)
	# - by semi-phrase => (bars1 + bars1)
	#                  => bars1 + bars2
	#                  => bars1 + bars1 + bars1
	#                  => bars1 + bars1 + bars2
	#                  => bars1 + bars2 + bars3
	# - by semi-semi-phrase => (bars1 + bars2) + (bars1 + bars2)
	#                       => (bars1 + bars2) + (bars1 + bars2) + bars1
	#                       => (bars1 + bars2) + (bars1 + bars2) + bars2
	#                       => (bars1 + bars2) + (bars1 + bars2) + bars3
	#                       => (bars1 + bars2) + (bars1 + bars3) ...
	#                       => (bars1 + bars1) + (bars1 + bars2) ...
	#                       => (bars1 + bars2) + (bars1 + bars2) + (bars1 + bars2)
	#                       => (bars1 + bars2) + (bars1 + bars2) + (bars1 + bars3)
	#                       => (bars1 + bars2) + (bars1 + bars3) + (bars1 + bars3)
	#                       => (bars1 + bars1) + (bars1 + bars2) + (bars1 + bars2)
	#                       => (bars1 + bars1) + (bars1 + bars2) + (bars1 + bars3)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars2)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars3)

	#                       => (bars1 + bars2 + bars3) + (bars1 + bars2 + bars3)
	#                       => (bars1 + bars2 + bars3) + (bars1 + bars2 + bars3) + (bars1 + bars2)
	#                       => (bars1 + bars2 + bars3) + (bars1 + bars2 + bars3) + (bars1 + bars3)
	#                       => (bars1 + bars2 + bars3) + (bars1 + bars2 + bars3) + (bars2 + bars3)
	#                       => (bars1 + bars2 + bars3) + (bars1 + bars2) + (bars1 + bars2 + bars3)
	#                       => (bars1 + bars2 + bars3) + (bars1 + bars3) + (bars1 + bars2 + bars3)
	#                       => (bars1 + bars2 + bars3) + (bars2 + bars3) + (bars1 + bars2 + bars3)

	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars2) + (bars1 + bars2)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars2) + (bars1 + bars3)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars2) + (bars2 + bars3)

	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars3) + (bars1 + bars3)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars3) + (bars1 + bars2)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars3) + (bars2 + bars3)

	#                       => (bars1 + bars1 + bars2) + (bars1 + bars2) + (bars1 + bars1 + bars2)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars3) + (bars1 + bars1 + bars2)

	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars2) + (bars1 + bars1 + bars2)
	#                       => (bars1 + bars1 + bars2) + (bars1 + bars1 + bars2) + (bars1 + bars1 + bars3)
class Section:
	def __init__ (self, phrases): pass
class Intro  (Section):
	def __init__ (self, verse_structure, last_song, verse):
		Section.__init__ (self, verse_structure)
class Pre    (Section):
	def __init__ (self, verse_structure, verse, chorus):
		Section.__init__ (self, verse_structure)
class Outtro (Section):
	def __init__ (self, verse_structure, chorus):
		Section.__init__ (self, verse_structure)
class Verse  (Section):
	def __init__ (self, verse_structure, intro_or_last_song):
		Section.__init__ (self, verse_structure)
class Chorus (Section):
	def __init__ (self, verse_structure, verse): # , bridge):
		Section.__init__ (self, verse_structure)
class Bridge (Section):
	def __init__ (self, verse_structure, chorus):
		Section.__init__ (self, verse_structure)
class Song:
	def __init__ (self, song_structure):
		self.song_structure      =      song_structure
		# TODO get bjorklund strategy--by song, by section, by phrase, etc
		# TODO get meter     strategy--by song, by section, by phrase, etc
		# TODO get chord     strategy--by song, by section, by phrase, etc
		# TODO at least one must not be by song ?
		# TODO not all can be by measure ?
		for section in song_structure:
			# TODO get ratios
			# TODO get tempo
			# TODO get verse_structure
			# TODO get bjorklund structure
			# TODO get meter
			# TODO get poetic meter
		# TODO get chord function progression
		# TODO get chord progression
		# TODO get CT-NCT, CT-NCT-NCT
		# TODO get melody
		# TODO get harmony

		# verse_structure determines the bjorklund structure
		# and                        the meter
		# meter           determines the chord_progression
		self.bjorklund_structure = bjorklund_structure

		# TODO get song sections

		

		verse  = Verse  ()
		intro  = Intro  (verse, last_song)
		pre    = Pre    (verse)
		outtro = Outtro (verse)
		chorus = Chorus (verse, pre, outtro)
		bridge = Bridge (verse, chorus)
class Songs:
	def __init__ (self): pass
class Album    (Songs): # "playlist" ?
	def __init__ (self):
		# TODO generate Songs
		# TODO vary some Songs
		# TODO pattern of repetition
		pass
class Symphony (Songs):
	def __init__ (self):
		movements[0] = Song      (None,         self, False)
		movements[1] = vary_song (movements[0], self, False)
		movements[2] = vary_song (movements[1], self, False)
		movements[3] = vary_song (movements[2], self, True)
		
# TODO other song repetition structures
class Playlist:
	def __init__ (self):
		# TODO albums
		# TODO pattern of brainwaves
class VerseStructure:
	def __init__ (self):
		pass
	# TODO measure iterator
class VerseStructure0:
	def __init__ (self):
		VerseStructure.self.__init__ (self)
class ChordProgression:
	def __init__ (self, verse_structure):
		self.verse_structure = verse_structure
		

# function of each diatonic chord
#chord_functions_db = {
#	0:
#}

def borrow_chords (ratios, key, scale, mode, chord_progression):
	# TODO 

# TODO repetition pattern
# TODO bjorklund

poetic_feet_db = [
    [1, 1],    // spondee
    [1, 0],    // trochee, choree
    [0, 1],    // iamb
    [0, 0],    // pyrrhus, dibrach
    [1, 1, 1], // molossus
    [1, 1, 0], // antibaccius
    [1, 0, 1], // cretic, amphimacer
    [1, 0, 0], // dactyl
    [0, 1, 1], // baccius
    [0, 1, 0], // amphibrach
    [0, 0, 1], // anapaest, antidactylus
    [0, 0, 0], // tribrach
]

# TODO how to select poetic meter

def rhythm (bjorklund):
	for index in range (0, len (bjorklund)):
		# quarter note if current and next
		# quarter note if current and next DNE
		# half    note if current and not next and next next DNE
		# half    note if current and not next and random
		# quarter note if not current and random
		# eighth  note if not current and random
		# rest         if not current and random
		current = bjorklund[index]
		if index == len (bjorklund) - 1: next = None
		else:                            next = bjorklund[index + 1]
		if current:
			if 
			

def poetic_feet (rhythm):
	# TODO a string of poetic feet
	# s.t. accented feet fall on accented beats
	# and non-accented feet on non-accented beats
	# or accented feet tie over to non-accented beats



# TODO poetic feet
# TODO rhythms
# TODO CT-NCT, CT-NCT-NCT
# TODO motif
# TODO repetition structure
# TODO melody shape (i.e., rise toward middle or end)
# TODO melody
# TODO harmony











from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio

try:
	from itertools import izip
except ImportError: # Python 3
	izip = zip
	xrange = range

def sine_tone(frequency, duration, volume=1, sample_rate=22050):
	n_samples = int(sample_rate * duration)
	restframes = n_samples % sample_rate

	p = PyAudio()
	stream = p.open(format=p.get_format_from_width(1), # 8bit
					channels=2, # mono
					rate=sample_rate,
					output=True)
	s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
	samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
	for buf in izip(*[samples]*sample_rate): # write several samples at a time
		stream.write(bytes(bytearray(buf)))

	# fill remainder of frameset with silence
	stream.write(b'\x80' * restframes)

	stream.stop_stream()
	stream.close()
	p.terminate()

base_frequency = 432
ratios = ratios_db[0]
key = 0
lower_tetrachord = tetrachords_db[0]
upper_tetrachord = tetrachords_db[0]
scale = make_scale (ratios, lower_tetrachord, upper_tetrachord)
mode = 0

#print ("ratios=%s, %s" % (len (ratios), ratios), end="\n")
for key in range (0, len (ratios)):
	print ("key=%s" % key, end="\n")
	#for index in range (0, len (ratios)):
	#	print (keyPitch (ratios, index, 0, key), end=" ")
	#print (end="\n")
	#for index in range (0, len (scale)):
	#	print (scalePitch (ratios, index, 0, key, scale), end=" ")
	#print (end="\n")
	for mode in range (0, len (scale)):
		print ("mode=%s" % mode, end="\n")
		for index in range (0, len (scale)):
			print (modePitch (ratios, index, 0, key, scale, mode), end=" ")
			sine_tone(
			    frequency=bfPitch (base_frequency, modePitch (ratios, index, 0, key, scale, mode)),
			    duration=3.21,
			    volume=.01,
			    sample_rate=22050
			)

		print (end="\n")
	print (end="\n")



def darken_key    (key, octave, ratios):
	key    = key - (len (ratios) // 2 - 1)
	if key < 0: octave = octave - 1
	key    = key % len (ratios)
	return (key, octave)
def brighten_key  (key, octave, ratios):
	key    = key + (len (ratios) // 2 + 1)
	octave = key // len (ratios) + octave
	key    = key %  len (ratios)
	return (key, octave)
def darken_mode   (key, octave, ratios, scale, mode):
	if mode == len (scale) - 1:
		key    = key - 1
		if key < 0: octave = octave - 1
		key    = key % len (ratios)
	mode   = mode - (len (scale) // 2)
	if mode < 0: octave = octave - 1
	mode   = mode % len (scale)
	return (key, octave, mode)
def brighten_mode (key, octave, ratios, scale, mode):
	if mode == len (scale) // 2:
		key    = key + 1
		octave = key // len (ratios) + octave
		key    = key %  len (ratios)
	mode   = mode + (len (scale) // 2)
	octave = mode // len (scale) + octave
	mode   = mode % len (scale)
	return (key, octave, mode)
# TODO radiohead change
# TODO andelusian, mario
# TODO chromatic
# TODO chromatic mediant

# TODO generate chord progression and/or modulation sequence
# TODO get meter
# TODO poetic feet
# TODO rhythms... 1 note, 1/2 note, 1/4 note, 1/8 note
# TODO CT-NCT, CT-NCT-NCT... accented vs unaccented
# TODO generate motif
# TODO get repetition pattern

# TODO keep track of which keys, modes & scales have been visited
# TODO at song end, modulate to less commonly used keys

