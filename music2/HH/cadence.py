#! /usr/bin/env python3

from enum      import Enum
from numba     import jit
from random    import choice, randrange, shuffle
from itertools import accumulate, chain

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
	@jit
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
		self.uniq  = uniq
	def __repr__ (self): return "Cadence [%s, uniq=%s]" % (Pattern.__repr__ (self), self.uniq)
	@jit
	def elem (self, i):
		v = Pattern.elem (self, i)
		#return self.u (v)
		return self.uniq[v]
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
	#@jit
	#def elem (self, i):
	#	v = Cadence.elem (self, i)
	#	return v.value ()
	#@jit
	#def all (self): return (v.value () for v in Cadence.all (self))
	#def v (self, v): return Cadence.v (self, v.value ())
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
	n     = randrange (min_n, max_n + 1)
	# TODO map from cardinalities nsection to n
	temp0 = range (0, nsection)
	temp1 = (randrange (0, nsection) for _ in range (0, nsection - n))
	temp  = list (chain (temp0, temp1)) 
	shuffle (temp)
	return SongCadence0 (sc, temp)
	
	
	
	
	
	
class SongCadence (Cadence):
	#@jit
	@staticmethod
	def init_uniq (ss, sc, lc):
		uniq = {}
		sci  = 0
		lci  = 0
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
		return uniq
	def __init__ (self, ss, sc, lc):
		Cadence.__init__ (self, SongCadence.init_uniq (ss, sc, lc), ss.order)
		self.ss = ss # song  cadence
		self.sc = sc # short cadence
		self.lc = lc # long  cadence
	def __repr__ (self): return "SongCadence [ss=%s, sc=%s, lc=%s]" % (self.ss, self.sc, self.lc)
	@jit
	def elem (self, i):
		c, v = Cadence.elem (self, i)
		#return c.uniq[v.value ()]
		#print ("c=%s (v=%s): %s" % (c, v, c.uniq[v]))
		short = (c == self.sc)
		assert (not short) == (c == self.lc)
		return c.uniq[v]
		#return c.u (v)
	#@jit
	#def all (self): return (c.uniq[v.value ()] for c, v in Cadence.all (self))
	def all (self): return (c.uniq[v] for c, v in Cadence.all (self))
	#def all (self):
	#	for c, v in Cadence.all (self):
	#		print ("c=%s (v=%s): %s" % (c, v, c.uniq[v]))
	#		yield c.uniq[v]
	#def all (self): return (c.u (v) for c, v in Cadence.all (self))
	#def v (self, v): return Cadence.v (self, v.value ())
def random_song_cadence (ss=None, sc=None, lc=None):
	if ss is None: ss = random_song_structure ()
	nsc = ss.nsc ()                      # number of short sections
	nlc = ss.nlc ()                      # number of long  sections
	#assert len (ss.order) == nsc + nlc, "tot: %s, short: %s, long: %s" % (len (ss.order), nsc, nlc)
	assert len (set (ss.order)) == nsc + nlc, "tot: %s, short: %s, long: %s" % (len (set (ss.order)), nsc, nlc)
	if sc is None: sc = random_sc0 (nsc) # short sections
	if lc is None: lc = random_sc0 (nlc) # long  sections
	assert len (sc.uniq) == nsc # TODO len (sc.uniq) ?
	assert len (lc.uniq) == nlc
	return SongCadence (ss, sc, lc)
	
	
	
	
	
	
	
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
	def __init__ (self, sc, mapping): Cadence.__init__ (sc, mapping)
def random_section_cadence (short=None):
	if short is None: short = random_bool ()
	if short is True: temp = section_db[1 - 1]
	elif short is False:
		temp = randrange (2, len (section_db) + 1) - 1
		temp = section_db[temp]
	else: raise Exception (short)
	sc = choice (temp)
	assert sc is not None
	assert type (sc) is tuple, nsection
	return sc
def random_section_cadences (nsection, short=None):
	sc = [random_section_cadence (short) for _ in range (0, nsection)]
	nphrase = ?
	
	return SectionCadence (sc, mapping)
	

	
	min_n = max (sc) + 1
	max_n = min_n
	assert max_n <= nsection, "max n: %s, n section: %s" % (max_n, nsection)
	n     = randrange (min_n, max_n + 1)
	# TODO map from cardinalities nsection to n
	temp0 = range (0, nsection)
	temp1 = (randrange (0, nsection) for _ in range (0, nsection - n))
	temp  = list (chain (temp0, temp1)) 
	shuffle (temp)
	return SongCadence0 (sc, temp)








	
	
	
	
	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	def main ():
		for nsection in range (0, 3 + 1):
			sc = random_sc0 (nsection)
			print (sc)
			print (list (sc.all ()))
		print ()
		sc = random_song_cadence ()
		print (sc)
		print (list (sc.all ()))
	main ()
	
