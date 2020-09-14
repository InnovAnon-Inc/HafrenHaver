#! /usr/bin/env python3

from enum      import Enum
from numba     import jit
from random    import choice, randrange, shuffle
from itertools import accumulate, chain, permutations

from math import factorial

from section_type import SectionType, short_section, long_section
#from random_util import subsets, random_bjorklund2, random_bool
#from song        import random_song#, apply_song
#from mode        import random_mode

VERSE  = SectionType.VERSE
CHORUS = SectionType.CHORUS
BRIDGE = SectionType.BRIDGE
INTRO  = SectionType.INTRO
OUTRO  = SectionType.OUTRO
PRE    = SectionType.PRE

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

class Pattern:
	def __init__ (self, order):
		#rev = {}
		#I   = range (0, len (order))
		#for i, v in zip (I, order):
		#	if v in rev: temp = rev[v]
		#	else:        temp = []
		#	rev[v] = tuple (temp + [i])
		self.order = order
		#self.rev   = rev
	def __repr__ (self): return "Pattern [order=%s]" % (self.order,)
	#@jit
	def elem (self, i): return self.order[i]
	#@jit
	def all (self): return self.order
	@jit
	def indices (self, k):
		I = range (0, len (self.order))
		#for i, v in zip (I, self.order):
		#	if v == k: yield i
		I = zip (I, self.order)
		I = filter (lambda iv: v == k, I)
		return (i for i, v in I)


	
song_structure_db = (
	# pop song structures
	(       VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS),                                #   V1 V2   C V3   C B C          0
	(INTRO, VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS),                                # I V1 V2   C V3   C B C          1
	(       VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, OUTRO),                         #   V1 V2   C V3   C B C O        2
	(INTRO, VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, OUTRO),                         # I V1 V2   C V3   C B C O        3
	(       VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS),                                #   V1 V2 P C V3 P C B C          4
	(INTRO, VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS),                                # I V1 V2 P C V3 P C B C          5
	(       VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, OUTRO),                         #   V1 V2 P C V3 P C B C O        6
	(INTRO, VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, OUTRO),                         # I V1 V2 P C V3 P C B C O        7
	
	(       VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS),                #   V1 V2   C B C V3   C B C      8
	(       VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS),                #                                 9
	(INTRO, VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS),                #                                10
	(INTRO, VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS),                #                                11
	(       VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, OUTRO),         #                                12
	(       VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, OUTRO),         #                                13
	(INTRO, VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, OUTRO),         #                                14
	(INTRO, VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, OUTRO),         #                                15
	(       VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS),        #   V1 V2   C B C V3   C B C C   16
	(       VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS),        #                                17
	(INTRO, VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS),        #                                18
	(INTRO, VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS),        #                                19
	(       VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS, OUTRO), #                                20
	(       VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS, OUTRO), #                                21
	(INTRO, VERSE, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS, OUTRO), #                                22
	(INTRO, VERSE, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, BRIDGE, CHORUS, CHORUS, OUTRO), #                                23

	# TODO I O P for ^^^
	# folk song structures
	(       VERSE, CHORUS,    VERSE, CHORUS,    VERSE, CHORUS, VERSE, CHORUS),                             #                                24
	(       VERSE, CHORUS,    VERSE, CHORUS,    VERSE, CHORUS, CHORUS),                                    #                                25

	(       VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, VERSE,      CHORUS),                   #                                26
	(       VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, VERSE, PRE, CHORUS),                   #                                27
	(INTRO, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, VERSE,      CHORUS),                   #                                28
	(INTRO, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, VERSE, PRE, CHORUS),                   #                                29
	(       VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, VERSE,      CHORUS, OUTRO),            #                                30
	(       VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, VERSE, PRE, CHORUS, OUTRO),            #                                31
	(INTRO, VERSE,      CHORUS, VERSE,      CHORUS, BRIDGE, CHORUS, VERSE,      CHORUS, OUTRO),            #                                32
	(INTRO, VERSE, PRE, CHORUS, VERSE, PRE, CHORUS, BRIDGE, CHORUS, VERSE, PRE, CHORUS, OUTRO),            #                                33
)
class SongStructure (Pattern):
	def __init__ (self, ss): Pattern.__init__ (self, ss)
	def __repr__ (self): return "SongStructure [%s]" % Pattern.__repr__ (self)
	#def nsc (self): return len (set (filter (short_section, self.all ())))
	def nsc (self): return len (set (filter (short_section, Pattern.all (self))))
	#def nlc (self): return len (set (filter ( long_section, self.all ())))
	def nlc (self): return len (set (filter ( long_section, Pattern.all (self))))
	#@jit
	#def elem (self, i):
	#	v = Pattern.elem (self, i)
	#	return v.value ()
	#@jit
	#def all (self): return (v.value () for v in Pattern.all (self))
def random_song_structure ():
	ss = choice (song_structure_db)
	return SongStructure (ss)









class Cadence (Pattern):
	def __init__ (self, uniq, order):
		Pattern.__init__ (self, order)
		self.uniq = uniq
	def __repr__ (self): return "Cadence [%s, uniq=%s]" % (Pattern.__repr__ (self), self.uniq)
	#@jit
	def elem (self, i):
		#v = Pattern.elem (self, i)
		v = self.pattern (i)
		#return self.u (v)
		return self.uniq[v]
	def pattern (self, i): return Pattern.elem (self, i)
	#@jit
	#def all (self): return (self.u (v) for v in Pattern.all (self))
	def all (self): return (self.uniq[v] for v in Pattern.all (self))
	#@jit
	#def v (self, v): return v
	#@jit
	#def u (self, v):
	#	v = self.v (v)
	#	return self.uniq[v]
	# TODO indices for which elem() is k	








sc0_db = (
	#(tuple ([]),),
	((0,),),       # one   section
	((0, 0),      # two   sections, same      section cadence
	 (0, 1),),    # two   sections, different section cadences
	((0, 0, 0),   # three sections, same      section cadence
	 (0, 0, 1),   # three sections, last      section cadence  different
	 (0, 1, 0),   # three sections, middle    section cadence  different
	 (0, 1, 1),   # three sections, first     section cadence  different
	 (0, 1, 2),), # three sections, all       section cadences different
)
class SongCadence0 (Cadence):
	def __init__ (self, sc, mapping): Cadence.__init__ (self, sc, mapping)
	def __repr__ (self): return "SC0 [%s]" % Cadence.__repr__ (self)
	def sections (self): return self.uniq.items () # TODO test
	def section_type (self, i): return Cadence.pattern (self, i)
	# TODO or max ?
	def ns (self): return len (self.uniq)
	def nuniq (self): return len (set (self.uniq))
	#@jit
	#def elem (self, i): # section_no to section
	#	v = Cadence.elem (self, i)
	#	return v.value ()
	#@jit
	#def all (self): return (v.value () for v in Cadence.all (self))
	#def v (self, v): return Cadence.v (self, v.value ())
#@jit
def reduce_map (m, min_n, max_n): # map from cardinality m to n, where n in [min_n, max_n]
	n     = randrange (min_n, max_n + 1)
	temp0 = range (0, m)
	# TODO maybe just increment-modulo by a relatively prime amount
	temp1 = (randrange (0, m) for _ in range (0, m - n))
	#temp1 = [randrange (0, m) for _ in range (0, m - n)]
	temp  = list (chain (temp0, temp1))
	shuffle (temp)
	temp  = tuple (temp)
	return temp
def random_sc0 (nsection):
	if nsection == 0: return SongCadence0 ([], {})
	temp  = sc0_db[nsection - 1]
	#temp  = sc0_db[nsection]
	assert temp is not None
	sc    = choice (temp)
	assert sc is not None
	assert type (sc) is tuple, nsection
	min_n = max (sc) + 1
	max_n = min_n
	assert max_n <= nsection, "max n: %s, n section: %s" % (max_n, nsection)
	#n     = randrange (min_n, max_n + 1)
	## TODO map from cardinalities nsection to n
	#temp0 = range (0, nsection)
	#temp1 = (randrange (0, nsection) for _ in range (0, nsection - n)) # TODO maybe just increment-modulo by a relatively prime amount
	#temp  = list (chain (temp0, temp1)) 
	#shuffle (temp)
	temp = reduce_map (nsection, min_n, max_n)
	return SongCadence0 (sc, temp)
	
	
	
	
















	
	
class SongCadence (Cadence):
	#@jit
	@staticmethod
	def init_uniq (ss, sc, lc):
		uniq = {}
		sci  = 0
		lci  = 0
		#lci = len (sc.uniq)
		for s in ss.order:
			if s in uniq: continue
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
		assert sci == len (sc.uniq)
		assert lci == len (lc.uniq)
		#print ("uniq: %s" % uniq)
		return uniq
	def __init__ (self, ss, sc, lc):
		Cadence.__init__ (self, SongCadence.init_uniq (ss, sc, lc), ss.order)
		self.ss = ss # song  cadence
		self.sc = sc # short cadence
		self.lc = lc # long  cadence
	def __repr__ (self): return "SongCadence [%s, ss=%s, sc=%s, lc=%s]" % (Cadence.__repr__ (self), self.ss, self.sc, self.lc)
	#@jit
	def elem (self, i): # section_no to section
		c, v = self.section1d (i)
		##return c.uniq[v.value ()]
		##print ("c=%s (v=%s): %s" % (c, v, c.uniq[v]))
		##short = (c == self.sc)
		##assert short == (c != self.lc)
		#assert (c == self.sc or c == self.lc)
		#r = c.elem (v)
		##assert r == c.uniq[v]
		#return (c == self.sc, r)
		return self.section2d (c, v)
		#return (c == self.sc, c.uniq[v])
		#return (c == self.sc, c.elem (v))
		#return c.u (v)
		#if not short:
		#	print ("long")
		#	return c.uniq[v] + len (self.sc.uniq)
		#if short: print ("short")
		#return c.uniq[v]
	def section_type (self, i): return Cadence.pattern (self, i)
	#def sections (self): return self.uniq.items () # TODO test
	#def sections (self): return self.ss.uniq.items () # TODO test
	def sections (self): return set (self.all ())
	def section1d (self, i): return Cadence.elem (self, i)
	def section2d (self, c, v):
		assert (c == self.sc or c == self.lc)
		r = c.elem (v)
		#assert r == c.uniq[v]
		return (c == self.sc, r)
	#@jit
	#def all (self): return (c.uniq[v.value ()] for c, v in Cadence.all (self))
	#def all (self): return ((c == self.sc, c.uniq[v]) for c, v in Cadence.all (self))
	#def all (self): return (self.section2d (c, v) for c, v in Cadence.all (self))
	#def all (self): return map (lambda cv: self.section2d (*cv), Cadence.all (self))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	# TODO Cadence.all (self)
	def all (self):
		for s in self.ss.order:
			c, ci = self.uniq[s]
			yield self.section2d (c, ci)
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
	def nsc (self):
		assert self.ss.nsc () == self.sc.ns ()
		#return self.ss.nsc ()
		return self.sc.ns ()
	def nlc (self):
		assert self.ss.nlc () == self.lc.ns ()
		#return self.ss.nlc ()
		return self.lc.ns ()
	#def ns (self): return self.nsc () + self.nlc ()
	def ns (self): return len (tuple (self.all ()))
	def nsuniq (self): return self.sc.nuniq ()
	def nluniq (self): return self.lc.nuniq ()
	def nuniq (self): return self.nsuniq () + self.nluniq ()
	def first_section  (self): return 0, tuple (self.all ())[ 0]
	def  last_section  (self):
		temp = tuple (self.all ())
		return len (temp) - 1, temp[-1]
	def   pre_sections (self):
		sections = tuple (self.all ())
		n        = len (sections)
		for i, section in zip (range (1, n), sections[1:]):
			st = self.section_type (i)
			if st != CHORUS: continue
			yield i - 1, self.elem (i - 1)
	def chorii (self):
		sections = tuple (self.all ())
		n        = len (sections)
		for i, section in zip (range (0, n), sections):
			st = self.section_type (i)
			if st != CHORUS: continue
			yield i, self.elem (i)
def random_song_cadence (ss=None, sc=None, lc=None):
	if ss is None: ss = random_song_structure ()
	nsc = ss.nsc ()                      # number of short sections
	nlc = ss.nlc ()                      # number of long  sections
	#assert len (ss.order) == nsc + nlc, "tot: %s, short: %s, long: %s" % (len (ss.order), nsc, nlc)
	assert len (set (ss.order)) == nsc + nlc, "tot: %s, short: %s, long: %s" % (len (set (ss.order)), nsc, nlc)

	if lc is None: lc = random_sc0 (nlc) # long  sections
	
	# chorus (2-3) <= verse  (2-4, 3-9)
	# verse  (2-9) <= bridge (2-4, 3-6, 4-8, 5-9, 6-9, 7-9, 9-9)
	
	#      intro < verse     (1-1, 1-2, 1-3, 1-4, 1-4, 1-4, 1-4, 1-4)
	# TODO pre   < chorus    (1-1, 1-2)
	#      outro < bridge ?  
	if sc is None: sc = random_sc0 (nsc) # short sections
	assert len (sc.uniq) == nsc # TODO len (sc.uniq) ?
	assert len (lc.uniq) == nlc
	#assert sc.nuniq () == nsc
	#assert lc.nuniq () == nlc
	assert sc.ns () == nsc
	assert lc.ns () == nlc
	return SongCadence (ss, sc, lc)
	
	
	
	
	
	
	
section_db = (
	((0,),),       # one   phrase
	((0, 0),     # two   phrases, same      cadence
	 (0, 1),),    # two   phrases, different cadence
	((0, 0, 0),  # three phrases, same      cadence
	 (0, 0, 1),  # three phrases, last  different
	 (0, 1, 0),  # three phrases, mid   different
	 (0, 1, 1), # three phrases, first different
	 #(0, 1, 2),
	),
	 
# TODO allow for longer sections (including longer short sections)
	((0, 0, 0, 0),
	 (0, 0, 0, 1),
	 (0, 0, 1, 0),
	 (0, 1, 0, 0),
	 (0, 0, 1, 1),
	 (0, 1, 0, 1),
	 (0, 1, 1, 1),),
)
class SectionCadence (Cadence):
	@staticmethod
	def mapping (sc, scs, lcs):
		# TODO
		uniq = {}
		sci = 0
		lci = 0
		#for section_no, cv in sc.sections ():
		#for short, index in sc.all ():
		for short, index in sc.sections ():
			#section_type, index = cv
			#short,        index = sc.section2d (*cv)
			#print ("short: %s, index: %s" % (short, index))
			assert (short, index) not in uniq
			if short:
				uniq[(short, index)] = short, sci
				sci = sci + 1
			else:
				uniq[(short, index)] = short, lci
				lci = lci + 1
		order = []
		#phrase_no = 0
		#section_no = 0
		#spmap = []
		for short, index in sc.all ():
			if short:
				#print ("scs[%s]: %s" % (index, scs[index]))
				dp = len (scs[index])
			else:
				#print ("lcs[%s]: %s" % (index, lcs[index]))
				dp = len (lcs[index])
			for k in range (0, dp):
				#order = order + [(short, index, k)]
				order = order + [(short, index)]
				#phrase_no = phrase_no + 1
			#spmap[section_no] = spma
			#phrase_no = phrase_no + dp
			#section_no = section_no + 1
		order = tuple (order)
		
		for short, index in order:        assert (short, index) in uniq,  "short: %s, index: %s, uniq: %s" % (short, index, uniq)
		for short, index in uniq.keys (): assert (short, index) in order, "short: %s, index: %s, uniq: %s" % (short, index, uniq)
		
		#spmap = tuple (spmap)
		#print ("uniq =%s" % (uniq,))
		#print ("order=%s" % (order,))
		return uniq, order
	@staticmethod
	def init_psmap (sc, scs, lcs):
		phrase_no = 0
		section_no = 0
		#spmap = []
		psmap = []
		for short, index in sc.all ():
			if short: dp = len (scs[index])
			else:     dp = len (lcs[index])
			for k in range (0, dp):
				#order = order + [(short, index, k)]
				#order = order + [(short, index)]
				psmap = psmap + [(section_no, k)]
				#phrase_no = phrase_no + 1
			#spmap = spmap + [tuple (range (phrase_no, phrase_no + dp))]
			phrase_no = phrase_no + dp
			section_no = section_no + 1
		#spmap = tuple (spmap)
		psmap = tuple (psmap)
		assert len (psmap) == phrase_no
		return psmap
	@staticmethod
	def init_spmap (sc, scs, lcs):
		phrase_no = 0
		section_no = 0
		spmap = []
		#print ("all: %s" % list (sc.all ()))
		for short, index in sc.all ():
			if short:
				dp = len (scs[index])
				#print ("scs[%s]: %s" % (index, scs[index]))
			else:
				dp = len (lcs[index])
				#print ("lcs[%s]: %s" % (index, lcs[index]))
			#dp = dp + 1
			spmap = spmap + [tuple (range (phrase_no, phrase_no + dp))]
			phrase_no = phrase_no + dp
			section_no = section_no + 1
		spmap = tuple (spmap)
		assert len (spmap) == section_no
		return spmap
		
	def __init__ (self, sc, scs, lcs):
		#Cadence.__init__ (self, *SectionCadence.init_map (sc, scs, lcs))
		Cadence.__init__ (self, *SectionCadence.mapping (sc, scs, lcs)) # phrase_no to section_no
		self.sc  = sc
		self.scs = scs
		self.lcs = lcs
		#self.sp, self.ps = SectionCadence.init_spmap (sc, scs, lcs)
		self.ps = SectionCadence.init_psmap (sc, scs, lcs)
		self.sp = SectionCadence.init_spmap (sc, scs, lcs)
		#print ("sp: %s" % (self.sp,))
		#print ("ps: %s" % (self.ps,))
	def __repr__ (self): return "SectionCadence [%s, sc=%s, scs=%s, lcs=%s]" % (Cadence.__repr__ (self), self.sc, self.scs, self.lcs)
	# TODO
	# section_type (section_no)
	# section_index (phrase_no)
	# sections ()
	def first_section  (self):
		section_no, si = self.sc.first_section ()
		short, i = si
		return section_no, self.section0 (short, i)
	def  last_section  (self):
		section_no, si = self.sc.last_section ()
		short, i = si
		return section_no, self.section0 (short, i)
	def   pre_sections (self):
		sis = self.sc.pre_sections ()
		for section_no, si in sis:
			short, i = si
			yield section_no, self.section0 (short, i)
	def chorii (self):
		sis = self.sc.chorii ()
		for section_no, si in sis:
			short, i = si
			yield section_no, self.section0 (short, i)
	def first_phrase (self):
		section_no, si = self.first_section ()
		#print ("section_no: %s, si: %s" % (section_no, si))
		phrase_nos = self.sp[section_no]
		#print ("sp: %s" % (self.sp,))
		#print ("ps: %s" % (self.ps,))
		#print ("phrase_nos: %s" % (phrase_nos,))
		phrase_no  = phrase_nos[0]
		assert phrase_no == 0
		#print (phrase_no)
		#print (type (phrase_no))
		phrase     = self.elem (phrase_no)
		assert phrase == tuple (self.all ())[0], "phrase: %s, %s" % (phrase, tuple (self.all ())[0])
		return 0, phrase
	def  last_phrase (self):
		section_no, si = self.last_section ()
		#print ("section_no: %s, si: %s" % (section_no, si))
		phrase_nos = self.sp[section_no]
		#print ("sp: %s" % (self.sp,))
		#print ("ps: %s" % (self.ps,))
		#print ("phrase_nos: %s" % (phrase_nos,))
		phrase_no  = phrase_nos[-1]
		#print (phrase_no)
		#print (type (phrase_no))		
		phrase     = self.elem (phrase_no)
		#print ("phrase: %s" % (phrase,))
		assert phrase == tuple (self.all ())[-1], "phrase: %s, %s" % (phrase, tuple (self.all ())[-1],)
		assert phrase_no + 1 == len (tuple (self.all ())), "phrase_no: %s, len: %s" % (phrase_no, len (tuple (self.all ())))
		return phrase_no, phrase
	def pre_phrases (self):
		for section_no, si in self.pre_sections ():
			phrase_nos = self.sp[section_no]
			phrase_no  = phrase_nos[-1]
			phrase     = self.elem (phrase_no)
			#assert phrase == tuple (self.all ())[-1], "phrase: %s, %s" % (phrase, tuple (self.all ())[-1],)
			#assert phrase_no + 1 == len (tuple (self.all ())), "phrase_no: %s, len: %s" % (phrase_no, len (tuple (self.all ())))
			yield phrase_no, phrase






	# TODO Cadence.elem ()
	#@jit
	def section (self, phrase_no): # phrase_no to section
		#section_no, k = self.psmap[phrase_no]
		#section_no, k = Cadence.elem (self, phrase_no)
		#return self.section0 (section_no, k)
		#section = c[i]
		#return section[k]
		#short, i    = Cadence.elem (self, phrase_no)
		short, i = self.order [phrase_no]
		#print ("short: %s, i: %s" % (short, i))
		return self.section0 (short, i)
	def section0 (self, short, i):
		if short: c = self.scs
		else:     c = self.lcs
		#print ("c: %s, c[i=%s]: %s" % (c, i, c[i]))
		return c[i]
	def elem (self, phrase_no): # phrase_no to phrase
		#print ("phrase_no: %s" % (phrase_no,))
		#print (type (phrase_no))
		section = self.section (phrase_no)
		#print ("section: %s" % (section,))
		sk      = self.ps[phrase_no]
		section_no, k = sk
		#print ("section_no: %s, k: %s" % (section_no, k))
		assert self.sp[section_no][k] == phrase_no, "%s, %s" % (self.sp[section_no][k], phrase_no)
		#print (k)
		return section[k]
	#@jit
	# TODO Cadence.all (self)
	def all_sections (self):
		#print ("parent: %s" % list (Cadence.all (self)))
		#k = 0
		#for short, i in Cadence.all (self):
		for short, i in self.sc.all ():
			section = self.section0 (short, i)
			#k       = 
			#yield section[k]
			#k = k + 1
			yield section
	def all (self): return chain (*self.all_sections ())
	
	
	def all_phrases (self): return chain (*self.all_sections ())
	def phrase_elem (self, phrase_no):
		return self.elem (phrase_no)
	def section_elem (self, section_no):
		#print (section_no)
		#phrase_nos = self.sp[section_no]
		#return (self.phrase_elem (phrase_no) for phrase_no in phrase_nos)
		return tuple (self.all_sections ())[section_no]
	
	def nsc    (self): return self.sc.nsc    () # number of      short sections
	def nlc    (self): return self.sc.nlc    () # number of      long  sections
	def ns     (self): return self.sc.ns     () # number of            sections
	def nsuniq (self): return self.sc.nsuniq () # number of uniq short sections
	def nluniq (self): return self.sc.nluniq () # number of uniq long  sections
	def nuniq  (self): return self.sc.nuniq  () # number of uniq       sections
	def np (self):
		s = sum (len (section) for section in self.all_sections ())
		assert s == len (tuple (self.all ()))
		return s
	#def npuniq (self): return len (set (self.uniq.values ()))
	def npuniq (self): return len (set (self.all ()))
def random_section_cadence (maxsc=None):
	#if short is None: short = random_bool ()
	if maxsc is None:
		temp = randrange (2, len (section_db) + 1) - 1 # temp = section_db[1 - 1]
		temp = section_db[temp]
	#elif short is False:
	else:
		#temp = randrange (2, len (section_db) + 1) - 1
		temp = randrange (1, maxsc + 1) - 1
		temp = section_db[temp]
	#else: raise Exception (short)
	sc = choice (temp)
	assert sc is not None
	assert type (sc) is tuple, nsection
	return sc
def cadence_helper0 (cs): # cadences => uniq, dups
	uniq = {}
	dups = {}
	for c in chain (*cs.values ()):
		if c in uniq:
			dups[c] = dups[c] + 1
			continue
		uniq[c] = len (set (c)) #max (c) + 1
		dups[c] = 1
	print ("uniq: %s" % uniq)
	print ("dups: %s" % dups)
	return uniq, dups
def cadence_helper1 (uniq, dups): # uniq, dups => min, max
	minsum, maxsum = 0, 0
	for c, max_c in uniq.items ():
		ndup = dups[c]
		cmin = max (max_c - minsum, 0) # min number to preserve uniqueness constraint
		cmax = max_c * ndup # max number possible
		assert cmin <= cmax
		while True:
			nperm = factorial (cmin + minsum) # number of unique combinations
			if nperm >= cmax: break
			cmin  = cmin + 1
			assert cmin <= cmax
		minsum = cmin + minsum
		maxsum = cmax + maxsum
	print ("min: %s" % minsum)
	print ("max: %s" % maxsum)
	return minsum, maxsum
def cadence_helper2 (kvs, minsum, maxsum):
	phrase_ndxs = tuple (range (0, maxsum))
	print ("ndxs: %s" % (phrase_ndxs,))
	mapping = {}		
	for CI, C in kvs.items ():
		for c in C:		
			pt = list (phrase_ndxs)
			shuffle (pt)
			pt = permutations (tuple (pt), len (set (c)))
			while True:
				temp = next (pt)
				if temp not in chain (*mapping.values ()): break
			if CI in mapping: mapping[CI] = tuple (list (mapping[CI]) + [temp])
			else:             mapping[CI] = tuple ([temp])
			
	print ("map1: %s" % mapping.items ())
	print ("map2: %s" % set (chain (*chain (*mapping.values ()))))
	n = len (set (chain (*chain (*mapping.values ()))))
	print ("n  : %s" % n)
	# TODO
	#assert minsum <= n,      "minsum: %s, n: %s" % (minsum, n)
	#assert n      <= maxsum, "maxsum: %s, n: %s" % (maxsum, n)
	return mapping, n
def cadence_helper3 (mapping):
	mapuniq = {}
	normndx = 0
	for short, phrases in mapping.items (): # normalize indices
		for phrase in phrases:
			for ndx in phrase:
				if ndx in mapuniq: continue
				mapuniq[ndx] = normndx
				normndx = normndx + 1
	print ("mapuniq: %s" % mapuniq)
	return mapuniq
def cadence_helper4 (mapping, mapuniq):
	ret = {}
	#msc = []
	#mlc = []
	#for ndxs in mapping[False]:
	for short, phrases in mapping.items (): # normalize indices
		for phrase in phrases:
			new_phrase = tuple (mapuniq[ndx] for ndx in phrase)
			#if short: msc = msc + [new_phrase]
			#else:     mlc = mlc + [new_phrase]
			if short in ret: ret[short] = tuple (list (ret[short]) + [new_phrase])
			else:            ret[short] = tuple ([new_phrase])
	#msc  = tuple (msc)
	#mlc  = tuple (mlc)
	#print ("msc : %s" % (msc,))
	#print ("mlc : %s" % (mlc,))
	#return msc, mlc
	return ret
#def cadence_helper5 (msc, mlc, sc, lc):
def cadence_helper5 (m, s):
	#msc2 = []
	#mlc2 = []
	m2 = {}
	for k, v in m.items ():
		for phrase, cadence in zip (v, s[k]):
			new_phrase = tuple (phrase[ndx] for ndx in cadence)				
			if k in m2: m2[k] = tuple (list (m2[k]) + [new_phrase])
			else:       m2[k] = tuple ([new_phrase])
		
	#for phrase, cadence in zip (msc, sc): # expand indices		
	#	new_phrase = tuple (phrase[ndx] for ndx in cadence)				
	#	msc2 = msc2 + [new_phrase]
	#for phrase, cadence in zip (mlc, lc): # expand indices
	#	new_phrase = tuple (phrase[ndx] for ndx in cadence)
	#	mlc2 = mlc2 + [new_phrase]
	#msc2 = tuple (msc2)
	#mlc2 = tuple (mlc2)
	#print ("msc2: %s" % (msc2,))
	#print ("mlc2: %s" % (mlc2,))
	#return msc2, mlc2
	return m2
def random_section_cadences (ss=None, ss_arg=None, sc=None, lc=None):
	if ss is None: ss = random_song_cadence (*ss_arg)
	nsc = ss.nsuniq ()
	nlc = ss.nluniq ()
	print ("nsc : %s" % nsc)
	print ("nlc : %s" % nlc)
	if lc is None: lc = tuple ((random_section_cadence () for _ in range (0, nlc)))
	maxsc = min (len (c) for c in lc) - 1
	if sc is None: sc = tuple ((random_section_cadence (maxsc)  for _ in range (0, nsc)))
	assert nsc == len (sc)
	assert nlc == len (lc)
	print ("sc  : %s" % (sc,))
	print ("lc  : %s" % (lc,))
	
	cs = { True : sc, False : lc }
	
	uniq, dups = cadence_helper0 (cs)
	minsum, maxsum = cadence_helper1 (uniq, dups)
	mapping, n = cadence_helper2 (cs, minsum, maxsum)
	#assert True  in mapping
	#assert False in mapping
	mapuniq = cadence_helper3 (mapping)
	#assert True  in mapuniq
	#assert False in mapuniq
	#msc, mlc = cadence_helper4 (mapping, mapuniq)
	msc = cadence_helper4 (mapping, mapuniq)
	#assert True  in msc
	#assert False in msc
	#msc2, mlc2 = cadence_helper5 (msc, mlc, sc, lc)
	m = cadence_helper5 (msc, cs)
	#msc2 = m[True]
	#mlc2 = m[False]
	if True  in m: msc2 = m[True]
	else:          msc2 = ()
	if False in m: mlc2 = m[False]
	else:          mlc2 = ()
	return SectionCadence (ss, msc2, mlc2)
	









































phrase_db = (
	((0,),),     # one   segment
	((0, 0),     # two   segments, same cadence
	 (0, 1)),    # two   segments, same cadence
	((0, 0, 0),  # three segments, same cadence
	 (0, 0, 1),  # three segments, last  different
	 (0, 1, 1)), # three segments, first different
)
class PhraseCadence (Cadence):
	def __init__ (self, sc, m):
		Cadence.__init__ (self, m, tuple (sc.all ()))
		#print ("m: %s" % (m,))
		#print ("sc: %s" % list (sc.all ()))
		self.sc = sc
	def __repr__ (self): return "PhraseCadence [%s]" % (Cadence.__repr__ (self))
	#def elem (self, segment_no): # phrase cadence
	#def phrase_elem (self, phrase_no): # section cadence
	#	return self.uniq[phrase_no]
	def phrase_elem (self, phrase_no): return Cadence.elem (self, phrase_no)
	def all_phrases (self): return Cadence.all (self)
	#def all_phrases (self): return (self.uniq[phrase_no] for phrase_no in self.sc.all ())
	def segment_elem (self, segment_no):
		#phrase_no = self.sp[segment_no]
		#phrase    = self.phrase_elem (phrase_no)
		#segno     = self.ss[segment_no]
		#return phrase[segno]
		return tuple (self.all_segments ())[segment_no]
	def all_segments (self): return chain (*self.all_phrases ())
	def section_elem (self, section_no):
		#print (section_no)
		phrase_nos = self.sc.section_elem (section_no)
		return (self.phrase_elem (phrase_no) for phrase_no in phrase_nos)
	def all_sections (self):
		for section_no in chain (*self.sc.all_sections ()):
			yield tuple (self.section_elem (section_no))
	#def all_sections (self): return chain (*self.all_sections0 ())
	def first_section (self): return 0, tuple (self.section_elem (0))
	def nsection (self): return self.sc.ns ()
	def  last_section (self):
		n = self.nsection ()
		assert tuple (self.section_elem (n - 1)) == tuple (self.section_elem (-1)), "%s, %s" % (tuple (self.section_elem (n - 1)), tuple (self.section_elem (-1)))
		return n - 1, tuple (self.section_elem (-1))
	def first_phrase (self): return 0, tuple (self.phrase_elem (0))
	def nphrase (self): return self.sc.np ()
	def  last_phrase (self):
		n = self.nphrase ()
		assert self.phrase_elem (n - 1) == self.phrase_elem (-1)
		return n - 1, tuple (self.phrase_elem (-1))
	def first_segment (self): return 0, self.segment_elem (0)
	def nsegment (self): return len (tuple (self.all_segments ()))
	def last_segment (self):
		n = self.nsegment ()
		assert self.segment_elem (n - 1) == self.segment_elem (-1)
		return n - 1, self.segment_elem (-1)
	"""
	def first_section  (self):
		section_no, si = self.sc.first_section ()
		short, i = si
		return section_no, self.section0 (short, i)
	def  last_section  (self):
		section_no, si = self.sc.last_section ()
		short, i = si
		return section_no, self.section0 (short, i)
	def   pre_sections (self):
		sis = self.sc.pre_sections ()
		for section_no, si in sis:
			short, i = si
			yield section_no, self.section0 (short, i)
	def chorii (self):
		sis = self.sc.chorii ()
		for section_no, si in sis:
			short, i = si
			yield section_no, self.section0 (short, i)
	def first_phrase (self):
		section_no, si = self.first_section ()
		#print ("section_no: %s, si: %s" % (section_no, si))
		phrase_nos = self.sp[section_no]
		#print ("sp: %s" % (self.sp,))
		#print ("ps: %s" % (self.ps,))
		#print ("phrase_nos: %s" % (phrase_nos,))
		phrase_no  = phrase_nos[0]
		assert phrase_no == 0
		#print (phrase_no)
		#print (type (phrase_no))
		phrase     = self.elem (phrase_no)
		assert phrase == tuple (self.all ())[0], "phrase: %s, %s" % (phrase, tuple (self.all ())[0])
		return 0, phrase
	def  last_phrase (self):
		section_no, si = self.last_section ()
		#print ("section_no: %s, si: %s" % (section_no, si))
		phrase_nos = self.sp[section_no]
		#print ("sp: %s" % (self.sp,))
		#print ("ps: %s" % (self.ps,))
		#print ("phrase_nos: %s" % (phrase_nos,))
		phrase_no  = phrase_nos[-1]
		#print (phrase_no)
		#print (type (phrase_no))		
		phrase     = self.elem (phrase_no)
		#print ("phrase: %s" % (phrase,))
		assert phrase == tuple (self.all ())[-1], "phrase: %s, %s" % (phrase, tuple (self.all ())[-1],)
		assert phrase_no + 1 == len (tuple (self.all ())), "phrase_no: %s, len: %s" % (phrase_no, len (tuple (self.all ())))
		return phrase_no, phrase
	def pre_phrases (self):
		for section_no, si in self.pre_sections ():
			phrase_nos = self.sp[section_no]
			phrase_no  = phrase_nos[-1]
			phrase     = self.elem (phrase_no)
			#assert phrase == tuple (self.all ())[-1], "phrase: %s, %s" % (phrase, tuple (self.all ())[-1],)
			#assert phrase_no + 1 == len (tuple (self.all ())), "phrase_no: %s, len: %s" % (phrase_no, len (tuple (self.all ())))
			yield phrase_no, phrase
	"""
	
	"""
	def elem (self, segment_no):
		phrase_no = self.sp[segment_no]
		

	#@jit
	def section (self, phrase_no): # phrase_no to section
		#section_no, k = self.psmap[phrase_no]
		#section_no, k = Cadence.elem (self, phrase_no)
		#return self.section0 (section_no, k)
		#section = c[i]
		#return section[k]
		#short, i    = Cadence.elem (self, phrase_no)
		short, i = self.order [phrase_no]
		#print ("short: %s, i: %s" % (short, i))
		return self.section0 (short, i)
	def section0 (self, short, i):
		if short: c = self.scs
		else:     c = self.lcs
		#print ("c: %s, c[i=%s]: %s" % (c, i, c[i]))
		return c[i]
	def elem (self, phrase_no): # phrase_no to phrase
		#print ("phrase_no: %s" % (phrase_no,))
		#print (type (phrase_no))
		section = self.section (phrase_no)
		#print ("section: %s" % (section,))
		sk      = self.ps[phrase_no]
		section_no, k = sk
		#print ("section_no: %s, k: %s" % (section_no, k))
		assert self.sp[section_no][k] == phrase_no, "%s, %s" % (self.sp[section_no][k], phrase_no)
		#print (k)
		return section[k]
	#@jit
	def all_sections (self):
		#print ("parent: %s" % list (Cadence.all (self)))
		#k = 0
		#for short, i in Cadence.all (self):
		for short, i in self.sc.all ():
			section = self.section0 (short, i)
			#k       = 
			#yield section[k]
			#k = k + 1
			yield section
	def all (self): return chain (*self.all_sections ())
	def nsc    (self): return self.sc.nsc    () # number of      short sections
	def nlc    (self): return self.sc.nlc    () # number of      long  sections
	def ns     (self): return self.sc.ns     () # number of            sections
	def nsuniq (self): return self.sc.nsuniq () # number of uniq short sections
	def nluniq (self): return self.sc.nluniq () # number of uniq long  sections
	def nuniq  (self): return self.sc.nuniq  () # number of uniq       sections
	def np (self):
		s = sum (len (section) for section in self.all_sections ())
		assert s == len (tuple (self.all ()))
		return s
	#def npuniq (self): return len (set (self.uniq.values ()))
	def npuniq (self): return len (set (self.all ()))		
		"""
		
		
		
		
		
		
		
		
		
def random_phrase_cadence (nseg=None):
	if nseg is None: nseg = randrange (0, len (phrase_db))
	temp = phrase_db[nseg]
	return choice (temp)
def random_phrase_cadences (sc=None, sc_args=None, pc=None):
	if sc is None: sc = random_section_cadences (*sc_args)
	np = sc.npuniq ()
	if pc is None: pc = tuple ((random_phrase_cadence () for _ in range (0, np)))
	assert np == len (pc)
	
	cs = { True : pc }
	uniq, dups     = cadence_helper0 (cs)
	minsum, maxsum = cadence_helper1 (uniq, dups)
	mapping, n     = cadence_helper2 (cs, minsum, maxsum)
	mapuniq        = cadence_helper3 (mapping)
	msc            = cadence_helper4 (mapping, mapuniq)
	m              = cadence_helper5 (msc, cs)
	msc2 = m[True] 
	return PhraseCadence (sc, msc2)	
	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	def main ():
		#for nsection in range (0, 3 + 1):
		#	sc = random_sc0 (nsection)
		#	print (sc)
		#	print (list (sc.all ()))
		#print ()
		sc = random_song_cadence ()
		print ("song cadence  : %s" % sc)
		print ("sections      : %s" % list (sc.all ()))
		print (list (zip (sc.order, list (sc.all ()))))
		print ("first section : %s" % (sc.first_section (),))
		print ("last  section : %s" % (sc. last_section (),))
		print ("pre   sections: %s" % list (sc.  pre_sections ()))
		print ("chorii        : %s" % list (sc.  chorii       ()))
		print ("nsection      : %s" % sc.ns    ())
		print ("uniq          : %s" % sc.nuniq ())
		sc = random_section_cadences (sc)
		print ("section cadence: %s" % sc)
		print ("all sections  : %s" % list (sc.all_sections ()))
		print ("all phrases   : %s" % list (sc.all          ()))
		print ("first section : %s" % (sc.first_section (),))
		print ("last  section : %s" % (sc. last_section (),))
		print ("pre   sections: %s" % list (sc.  pre_sections ()))
		print ("chorii        : %s" % list (sc.  chorii       ()))
		print ("nsection      : %s" % sc.ns     ())
		print ("uniq          : %s" % sc.nuniq  ())
		print ("nphrase       : %s" % sc.np     ())
		print ("uniq          : %s" % sc.npuniq ())
		print ("first phrase  : %s" % (sc.first_phrase (),))
		print ("last  phrase  : %s" % (sc. last_phrase (),))
		print ("pre   phrases : %s" % list (sc.  pre_phrases (),))
		pc = random_phrase_cadences (sc)
		print ("phrase cadence: %s" % pc)
		print ("all sections  : %s" % (list (pc.all_sections ())))
		print ("all phrases   : %s" % (list (pc.all_phrases  ())))
		print ("all segments  : %s" % (list (pc.all_segments ())))
		print ("first section : %s" % (pc.first_section (),))
		print ("first phrase  : %s" % (pc.first_phrase  (),))
		print ("first segment : %s" % (pc.first_segment (),))
		print ("last  section : %s" % (pc. last_section (),))
		print ("last  phrase  : %s" % (pc. last_phrase  (),))
		print ("last  segment : %s" % (pc. last_segment (),))
		print ("chorii        : %s" % list (pc.  chorii       ()))
		print ("nsection      : %s" % pc.nsection ())
		print ("uniq          : %s" % pc.nuniq    ())
		print ("nphrase       : %s" % pc.nphrase  ())
		print ("uniq          : %s" % pc.npuniq   ())
		print ("nsegment      : %s" % pc.nsegment ())
		print ("uniq          : %s" % pc.nsuniq   ())
		print ("first phrase  : %s" % (pc.first_phrase (),))
		print ("last  phrase  : %s" % (pc. last_phrase (),))
		print ("pre   phrases : %s" % list (pc.  pre_phrases (),))
	main ()
	
