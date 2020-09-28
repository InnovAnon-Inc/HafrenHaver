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
		
phrase_db = (
	#((0,),),     # one   segment
	((0, 0),     # two   segments, same cadence
	 (0, 1),),    # two   segments, same cadence
	((0, 0, 0),  # three segments, same cadence
	 (0, 0, 1),  # three segments, last  different
	 (0, 1, 0),
	 (0, 1, 1),), # three segments, first different
)
# for a standard verse there are two phrases,
# A A1
# A A2
# where A, A1 and A2 are segments
# phrase_no => hash => segment_no
# (no longer need to worry about long vs short section types)
class PhraseCadence (Cadence):
	@staticmethod
	def init_spmap (sc, m):
		segment_no = 0
		spmap = []
		for phrase_no in sc.all_phrases ():
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
		for phrase_no in sc.all_phrases ():
			phrase = m[phrase_no]
			dp     = len(phrase)
			temp = tuple (range (segment_no, segment_no + dp))
			psmap = psmap + [temp]
			segment_no = segment_no + dp
			pn = pn + 1
		psmap = tuple (psmap)
		assert len (psmap) == pn
		return psmap
	def __init__ (self, sc, m):
		Cadence.__init__ (self, m, sc.all_phrases ())
		#print ("fuck: %s" % (sc.all_phrases(),))
		#print ("m: %s" % (m,))
		#print ("uniq: %s" % (self.uniq,))
		#print ("m: %s" % (m,))
		#print ("sc: %s" % list (sc.all ()))
		self.sc = sc
		self.sp = PhraseCadence.init_spmap (sc, m)
		self.ps = PhraseCadence.init_psmap (sc, m)
		print ("sp: %s" % (self.sp,))
		assert len (self.sp) == self.nsegment ()
		assert len (self.ps) == self.nphrase ()
	def __repr__ (self): return "PhraseCadence [%s, sc=%s]" % (Cadence.__repr__ (self), self.sc)
	
	def nsection (self): return self.sc.nsection ()
	def nphrase (self): return self.sc.nphrase ()
	def nsegment (self): return len (self.all_segments ())
	#def nuniq (self): return len (self.uniq) # TODO
	def nuniq_segment (self): return len (set (self.all_segments ()))
	def nuniq_phrase (self): return self.sc.nuniq_phrase ()
	def nuniq_section (self): return self.sc.nuniq_section ()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	#def elem (self, segment_no): # phrase cadence
	#def phrase_elem (self, phrase_no): # section cadence
	#	return self.uniq[phrase_no]
	def phrase_elems (self, phrase_no):
		#print ("phrase_no: %s" % (phrase_no,))
		#phrase = self.sc.phrase_elem (phrase_no)
		phrase = self.pattern (phrase_no)
		#print ("phrase: %s" % (phrase,))
		#print ("uniq: %s" % (self.uniq,))
		#return self[phrase] #Cadence.__getitem__ (self, phrase_no)
		fuck = self.uniq[phrase]
		#print ("fuck: %s" % (fuck,))
		return fuck
		#return tuple (self[i] for i in phrase)
		#return self[phrase_no]
	def all_phrases (self): return iter (self) # return Cadence.all (self)
	#def all_phrases (self): return (self.uniq[phrase_no] for phrase_no in self.sc.all ())
	def segment_elem (self, segment_no):
		assert segment_no < self.nsegment ()
		phrase_no, i = self.sp[segment_no]
		assert phrase_no < self.nphrase ()
		#phrase = self.phrase_elems (phrase_no)
		phrase = self.uniq[phrase_no]
		#phrase = self[phrase_no]
		assert i < len (phrase), "\ni: %s\nphrase: %s\nsp: %s\nps: %s" % (i, phrase, self.sp, self.ps)
		return phrase[i]
		#phrase    = self.phrase_elem (phrase_no)
		#segno     = self.ss[segment_no]
		#return phrase[segno]
		# TODO
		#return tuple (self.all_segments ())[segment_no]
	def all_segments (self): return tuple (chain (*self.all_phrases ()))
	def section_elem (self, section_no):
		#print (section_no)
		phrase_nos = self.sc.section_elems (section_no)
		#print ("phrase_nos: %s" % (phrase_nos,))
		#phrase_nos = chain (*phrase_nos)
		#print ("phrase_nos: %s" % (phrase_nos,))
		#return (self.phrase_elem (phrase_no) for phrase_no in phrase_nos)
		return tuple (map (lambda x: self.uniq[x], phrase_nos))
		#return tuple (map (self.phrase_elem, self.sc.section_elems (section_no)))
	def all_sections (self):
		#for section_no in chain (*self.sc.all_sections ()):
		#	yield tuple (self.section_elem (section_no))
		#temp = (tuple (self.section_elem (section_no)) for section_no in chain (*self.sc.all_sections ()))
#		temp = (tuple (self.section_elem (section_no)) for section in self.sc.all_sections ())
#		temp = tuple (temp)
#		t1 = tuple (chain (*temp))
#		t2 = tuple (self.all_phrases ())
		#assert t1 == t2, "%s\n\n%s" % (t1, t2) 
#		return temp
		#return tuple (tuple (map (self.phrase_elem, section)) for section in self.sc.all_sections ())
		#print ("fuck all sections: %s" % (tuple (self.sc.all_sections ()),))
		#print ("fuck all sections: %s" % (tuple (self.sc.all_sections ()),))
		for section in self.sc.all_sections ():
			section = tuple (section)
			#print ("fuck section: %s" % (section,))
			#yield tuple (map (self.phrase_elem, section))
			yield tuple (map (lambda x: self[x], section))
			
			
	def section_types (self): return tuple ((st, tuple (map (lambda x: self[x], tuple (section)))) for st, section in self.sc.section_types ())
	def all_section_types (self): return self.sc.all_section_types ()
		
	#def all_sections (self): return chain (*self.all_sections0 ())
	def first_section (self): return 0, tuple (self.section_elem (0))
	
	def  last_section (self):
		n = self.nsection ()
		assert tuple (self.section_elem (n - 1)) == tuple (self.section_elem (-1)), "%s, %s" % (tuple (self.section_elem (n - 1)), tuple (self.section_elem (-1)))
		return n - 1, tuple (self.section_elem (-1))
	def first_phrase (self): return 0, tuple (self.phrase_elems (0))
	
	
	
	def  last_phrase (self):
		n = self.nphrase ()
		#print ("n: %s" % (n,))
		a = self.phrase_elems (n - 1)
		b = self.phrase_elems (  - 1)
		assert tuple (a) == tuple (b), "%s != %s" % (a, b)
		return n - 1, tuple (self.phrase_elems (-1))
	def first_segment (self): return 0, self.segment_elem (0)
	
	def last_segment (self):
		n = self.nsegment ()
		a = self.segment_elem (n - 1)
		b = self.segment_elem (-1)
		assert a == b, "%s != %b" % (a, b)
		return n - 1, self.segment_elem (-1)
	def chorii (self):
		temp = self.sc.chorii ()
		for section_no, phrases in temp:
			#yield section_no, tuple (self.phrase_elems (phrase_no) for phrase_no in phrases)
			yield (section_no, tuple (map (lambda x: self.uniq[x], phrases)))
	def pre_phrases (self):
		temp = tuple (self.sc.pre_phrases ())
		for section_no, phrases in temp:
			# TODO
			#print (section_no)
			#print (phrases)
			#yield section_no, tuple (self.phrase_elems (phrase_no) for phrase_no in phrases)
			yield section_no, self.uniq[phrases]
	
	def pre_sections (self):
		sections = tuple (self.sc.pre_sections ())
		for section_no, phrases in sections:
			#print (section_no)
			#print (phrases)
			yield (section_no, tuple (map (lambda x: self.uniq[x], phrases)))
			
	def pre_segments (self):
		temp = tuple (self.sc.pre_phrases ())
		for phrase_no, phrases in temp:
			segment_nos = self.ps[phrase_no]
			segment_no  = segment_nos[-1]
			yield segment_no, self.uniq[phrases][-1]
		
		
		
		
		
		
		
def random_phrase_cadence (nseg=None):
	if nseg is None: nseg = randrange (0, len (phrase_db))
	temp = phrase_db[nseg]
	return choice (temp)
def random_phrase_cadences (sc=None, sc_args=None, pc=None):
	if sc is None: sc = random_section_cadences (*sc_args)
	np = sc.nuniq_phrase ()
	if pc is None: pc = tuple ((random_phrase_cadence () for _ in range (0, np)))
	assert np == len (pc)
	
	cs = { True : pc }
	m = cadence_helper05 (cs)
	#uniq, dups     = cadence_helper0 (cs)
	#minsum, maxsum = cadence_helper1 (uniq, dups)
	#mapping, n     = cadence_helper2 (cs, minsum, maxsum)
	#mapuniq        = cadence_helper3 (mapping)
	#msc            = cadence_helper4 (mapping, mapuniq)
	#m              = cadence_helper5 (msc, cs)
	msc2 = m[True] 
	return PhraseCadence (sc, msc2)	
