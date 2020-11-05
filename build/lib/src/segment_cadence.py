#! /usr/bin/env python3

from enum      import Enum
#from numba     import jit
from random    import choice, randrange, shuffle
from itertools import accumulate, chain, permutations

from math import factorial

from section_type import SectionType, short_section, long_section, INTRO, VERSE, PRE, CHORUS, BRIDGE, OUTRO
from random_util import subsets, random_bjorklund2, random_bool
#from song        import random_song#, apply_song
#from mode        import random_mode

from av import random_av

# each separate layer proves to be a unique nightmare to implement,
# encapsulating approximately one hell per layer.
# hashing is used to moderate the combinatorial explosion,
# and implements the concept of motifs



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

from pattern import Pattern
from song_structure import random_song_structure
from cadence import Cadence
from song_cadence0 import random_sc0
from song_cadence import random_song_cadence
from section_cadence import random_section_cadences, cadence_helper05
from phrase_cadence import random_phrase_cadences
			
# segment cadence: ~2 bars/measures
# one more layer of hash function will map from the segment cadence's bars to actual measure lengths
# segment_no => hash => bar_no

segment_db = (
	((0,),),          # one   bar
	((0, 0),        # two   bars, same      cadence
	 (0, 1),),       # two   bars, different cadence
	((0, 0, 0),     # three bars, same      cadence
	 (0, 0, 1),     # three bars, last  different
	 (0, 1, 1),),    # three bars, first different
	((0, 0, 0, 1),  # four  bars, last  different
	 (0, 0, 1, 1),  # four  bars, last two different
	 (0, 1, 0, 1),  # four  bars, every other is different
	 (0, 1, 1, 1),), # four  bars, first different
)
class SegmentCadence (Cadence):
	@staticmethod
	def init_spmap (sc, m):
		segment_no = 0
		spmap = []
		for phrase_no in sc.all_segments ():
			#print ("phrase_no: %s" % (phrase_no,))
			phrase = m[phrase_no]
			dp = len (phrase)
			temp  = [(phrase_no, k) for k in range (0, dp)]
			spmap = spmap + temp
			segment_no = segment_no + dp
			phrase_no = phrase_no + 1
		spmap = tuple (spmap)
		assert len (spmap) == segment_no
		return spmap
	@staticmethod
	def init_psmap (sc, m):
		segment_no = 0
		pn  = 0
		psmap = []
		for phrase_no in sc.all_segments ():
			phrase = m[phrase_no]
			dp     = len(phrase)
			temp = tuple (range (segment_no, segment_no + dp))
			psmap = psmap + [temp]
			segment_no = segment_no + dp
			pn = pn + 1
		psmap = tuple (psmap)
		assert len (psmap) == pn
		return psmap
	def __init__ (self, pc, m):
		Cadence.__init__ (self, m, pc.all_segments ())
		self.pc = pc
		self.bs = SegmentCadence.init_spmap (pc, m)
		self.sb = SegmentCadence.init_psmap (pc, m)
		assert len (self.bs) == self.nbar ()
		assert len (self.sb) == self.nsegment ()	
	def __repr__ (self): return "SegmentCadence [%s, pc=%s]" % (Cadence.__repr__ (self), self.pc)
	
	def nsection (self): return self.pc.nsection ()
	def nphrase (self): return self.pc.nphrase ()
	def nsegment (self): return self.pc.nsegment ()
	def nuniq_segment (self): return self.pc.nuniq_segment ()
	def nuniq_phrase (self): return self.pc.nuniq_phrase ()
	def nuniq_section (self): return self.pc.nuniq_section ()	
	
	def nbar (self): return len (self.all_bars ())
	def nuniq_bar (self): return len (set (self.all_bars ()))
		
	def segment_elems (self, phrase_no):
		phrase = self.pattern (phrase_no)
		fuck = self.uniq[phrase]
		return fuck
	def all_segments (self): return iter (self) # return Cadence.all (self)
	def bar_elem (self, segment_no):
		assert segment_no < self.nbar ()
		phrase_no, i = self.bs[segment_no]
		assert phrase_no < self.nsegment ()
		phrase = self.uniq[phrase_no]
		assert i < len (phrase)
		return phrase[i]
	def all_bars (self): return tuple (chain (*self.all_segments ()))
	def phrase_elem (self, section_no):
		phrase_nos = self.pc.phrase_elems (section_no)
		return tuple (map (lambda x: self.uniq[x], phrase_nos))
	def all_phrases (self):
		for section in self.pc.all_phrases ():
			section = tuple (section)
			yield tuple (map (lambda x: self[x], section))

	def all_sections (self):
		for section in self.pc.all_sections ():
			yield tuple (tuple (map (lambda x: self[x], phrase)) for phrase in section)
	def section_elem (self, section_no):	
		section = self.pc.section_elem (section_no)
		return tuple (tuple (map (lambda x: self[x], phrase)) for phrase in section)
		
	def section_types (self): return tuple ((st, tuple (tuple (map (lambda x: self[x], phrase)) for phrase in section)) for st, section in self.pc.section_types ())
	def all_section_types (self): return self.pc.all_section_types ()
	
	def first_section (self): return 0, tuple (self.section_elem (0))
	def  last_section (self):
		n = self.nsection ()
		assert tuple (self.section_elem (n - 1)) == tuple (self.section_elem (-1)), "%s, %s" % (tuple (self.section_elem (n - 1)), tuple (self.section_elem (-1)))
		return n - 1, tuple (self.section_elem (-1))
	def first_phrase (self): return 0, tuple (self.phrase_elem (0))
	def  last_phrase (self):
		n = self.nphrase ()
		#print ("n: %s" % (n,))
		a = self.phrase_elem (n - 1)
		b = self.phrase_elem (  - 1)
		assert tuple (a) == tuple (b), "%s != %s" % (a, b)
		return n - 1, tuple (self.phrase_elem (-1))
	def first_segment (self): return 0, self.segment_elems (0)
	def last_segment (self):
		n = self.nsegment ()
		a = self.segment_elems (n - 1)
		b = self.segment_elems (-1)
		assert a == b, "%s != %b" % (a, b)
		return n - 1, self.segment_elems (-1)
		
	def first_bar (self): return 0, self.bar_elem (0)
	def  last_bar (self):
		n = self.nbar ()
		a = self.bar_elem (n - 1)
		b = self.bar_elem ( - 1)
		assert a == b, "%s != %b" % (a, b)
		return n - 1, self.bar_elem (-1)
	
	def chorii (self):
		temp = self.pc.chorii ()
		for section_no, phrases in temp:
			#for phrase in phrases:
				#for segment in phrase:
				#	self.uniq[segment]
				#map (lambda x: self.uniq[x], phrase)
			#map (lambda x: self.uniq[x], phrase) for phrase in segments
			yield section_no, tuple (tuple (map (lambda x: self.uniq[x], segments)) for segments in phrases)
			
	#def pre_phrases (self):
	#	temp = tuple (self.pc.pre_phrases ())
	#	for section_no, phrases in temp:
	#		#for phrase in phrases:
	#		#	for segment in phrase:
	#		yield section_no, tuple (tuple (map (lambda x: self.uniq[x], segments)) for segments in phrases)
			
	def pre_sections (self):
		sections = tuple (self.pc.pre_sections ())
		for section_no, phrases in sections:
			#print (section_no)
			#print (phrases)
			yield section_no, tuple (tuple (map (lambda x: self.uniq[x], segments)) for segments in phrases)
			
	def pre_phrases (self):
		phrases = tuple (self.pc.pre_phrases ())
		for phrase_no, phrase in phrases:
			#yield phrase_no, tuple (map (lambda x: self.uniq[x], segment) for segment in phrase)
			yield phrase_no, tuple (self.uniq[segment] for segment in phrase)
			
	def pre_segments (self):
		temp = tuple (self.pc.pre_segments ())
		for segment_no, segment in temp:
			yield segment_no, self.uniq[segment]

	def pre_bars (self):
		temp = tuple (self.pc.pre_segments ())
		for segment_no, segment in temp:
			bar_nos = self.sb[segment_no]
			bar_no  = bar_nos[-1]
			yield bar_no, self.uniq[segment][-1]	
		
		
def random_segment_cadence ():
	temp = choice (segment_db)
	return choice (temp)
def random_segment_cadences (pc=None, pc_args=None, sc=None):
	if pc is None: pc = random_phrase_cadences (*pc_args)
	ns = pc.nuniq_segment ()
	if sc is None: sc = tuple ((random_segment_cadence () for _ in range (0, ns)))
	assert ns == len (sc)
	
	cs = { True : sc }
	m = cadence_helper05 (cs)
	#uniq, dups     = cadence_helper0 (cs)
	#minsum, maxsum = cadence_helper1 (uniq, dups)
	#mapping, n     = cadence_helper2 (cs, minsum, maxsum)
	#mapuniq        = cadence_helper3 (mapping)
	#msc            = cadence_helper4 (mapping, mapuniq)
	#m              = cadence_helper5 (msc, cs)
	msc2 = m[True] 
	return SegmentCadence (pc, msc2)
