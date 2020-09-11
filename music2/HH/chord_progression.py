#! /usr/bin/env python3

from numba     import jit
from random    import choice, randrange
from itertools import accumulate, chain

from random_util import subsets, random_bjorklund2, random_bool
from song        import random_song#, apply_song
from mode        import random_mode

# song structure
# meter
# chord functions
# modes (modulations)
# modal interchange
# chords (more borrowing, inversions, voice leading)
# accent pattern
# poetic meter
# rhythm
# CT-NCT, CT-NCT-NCT cadence
# melody
# contrapuntal harmony


	
	
	
	
	
		
		
		

section_db = (
	((0)),       # one   phrase
	((0, 0),     # two   phrases, same      cadence
	 (0, 1)),    # two   phrases, different cadence
	((0, 0, 0),  # three phrases, same      cadence
	 (0, 0, 1),  # three phrases, last  different
	 (0, 1, 0),  # three phrases, mid   different
	 (0, 1, 1)), # three phrases, first different
)
class SectionCadence (Cadence):
	def __init__ (self, sc):
		Cadence.__init__ (sc)
def random_section_cadence (short=None):
	if short is None: short = random_bool ()
	if short is True: temp = section_db[1 - 1]
	else:
		temp = randrange (2, 3 + 1) - 1
		temp = section_db[temp]
	sc = choice (temp)
	return SectionCadence (sc)

phrase_db = (
	((0)),       # one   segment
	((0, 0),     # two   segments, same cadence
	 (0, 1)),    # two   segments, same cadence
	((0, 0, 0),  # three segments, same cadence
	 (0, 0, 1),  # three segments, last  different
	 (0, 1, 1)), # three segments, first different
)
class PhraseCadence (Cadence):
	def __init__ (self, pc):
		Cadence.__init__ (pc)
def random_phrase_cadence ():
	temp = choice (phrase_db)
	pc   = choice (temp)
	return PhraseCadence (pc)
def random_phrase_cadences (nsection):
	pcs = [random_phrase_cadence () for _ in range (0, nsection)]
	# TODO
segment_db = (
	((0)),          # one   bar
	((0, 0),        # two   bars, same      cadence
	 (0, 1)),       # two   bars, different cadence
	((0, 0, 0),     # three bars, same      cadence
	 (0, 0, 1),     # three bars, last  different
	 (0, 1, 1)),    # three bars, first different
	((0, 0, 0, 1),  # four  bars, last  different
	 (0, 0, 1, 1),  # four  bars, last two different
	 (0, 1, 0, 1),  # four  bars, every other is different
	 (0, 1, 1, 1)), # four  bars, first different
)
class SegmentCadence (Cadence):
	def __init__ (self, sc):
		Cadence.__init__ (sc)
def random_segment_cadence ():
	temp = choice (segment_db)
	sc   = choice (temp)
	return SegmentCadence (sc)

class MeterCadence:# (Cadence):
	def __init__ (self, ss, secc, phrc, segc, barc):
		# TODO map bars
		#Cadence.__init__ ()
		self.ss   = ss
		self.secc = secc
		self.phrc = phrc
		self.segc = segc
		self.barc = barc
def random_meter_cadence ():
	ss          = random_song_cadence ()
	
	nsection    = ss.nsection ()
	secc        = random_section_cadences (ss)
	#ss.secc     = secc
	
	min_nphrase = ss.min_nphrase () # min number of distinct phrases, given section patterns: max of all
	max_nphrase = ss.max_nphrase () # max number of distinct phrases, given section patterns: sum of maxes of all
	nphrase     = randrange (min_nphrase, max_nphrase + 1)
	phrc        = random_phrase_cadences (secc, nphrase)
	#ss.phrc     = phrc
	
	min_nsegment = ss.min_nsegment ()
	max_nsegment = ss.max_nsegment ()
	nsegment     = randrange (min_nsegment, max_nsegment + 1)
	segc         = random_segment_cadences (phrc, nsegment)
	#ss.segc      = segc
	
	min_nbar     = ss.min_nbar ()
	max_nbar     = ss.max_nbar ()
	nbar         = randrange (min_nbar, max_nbar)
	barc         = random_bar_cadences (segc, nbar)
	#ss.barc      = barc
	
	return MeterCadence (ss, secc, phrc, segc, barc)
def random_section_cadences_helper (uniq, min_n, max_n, short=None):
	n        = randrange (min_n, max_n + 1)
	sections = [random_section_cadence (short) for _ in range (0, n)]

	# TODO indices := map from uniq.section to sections; nsection <= len (uniq.sections)
	#indices  = shuffle (range (0, len (sections)))

	# all combos of indices of len(uniq)
	# 
	indices = []
	for _ in range (0, len (uniq)):
		index   = ?
		indices = indices + [index]
	
	assert len (indices) == len (uniq)
	mapping  = {}
	for section, i in zip (uniq, indices):
		assert section not in mapping
		mapping[section] = i
	return sections, mapping
def random_section_cadences (sc): # song cadence => section cadences
	long_sections,  lm = random_section_cadences_helper (sc.long_uniq,  sc.min_nlsection (), sc.max_nlsection (), False)
	short_sections, ls = random_section_cadences_helper (sc.short_uniq, sc.min_nssection (), sc.max_nssection (), True)
	

	












# song structure
# section structure
# => nphrase_tot, nphrase_uniq


# ~nbeat for phrase
# phrase structure
# => nbeat per segment

# ~nbeat per segment
# segment structure
# => nbeat per bar, longer bars toward end
"""

class Meter:
	def __init__ (self, mc, nbeats):
		self.mc     = mc
		self.nbeats = nbeats
def random_meter (mc=None, nbeats=None):
	if mc     is None: mc     = random_meter_cadence ()
	if nbeats is None: nbeats = random_nbeats (mc.nbar ())
	return Meter (mc, nbeats)
	
	
	
	
	
	
	
	
	
	
def random_song_structure ():
	ss = choice (song_structure_db)
	return SongStructure (ss)
def random_sections (ss):
	sections = ss.uniq
	for section in sections:
		
		
		
def random_meter ():
	min_nbar = ?
	max_nbar = ?
	nbar = randrange (min_nbar, max_nbar)
	tbar = ?
	bars = [random_bar (tbar) for k in range (0, nbar)]











class SongStructure (Mapping):
	def __init__ (self, sections, order):
		Mapping.__init__ (self, sections, order)
		long_uniq      = {}
		short_uniq     = {}
		for i, section in zip (range (0, len (sections)), sections):
			if section in [0, 1, 2]:
				long_sections  = long_sections  + [section]
				if section in long_uniq: temp = long_uniq[section]
				else:                    temp = []
				long_uniq[section]  = temp[i]
			if section in [3, 4, 5]:
				short_sections = short_sections + [section]
				if section in short_uniq: temp = short_uniq[section]
				else:                     temp = []
				short_uniq[section] = temp[i]
		self.long_uniq  = long_uniq
		self.short_uniq = short_uniq
		
	def phrases (self): return chain ((     section.phrases  for section in self.order))
	def nphrase (self): return sum   ((len (section.phrases) for section in self.order))
	def section (self, phrase_no):
		acc = accumulate ((len (section.phrases) for section in self.order))
		assert len (acc) == len (self.order)
		for i, v in zip (range (0, len (self.order)), acc):
			if v <= phrase_no: return i
		raise Exception ()
		
	def segments (self): return chain ((section.segments () for section in self.order))
	def nsegment (self): return sum   ((section.nsegment () for section in self.order))
	def phrase   (self, segment_no):
		phrases = list (self.phrases ())
		acc = accumulate ((len (phrase.segments) for phrase in phrases))
		assert len (acc) == self.nphrase ()
		for i, v in zip (range (0, len (phrases)), acc):
			if v <= segment_no: return i
		raise Exception ()
		
	def bars    (self): return chain ((section.bars () for section in self.order))
	def nbar    (self): return sum   ((section.nbar () for section in self.order))
	def segment (self, bar_no):
		pass
		
	def bar (self, beat_no): pass
	
	#def uniq_phrases (self): 



def random_song_structure ():
	sections = choice (songs_db)
	return SongStructure (sections)
	
	
section_db = {
	"1" : ((0)),
	"2" : ((0, 0), (0, 1)),
	"3" : ((0, 0, 0), (0, 0, 1), (0, 1, 1)),
}
class Section:
	def __init__ (self, phrases): self.phrases = phrases
	def segments (self): return chain (*(phrase .segments () for phrase  in self.phrases))
	def bars     (self): return chain (*(segment.bars     () for segment in self.segments ()))
	#def nbeat    (self): return 
phrase_db = {
	"1" : ((0)),
	"2" : ((0, 0), (0, 1)),
	"3" : ((0, 0, 0), (0, 0, 1), (0, 1, 1)),
}
class Phrase:
	def __init__ (self, segments): self.segments = segments	
	def nbeat   (self): return sum ((segment.nbeat ()   for segment in self.segments))
	def nbar    (self): return sum ((len (segment.bars) for segment in self.segments))
	def segment (self, i):
		pass
	def bar     (self, i):
		pass
segment_db = {
	"1" : ((0)),
	"2" : ((0, 0), (0, 1)),
	"3" : ((0, 0, 0), (0, 0, 1), (0, 1, 1)),
	"4" : ((0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 0, 1), (0, 1, 1, 1)),
}
class Segment:
	def __init__ (self, bars)
		self.bars = bars
	def nbeat (self): return sum ((bar.nbeat for bar in self.bars))
	def bar   (self, i):
		acc = accumulate (self.bars, lambda bar: bar.nbeat):
		for p, n in zip (acc[:-1], acc[1:]):
			if i >= p and i < n: return p
		raise Exception ()
class Bar:
	def __init__ (self, nbeat): self.nbeat = nbeat

class Meter:
	def __init__ (self, ss, sections):
		pass
	"""
	
	
	

class Song:
	@staticmethod
	def init_map (sections, song_structure):
		section_ret = []
		for section in sections:
			phrases, segments, bars, mappings1, mappings2 = apply_section (section)
			phrase_ret = []
			for phrase_no in section.phrases:
				phrase = phrases[phrase_no]
				segment_ret = []
				for segment_no in phrase.segments:
					segno = mappings1[phrase_no][segment_no]
					segment = segments[segno]
					bar_ret = []
					for bar_no in segment.bars:
						barno = mappings2[segno][bar_no]
						bar = bars[barno]
						bar_ret = bar_ret + [bar]
					segment_ret = segment_ret + [bar_ret]
				phrase_ret = phrase_ret + [segment_ret]
			section_ret = section_ret + [phrase_ret]
		return [(section, section_ret[section]) for section in song_structure.sections]
	def __init__ (self, sections, song_structure):
		self.sections       = sections
		self.song_structure = song_structure
		self.map            = Song.init_map (sections, song_structure)
def random_song (song_structure=None, sections=None, long_sections=None, short_sections=None):
	if not song_structure: song_structure = random_song_structure ()
	if not sections:
		if not long_sections: long_sections = [random_section (2) for _ in range (0, 3)]
		if not short_sections:
			#min_bar = min (bar.nbeat for phrase in long_sections for segment in phrase.segments for bar in segment.bars)
			#max_bar = max (bar.nbeat for phrase in long_sections for segment in phrase.segments for bar in segment.bars)
			#short_sections = [random_section (1, min_bar, max_bar) for _ in range (0, 3)]
			short_sections = [random_section (1) for _ in range (0, 3)]
		sections = long_sections + short_sections
	return Song (sections, song_structure)




























class Cadence:
	def __init__ (self, cp, arr):
		self.cp  = cp
		self.arr = arr
class Cadence4 (Cadence): # one chord per song
	def __init__ (self, arr):
		Cadence.__init__ (self, 4, arr)
		assert len (arr) == 1
	def elem (self): return self.arr[0]
class Cadence3 (Cadence): # one chord per song section
	def __init__ (self, arr): Cadence.__init__ (self, 3, arr)
	def elem (self, section_no): return self.arr[section_no]
class Cadence2 (Cadence): # one chord per phrase
	@staticmethod
	def init_map (song):
		mapping = []
		pn = 0
		for section_type, section in song:
			mapping_temp = []
			for phrase in section:
				mapping_temp = mapping_temp + [pn]
				pn = pn + 1
			mapping = mapping + [mapping_temp]
		return mapping
	def __init__ (self, arr, song_structure):
		Cadence.__init__ (self, 2, arr)
		self.map = Cadence2.init_map (song_structure)
		self.song_structure = song_structure
	def elem (self, section_no, phrase_no): 
		pn = self.map[section_no][phrase_no]
		return self.arr[pn]
class Cadence1 (Cadence): # one chord per segment, different pattern per section
	@staticmethod
	def init_map (song):
		uniq = {}
		for st, section in song:
			if st in uniq: continue
			uniq[st] = section
			
		mapping = {}
		for st, section in uniq.items ():
			mapping_temp = []
			pn = 0
			for phrase in section:
				phrase_temp = []
				for segment in phrase:
					phrase_temp = phrase_temp + [pn]
					pn = pn + 1
				mapping_temp = mapping_temp + [phrase_temp]
			mapping[st] = mapping_temp
			
		mapping2 = []
		for st, section in song:
			temp = mapping[st]
			mapping2 = mapping2 + [temp]
		return mapping2
	def __init__ (self, arr, song_structure):
		Cadence.__init__ (self, 1, arr)
		self.map = Cadence1.init_map (song_structure)
		self.song_structure = song_structure
	def elem (self, section_no, phrase_no, segment_no):
		pn  = self.map[section_no][phrase_no][segment_no]
		arr = self.arr[section_no]
		return arr[pn]
class Cadence0 (Cadence): # one chord per bar, different pattern per section
	@staticmethod
	def init_map (song):
		uniq = {}
		for st, section in song:
			if st in uniq: continue
			uniq[st] = section
		
		mapping = {}
		for st, section in uniq.items ():
			mapping_temp = []
			pn = 0
			for phrase in section:
				phrase_temp = []
				for segment in phrase:
					segment_temp = []
					for bar in segment:
						segment_temp = segment_temp + [pn]
						pn = pn + 1
					phrase_temp = phrase_temp + [segment_temp]
				mapping_temp = mapping_temp + [phrase_temp]
			mapping[st] = mapping_temp
			
		mapping2 = []
		for st, section in song:
			temp     = mapping[st]
			mapping2 = mapping2 + [temp]
		return mapping2
	def __init__ (self, arr, song_structure):
		Cadence.__init__ (self, 0, arr)
		self.map = Cadence0.init_map (song_structure)
		self.song_structure = song_structure
	def elem (self, section_no, phrase_no, segment_no, bar_no):
		pn  = self.map[section_no][phrase_no][segment_no][bar_no]
		arr = self.arr[section_no]
		#arr = list (chain (*arr))
		return arr[pn]
		
	
class HarmonicFunctionCadence4 (Cadence4):
	def __init__ (self, arr):
		Cadence4.__init__ (self, list (chain (*arr)))
		self.arr2 = arr
	def __repr__ (self): return "HarmonicFunctionCadence1 [arr=%s, arr2=%s]" % (self.arr, self.arr2)
	def nsegment  (self): return len (self.arr2)
	def nsegments (self): return self.nsegment ()
class HarmonicFunctionCadence3 (Cadence3):
	def __init__ (self, arr):
		Cadence3.__init__ (self, list (chain (*arr)))
		self.arr2 = arr
	def __repr__ (self): return "HarmonicFunctionCadence1 [arr=%s, arr2=%s]" % (self.arr, self.arr2)
	def nsegment  (self): return len (self.arr2)
	def nsegments (self): return self.nsegment ()
class HarmonicFunctionCadence2 (Cadence2):
	def __init__ (self, arr, song_structure):
		Cadence2.__init__ (self, list (chain (*arr)), song_structure)
		self.arr2 = arr
	def __repr__ (self): return "HarmonicFunctionCadence1 [arr=%s, arr2=%s]" % (self.arr, self.arr2)
	def nsegment  (self): return len (self.arr2)
	def nsegments (self): return self.nsegment ()
class HarmonicFunctionCadence1 (Cadence1):
	def __init__ (self, arrs, song_structure):
		Cadence1.__init__ (self, [list (chain (*arr)) for arr in arrs], song_structure)
		self.arr2 = arrs
	def __repr__ (self): return "HarmonicFunctionCadence1 [arr=%s, arr2=%s]" % (self.arr, self.arr2)
	def nsegment  (self, section_no): return len (self.arr2[section_no])
	def nsegments (self): return sum (len (arr) for arr in self.arr2)
class HarmonicFunctionCadence0 (Cadence0):
	def __init__ (self, arrs, song_structure):
		Cadence0.__init__ (self, [list (chain (*arr)) for arr in arrs], song_structure)
		self.arr2 = arrs
	def __repr__ (self): return "HarmonicFunctionCadence1 [arr=%s, arr2=%s]" % (self.arr, self.arr2)
	def nsegment  (self, section_no): return len (self.arr2[section_no])
	def nsegments (self): return sum (len (arr) for arr in self.arr2)
	
		
















harmonic_progression_db = {}
#@jit
def init_harmonic_progression_db (nc):
	if nc in harmonic_progression_db: return harmonic_progression_db[nc]
	if nc == 1:
		progression                 = [1]
		progressions                = [progression]
		harmonic_progression_db[nc] = progressions
		return progressions
	#print ("nc=%s" % nc, end="\n")
	# TODO get uniq lengths from chord_progression_db
	# TODO allow [1, 2, 3, 4], but filter sequences with too many 1s
	#arr          = [1, 2, 3, 4]
	arr           = [2, 3, 4]
	#arr          = []
	#arr          = arr + [1] * (nc // 1)
	#arr          = arr + [2] * (nc // 2)
	#arr          = arr + [3] * (nc // 3)
	#arr          = arr + [4] * (nc // 4)
	#progressions = printAllSubsets (arr, len (arr), nc)
	progressions = subsets (arr, nc)
	#progressions = [progression[::-1] for progression in progressions]
	progressions = list (progressions)
	harmonic_progression_db[nc] = progressions
	return progressions

#@jit
class HarmonicProgression: # harmonic rhythm
	def __init__ (self, harmonic_progression): self.harmonic_progression = harmonic_progression
	def __repr__ (self): return "HarmonicProgression [harmonic_progression=%s]" % self.harmonic_progression
def random_harmonic_progression (nc):
	if nc == 1: progression = [1]
	else:
		progressions = init_harmonic_progression_db (nc - 1)
		progression  = choice (progressions)
		progression  = [1] + progression
	return HarmonicProgression (progression)

# TODO chord_progression = T-T,
# T-D(-T), T-S(-T),
# T-S-D(-T), T-D-S(-T),
# T-S-D-S(-T), T-D-S-D(-T), T-S-S-D(-T), T-D-S-S(-T)
# I-vii-iii-vi-IV-ii-V => T-S-D-T-S-S-D(-T)
function_progression_db = [
	#[0],          # T(-T)
	#[0, 1],       # T-D(-T)
	#[0, 2],       # T-S(-T)
	#[0, 2, 1],    # T-S-D(-T)
	#[0, 1, 2],    # T-D-S(-T)
	#[0, 2, 2],    # T-S-S(-T)
	#[0, 1, 1],    # T-D-D(-T)
	#[0, 2, 2, 1], # T-S-S-D(-T)
	#[0, 2, 1, 2], # T-S-D-S(-T)
	#[0, 1, 2, 2], # T-D-S-S(-T)
	
	[0],          # T(-T)
	[1, 0],       # T-D(-T)
	[2, 0],       # T-S(-T)
	[2, 1, 0],    # T-S-D(-T)
	[1, 2, 0],    # T-D-S(-T)
	[2, 2, 0],    # T-S-S(-T)
	[1, 1, 0],    # T-D-D(-T)
	[2, 2, 1, 0], # T-S-S-D(-T)
	[2, 1, 2, 0], # T-S-D-S(-T)
	[1, 2, 2, 0], # T-D-S-S(-T)
]
#@jit
class FunctionProgression:
	def __init__ (self, progression): self.progression = progression
	def __repr__ (self): return "FunctionProgression [progression=%s]" % self.progression
def random_function_progression (harmonic_progression):
	progression = []
	for nsegment in harmonic_progression.harmonic_progression:
		if   nsegment == 1: segment =         function_progression_db[0]
		elif nsegment == 2: segment = choice (function_progression_db[1:3])
		elif nsegment == 3: segment = choice (function_progression_db[3:7])
		elif nsegment == 4: segment = choice (function_progression_db[7:])
		progression = progression + [segment]
		#progression = progression + segment
	return FunctionProgression (progression)






def increment_mode         (mode):
	mode, doctave = mode.increment ()
	assert mode is not None
	return mode
def increment_key          (mode):
	mode, doctave = mode.increment_key ()
	assert mode is not None
	return mode
def increment_scale        (mode):
	mode, doctave = mode.increment_scale ()
	assert mode is not None
	return mode
def brighter_mode          (mode):
	mode, doctave = mode.brighter ()
	assert mode is not None
	return mode
#def brighter_scale         (mode): return mode.brighter_scale ()
def brighter_key           (mode):
	mode, doctave = mode.brighter_key ()
	assert mode is not None
	return mode
def parallel_mode_brighter (mode):
	mode, doctave = mode.parallel_mode_brighter ()
	assert mode is not None
	return mode
#def fifth_key              (mode): pass
#def god_key                (mode): pass
modulation_brighter_db = [
	increment_mode,
	increment_key,
	increment_scale,
	brighter_mode,
	#brighter_scale,
	brighter_key,
	parallel_mode_brighter,
]	
	
def decrement_mode         (mode):
	mode, doctave = mode.decrement ()
	assert mode is not None
	return mode
def decrement_key          (mode):
	mode, doctave = mode.decrement_key ()
	assert mode is not None
	return mode
def decrement_scale        (mode):
	mode, doctave = mode.decrement_scale ()
	assert mode is not None
	return mode
def darker_mode            (mode):
	mode, doctave = mode.darker ()
	assert mode is not None
	return mode
#def darker_scale           (mode): return mode.darker_scale ()
def darker_key             (mode):
	mode, doctave = mode.darker_key ()
	assert mode is not None
	return mode
def parallel_mode_darker (mode):
	mode, doctave = mode.parallel_mode_darker ()
	assert mode is not None
	return mode
#def fourth_key             (mode): pass
#def god_key                (mode): pass
modulation_darker_db = [
	decrement_mode,
	decrement_key,
	decrement_scale,
	darker_mode,
	#darker_scale,
	darker_key,
	parallel_mode_darker,
]
def parallel_key_invert    (mode): pass
def relative_mode_invert   (mode): pass
def radiohead_mod          (mode): pass
def negative_mode          (mode): pass
def tritone_mod            (mode): pass
modulate_invert_db = [
	#parallel_key_invert,    # c major to c  minor
	                     # or c minor to c  major
	#relative_mode_invert,   # c major to a  minor
	                     # or c minor to eb major
	#radiohead_mod,          # c major to c# minor
	                     # or c minor to b  major
	#negative_mode,          # c major to e? phrygian
	#tritone_mod,            # b dim   to a  major ???
]

# TODO decide random insertion points for 0s
# subtract that number of points from nc in init_hue_cadence(nc)

class HueCadence: # nbrighter vs. ndarker
	def __init__ (self, pattern): self.pattern = pattern
	def __repr__ (self): return "HueCadence [pattern=%s]" % self.pattern
hue_cadence_db = {}
def init_hue_cadence_db (nc):
	if nc in hue_cadence_db: return hue_cadence_db[nc]
	if nc == 1:
		progression                 = [1]
		progressions                = [progression]
		hue_cadence_db[nc] = progressions
		return progressions
	#arr           = [1, 2, 3, 4]
	# TODO allow [1, !1, 1], but not [1, 1]
	arr           = [2, 3, 4]
	progressions = subsets (arr, nc)
	progressions = list (progressions)
	hue_cadence_db[nc] = progressions
	return progressions
def random_hue_cadence (nmodulation):
	progressions = init_hue_cadence_db (nmodulation)
	progression  = choice (progressions)
	assert sum (progression) == nmodulation
	return HueCadence (progression)
class HueRhythm: # brighter vs darker
	def __init__ (self, pattern): self.pattern = pattern
	def __repr__ (self): return "HueRhythm [pattern=%s]" % self.pattern
def random_hue_rhythm (nmodulation, hc=None, hcs0=None):
	if hc is None: hc = random_hue_cadence (nmodulation)
	#hcs = (-1, 1)
	# TODO remove 0 ?
	hcs = (-1, 0, 1)
	if hcs0 is None: hcs0 = hcs
	hue  = choice (hcs0)
	hues = []
	# TODO not more than one consecutive 0
	for nh in hc.pattern:
		#temp = [hue for _ in range (0, nh)]
		temp = [hue] * nh
		#temp = [hue]
		#hues = hues + [temp]
		hues = hues + temp
		while True:
			new_hue = choice (hcs)
			if new_hue != hue: break
		hue  = new_hue
	assert len (hues) == nmodulation
	return HueRhythm (hues)
class Hues:
	def __init__ (self, pattern): self.pattern = pattern
	def __repr__ (self): return "Hues [pattern=%s]" % self.pattern
def random_hues (fc, nmodulation, hr=None, hc=None, mode=None):
	if hr   is None: hr   = random_hue_rhythm (nmodulation, hc)
	if mode is None: mode = random_mode ()
	assert len (hr.pattern) == nmodulation
	modulations = []
	modes       = [mode]
	#print (fc)
	#print (hr.pattern)
	#print (nmodulation)
	# TODO handle chorus sections
	for f, hue in zip (chain (*fc), hr.pattern):
		#f = f[0]
		if   hue == 1:
			db = modulation_brighter_db
			# TODO
			#if is_minor (mode): db = db + modulate_invert_db
			temp = choice (db)
		elif hue == -1:
			db = modulation_darker_db
			# TODO
			#if is_major (mode): db = db + modulate_invert_db
			temp = choice (db)
		else: # hue == 0
			# TODO modulate to enharmonic scale/mode
			# TODO make 0s sparse
			temp = lambda mode: mode
		modulations = modulations + [temp]
		mode        = temp (mode)
		assert mode is not None
		modes       = modes + [mode]
	return modes
def random_hues1 (fc):
	ss = fc.song_structure
	chord_progressions = {}
	nmodulation = 0
	for sts, section_no in zip (ss, range (0, len (ss))):
		st, section = sts
		nsegment = fc.nsegment (section_no)
		nmodulation = nmodulation + nsegment
		if st in chord_progressions: continue
		#segments = fc.arr2[section_no]
		#nsegment = len (segments)
		#print (len (fc.arr[section_no]))
		#print (len (fc.arr2[section_no]))
		#print ()
		if st == 1: hcs = (1,  0)
		else:       hcs = (0, -1)
		hr       = random_hue_rhythm (nsegment, None, hcs)
		# TODO random_hues
		chord_progressions[st] = hr
		
	mapping2 = []	
	for st, section in ss:
		temp     = chord_progressions[st]
		mapping2 = mapping2 + temp.pattern
	assert len (mapping2) == nmodulation
	mapping2 = mapping2[:-1]
	hr = HueRhythm (mapping2)
	#assert len (hr.pattern) == nmodulation
	assert len (hr.pattern) == nmodulation - 1
	
	#print ("nmodulation=%s" % nmodulation)
	
	#nmodulation = sum ((len (arr) for arr in fc.arr2))
	#modulations = random_hues (fc.arr, nmodulation, mapping2)
	#return Cadence1 (mapping2, ss)
	#modulations = random_hues (fc.arr2, nmodulation, hr)
	# TODO these need to be computed by section ?
	modulations = random_hues (fc.arr2, nmodulation - 1, hr)
	print (len (modulations))
	print (nmodulation)
	assert len (modulations) == nmodulation
	return modulations
def random_hues0 (fc):
	ss = fc.song_structure
	chord_progressions = {}
	nmodulation = 0
	for sts, section_no in zip (ss, range (0, len (ss))):
		st, section = sts
		nsegment = fc.nsegment (section_no)
		nmodulation = nmodulation + nsegment
		if st in chord_progressions: continue
		#segments = fc.arr2[section_no]
		#nsegment = len (segments)
		if st == 1: hcs = (1,  0)
		else:       hcs = (0, -1)
		hr       = random_hue_rhythm (nsegment, None, hcs)
		chord_progressions[st] = hr
		
	#print ("nmodulation=%s" % nmodulation)
		
	mapping2 = []
	for st, section in ss:
		temp     = chord_progressions[st]
		mapping2 = mapping2 + temp.pattern
		#nmodulation = nmodulation + len (temp.pattern)
	mapping2 = mapping2[:-1]
	mapping2 = HueRhythm (mapping2)
	
	#nmodulation = sum ((len (arr) for arr in fc.arr2))
	#modulations = random_hues (fc.arr, nmodulation, mapping2)
	#return Cadence0 (mapping2, ss)
	#return random_hues (fc.arr2, nmodulation, mapping2)
	# TODO these need to be computed by section ?
	modulations = random_hues (fc.arr2, nmodulation - 1, mapping2)
	assert len (modulations) == nmodulation
	return modulations


"""
# TODO modulation pattern given number of function progression fragments
#@jit
class ModulationRythym:
	def __init__ (self, mr): self.mr = mr
def random_modulation_rhythm (nfp):
	m = random_bjorklund2 (nfp)
	return ModulationRythym (m)
#@jit
class Modulations:
	def __init__ (self, modulations): self.modulations = modulations
def random_modulations (nfp, mr=None):
	if not mr: mr = random_modulation_rhythm (nfp)
	mp = [choice (modulation_db) for s in mr.mr if s]
	#mp = [m () for m in mp]
	return Modulations (mp)
	#elif sp.cp in [3, 4]:
	#	uniq = {}
	#	for st, section in song:
	#		if st in uniq: continue
	#		uniq[st] = section
	#		
	#	mps = {}
	#	for st, section in uniq.items ():
	#		nfp     = 
	#		nm      = random_nmodulation (nfp)
	#		m       = bjorklund (nm, nfp)
	#		# TODO reverse, rotate
	#		mp      = [choice (modulation_db) for s in m if s]
	#		mps[st] = mp
	#	return mps
"""
	
#	
# TODO
#class ChordProgression:
#	def __init__ (self, chords):
#		self.chords = chords
#def random_chord_progression (function_progression, mode=None):
#	if not mode: mode = random_mode ()
#	nnote = len (mode.scale.intervals)
#	# TODO first and last chord are consonances
#	# TODO 
#
#def apply_chord_progression (cp, chord_progression):
#	# TODO modulations
#	# TODO borrow chords... now or per verse?
#	# TODO handle chorus and/or song end
#	# TODO voice leading
#	# TODO polytonality
#	pass

# TODO where 0s are: modulations to same scales that are modes of this one, but with different tetrachords
# TODO modulations to scales composed of different tetrachords than this one

class BorrowRhythm:
	def __init__ (self, pattern): self.pattern = pattern
def random_borrow_rhythm (segments):
	mapping = {}
	j = 0 # number of segments which can contain borrowed chords
	k = 0 # number of chords   which can be      borrowed chords
	# TODO maybe allow borrowing on [0]
	for i in range (0, len (segments)):
		nchord = len (segments[i])
		if nchord == 1: continue
		mapping[j] = i
		j = j + 1
		k = k + nchord
	assert j <= k
	n = max (int (2 / 3 * k) + 1, j)
	#assert n < j
	bj = random_bjorklund2 (n)
	return mapping, BorrowRhythm (bj)
class BorrowCadence:
	def __init__ (self, pattern): self.pattern = pattern
def random_borrow_cadence (br):
	pattern = []
	for bit in br.pattern:
		if bit:
			if random_bool (): temp = [ 1]
			else:              temp = [-1]
			# TODO augmented and diminished ?
			# TODO tension vs. resolution ?
			pattern = pattern + temp
		else: pattern = pattern + [0]
	return BorrowCadence (pattern)
# TODO maybe a layer of increasing/decreasing cadence to smooth it out
# secondary dominant ?
# major/minor ?
# given: mode, modulation hue, chord function, when borrowing should occur
class BorrowHue:
	def __init__ (self, pattern): self.pattern = pattern
def random_borrow_hue (bc, modes):
	# TODO
	#assert len (bc.pattern) == len (modes)
	# given previous mode, previous chord function
	# given current  mode, current  chord function
	# given next     mode, next     chord function
	# given borrow hue, either 1 or -1
	# if previous mode is enharmonic to next mode
	# then current mode should be different
	# else current mode should borrow a chord that's in previous or next
	modulations = []
	for hue, mode in zip (bc.pattern, modes):
		if   hue ==  1:
			db = modulation_brighter_db
			modulation = choice (db)
			modulation = modulation (mode)
		elif hue == -1:
			db = modulation_darker_db
			modulation = choice (db)
			modulation = modulation (mode)
		elif hue ==  0: modulation = mode
		else: raise Exception (hue)
		modulations = modulations + [modulation]
	return BorrowHue (modulations)
# TODO each layer should be able to be divided in this way		
def random_borrow_pattern0 (sp, ss, bc=None, br=None): # by song
	fc    = sp.function_cadence
	modes = sp.modulations
	
	segments = []
	#ss = fc.song_structure
	bcs = {}
	nborrow = 0
	for sts, section_no in zip (ss, range (0, len (ss))):
		st, section = sts
		nsegment = sum ((len (phrase) for phrase in section))
		segments = segments + [segment for phrase in section for segment in phrase]
		nchord   = sum ((len (segment) for phrase in section for segment in phrase))
		nborrow = nborrow + nchord
		# for v1
		#if st in bcs: continue
		#if bcs[st] is None:
		#	if brs[st] is None: brs[st] = random_borrow_rhythm (nchord)
		#	bcs[st] = random_borrow_cadence (brs)
		#	#bhs[st] = random_borrow_hue (bcs[st], modes) # TODO modes of this section
	#print (nborrow)
	# for v0
	if bc is None:
		#if br is None: br = random_borrow_rhythm (nborrow)
		if br is None: mapping, br = random_borrow_rhythm (segments)
		bc = random_borrow_cadence (br)
	return random_borrow_hue (bc, modes) # TODO modes of all sections
	# for v1
	#mapping2 = []
	#for st, section in ss:
	#	temp     = bcs[st]
	#	mapping2 = mapping2 + temp.pattern
	#return random_borrow_hue (mapping2, modes)
def random_borrow_pattern1 (sp, ss, bcs=None, brs=None): # by section
	fc    = sp.function_cadence
	modes = sp.modulations
	
	#ss = fc.song_structure
	if brs is None: brs = {}
	if bcs is None: bcs = {}
	nborrow = 0
	for sts, section_no in zip (ss, range (0, len (ss))):
		st, section = sts
		nsegment = sum ((len (phrase) for phrase in section))
		segments = [segment for phrase in section for segment in phrase]
		nchord   = sum ((len (segment) for phrase in section for segment in phrase))
		nborrow = nborrow + nchord
		# for v1
		if st in bcs: continue
		#if st not in brs: brs[st] = random_borrow_rhythm (nchord)
		if st not in brs: mapping, brs[st] = random_borrow_rhythm (segments)
		bcs[st] = random_borrow_cadence (brs[st])
		#bhs[st] = random_borrow_hue (bcs[st], modes) # TODO modes of this section
	# for v0
	#if bc is None:
	#	if br is None: br = random_borrow_rhythm (nborrow)
	#	bc = random_borrow_cadence (br)
	#return random_borrow_hue (bc, modes) # TODO modes of all sections
	# for v1
	mapping2 = []
	for st, section in ss:
		temp     = bcs[st]
		print (temp.pattern)
		mapping2 = mapping2 + temp.pattern
	bc = BorrowCadence (mapping2)
	return random_borrow_hue (bc, modes)
def random_borrow_pattern (sp, song):
	bp = randrange (0, 2)
	if   bp == 0: return random_borrow_pattern0 (sp, song)
	elif bp == 1: return random_borrow_pattern1 (sp, song)
		
class SongProgression2:
	def __init__ (self, sp, borrows):
		self.song_progression = sp
		self.borrows          = borrows
	def mode (self, bar_no): return self.borrows.pattern[bar_no]
def random_song_progression2 (sp, song):
	#if sp is None: sp = random_song_progression ()
	borrows = random_borrow_pattern (sp, song)
	return SongProgression2 (sp, borrows)
		
		
		
		
		
		
		
		
# decide borrow cadence for song structure:
# - cadence for whole song
# - cadence for each section

# voice leading ?
# TODO how to select chords/inversions?


"""
#@jit
class SongProgression:
	def __init__ (self, cp): self.cp = cp
	#def chord (section_no, phrase_no, segment_no, bar_no): raise Exception ()
#@jit
class SongProgression4 (SongProgression):
	def __init__ (self, chord_progression, modulations):
		SongProgression.__init__ (self, 4)
		self.chord_progression = chord_progression
		self.modulations       = modulations
		
		#if len (chord_progression.progression) != 1: raise Exception (len (chord_progression.progression))
	#def chord (section_no, phrase_no, segment_no, bar_no): return chord_progression[0]
	def chord      (self): return self.chord_progression.progression[0]
	def modulation (self): return self.modulations[0]
#@jit
class SongProgression3 (SongProgression):
	def __init__ (self, chord_progression, modulations):
		SongProgression.__init__ (self, 3)
		self.chord_progression = chord_progression
		self.modulations       = modulations
	#def chord (section_no, phrase_no, segment_no, bar_no): return chord_progression[section_no]
	def chord      (self, section_no):
		progression = self.chord_progression.progression
		progression = list (chain (*progression))
		return progression[section_no]
	def modulation (self, section_no): return self.modulations[section_no]
#@jit
class SongProgression2 (SongProgression):
	def __init__ (self, chord_progression, modulations, song):
		SongProgression.__init__ (self, 2)
		self.chord_progression = chord_progression
		self.modulations       = modulations
		self.map               = SongProgression2.init_map (song)
	@staticmethod
	def init_map (song):
		mapping = []
		pn = 0
		for section_type, section in song:
			mapping_temp = []
			for phrase in section:
				mapping_temp = mapping_temp + [pn]
				pn = pn + 1
			mapping = mapping + [mapping_temp]
		return mapping
	#def chord (section_no, phrase_no, segment_no, bar_no):
	def chord     (self, section_no, phrase_no):
		pn          = self.map[section_no][phrase_no]
		progression = self.chord_progression.progression
		progression = list (chain (*progression))
		return progression[pn]
	def modulaton (self, section_no, phrase_no):
		pn          = self.map[section_no][phrase_no]
		return self.modulations[pn]
#@jit
class SongProgression1 (SongProgression):
	def __init__ (self, chord_progressions, modulations, song):
		SongProgression.__init__ (self, 1)
		self.chord_progressions = chord_progressions
		self.modulations        = modulations
		self.map                = SongProgression1.init_map (song)
	@staticmethod
	def init_map (song):
		uniq = {}
		for st, section in song:
			if st in uniq: continue
			uniq[st] = section
		
		#mapping = []
		mapping = {}
		for st, section in uniq.items ():
			mapping_temp = []
			pn = 0
			for phrase in section:
				phrase_temp = []
				#pn = 0
				for segment in phrase:
					#segment_temp = []
					#for bar in segment:
					#	segment_temp = segment_temp + [pn]
					#	pn = pn + 1
					#phrase_temp = phrase_temp + [segment_temp]
					phrase_temp = phrase_temp + [pn]
					pn = pn + 1
				mapping_temp = mapping_temp + [phrase_temp]
			#mapping = mapping + [mapping_temp]
			mapping[st] = mapping_temp
			
		mapping2 = []
		for st, section in song:
			temp = mapping[st]
			mapping2 = mapping2 + [temp]
		return mapping2
	#def chord (section_no, phrase_no, segment_no, bar_no):
	def chord      (self, section_no, phrase_no, segment_no):
		pn          = self.map[section_no][phrase_no][segment_no]
		progression = self.chord_progressions[section_no]
		progression = progression.progression
		#print ("progression=%s" % progression.progression, end="\n")
		#print ("pn=%s" % pn, end="\n")
		progression = list (chain (*progression))
		return progression[pn]
	def modulation (self, section_no, phrase_no, segment_no):
		pn          = self.map[section_no][phrase_no][segment_no]
		modulations = self.modulations[section_no]
		return modulations[pn]
#@jit
class SongProgression0 (SongProgression):
	def __init__ (self, chord_progressions, modulations, song):
		SongProgression.__init__ (self, 0)
		self.chord_progressions = chord_progressions
		self.modulations        = modulations
		self.map                = SongProgression0.init_map (song)
	@staticmethod
	def init_map (song):
		uniq = {}
		for st, section in song:
			if st in uniq: continue
			uniq[st] = section
		
		#mapping = []
		mapping = {}
		for st, section in uniq.items ():
			mapping_temp = []
			pn = 0
			for phrase in section:
				phrase_temp = []
				for segment in phrase:
					segment_temp = []
					for bar in segment:
						segment_temp = segment_temp + [pn]
						pn = pn + 1
					phrase_temp = phrase_temp + [segment_temp]
				mapping_temp = mapping_temp + [phrase_temp]
			#mapping = mapping + [mapping_temp]
			mapping[st] = mapping_temp
			
		mapping2 = []
		for st, section in song:
			temp     = mapping[st]
			mapping2 = mapping2 + [temp]
		return mapping2
	def chord      (self, section_no, phrase_no, segment_no, bar_no):
		pn          = self.map[section_no][phrase_no][segment_no][bar_no]
		progression = self.chord_progressions[section_no]
		progression = progression.progression
		progression = list (chain (*progression))
		return progression[pn]
	def modulation (self, section_no, phrase_no, segment_no, bar_no):
		pn          = self.map[section_no][phrase_no][segment_no][bar_no]
		modulations = self.modulations[section_no]
		return modulations[pn]
"""





class SongProgression:
	@staticmethod
	def init_map (fc, modes):
		mapping = []
		m_no = 0
		if fc.cp in [2, 3, 4]:
			for arr in fc.arr2:
				temp = [m_no] * len (arr)
				mapping = mapping + temp
				m_no = m_no + 1
			assert m_no == len (fc.arr2)
			assert len (mapping) == sum ((len (arr) for arr in fc.arr2))
		elif fc.cp in [0, 1]:
			for arrs in fc.arr2:
				for arr in arrs:
					temp = [m_no] * len (arr)
					mapping = mapping + temp
					m_no = m_no + 1
			assert m_no == sum ((len (arr) for arr in fc.arr2))
			assert len (mapping) == sum ((sum ((len (a) for a in arr)) for arr in fc.arr2))
		#print (m_no)
		#print (len (modes))
		assert m_no == len (modes)
		return mapping
	def __init__ (self, function_cadence, modulations): #, borrows):
		self.function_cadence = function_cadence
		self.modulations      = modulations
		#self.borrows          = borrows
		self.map              = SongProgression.init_map (function_cadence, modulations)
	def __repr__ (self): return "SongProgression [%s, modulations=%s, map=%s]" % (self.function_cadence, self.modulations, self.map)
	def mode (self, bar_no):
		i = self.map[bar_no]
		#print ("%s / %s,   %s / %s" % (bar_no, len (self.map), i, len (self.modulations)))
		assert i < len (self.modulations)
		return self.modulations[i]
	#def mode2 (self, bar_no):
	#	i = self.map2[bar_no]
	#	assert i < len (self.borrows)
	#	return self.borrows[i]
		
def random_function_cadence_4 (song):
	nchord                  = 1
	print ("nchord: %s" % nchord, end="\n")
	harmonic_progression    = random_harmonic_progression (nchord)
	print ("harmonic progression: %s" % harmonic_progression.harmonic_progression, end="\n")
	function_progression    = random_function_progression (harmonic_progression)
	print ("function progression: %s" % function_progression.progression, end="\n")
	return HarmonicFunctionCadence4 (function_progression.progression)
def random_function_cadence_3 (song):
	nverse                  = len (song)
	print ("nverse: %s" % nverse, end="\n")
	harmonic_progression    = random_harmonic_progression (nverse)
	print ("harmonic progression: %s" % harmonic_progression.harmonic_progression, end="\n")
	function_progression    = random_function_progression (harmonic_progression)
	print ("function progression: %s" % function_progression.progression, end="\n")
	return HarmonicFunctionCadence3 (function_progression.progression)
def random_function_cadence_2 (song):
	nphrase                 = sum ((len (section) for st, section in song))
	print ("nphrase: %s" % nphrase, end="\n")
	harmonic_progression    = random_harmonic_progression (nphrase)
	print ("harmonic progression: %s" % harmonic_progression.harmonic_progression, end="\n")
	function_progression    = random_function_progression (harmonic_progression)
	print ("function progression: %s" % function_progression.progression, end="\n")
	return HarmonicFunctionCadence2 (function_progression.progression, song)
def random_function_cadence_1 (song):
	uniq = {}
	for st, section in song:
		if st in uniq: continue
		uniq[st] = section
	
	chord_progressions = {}
	for st, section in uniq.items ():
		nsegment               = sum ((len (phrase) for phrase in section))
		print ("nsegment: %s" % nsegment, end="\n")
		harmonic_progression   = random_harmonic_progression (nsegment)
		print ("harmonic progression: %s" % harmonic_progression.harmonic_progression, end="\n")
		function_progression   = random_function_progression (harmonic_progression)
		print ("function progression: %s" % function_progression.progression, end="\n")
		chord_progressions[st] = function_progression.progression
		
	mapping2 = []
	for st, section in song:
		temp     = chord_progressions[st]
		mapping2 = mapping2 + [temp]
		
	return HarmonicFunctionCadence1 (mapping2, song)
def random_function_cadence_0 (song):
	uniq = {}
	for st, section in song:
		if st in uniq: continue
		uniq[st] = section
		
	chord_progressions = {}
	for st, section in uniq.items ():
		nbar                   = sum ((len (segment) for phrase in section for segment in phrase))
		print ("nbar: %s" % nbar, end="\n")
		harmonic_progression   = random_harmonic_progression (nbar)
		print ("harmonic progression: %s" % harmonic_progression.harmonic_progression, end="\n")
		function_progression   = random_function_progression (harmonic_progression)
		print ("function progression: %s" % function_progression.progression, end="\n")
		chord_progressions[st] = function_progression.progression

	mapping2 = []
	for st, section in song:
		temp     = chord_progressions[st]
		mapping2 = mapping2 + [temp]
	
	return HarmonicFunctionCadence0 (mapping2, song)
def random_song_progression (song, cp=None):
	if cp is None: cp = randrange (0, 5)
	if   cp == 4: # by song (one chord for whole song)
		function_cadence = random_function_cadence_4 (song)
		#nfp                     = len (function_cadence.arr)
		#modulations             = random_modulations (nfp)
		#modulations = random_hues (function_cadence.arr, nfp)
		modulations = random_hues (function_cadence.arr2, function_cadence.nsegments () - 1)
		assert len (modulations) == function_cadence.nsegments ()
		#modulations = []
		#song_progression        = SongProgression4 (function_progression, modulations)
		#song_progression        = SongProgression (function_cadence, modulations)
		#print ("song progression: %s" % song_progression, end="\n")
		#return (cp, song_progression) 
		#borrows                 = random_borrow_pattern0 (function_cadence, modulations)
	elif cp == 3: # by verse (one chord for whole verse => chord progression for song)
		function_cadence = random_function_cadence_3 (song)
		#nfp                     = len (function_cadence.arr)
		#modulations             = random_modulations (nfp)
		#modulations = random_hues (function_cadence.arr, nfp - 1)
		#modulations = random_hues (function_cadence.arr, nfp)
		modulations = random_hues (function_cadence.arr2, function_cadence.nsegments () - 1)
		assert len (modulations) == function_cadence.nsegments ()
		#song_progression        = SongProgression3 (function_progression, modulations)
		#song_progression        = SongProgression (function_cadence, modulations)
		#print ("song progression: %s" % song_progression, end="\n")
		#return (cp, song_progression)
		#borrows                 = random_borrow_pattern0 (function_cadence, modulations)
	elif cp == 2: # by phrase (one chord per phrase => chord progression for song)
		function_cadence = random_function_cadence_2 (song)
		#nfp                     = len (function_cadence.arr)
		#modulations             = random_modulations (nfp)
		#modulations = random_hues (function_cadence.arr, nfp - 1)
		#modulations = random_hues (function_cadence.arr, nfp)
		modulations = random_hues (function_cadence.arr2, function_cadence.nsegments () - 1)
		assert len (modulations) == function_cadence.nsegments ()
		#song_progression        = SongProgression2 (function_progression, modulations, song)
		#song_progression        = SongProgression (function_cadence, modulations)
		#print ("song progression: %s" % song_progression, end="\n")
		#return (cp, song_progression)
		#borrows                 = random_borrow_pattern0 (function_cadence, modulations)
	elif cp == 1: # by semi-phrase (chord progression for verse)
		"""
		uniq = {}
		for st, section in song:
			if st in uniq: continue
			uniq[st] = section
		
		#chord_progressions = []
		chord_progressions = {}
		modulations        = {}
		for st, section in uniq.items ():
			nsegment               = sum ((len (phrase) for phrase in section))
			print ("nsegment: %s" % nsegment, end="\n")
			harmonic_progression   = random_harmonic_progression (nsegment)
			print ("harmonic progression: %s" % harmonic_progression.harmonic_progression, end="\n")
			function_progression   = random_function_progression (harmonic_progression)
			print ("function progression: %s" % function_progression.progression, end="\n")
			#song_progression     = SongProgression1 (chord_progression, song)
			#print ("song progression: %s" % song_progression, end="\n")
			#chord_progressions = chord_progressions + [song_progression]
			#chord_progressions = chord_progressions + [chord_progression]
			chord_progressions[st] = function_progression
			nfp                    = len (function_progression.progression)
			modulation             = random_modulations (nfp)
			modulations[st]        = modulation
			
		mapping2 = []
		mapping3 = []
		for st, section in song:
			#temp = uniq[st]
			#temp = chord_progressions[temp]
			temp     = chord_progressions[st]
			mapping2 = mapping2 + [temp]
			
			temp     = modulations[st]
			mapping3 = mapping3 + [temp]
			"""
			
		#function_cadence = Cadence1 (mapping2, song)
		function_cadence = random_function_cadence_1 (song)
		#for ? in function_cadence
		#modulations      = mapping3
		modulations = random_hues1 (function_cadence)
		assert len (modulations) == function_cadence.nsegments ()
			
		#song_progression = SongProgression1 (mapping2, mapping3, song)
		#song_progression = SongProgression (function_cadence, mapping3)
		#return (cp, song_progression)
		#borrows                 = random_borrow_pattern1 (function_cadence, modulations)
	elif cp == 0: # by measure (chord progression for verse)
		"""
		uniq = {}
		for st, section in song:
			if st in uniq: continue
			uniq[st] = section
			
		chord_progressions = {}
		modulations        = {}
		for st, section in uniq.items ():
			nbar                   = sum ((len (segment) for phrase in section for segment in phrase))
			print ("nbar: %s" % nbar, end="\n")
			harmonic_progression   = random_harmonic_progression (nbar)
			print ("harmonic progression: %s" % harmonic_progression.harmonic_progression, end="\n")
			function_progression   = random_function_progression (harmonic_progression)
			print ("function progression: %s" % function_progression.progression, end="\n")
			#chord_progression     = SongProgression0 (function_progression)
			#print ("song progression: %s" % chord_progression, end="\n")
			chord_progressions[st] = function_progression
			
			nfp                    = len (function_progression.progression)
			modulation             = random_modulations (nfp)
			modulations[st]        = modulation
		
		mapping2 = []
		mapping3 = []
		for st, section in song:
			#temp = uniq[st]
			#temp = chord_progressions[temp]
			temp     = chord_progressions[st]
			mapping2 = mapping2 + [temp]
			
			temp     = modulations[st]
			mapping3 = mapping3 + [temp]
			"""
		
		#function_cadence = Cadence0 (mapping2, song)
		function_cadence = random_function_cadence_0 (song)
		modulations      = random_hues0 (function_cadence)
		assert len (modulations) == function_cadence.nsegments ()
		#modulations      = mapping3
		
		#song_progression = SongProgression0 (mapping2, mapping3, song)
		#song_progression = SongProgression (function_cadence, mapping3)
		#return (cp, song_progression)
		#borrows                 = random_borrow_pattern1 (function_cadence, modulations)
	#if   cp in [2, 3, 4]:
	#	nfp                     = len (function_cadence.arr)
	#	modulations             = random_modulations (nfp)
		
	#song_progression = SongProgression (function_cadence, modulations, borrows)
	song_progression = SongProgression (function_cadence, modulations)
	return (cp, song_progression)


# TODO
#@jit
class ChordProgression:
	def __init__ (self, chords):
		self.chords = chords
#def random_chord_progression (function_progression, mode=None):
#	if not mode: mode = random_mode ()
#	nnote = len (mode.scale.intervals)
#	# TODO first and last chord are consonances
#	# TODO 

def apply_chord_progression (cp, chord_progression):
	# TODO modulations
	# TODO borrow chords... now or per verse?
	# TODO handle chorus and/or song end
	# TODO voice leading
	# TODO polytonality
	pass
	
if __name__ == "__main__":
	#for song1 in range (0, len (songs_db)):
	#	for song2 in range (song1 + 1, len (songs_db)):
	#		if songs_db[song1] == songs_db[song2]:
	#			print (song1)
	#			print (song2)
	#			raise Exception ()
	
	def main (cp=None):
		song1 = random_song ()
		#song2 = apply_song (song1)
		song2 = song1.map
		cp, chord_progression = random_song_progression (song2, cp)
		sp = random_song_progression2 (chord_progression, song2)
		#chord_progression = chord_progression.progression
		section_no = 0
		measure_no = 0
		borrow_ndx = 0
		print ("cp=%s" % cp, end="\n")
		print ("chord progression: %s" % chord_progression, end="\n")
		# one chord for the whole song
		if cp == 4: print ("%s %s" % (chord_progression.function_cadence.elem (), chord_progression.mode (0)), end="\n")
		for section_type, section in song2:
			if   section_type == 0: section_type = "verse"
			elif section_type == 1: section_type = "chorus"
			elif section_type == 2: section_type = "bridge"
			elif section_type == 3: section_type = "intro"
			elif section_type == 4: section_type = "outro"
			elif section_type == 5: section_type = "pre"
			print (section_type, end="\n")
			#if   cp == 2: chord_no = 0
			#elif cp == 3: print ("%s" % chord_progression.chord (section_no), end="\n")
			# one chord per section
			if cp == 3:
				print ("%2s %2s" % (chord_progression.function_cadence.elem (section_no), chord_progression.mode (section_no)), end="\n")
				measure_no = measure_no + 1
			phrase_no = 0
			for phrase in section:
				if cp == 0: # one chord per measure
					segment_no = 0
					for segment in phrase:
						bar_no = 0
						for bar in segment:
							print ("%2s %2s" % (chord_progression.function_cadence.elem (section_no, phrase_no, segment_no, bar_no), chord_progression.mode (measure_no)), end=" ")
							bar_no = bar_no + 1
							measure_no = measure_no + 1
						segment_no = segment_no + 1
						print (end="    ")
					print (end="\n")
				elif cp == 1: # one chord per segment
					segment_no = 0
					for segment in phrase:
						print ("%2s %2s" % (chord_progression.function_cadence.elem (section_no, phrase_no, segment_no), chord_progression.mode (measure_no)), end="    ")
						segment_no = segment_no + 1
						measure_no = measure_no + 1
					print (end="\n")
				elif cp == 2: # one chord per phrase
					print ("%2s %2s" % (chord_progression.function_cadence.elem (section_no, phrase_no), chord_progression.mode (measure_no)), end="\n")
					measure_no = measure_no + 1
					
				for segment in phrase:
					for bar in segment:
						print ("%5s" % sp.mode (borrow_ndx), end=" ")
						borrow_ndx = borrow_ndx + 1
					print (end="    ")
				print (end="\n")
					
				for segment in phrase:
					for bar in segment:
						print ("%5s" % bar.nbeat, end=" ")
					print (end="    ")
				print (end="\n")
				phrase_no = phrase_no + 1
			print (end="\n")
			section_no = section_no +  1
		print (end="\n")
		print (end="\n")
	for cp in (4, 3, 2, 1, 0): main (cp)
