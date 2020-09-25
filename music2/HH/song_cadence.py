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
	
# which section types, which order, and which ones have the same meter
# this layer separates short sections and long sections, which is necessary for random-generation constraints
class SongCadence (Cadence):
	#@jit
	@staticmethod
	def init_uniq (ss, sc, lc):
		uniq = {}
		sci  = 0
		lci  = 0
		#lci = len (sc.uniq)
		for s in ss.uniq_elements ():
			#if s in uniq: continue
			assert long_section (s) or short_section (s)
			if short_section (s):
				i   = (sc, sci)
				sci = sci + 1
				assert not long_section (s)
			if  long_section (s):
				i   = (lc, lci)
				lci = lci + 1
				assert not short_section (s)
			uniq[s] = i
		#assert sci == len (sc.uniq)
		#assert lci == len (lc.uniq)
		assert sci == len (sc)
		assert lci == len (lc)
		return uniq
	def __init__ (self, ss, sc, lc):
		Cadence.__init__ (self, SongCadence.init_uniq (ss, sc, lc), ss)
		self.ss = ss # song  cadence
		self.sc = sc # short cadence
		self.lc = lc # long  cadence
	def __repr__ (self): return "SongCadence [%s, ss=%s, sc=%s, lc=%s]" % (Cadence.__repr__ (self), self.ss, self.sc, self.lc)
	#@jit
#	def __getitem__ (self, i): # section_no to section
#		c, v = self.section1d (i)
#		return self.section2d (c, v)
	
	#def section_type (self, i): return self.pattern (i)
	#def sections (self): return self.uniq.items () # TODO test
	#def sections (self): return self.ss.uniq.items () # TODO test
	# TODO
	#def sections (self): return set (self.all ())
	def uniq_section_types (self): return self.ss.uniq_sections ()
	def uniq_short_sections (self): return ((True,  i) for i in self.sc.uniq_elements ())
	def uniq_long_sections  (self): return ((False, i) for i in self.lc.uniq_elements ())
	def uniq_sections (self): return chain (self.uniq_short_sections (), self.uniq_long_sections ())
		#kvs = self.uniq_elements ()
		#for section_type, index in kvs.values ():
		#	print ("%s[%s]: %s" % (section_type == self.sc, index, section_type[index]))
		#	yield section_type == self.sc, section_type[index]
	
	#def sections (self): return set (self)
	#def section1d (self, i): return Cadence.elem (self, i)
	"""
	def section1d (self, i): return Cadence.__getitem__ (self, i)
	def section2d (self, c, v):
		assert (c == self.sc or c == self.lc)
		#r = c.elem (v)
		r = c[v]
		#assert r == c.uniq[v]
		return (c == self.sc, r)
		"""
	#@jit
	#def all (self): return (c.uniq[v.value ()] for c, v in Cadence.all (self))
	#def all (self): return ((c == self.sc, c.uniq[v]) for c, v in Cadence.all (self))
	#def all (self): return (self.section2d (c, v) for c, v in Cadence.all (self))
	#def all (self): return map (lambda cv: self.section2d (*cv), Cadence.all (self))
	
	
	#def __getitem__ (self, i): # section_no to section
		# v = self.pattern (i) # section type
		# return self.uniq[v]  # is_short, index
		
		# section_no to section_type, index
			
		
		#c, v = self.pattern (i)
		#return self.section2d (c, v)
	#def pattern (self, i): return Cadence.__getitem__ (self, i)
	
	def section_type (self, i): 
		a = Cadence.pattern (self, i)
		b = self.ss.section_type (i)
		assert a == b, "%s != %s" % (a, b)
		return a

#	def __getitem__ (self, i):
#		section_type, index = Cadence.__getitem__ (self, i)
#		return section_type == self.sc, section_type[index]
#	#def __iter__ (self):
#	#	# (self[st] for st in Pattern.__iter__ (self))
#	#	return (self
#	def section_index (self, i):
#		st = Pattern.__getitem__ (self, i)
#		return self[st]
#	def __iter__ (self):
#		test = tuple (self.section_index (i) for i in range (0, len (self)))
#		assert test == tuple (Cadence.__iter__ (self))
#		return Cadence.__iter__ (self)
	def __getitem__ (self, i):
		st = Pattern.__getitem__ (self, i)
		return self.section_index (st)
	def section_index (self, st):
		section_type, index = Cadence.__getitem__ (self, st)
		return section_type == self.sc, section_type[index]
	def __iter__ (self): return (self.section_index (st) for st in Pattern.__iter__ (self))
	def all_sections (self):
		assert len (list (iter (self))) == self.nsection ()
		return iter (self)
	
	
	
	def section_types (self): return tuple ((st, self.section_index (st)) for st in self.uniq_section_types ())
	def all_section_types (self): return tuple (self.ss)
	
	
	
	
	
	
	
	
	
	
	
	# TODO Cadence.all (self)
	#def all (self):
	#	return iter (self)
#		for s in self.ss.order:
#			c, ci = self.uniq[s]
#			yield self.section2d (c, ci)
		#for c, v in Cadence.all (self):
			##r = c.uniq[v]
			#r = c.elem (v)
			##assert r == c.uniq[v], "%s, %s" % (r, c.uniq[v])
			#print ("c=%s (v=%s): %s" % (c, v, r))
			#assert (c == self.sc or c == self.lc)
			#yield (c == self.sc, r)
		#	yield self.section2d (c, v)
	#def all (self): return (c.u (v) for c, v in Cadence.all (self))
	#def v (self, v): return Cadence.v (self, v.value ())
	
	
	
	
	
	
	def nsection (self):
		assert self.ss.nsection () == len (self)
		return len (self)
	def nshort_section (self): return self.ss.nshort_section ()
	def nshort_section_types (self): return self.sc.nsection ()
	def nlong_section (self): return self.ss.nlong_section ()
	def nlong_section_types (self): return self.lc.nsection ()
	#def ns (self): return self.nsc () + self.nlc ()
	#def ns (self): return len (tuple (self.all ()))
	def nuniq_short_section (self): return self.sc.nuniq ()
	def nuniq_long_section (self): return self.lc.nuniq ()
	def nsection_type (self): return Cadence.nuniq (self)
	def nuniq (self): return self.nuniq_short_section () + self.nuniq_long_section ()
	def first_section  (self): return 0, self[0] # return 0, self.section_index (0) # return 0, tuple (self.all ())[ 0]
	def  last_section  (self):
		#temp = tuple (self.all ())
		#return len (temp) - 1, temp[-1]
		a = self[-1]
		n = self.nsection ()
		b = self[n - 1]
		assert a == b, "%s != %s" % (a, b)
		return len (self) - 1, self[-1] #self.section_index (-1)
	def   pre_sections (self):
		#sections = tuple (self.all ())
		sections = self
		n        = len (sections)
		#for i, section in zip (range (1, n), sections[1:]):
		for i in range (1, n):
			st = self.section_type (i)
			if st != CHORUS: continue
			yield i - 1, self[i - 1]
	def chorii (self):
		#sections = tuple (self.all ())
		sections = self
		n        = len (sections)
		for i, section in zip (range (0, n), sections):
			st = self.section_type (i)
			if st != CHORUS: continue
			yield i, section
def random_song_cadence (ss=None, sc=None, lc=None):
	if ss is None: ss = random_song_structure ()
	nsc = ss.nuniq_short_section ()
	nlc = ss.nuniq_long_section ()
	#nsc = ss.nsc ()                      # number of short sections
	#nlc = ss.nlc ()                      # number of long  sections
	#assert len (ss.order) == nsc + nlc, "tot: %s, short: %s, long: %s" % (len (ss.order), nsc, nlc)
	#assert len (set (ss.order)) == nsc + nlc, "tot: %s, short: %s, long: %s" % (len (set (ss.order)), nsc, nlc)

	if lc is None: lc = random_sc0 (nlc) # long  sections
	
	# chorus (2-3) <= verse  (2-4, 3-9)
	# verse  (2-9) <= bridge (2-4, 3-6, 4-8, 5-9, 6-9, 7-9, 9-9)
	
	#      intro < verse     (1-1, 1-2, 1-3, 1-4, 1-4, 1-4, 1-4, 1-4)
	# TODO pre   < chorus    (1-1, 1-2)
	#      outro < bridge ?  
	if sc is None: sc = random_sc0 (nsc) # short sections
	#assert len (sc) == nsc
	#assert len (lc) == nlc
	#assert len (sc.uniq) == nsc # TODO len (sc.uniq) ?
	#assert len (lc.uniq) == nlc
	#assert sc.nuniq () == nsc
	#assert lc.nuniq () == nlc
	#assert sc.nsection () == nsc, "%s, %s, %s" % (sc.nsection (), nsc, ss)
	#assert lc.nsection () == nlc, "%s, %s, %s" % (lc.nsection (), nlc, ss)
	#assert sc.nuniq () == nsc
	#assert lc.nuniq () == nlc
	return SongCadence (ss, sc, lc)
