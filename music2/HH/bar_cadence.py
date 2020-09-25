#! /usr/bin/env python3

from enum      import Enum
from numba     import jit
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
from segment_cadence import random_segment_cadences
			
class BarCadence (Cadence):
	def __init__ (self, sc, m):
		Cadence.__init__ (self, m, sc.all_bars ())
		self.sc = sc
	def __repr__ (self): return "BarCadence [%s, sc=%s]" % (Cadence.__repr__ (self), self.sc)
	
	def nsection (self): return self.sc.nsection ()
	def nphrase (self): return self.sc.nphrase ()
	def nsegment (self): return self.sc.nsegment ()
	def nuniq_segment (self): return self.sc.nuniq_segment ()
	def nuniq_phrase (self): return self.sc.nuniq_phrase ()
	def nuniq_section (self): return self.sc.nuniq_section ()	
	def nbar (self): return self.sc.nbar ()
	def nuniq_bar (self): return self.sc.nuniq_bar ()

	def segment_elems (self, segment_no): return tuple (self.uniq[barno] for barno in self.sc.segment_elems (segment_no))
	def all_segments (self): return tuple (tuple (self.segment_elems (segno)) for segno in range (0, self.nsegment ()))
	def bar_elem (self, barno):
		barno = self.order[barno]
		return self.uniq[barno]
	def all_bars (self): return iter (self)
	def phrase_elem (self, pno):
		phrase = self.sc.phrase_elem (pno)
		for segment in phrase: yield tuple (self.uniq[barno] for barno in segment)
	def all_phrases (self):
		for pno in range (0, self.nphrase ()): yield tuple (self.phrase_elem (pno))
	def section_elem (self, section_no):	
		section = self.sc.section_elem (section_no)
		for phrase in section:
			yield tuple (tuple (self.uniq[barno] for barno in segment) for segment in phrase)
	def all_sections (self):
		for sno in range (0, self.nsection ()): yield tuple (self.section_elem (sno))
		
	def section_types (self): return tuple ((st, tuple (tuple (tuple (self.uniq[barno] for barno in segment) for segment in phrase) for phrase in section)) for st, section in self.sc.section_types ())
	def all_section_types (self): return self.sc.all_section_types ()
			
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
		assert a == b, "%s != %s" % (a, b)
		return n - 1, self.segment_elems (-1)
	def first_bar (self): return 0, self.bar_elem (0)
	def  last_bar (self):
		n = self.nbar ()
		a = self.bar_elem (n - 1)
		b = self.bar_elem ( - 1)
		assert a == b, "%s != %s" % (a, b)
		return n - 1, self.bar_elem (-1)
	
	
	
	
	
	def chorii (self):
		temp = self.sc.chorii ()
		for section_no, phrases in temp: yield section_no, tuple (tuple (tuple (map (lambda x: self.uniq[x], segment)) for segment in phrase) for phrase in phrases)
			
	def pre_sections (self):
		temp = self.sc.pre_sections ()
		for section_no, phrases in temp: yield section_no, tuple (tuple (tuple (map (lambda x: self.uniq[x], segment)) for segment in phrase) for phrase in phrases)
			
	def pre_phrases (self):
		temp = self.sc.pre_phrases ()
		for phrase_no, phrase in temp: yield phrase_no, tuple (tuple (map (lambda x: self.uniq[x], segment)) for segment in phrase)
			
	def pre_segments (self):
		temp = self.sc.pre_segments ()
		for segment_no, segment in temp: yield segment_no, tuple (map (lambda x: self.uniq[x], segment))

	def pre_bars (self):
		temp = self.sc.pre_bars ()
		for bar_no, bar in temp: yield bar_no, self.uniq[bar]

	def nbeat (self): return sum (self.all_bars ())
	def play (self, av):
		assert len (list (self.all_bars ())) == self.nbar ()
		for bar in list (self.all_bars ()):
			av.append (bar)
		print ("save")
		av.save ()
		print ("play")
		#audio.play ()











def random_bar_cadence (sc=None, sc_arg=None):
	if sc is None: sc = random_segment_cadences (*sc_arg)
	
	bar_min = 1
	bar_max = 3
	bar_rng = bar_max - bar_min + 1
	
	phrase_min = 16 / 2
	phrase_max = 16 * 2
	flag = False
	while not flag:
		flag = True
		pmins = []
		pmaxs = []
		for phrase in tuple (sc.all_phrases ()):
			bars = tuple (chain (*phrase))
			#pmin = sum (bar_min for bar_no in bars)
			#pmax = sum (bar_max for bar_no in bars)
			pmin = sum (bar_max for bar_no in bars)
			pmax = sum (bar_min for bar_no in bars)
			pmins = pmins + [pmin]
			pmaxs = pmaxs + [pmax]
		for pmin, pmax in zip (pmins, pmaxs):
			#if pmin >= pmax: continue		
			if pmin < phrase_min:
				#bar_min = bar_min + 1
				bar_max = bar_max + 1
				flag = False
				break
		#for pmin, pmax in zip (pmins, pmaxs):
		#	#if pmin >= pmax: continue		
		#	if pmax < phrase_min:
		#		#bar_min = bar_min + 1
		#		bar_min = bar_min + 1
		#		flag = False
		#		break
		#for pmin, pmax in zip (pmins, pmaxs):
		#	if pmax > phrase_max:
		#		#bar_max = bar_max - 1
		#		bar_min = bar_min - 1
		#		flag = False
		#		break
		if bar_min > bar_max:
			temp = bar_min
			bar_min = bar_max
			bar_max = temp
			exit (2)
		#print (pmin)
		#print (pmax)
		#print (bar_min)
		#print (bar_max)
		#print ()
	#exit (2)
		
	nbar = sc.nuniq_bar ()
	#barlens = [bar_min] * nbar
	#barlens = [bar_max] * nbar
	barlens = [randrange (bar_min, bar_max + 1) for _ in range (0, nbar)]
	#for k in range (0, nbar): barlens[k] = (k + 1) % (bar_rng) + bar_min
	#for k in range (0, nbar): barlens[k] = bar_min

	flag = False
	pas  = random_bool ()
	while not flag:
		flag = True
		phrases = tuple (sc.all_phrases ())
		if pas: phrases = phrases[::-1]
		pas = not pas
		for phrase in phrases:
			bars = tuple (chain (*phrase))
			nbeat = sum (barlens[bar_no] for bar_no in bars)
			if nbeat < phrase_min:
				for bar in bars[::-1]:
					if barlens[bar] < bar_max:
						barlens[bar] = barlens[bar] + 1
						flag = False
						break
				if not flag: continue
				
			if nbeat > phrase_max:
				for bar in bars:
					if barlens[bar] > bar_min:
						barlens[bar] = barlens[bar] - 1
						flag = False
				if not flag: continue
		# TODO check uniq segments for duplicate barlen combos
	
	print ("barlens: %s" % (barlens,))
	
	# TODO how to determine lengths of bars
	return BarCadence (sc, barlens)
