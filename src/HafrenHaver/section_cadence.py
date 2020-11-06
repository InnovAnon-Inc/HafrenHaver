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
		
section_db = (
	((0,),),       # one   phrase
	((0, 0),     # two   phrases, same      cadence
	 (0, 1),),    # two   phrases, different cadence
	((0, 0, 0),  # three phrases, same      cadence
	 (0, 0, 1),  # three phrases, last  different
	 (0, 1, 0),  # three phrases, mid   different
	 (0, 1, 1), # three phrases, first different
	 
	 (0, 1, 2),
	),	 
	((0, 0, 0, 0),
	 (0, 0, 0, 1),
	 (0, 0, 1, 0),
	 (0, 1, 0, 0),
	 (0, 0, 1, 1),
	 (0, 1, 0, 1),
	 (0, 1, 1, 1),
	 (0, 1, 2, 1),),
)
# the number of phrases in each section;
# long phrases and short phrases are handled separately
# section_no => hash => phrase_no
class SectionCadence (Cadence):
	@staticmethod
	def mapping (sc, scs, lcs):
		# TODO
		uniq = {}
		sci = 0
		lci = 0
		assert len (list (sc.all_sections ())) == sc.nsection ()
		#for section_no, cv in sc.sections ():
		for short, index in sc.all_sections ():
		##for short, index in sc.uniq_sections ():
		#for F in range (0, sc.nsection ()):
			#short, index = sc[F]
			if (short, index) in uniq: continue
			#section_type, index = cv
			#short,        index = sc.section2d (*cv)
			assert (short, index) not in uniq
			if short:
				#uniq[(short, index)] = short, sci
				uniq[(short, index)] = scs[sci]
				#assert type (scs[sci]) is not tuple, "scs[%s]: %s" % (sci, scs[sci])
				sci = sci + 1
			else:
				#uniq[(short, index)] = short, lci
				uniq[(short, index)] = lcs[lci]
				#assert type (lcs[lci]) is not tuple, "lcs[%s]: %s" % (lci, lcs[lci])
				lci = lci + 1
		assert lci == len (lcs)
		assert sci == len (scs)
		#print ("\nlcs: %s\nscs: %s\n\n" % (lcs, scs))
		order = []
		#phrase_no = 0
		#section_no = 0
		#spmap = []
		for short, index in sc.all_sections ():
		#for F in range (0, sc.nsection ()):
		#	short, index = sc[F]
			assert (short, index) in uniq
			#if short:
				#dp = len (scs[index])
			#else:
				#dp = len (lcs[index])
			dp = len (uniq[(short, index)])
			order = order + [(short, index)]
#			for k in range (0, dp):
				#order = order + [(short, index, k)]
#				order = order + [(short, index)]
				#phrase_no = phrase_no + 1
			#spmap[section_no] = spma
			#phrase_no = phrase_no + dp
			#section_no = section_no + 1
		order = tuple (order)
		
		for short, index in order:        assert (short, index) in uniq,  "short: %s, index: %s, uniq: %s" % (short, index, uniq)
		for short, index in uniq.keys (): assert (short, index) in order, "short: %s, index: %s, uniq: %s, order: %s" % (short, index, uniq, order)
		
		#spmap = tuple (spmap)
		print ("uniq: %s" % (uniq,))
		print ("order: %s" % (order,))
		return uniq, order
	@staticmethod
	def init_psmap (sc, scs, lcs, uniq):
		phrase_no = 0
		section_no = 0
		#spmap = []
		psmap = []
		for short, index in sc.all_sections ():
		#for F in range (0, sc.nsection ()):
		#	short, index = sc[F]
			#if short: dp = len (scs[index])
			#else:     dp = len (lcs[index])
			dp = len (uniq[(short, index)])
			#print ("short: %s, index: %s, dp: %s" % (short, index, dp))
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
		assert section_no == sc.nsection ()
		#assert phrase_no == sc.nphrase ()
		print ("psmap: %s" % (psmap,))
		return psmap
	@staticmethod
	def init_spmap (sc, scs, lcs, uniq):
		phrase_no = 0
		section_no = 0
		spmap = []
		for short, index in sc.all_sections ():
		#for F in range (0, sc.nsection ()):
		#	short, index = sc[F]
			#if short:
			#	dp = len (scs[index])
			#else:
			#	dp = len (lcs[index])
			dp = len (uniq[(short, index)])
			#dp = dp + 1
			spmap = spmap + [tuple (range (phrase_no, phrase_no + dp))]
			phrase_no = phrase_no + dp
			section_no = section_no + 1
		spmap = tuple (spmap)
		assert section_no == sc.nsection ()
		#assert phrase_no == sc.nphrase ()
		assert len (spmap) == section_no
		print ("spmap: %s" % (spmap,))
		return spmap
		
	def __init__ (self, sc, scs, lcs):
		#Cadence.__init__ (self, *SectionCadence.init_map (sc, scs, lcs))
		Cadence.__init__ (self, *SectionCadence.mapping (sc, scs, lcs)) # phrase_no to section_no
		self.sc  = sc
		self.scs = scs
		self.lcs = lcs
		#self.sp, self.ps = SectionCadence.init_spmap (sc, scs, lcs)
		self.ps = SectionCadence.init_psmap (sc, scs, lcs, self.uniq)
		self.sp = SectionCadence.init_spmap (sc, scs, lcs, self.uniq)
		assert len (self.sp) == self.nsection ()
		print ("all sections: %s" % (list (self.all_sections ()),))
		assert len (self.ps) == self.nphrase (), "%s != %s, %s" % (len (self.ps), self.nphrase (), self.all_phrases ())
		assert len (self.order) == len (self.sp)
		#print ("sp: %s" % (self.sp,))
	def __repr__ (self): return "SectionCadence [%s, sc=%s, scs=%s, lcs=%s]" % (Cadence.__repr__ (self), self.sc, self.scs, self.lcs)
	# TODO
	# section_type (section_no)
	# section_index (phrase_no)
	# sections ()
	def first_section  (self):
		section_no, si = self.sc.first_section ()
		short, i = si
		return section_no, self[(short, i)]
	def  last_section  (self):
		section_no, si = self.sc.last_section ()
		short, i = si
		return section_no, self[(short, i)]
	def   pre_sections (self):
		sis = self.sc.pre_sections ()
		for section_no, si in sis:
			short, i = si
			yield section_no, self[(short, i)]
	def chorii (self):
		sis = self.sc.chorii ()
		for section_no, si in sis:
			short, i = si
			yield section_no, self[(short, i)]
	def first_phrase (self):
		section_no, si = self.first_section ()
		phrase_nos = self.sp[section_no]
		phrase_no  = phrase_nos[0]
		return phrase_no, si[0]
		#print ("section_no: %s, si: %s" % (section_no, si))
#		phrase_nos = self.sp[section_no]
		#print ("sp: %s" % (self.sp,))
		#print ("ps: %s" % (self.ps,))
		#print ("phrase_nos: %s" % (phrase_nos,))
#		phrase_no  = phrase_nos[0]
#		assert phrase_no == 0
		#print (phrase_no)
		#print (type (phrase_no))
		#phrase     = self.elem (phrase_no)
#		phrase = self[phrase_no]
		#assert phrase == tuple (self.all ())[0], "phrase: %s, %s" % (phrase, tuple (self.all ())[0])
#		return 0, phrase
#		short, i = self.phrase_index (0)
#		return self[(short, i)]
	def  last_phrase (self):
		section_no, si = self.last_section ()
		a = si[-1]
		b = self.all_phrases ()[-1]
		#b = b[-1]
		assert a == b, "%s != %s\n%s != %s" % (a, b, si, self.all_phrases ())
		n = self.nphrase ()
		c = self.all_phrases ()[n - 1]
		#c = c[-1]
		assert a == c, "%s != %s, %s" % (a, c, n)
		
		phrase_nos = self.sp[section_no]
		phrase_no  = phrase_nos[-1]
		
		return phrase_no, si[-1]
		#print ("section_no: %s, si: %s" % (section_no, si))
#		phrase_nos = self.sp[section_no]
		#print ("sp: %s" % (self.sp,))
		#print ("ps: %s" % (self.ps,))
		#print ("phrase_nos: %s" % (phrase_nos,))
#		phrase_no  = phrase_nos[-1]
		#print (phrase_no)
		#print (type (phrase_no))		
		#phrase     = self.elem (phrase_no)
#		phrase = self[phrase_no]
		#print ("phrase: %s" % (phrase,))
#		assert phrase == tuple (self.all ())[-1], "phrase: %s, %s" % (phrase, tuple (self.all ())[-1],)
#		assert phrase_no + 1 == len (tuple (self.all ())), "phrase_no: %s, len: %s" % (phrase_no, len (tuple (self.all ())))
#		return phrase_no, phrase
#		short, i = self.phrase_index (-1)
#		return self[(short, i)]
#		return self.phrase_elem (-1)
	def pre_phrases (self):
		for section_no, section in self.pre_sections ():
			phrase_nos = self.sp[section_no]
			phrase_no  = phrase_nos[-1]
			yield phrase_no, section[-1]
#		for section_no, si in self.pre_sections ():
#			phrase_nos = self.sp[section_no]
#			phrase_no  = phrase_nos[-1]
#			#phrase     = self.elem (phrase_no)
#			phrase = self[phrase_no]
#			#assert phrase == tuple (self.all ())[-1], "phrase: %s, %s" % (phrase, tuple (self.all ())[-1],)
#			#assert phrase_no + 1 == len (tuple (self.all ())), "phrase_no: %s, len: %s" % (phrase_no, len (tuple (self.all ())))
#			yield (phrase_no, phrase)



	
#	def section0 (self, short, i):
#		if short: c = self.scs
#		else:     c = self.lcs
#		#print ("c: %s, c[i=%s]: %s" % (c, i, c[i]))
#		return c[i]


	# TODO Cadence.elem ()
	##@jit
#	def section (self, phrase_no): # phrase_no to section
		#section_no, k = self.psmap[phrase_no]
		#section_no, k = Cadence.elem (self, phrase_no)
		#return self.section0 (section_no, k)
		#section = c[i]
		#return section[k]
		#short, i    = Cadence.elem (self, phrase_no)
#		short, i = self.order [phrase_no]
		#print ("short: %s, i: %s" % (short, i))
#		return self.section0 (short, i)
	
#	def elem (self, phrase_no): # phrase_no to phrase
		#print ("phrase_no: %s" % (phrase_no,))
		#print (type (phrase_no))
#		section = self.section (phrase_no)
		#print ("section: %s" % (section,))
#		sk      = self.ps[phrase_no]
#		section_no, k = sk
		#print ("section_no: %s, k: %s" % (section_no, k))
#		assert self.sp[section_no][k] == phrase_no, "%s, %s" % (self.sp[section_no][k], phrase_no)
		#print (k)
#		return section[k]
	##@jit
	
	
	
	
	
#	def __getitem__ (self, i):
#		st = Pattern.__getitem__ (self, i)
#		return self.section_index (st)
#	def section_index (self, st):
#		section_type, index = Cadence.__getitem__ (self, st)
#		return section_type == self.sc, section_type[index]
#	def __iter__ (self): return (self.section_index (st) for st in Pattern.__iter__ (self))
	
	
	
	
	
	
	
	

	def section_elems (self, section_no):
		short, i = self.order[section_no]
		section  = self.uniq[(short, i)]
		#print ("sn: %s, short: %s, i: %s, section: %s" % (section_no, short, i, section))
		return section
		#print ("%s[%s]" % (list (self), section_no))
		#print ("section elem: %s" % (self[section_no],))
		#return tuple (self)[section_no]
	def phrase_elem (self, phrase_no):
		section_no, k = self.ps[phrase_no]
		short, i = self.order[section_no]
		section  = self.uniq[(short, i)]
		#section = self[section_no]
		return section[k]
	def all_sections (self):
		#return tuple (map (self.section_elems, range (0, self.nsection ())))
		#for k in range (0, self.nsection ()):
		#	yield self.section_elems (k)
		ret = []
		ns = 0
		for short, i in self.order:
			section = self.uniq[(short, i)]
			ret = ret + [section]
			ns = ns + 1
		assert ns == self.nsection (), "%s != %s" % (ns, self.nsection ())
		return ret
	def all_phrases (self): return tuple (chain (*self.all_sections ()))
		
	def section_types (self): return tuple ((st, self.uniq[i]) for st, i in self.sc.section_types ())
	def all_section_types (self): return self.sc.all_section_types ()
		
#	def phrase_elem (self, phrase_no):
#		print ("ps: %s, phrase_no: %s" % (self.ps, phrase_no))
#		section_no, k = self.ps[phrase_no]
#		print ("sn: %s, k: %s" % (section_no, k))
#		short, i = self.order[section_no]
#		print ("short: %s, i: %s" % (short, i))
#		section  = self.uniq[short, i]
#		#section = self[section_no]
#		print ("section: %s, k: %s, pn: %s" % (section,k,phrase_no))
#		return section[k]
	
#	def phrase_index (self, i):
	#	print ("sc: %s" % (self.sc,))
	#	print ("i : %s" % (i,))
		#return self.sc[i] # => short, i
		# TODO
	#	return self.ps[i]
#		return self.pattern (i)
#	def phrase_elem  (self, phrase_no):
#		#print ("phrase_no: %s" % (phrase_no,))
#		short, i = self.phrase_index (phrase_no)
#		#print ("self[short: %s, i: %s]: %s" % (short, i, self[(short, i)]))
#		assert type (self[(short, i)]) is not tuple
#		return self[(short, i)]	
	
	#def __iter__ (self): return (phrase_elem (phrase_no) for phrase_no in range (0, self.nphrase ()))
	# TODO Cadence.all (self)
#	def all_sections (self):
		#assert self.nsection () == len (list (iter (self))), "%s != %s, %s" % (self.nsection (), len (self), list (self))
		#return iter (self)
#		return tuple (self.section_elems (k) for k in range (0, self.nsection ()))
		#for section_no in range (0, self.nsection ()):
			
#	def all_phrases (self): return tuple (chain (*self.all_sections ()))
#	def phrase_elem (self, phrase_no):
#		return self.elem (phrase_no)
#	def section_elems (self, section_no): #return tuple (map (self.phrase_elem, self.section_indices (section_no)))
#		#print (section_no)
#		phrase_nos = self.sp[section_no]
#		return tuple (self.phrase_elem (phrase_no) for phrase_no in phrase_nos)
#		#return tuple (self.all_sections ())[section_no]
#	def section_indices (self, section_no):
#		#print ("section_no: %s" % (section_no,))
#		#print ("sp: %s" % (self.sp,))
#		assert section_no < len (self.sp), "%s >= %s: %s" % (section_no, len (self.sp), self.sp)
#		#assert section_no in self.sp, "%s not in %s" % (section_no, self.sp)
#		#print ("sp[%s]: %s" % (section_no, self.sp[section_no]))
#		return self.sp[section_no]
	
	
	def nshort_section    (self): return self.sc.nshort_section    () # number of      short sections
	def nlong_section    (self): return self.sc.nlong_section    () # number of      long  sections
	def nsection     (self): return self.sc.nsection () # number of            sections
	def nuniq_short_section (self): return self.sc.nuniq_short_section () # number of uniq short sections
	def nuniq_long_section (self): return self.sc.nuniq_long_section () # number of uniq long  sections
	def nuniq_section  (self):
		assert self.sc.nuniq () == self.nuniq ()
		return self.sc.nuniq  () # number of uniq       sections
	#def nphrase (self): return len (self)
	# TODO
	def nphrase (self):
		#a = len (self)
		b = len (self.all_phrases ())
		#assert a == b, "%s != %s" % (a, b)
		#return a
		return b
#		s = sum (len (section) for section in self.all_sections ())
#		#assert s == len (tuple (self.all ()))
#		assert s == len (self)
#		return len (self)
		#return s
	#def npuniq (self): return len (set (self.uniq.values ()))
	def nuniq_phrase (self):
		#return self.nuniq ()
		return len (set (self.all_phrases ()))
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
def cadence_helper05 (cs):
	uniq   , dups   = cadence_helper0 (cs)
	minsum , maxsum = cadence_helper1 (uniq, dups)
	mapping, n      = cadence_helper2 (cs, minsum, maxsum)
	mapuniq         = cadence_helper3 (mapping)
	msc             = cadence_helper4 (mapping, mapuniq)
	return            cadence_helper5 (msc, cs)
def random_section_cadences (ss=None, ss_arg=None, sc=None, lc=None):
	if ss is None: ss = random_song_cadence (*ss_arg)
	nsc = ss.nuniq_short_section ()
	nlc = ss.nuniq_long_section ()
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
	
	m = cadence_helper05 (cs)
	#uniq, dups = cadence_helper0 (cs)
	#minsum, maxsum = cadence_helper1 (uniq, dups)
	#mapping, n = cadence_helper2 (cs, minsum, maxsum)
	##assert True  in mapping
	##assert False in mapping
	#mapuniq = cadence_helper3 (mapping)
	##assert True  in mapuniq
	##assert False in mapuniq
	##msc, mlc = cadence_helper4 (mapping, mapuniq)
	#msc = cadence_helper4 (mapping, mapuniq)
	##assert True  in msc
	##assert False in msc
	##msc2, mlc2 = cadence_helper5 (msc, mlc, sc, lc)
	#m = cadence_helper5 (msc, cs)
	##msc2 = m[True]
	##mlc2 = m[False]
	if True  in m: msc2 = m[True]
	else:          msc2 = ()
	if False in m: mlc2 = m[False]
	else:          mlc2 = ()
	print ("mlc2: %s" % (mlc2,))
	return SectionCadence (ss, msc2, mlc2)
