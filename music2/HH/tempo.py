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
from song_cadence0 import random_sc0, reduce_map
from song_cadence import random_song_cadence
from section_cadence import random_section_cadences, cadence_helper05
from phrase_cadence import random_phrase_cadences
from segment_cadence import random_segment_cadences
from bar_cadence import random_bar_cadence
			
class Tempo (Enum): # measured in BPM
	LARGHISSIMO      = ( 20,  24) # very, very slowly
	ADAGISSIMO       = ( 26,  36) # very slowly
	GRAVE            = ( 25,  45) # very slow
	LARGO            = ( 40,  60) # broadly
	LENTO            = ( 45,  60) # slowly
	LARGHETTO        = ( 60,  66) # rather broadly
	ADAGIO           = ( 66,  76) # slowly with great expression
	ADAGIETTO_1      = ( 72,  76) # slower than adante
	ADAGIETTO_2      = ( 70,  80) # slightly faster than adagio
	ADANTE           = ( 76, 108) # at a walking pace
	ANDANTINO        = ( 80, 108) # slightly faster than andante
	MARCIA_MODERATO  = ( 83,  85) # moderately, in the manner of a march
	ANDANTE_MODERATO = ( 92,  98) # between andante and moderato
	MODERATO         = ( 98, 112) # at a moderate speed
	ALLEGRETTO       = (102, 110) # moderately fast
	ALLEGRO_MODERATO = (116, 120) # close to, but not quite allegro
	ALLEGRO          = (120, 156) # fast, quick and bright
	MOLTO_ALLEGRO    = (124, 156)
	VIVACE           = (156, 176) # lively and fast
	VIVACISSIMO      = (172, 176) # very fast and lively
	ALLEGRISSIMO     = (172, 176) # very fast
	ALLEGRO_VIVACE   = (172, 176) # very fast
	PRESTO           = (168, 200) # very, very fast
	PRESTISSIMO      = (200, 220) # even faster than presto
def random_tempo (tempo=None):
	if tempo is None: tempo = choice (list (Tempo))
	tmin, tmax = tempo.value
	return uniform (tmin, tmax)








temporal_cadence_db = {
	#INTRO  : (0,),
	VERSE  : { 3: ((0, 0, 0), (0, 0, 1)),
		       4: ((0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 0, 1),), },
	#PRE    : (0,),
	CHORUS : { 3: ((0, 0, 0), (0, 0, 1),),
	           4: ((0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 0, 1),), },
	BRIDGE : { 2: ((0, 1),),
	           3: ((0, 0, 1), (0, 1, 1),),
	           4: ((0, 1, 0, 1), (0, 1, 1, 0),), },
	#OUTRO  : (0,),
}
class MacroTemporalCadence (Cadence): # intersection vs intrasection
	def __init__ (self, bc, tm):
		Cadence.__init__ (self, *TemporalCadence.initmap (bc, tm))
		self.bc    = bc
		self.tm    = tm
def random_macro_temporal_cadence (bc=None, bc_args=None):
	if bc is None: bc = random_bar_cadence (*bc_args)
	
	# handle whether uniq sections differ
	nmin = 1
	nmax = bc.nsection_type () - 1
	ns   = nmax
	h    = reduce_map (ns, nmin, nmax)
	#ns   = bc.nsection ()
	#h    = reduce_map (ns, nmin, nmax)
	us   = {}
	i    = 0
	for st, section in bc.section_types ():
		assert st not in us
		if st == VERSE: continue
		us[st] = h[i]
		i      = i + 1
	assert i == h
	
	# TODO get reference speeds of uniq sections
	sc = {}
	for st, section in bc.section_types ():
		if st == VERSE: continue
		if not us[st]:
	
	# TODO handle dup section cadences using db
	
	# TODO get speeds of dup sections
	
	# TODO handle tcs within sections
	
	
	# count of all sections
	# intro relative to verse
	# outro relative to chorus
	# bridge relative to verse or chorus, repeated bridges vary as per a cadence
	# chorus relative to verse, repeated chorii vary as per a cadence
	# pre relative to chorus or verse
	# => pick number of sections to be be different

	
	
	
	
	
	
	ss = {}
	for st, section in bc.section_types ():
		if st in [INTRO, PRE, OUTRO, BRIDGE]: ss[st] = [(-1, 0)]
		if st == CHORUS: ss[st] = [(0, 1)]
		
			
		
	# intro: same or slower vs verse
	# pre  : same or slower vs chorus
	# outro: same or slower vs chorus
			
	tcs = {}
	cts = {}
	
	vthres = randrange (2, 3 + 1)
	cthres = randrange (2, 3 + 1)
	bthres = randrange (2, 3 + 1)
	for st, section in bc.all_section_types ():			
		if ct not in cts: cts[st] = 1
		ct = cts[st]
		
		if st == VERSE:  temp = (    0,)   # reference tempo
		if st == BRIDGE: temp = (-1, 0)    # probably slower
		if st == CHORUS: temp = (    0, 1) # probably faster ?
		
		if st == BRIDGE: cond = ct > 1      and (ct + 1) % bthres == 0
		if st == VERSE:  cond = ct > vthres and ct % vthres == 1  
		if st == CHORUS: cond = ct > cthres and ct % cthres == 1
		if cond:            tcs[st] = tcs[st] + [(-1, 0, 1)] # TODO use different pattern than previous
		elif st not in tcs: tcs[st] = [temp]
		#else:               tcs[st] = tcs[st] + [tcs[st][-1]]
		else:               tcs[st] = tcs[st] + [(0,)]
		
		cts[st] = cts[st] + 1
		
		
		
		
		
		
	# given min and max number of tcs, do hash
	mintc = 1
	maxtc = bc.nuniq_section_type ()
	sts   = {}
	for st, section in bc.all_section_types ():
		if st not in [VERSE, BRIDGE, CHORUS]: continue
		if st in sts: sts[st] = sts[st] + 1
		else:         sts[st] = 1
		if sts[st] > 2 and sts[st] % 2 == 1: maxtc = maxtc + 1
	#ntc = randrange (mintc, maxtc + 1)
	# TODO determine section_nos where tempo can change
	
	
		
#class MicroTemporalCadence (Cadence):
# by phrase:  within a section, speed may vary by phrase
# by segment: within a phrase, speed may vary by segment	
	
#class TemporalProgression (Cadence): pass # not more than one 3 or 5 for 8 hz

#class Polymeter (Cadence): # two tempos
	# tries to use tempos from prev, next sections in primary temporal progression
	# polymeter ratio should be simpler at beginning, and during early chorii
	# meters should synchronize at least at the beginning and end of every section
	# needs to compute a sort of planck constant based on the product of the two tempos
	# does not need to be the same for repetitions of section types
	
# second layer for polymeter?
#   isochronic pulses implemented/implied here ? e.g., 30:16 or 32:15 or 8:60

from brain_waves import Brainwaves
	
class HeartBrain:
	def __init__ (self, scale, bwt, pt):
		self.scale = scale # scaling factor for brainwave precision
		self.bwt   = bwt   # target meditative state (brainwave type)
		self.pt    = pt    # primary tempo
def random_heartbrain ():
	# polymeter => scale
	scale = randrange (1, 100)
	
	bwt   = choice (list (Brainwaves))
	bwmin, bwmax = bwt.value
	bwmin = bwmin * scale * 60
	bwmin = max (bwmin, 1)
	bwmax = bwmax * scale * 60
	
	ptt   = choice (list (Tempo))
	ptmin, ptmax = ptt.value
	ptmin = ptmin * scale
	ptmax = ptmax * scale
	
	bw    = randrange (bwmin, bwmax) # in bpm * scale
	# lcm (x, y) = bw
	# ax : by
	# x = tempo_1
	# y = tempo_2
	
	
class HeartBrainTemporalMatrix: pass


	
# a layer for gradually speeding up (i.e., as during the pre and intro) and slowing down (as during the outro) (or throughout the course of the song) ?
	
# accent patterns	
		
# function cadences (i.e., lens):
#   can only change chords when meters synchronize, => negative correlation between temporal and harmonic complexity
#   pre is effectively prepended to chorus ?
#   intro must start on tonic ?
#   intro is effectively prepended to verse ?
#   outro must end on tonic
#   outro is effectively appended to chorus ?
#   pre should not be tonic ?
# function progression
# modulations: can only modulate after tonic ?
# major/minor, cons/diss => borrow pattern
# borrow pattern
# polytonic structure (modulations, major/minor, cons/diss, borrow pattern)
# monaural acoustic beat
# number of voices => number of notes in chords
# tight/spread
# chord progression
# texture (i.e., which instrument)
# negative space / phrasing => poetic meter
# rhythms
# dynamics
# melodic cadence
# melody
# note effects
# harmony (texture, poetry, rhythm, dynamics, melodic cadence, melody, note effects)

# or texture  goes after note effects ?





# modulations => play tonic notes
# borrowing => play tonic notes
# polytonality => play two notes
## number of notes in chords ~= number of voices => play polychords (just tonic)
## function progression => play polychords (according to function)
# => number of notes and number of voices possible for each part of polychord
## chord qualities: major/minor, consonant/dissonant, tight/spread, number of notes => play specific chords
# binaural beats ?
# chord progression











function_cadence_db = {}
#@jit
def init_function_cadence_db (nc):
	if nc in function_cadence_db: return function_cadence_db[nc]
	if nc == 1:
		progressions            = ((1,),)
		function_cadence_db[nc] = progressions
		return progressions
	if nc == 2:
		progressions            = ((1, 1), (2,),)
		function_cadence_db[nc] = progressions
		return progressions
	arr           = (2, 3, 4)
	progressions = subsets (arr, nc - 1)
	progressions = map (lambda p: (1,) + tuple (p), progressions)
	progressions = tuple (progressions)
	function_cadence_db[nc] = progressions
	return progressions
def random_function_cadence (nc):
	db = init_function_cadence_db (nc)
	return tuple (choice (db))

class HarmonicProgressionType (Enum):
	BY_SONG     = 0
	BY_SECTION  = 1
	BY_PHRASE_1 = 2
	BY_PHRASE_2 = 3
	BY_SEGMENT  = 4
	BY_BAR      = 5
BY_SONG     = HarmonicProgressionType.BY_SONG
BY_SECTION  = HarmonicProgressionType.BY_SECTION
BY_PHRASE_1 = HarmonicProgressionType.BY_PHRASE_1
BY_PHRASE_2 = HarmonicProgressionType.BY_PHRASE_2
BY_SEGMENT  = HarmonicProgressionType.BY_SEGMENT
BY_BAR      = HarmonicProgressionType.BY_BAR

class FunctionCadence (Cadence):
	@staticmethod
	def init_map (bc, hpt, hcs):
		#print ("hcs     : %s" % (hcs,))	
		"""
		if hpt == BY_SONG:
			assert len (hcs) == 1
			order = (0,)
			uniq  = {0: hcs[0]}
			return uniq, order
			"""
		if hpt == BY_SONG or hpt == BY_SECTION or hpt == BY_PHRASE_1:
			order = [] # function cadence length indices
			uniq  = {}
			i     = 0
			for hc in hcs:
				temp    = tuple (range (0, hc))
				#order   = order + [(i, temp)]
				order   = order + [i]
				#for j in temp: uniq[i, j] = hc, j, i + j
				temp = tuple (map (lambda j: i + j, temp))
				uniq[i] = hc, temp 
				i       = i + hc
			#rev   = chain (*order) # section_no to index, offset
			order = tuple (order)
			return uniq, order
	
		assert hpt == BY_PHRASE_2 or hpt == BY_SEGMENT or hpt == BY_BAR
		
		order = []
		uniq  = {}
		i     = 0
		#print ("fuck: %s" % (bc.all_section_types (),))
		for st in bc.all_section_types ():	
			for hc in hcs[st]:
				temp        = tuple (range (0, hc))
				order       = order + [(st, i)]
				temp        = tuple (map (lambda j: i + j, temp))
				uniq[st, i] = hc, temp
				i           = i + hc
		order = tuple (order)
		#print ("order: %s" % (order,))
		return uniq, order
	def __init__ (self, bc, hpt, hcs):
		Cadence.__init__ (self, *FunctionCadence.init_map (bc, hpt, hcs))
		self.bc  = bc
		self.hpt = hpt
		self.hcs = hcs
	def __repr__ (self): return "FunctionCadence [hpt=%s, hcs=%s, bc=%s]" % (self.hpt, self.hcs, self.bc)
	def section_types (self):
		#return tuple (self.uniq[sti] for sti in set (self.order))
		hpt = self.hpt
		if hpt == BY_SONG or hpt == BY_SECTION or hpt == BY_PHRASE_1: return self.hcs
		assert hpt == BY_PHRASE_2 or hpt == BY_SEGMENT or hpt == BY_BAR	
		#return tuple (self.hcs[st] for st in self.bc.all_section_types ())
		return tuple ((st, hcs) for st, hcs in self.hcs.items ())
	def nfunction_cadence (self): # uniq lens => count
		uniq = {}
		hpt  = self.hpt
		if hpt == BY_SONG or hpt == BY_SECTION or hpt == BY_PHRASE_1:
			for hc in self.hcs:
				if hc in uniq: uniq[hc] = uniq[hc] + 1
				else:          uniq[hc] = 1
		if hpt == BY_PHRASE_2 or hpt == BY_SEGMENT or hpt == BY_BAR:
			for st, hcs in self.hcs.items ():
				for hc in hcs:
					if hc in uniq: uniq[hc] = uniq[hc] + 1
					else:          uniq[hc] = 1
		return uniq
	def nfunction_cadences (self):
		hpt = self.hpt
		if hpt == BY_SONG or hpt == BY_SECTION or hpt == BY_PHRASE_1: return len (self.hcs)
		uniq = {}
		for st, section in self.bc.section_types ():	
			uniq[st] = len (self.hcs[st])
		return uniq
		
def random_function_cadences (bc=None, bc_args=None, hpt=None):
	if bc  is None: bc  = random_bar_cadence (*bc_args)
	if hpt is None: hpt = choice (list (HarmonicProgressionType))

	if hpt == BY_SONG:     nit = 1
	if hpt == BY_SECTION:  nit = bc.nsection ()
	if hpt == BY_PHRASE_1: nit = bc.nphrase  ()

	if hpt == BY_SONG     or hpt == BY_SECTION or hpt == BY_PHRASE_1: hcs = random_function_cadence (nit)
	if hpt == BY_PHRASE_2 or hpt == BY_SEGMENT or hpt == BY_BAR:
		hcs = {}
		for st, section in bc.section_types ():
			assert st not in hcs
			if hpt == BY_PHRASE_2: nit = len (section)
			if hpt == BY_SEGMENT:  nit = len (tuple (chain (*section)))
			if hpt == BY_BAR:      nit = len (tuple (chain (*chain (*section))))
			hcs[st] = random_function_cadence (nit)

	return FunctionCadence (bc, hpt, hcs)
	
	
	
	
	




from chromatic import ChordFunction

TONIC       = ChordFunction.TONIC
DOMINANT    = ChordFunction.DOMINANT
SUBDOMINANT = ChordFunction.SUBDOMINANT

function_progression_db = (
	((),),                                    # 0: nsegment = 1
	
	((   DOMINANT,),                           # 1: nsegment = 2
	 (SUBDOMINANT,),),
	 
	((SUBDOMINANT,    DOMINANT),              # 2: nsegment = 3
	 (   DOMINANT, SUBDOMINANT),
	 (SUBDOMINANT, SUBDOMINANT),
	 (   DOMINANT,    DOMINANT),),
	 
	((SUBDOMINANT, SUBDOMINANT,    DOMINANT), # 3: nsegment = 4
	 (SUBDOMINANT,    DOMINANT, SUBDOMINANT),
	 (   DOMINANT, SUBDOMINANT, SUBDOMINANT),
	 
	 (SUBDOMINANT,    DOMINANT,    DOMINANT),
	 (   DOMINANT, SUBDOMINANT,    DOMINANT),),
)
def random_function_progression (nsegment):	
	segment     = function_progression_db[nsegment - 1]
	#print ("s0: %s" % (segment,))
	segment     = choice (segment)
	#print ("s1: %s" % (segment,))
	segment     = tuple (list (segment) + [TONIC])
	#print ("s2: %s" % (segment,))
	return segment
#@jit
class FunctionProgression (Cadence):
	@staticmethod
	def init_map (fc, fps):
		uniq  = {}
		order = []
		
		ndxs = {}
		#if fc.hpt == BY_SONG or fc.hpt == BY_SECTION or fc.hpt == BY_PHRASE_1: k = fc
		#else:                                                                  k = fc.section_types ()
		if fc.hpt == BY_SONG or fc.hpt == BY_SECTION or fc.hpt == BY_PHRASE_1:
			for c in fc.section_types ():
				#print ("c: %s" % (c,))
				if c in ndxs: i = ndxs[c]
				else:         i = 0
				u, o       = fps[c]
				
				#print ("nos: %s" % (nos,))
				#print ("i: %s" % (i,))
				#print ("o: %s" % (o,))
				#print ("u: %s" % (u,))
				#assert len (nos) == len (o), "%s != %s, %s != %s" % (len (nos), len (o), nos, o)
				temp       = (c, o[i])
				order      = order + [temp]
				uniq[temp] = u[o[i]]
				ndxs[c]    = i + 1
		if fc.hpt == BY_PHRASE_2 or fc.hpt == BY_SEGMENT or fc.hpt == BY_BAR:
			for st, cs in fc.section_types ():
				#print ("cs: %s" % (cs,))
				for c in cs:
					#print ("c: %s" % (c,))
					if c in ndxs: i = ndxs[c]
					else:         i = 0
					u, o       = fps[c]
					
					#print ("nos: %s" % (nos,))
					#print ("i: %s" % (i,))
					#print ("o: %s" % (o,))
					#print ("u: %s" % (u,))
					#assert len (nos) == len (o), "%s != %s, %s != %s" % (len (nos), len (o), nos, o)
					temp       = (c, o[i])
					order      = order + [temp]
					uniq[temp] = u[o[i]]
					ndxs[c]    = i + 1
		order = tuple (order)
		return uniq, order
	def __init__ (self, fc, fps):
		Cadence.__init__ (self, *FunctionProgression.init_map (fc, fps))
		self.fc  = fc
		self.fps = fps
	def __repr__ (self): return "FunctionProgression [fc=%s, fps=%s]" % (self.fc, self.fps)
	def nfunction_progression (self):
		uniq = {}
		for l, uo in self.fps.items ():
			u, o = uo
			ct = len (set (o))
			uniq[l] = ct
		return uniq
	def nprogression (self): return len (self.fc)
	def nprogressions (self): return self.fc.nfunction_cadences ()
	def nsection (self): return self.bc.nsection ()
def random_function_progressions (fc=None, fc_args=None):
	if fc is None: fc = random_function_cadences (*fc_args)
	
	# TODO hashing between sections ?
	
	lens = fc.nfunction_cadence ()
	fps  = {}
	for l, ct in lens.items ():
		minn   = 1
		max_n  = len (function_progression_db[l - 1])
		#print ("l: %s" % (l,))
		#print ("ct: %s" % (ct,))
		#print ("max_n: %s" % (max_n,))
		maxn   = min (ct, max_n)
		order  = reduce_map (ct, minn, maxn)
		n      = len (set (order))
		uniq   = tuple (random_function_progression (l) for _ in range (0, n))
		#print ("uniq : %s" % (uniq,))
		#print ("order: %s" % (order,))
		fps[l] = uniq, order
	
	return FunctionProgression (fc, fps)

	

















class ModulationCadenceType (Enum):
	INTRASECTION = 0 # hpt in [BY_SONG,     BY_SECTION, BY_PHRASE_1]
	INTERSECTION = 1 # hpt in [BY_PHRASE_2, BY_SEGMENT, BY_BAR]
	
class ModulationCadence (Cadence): # whether to modulate
	# nmodulation points: nsection() + nfps()
	@staticmethod
	def initmap (fp, mct, c1, c2, c3, intramods):
		hpt = fp.hpt
		if hpt == BY_SONG or hpt == BY_SECTION or hpt == BY_PHRASE_1:
			assert intramods is None
			assert mct == INTERSECTION
			uniq  = {}
			order = []
			
			
			
			order = tuple (order)
			return uniq, order
		if hpt == BY_PHRASE_2 or hpt == BY_SEGMENT or hpt == BY_BAR:
			if mct == INTERSECTION: pass
			if mct == INTRASECTION: pass
			uniq  = {}
			order = []
			
			order = tuple (order)
			return uniq, order
	def __init__ (self, fp, mct, c1, c2, c3, intramods=None):
		Cadence.__init__ (self, *ModulationCadence.initmap (fp, mct, c1, c2, c3, intramods))
		self.fp  = fp
		self.mct = mct
def random_modulation_cadence (fp=None, fp_args=None, mct=None):
	if fp is None:
		if mct is None: mct = choice (list (ModulationCadenceType))
		if mct == INTRASECTION: hpt = choice (BY_PHRASE_2, BY_SEGMENT, BY_BAR)
		else:                   hpt = None
		fp = random_function_progressions (None, (None, None, hpt))
	hpt = fp.hpt
	if mct is None:
		if hpt == BY_SONG or hpt == BY_SECTION or hpt == BY_PHRASE_1: mct = INTERSECTION
		else:                                                         mct = choice (list (ModulationCadenceType))
	
	if hpt == BY_SONG     or hpt == BY_SECTION or hpt == BY_PHRASE_1:
		assert mct == INTERSECTION
		maxn = fp.nfunction_progression ()
		n1   = randrange (0, max_n + 1)
		n2   = randrange (0, max_n + 1)
		n3   = randrange (0, max_n + 1)
		c1   = random_bjorklund3 (maxn, n1) # whether to modulate
		c2   = random_bjorklund3 (maxn, n2) # whether to do tetra-equiv
		c3   = random_bjorklund3 (maxn, n3) # which layer to apply first
		return ModulationCadence (fp, mct, c1, c2, c3)
	assert hpt == BY_PHRASE_2 or hpt == BY_SEGMENT or hpt == BY_BAR
	if mct == INTRASECTION:
		# TODO hash bjorklund results
		ns = fp.nsection ()
		n1 = randrange (0, ns + 1)
		n2 = randrange (0, ns + 1)
		n3 = randrange (0, ns + 1)
		c1 = random_bjorklund3 (ns, n1)
		c2 = random_bjorklund3 (ns, n2)
		c3 = random_bjorklund3 (ns, n3)
		
		intramods = {}
		nfps = fp.nprogressions ()
		for st, nfp in nfps:
			n1 = randrange (0, nfp + 1)
			n2 = randrange (0, nfp + 2)
			n3 = randrange (0, nfp + 3)
			c4 = random_bjorklund3 (nfp, n1)
			c5 = random_bjorklund3 (nfp, n2)
			c6 = random_bjorklund3 (nfp, n3)
			intramods[st] = (c4, c5, c6)
			
		return ModulationCadence (fp, mct, c1, c2, c3, intramods)
	n  = len (fp)
	n1 = randrange (0, n + 1)
	n2 = randrange (0, n + 1)
	n3 = randrange (0, n + 1)
	c1 = random_bjorklund3 (n, n1)
	c2 = random_bjorklund3 (n, n2)
	c3 = random_bjorklund3 (n, n3)
	return ModulationCadence (fp, mct, c1, c2, c3)
	
# for polytonality, two mcs: primary and secondary, starting modes either same or related
	
class ModulationHue (Cadence): # modulation type (brighter, darker, inv, recycle previous mode)
	# TODO for sections, decide whether to modulate to new key or reuse old key
	# TODO within sections, ""
	pass

class ModulationProgression (Cadence): # modulation level (key, tetra, mode)
	# inv, equiv must be tetra
	pass
	
# key
# - brighter, darker
# tetra:
# - brighter, darker
# - inv: reverse
# - equiv: different tetra/mode
# mode:
# - brighter, darker

#class TemporalCadence (Cadence): # when and where to change tempo
#class TemporalProgression (Cadence): # actual changes in tempo, based on key ?

#class BorrowCadence (Cadence): # whether to borrow, and whether to borrow from a new key or one of the mod keys
#	pass
#class BorrowHue (Cadence): # borrow type (no equiv, but include all equiv+mod_type variants)
#	pass
#class BorrowProgression (Cadence): # borrow level
#	pass

# TODO polytonality: a progression of modes on top or below the main modal progression

# major/minor, consonant/dissonant, tight/spread
#         consonant   dissonant
# major   c maj       c aug
# minor   c min       c dim

#class ChordProgression (Cadence):
	# TODO voice leading must be done at this level?
	# TODO how to reuse/hash chords ?
	# TODO inversions ?
	# TODO #chord tones... i.e., triads, sevenths, extended chords, polytonality ?




"""
class Meter ():
	def __init__ (self, bc, tm):
		self.bc = bc # bar cadence
		self.tm = tm # temporal modulations
"""















	
	
if __name__ == "__main__":
	def main ():
		for nsection in range (0, 3 + 1):
			sc = random_sc0 (nsection)
			print (sc)
		print ("\n\n")
		
		av = random_av ()
		
		ss = random_song_structure ()
		print ("song structure: %s\n" % ss)
		print ("all           : %s\n" % list (ss))
		print ("uniq          : %s\n" % list (ss.uniq_elements ()))
		print ("nsection      : %s" % ss.nsection ())
		print ("nuniq section : %s" % ss.nuniq_section ())
		print ("nshort section: %s" % ss.nuniq_short_section   ())
		print ("nlong  section: %s" % ss.nuniq_long_section   ())
		print ("suniq         : %s" % list (ss.uniq_short_sections ()))
		print ("luniq         : %s" % list (ss.uniq_long_sections ()))	
		# TODO first, last sections, etc
		print ("\n\n")
		
		sc = random_song_cadence (ss)
		print ("song cadence  : %s\n" % sc)
		ssc = sc.sc
		lsc = sc.lc
		print ("ssc           : %s" % ssc)
		print ("nsection      : %s" % ssc.nsection ())
		print ("nuniq         : %s" % ssc.nuniq ())
		#print ("ssc           : %s" % list (ssc))
		print ()
		print ("lsc           : %s" % lsc)
		print ("nsection      : %s" % lsc.nsection ())
		print ("uniq          : %s" % lsc.nuniq ())
		#print ("lsc           : %s" % list (lsc))
		print ()
		print ("sections      : %s\n" % list (sc))
		print (list (zip (sc.order, list (sc))))
		print ()
		print ("first section : %s" % (sc.first_section (),))
		print ("last  section : %s" % (sc. last_section (),))
		print ("pre   sections: %s" % list (sc.  pre_sections ()))
		print ("chorii        : %s" % list (sc.  chorii       ()))
		print ()
		print ("uniq s section: %s" % sc.uniq_short_sections ())
		print ("uniq l section: %s" % sc.uniq_long_sections ())
		print ("uniq          : %s" % list (sc.section_types ()))
		print ()
		print ("nsection      : %s" % sc.nsection ())
		#print ("nsection t    : %s" % sc.nsection_types ())
		print ("n s section   : %s" % sc.nshort_section ())
		print ("n l section   : %s" % sc.nlong_section ())
		print ("n s st        : %s" % sc.nshort_section_types ())
		print ("n l st        : %s" % sc.nlong_section_types ())
		print ("uniq          : %s" % sc.nuniq ())
		print ("uniq st       : %s" % (sc.uniq_section_types (),))
		print ("nuniq s section: %s" % sc.nuniq_short_section ())
		print ("nuniq l section: %s" % sc.nuniq_long_section ())
		print ("\n\n")
		assert (tuple (sc)) ==  (tuple (sc.all_sections ()))
		
		sc = random_section_cadences (sc)
		print ("section cadence: %s\n" % sc)
		print ("all sections  : %s\n" % list (sc.all_sections ()))
		print ("all phrases   : %s\n" % list (sc.all_phrases ()))
		print ("uniq          : %s" % list (sc.section_types ()))
		
		print ("first section : %s" % (sc.first_section (),))
		print ("last  section : %s" % (sc. last_section (),))
		print ("pre   sections: %s" % list (sc.  pre_sections ()))
		print ("chorii        : %s" % list (sc.  chorii       ()))
		print ()
		print ("first phrase  : %s" % (sc.first_phrase (),))
		print ("last  phrase  : %s" % (sc. last_phrase (),))
		print ("pre   phrases : %s" % list (sc.  pre_phrases (),))
		print ()
		print ("nsection      : %s" % sc.nsection     ())
		print ("nshort section: %s" % sc.nshort_section ())
		print ("nlong_section : %s" % sc.nlong_section ())
		print ("uniq          : %s" % sc.nuniq  ())
		print ("nuniq   section: %s" % sc.nuniq_section ())
		print ("nuniq s section: %s" % sc.nuniq_short_section ())
		print ("nuniq l section: %s" % sc.nuniq_long_section ())
		print ("nphrase       : %s" % sc.nphrase     ())
		print ("uniq phrase   : %s" % sc.nuniq_phrase ())
		print ()
		
		for k in range (0, sc.nsection ()): print (sc.section_elems (k))
		print ()
		for k in range (0, sc.nphrase  ()): print (sc.phrase_elem   (k))
		print ("\n\n")
		
		pc = random_phrase_cadences (sc)
		print ("phrase cadence: %s" % pc)
		print ("all sections  : %s" % (list (pc.all_sections ())))
		print ("all phrases   : %s" % (list (pc.all_phrases  ())))
		print ("all segments  : %s" % (list (pc.all_segments ())))
		print ("uniq          : %s" % list (pc.section_types ()))
		
		k = tuple (pc.all_sections ())
		assert len (k) == pc.nsection ()
		k = set (k)
		assert len (k) == pc.nuniq_section ()
		k = tuple (pc.all_phrases ())
		assert len (k) == pc.nphrase ()
		k = set (k)
		assert len (k) == pc.nuniq_phrase ()
		k = tuple (pc.all_segments ())
		assert len (k) == pc.nsegment ()
		k = set (k)
		assert len (k) == pc.nuniq_segment ()

		print ("nsection      : %s" % pc.nsection ())
		print ("uniq          : %s" % pc.nuniq_section    ())
		print ("nphrase       : %s" % pc.nphrase  ())
		print ("uniq phrase   : %s" % pc.nuniq_phrase   ())
		print ("nsegment      : %s" % pc.nsegment ())
		print ("uniq segment  : %s" % pc.nuniq   ())
		
		print ("first section : %s" % (pc.first_section (),))
		print ("first phrase  : %s" % (pc.first_phrase  (),))
		print ("first segment : %s" % (pc.first_segment (),))
		print ("last  section : %s" % (pc. last_section (),))
		print ("last  phrase  : %s" % (pc. last_phrase  (),))
		print ("last  segment : %s" % (pc. last_segment (),))
		print ("chorii        : %s" % list (pc.  chorii       ()))
		print ("pre  sections : %s" % list (pc.  pre_sections (),))
		print ("pre   phrases : %s" % list (pc.  pre_phrases (),))
		print ("pre  segments : %s" % list (pc.  pre_segments (),))
		print ()
		for k in range (0, pc.nsection ()): print (pc.section_elem (k))
		print (tuple (pc.phrase_elems (k) for k in range (0, pc.nphrase  ())))
		print (tuple (pc.segment_elem (k) for k in range (0, pc.nsegment ())))
		print ("\n\n")
		
		sc = random_segment_cadences (pc)
		print ("segment cadence : %s\n" % (sc,))
		print ("all sections  : %s" % (list (sc.all_sections ())))
		print ("all phrases   : %s" % (list (sc.all_phrases  ())))
		print ("all segments  : %s" % (list (sc.all_segments ())))
		print ("all bars      : %s" % (list (sc.all_bars ())))
		print ("uniq          : %s" % list (sc.section_types ()))
		
		k = tuple (sc.all_sections ())
		assert len (k) == sc.nsection ()
		k = set (k)
		assert len (k) == sc.nuniq_section ()
		k = tuple (sc.all_phrases ())
		assert len (k) == sc.nphrase ()
		k = set (k)
		assert len (k) == sc.nuniq_phrase ()
		k = tuple (sc.all_segments ())
		assert len (k) == sc.nsegment ()
		k = set (k)
		assert len (k) == sc.nuniq_segment ()
		k = tuple (sc.all_bars ())
		assert len (k) == sc.nbar ()
		k = set (k)
		assert len (k) == sc.nuniq_bar ()
		
		print ("nsection      : %s" % sc.nsection ())
		print ("uniq          : %s" % sc.nuniq_section    ())
		print ("nphrase       : %s" % sc.nphrase  ())
		print ("uniq phrase   : %s" % sc.nuniq_phrase   ())
		print ("nsegment      : %s" % sc.nsegment ())
		print ("uniq segment  : %s" % sc.nuniq   ())
		print ("nbar          : %s" % sc.nbar ())
		print ("uniq bar      : %s" % sc.nuniq_bar ())
		
		print ("first section : %s" % (sc.first_section (),))
		print ("first phrase  : %s" % (sc.first_phrase  (),))
		print ("first segment : %s" % (sc.first_segment (),))
		print ("first bar     : %s" % (sc.first_bar (),))
		print ("last  section : %s" % (sc. last_section (),))
		print ("last  phrase  : %s" % (sc. last_phrase  (),))
		print ("last  segment : %s" % (sc. last_segment (),))
		print ("last  bar     : %s" % (sc.last_bar (),))
		print ("chorii        : %s" % list (sc.  chorii       ()))
		print ("pre  sections : %s" % list (sc.  pre_sections (),))
		print ("pre   phrases : %s" % list (sc.  pre_phrases (),))
		print ("pre  segments : %s" % list (sc.  pre_segments (),))
		print ("pre      bars : %s" % list (sc.pre_bars (),))
		print ()
		for k in range (0, sc.nsection ()): print (sc.section_elem (k))
		print (tuple (sc.phrase_elem (k) for k in range (0, sc.nphrase  ())))
		print (tuple (sc.segment_elems (k) for k in range (0, sc.nsegment ())))
		print (tuple (sc.bar_elem (k) for k in range (0, sc.nbar ())))
		print ("\n\n")
		
		bc = random_bar_cadence (sc)
		print ("bar cadence : %s\n" % (bc,))
		print ("all sections  : %s" % (list (bc.all_sections ())))
		print ("all phrases   : %s" % (list (bc.all_phrases  ())))
		print ("all segments  : %s" % (list (bc.all_segments ())))
		print ("all bars      : %s" % (list (bc.all_bars ())))
		print ("uniq          : %s" % list (bc.section_types ()))
		
		#k = tuple (bc.all_sections ())
		#assert len (k) == bc.nsection ()
		#k = set (k)
		#assert len (k) == bc.nuniq_section ()
		#k = tuple (bc.all_phrases ())
		#assert len (k) == bc.nphrase ()
		#k = set (k)
		#assert len (k) == bc.nuniq_phrase ()
		#k = tuple (bc.all_segments ())
		#assert len (k) == bc.nsegment ()
		#k = set (k)
		#assert len (k) == bc.nuniq_segment ()
		#k = tuple (bc.all_bars ())
		#assert len (k) == bc.nbar ()
		# TODO
		#k = set (k)
		#assert len (k) == bc.nuniq_bar ()
		
		print ("nsection      : %s" % bc.nsection ())
		print ("uniq          : %s" % bc.nuniq_section    ())
		print ("nphrase       : %s" % bc.nphrase  ())
		print ("uniq phrase   : %s" % bc.nuniq_phrase   ())
		print ("nsegment      : %s" % bc.nsegment ())
		print ("uniq segment  : %s" % bc.nuniq   ())
		print ("nbar          : %s" % bc.nbar ())
		print ("uniq bar      : %s" % bc.nuniq_bar ())
		
		print ("first section : %s" % (bc.first_section (),))
		print ("first phrase  : %s" % (bc.first_phrase  (),))
		print ("first segment : %s" % (bc.first_segment (),))
		print ("first bar     : %s" % (bc.first_bar (),))
		print ("last  section : %s" % (bc. last_section (),))
		print ("last  phrase  : %s" % (bc. last_phrase  (),))
		print ("last  segment : %s" % (bc. last_segment (),))
		print ("last  bar     : %s" % (bc.last_bar (),))
		print ("chorii        : %s" % list (bc.  chorii       ()))
		print ("pre  sections : %s" % list (bc.  pre_sections (),))
		print ("pre   phrases : %s" % list (bc.  pre_phrases (),))
		print ("pre  segments : %s" % list (bc.  pre_segments (),))
		print ("pre      bars : %s" % list (bc.pre_bars (),))
		print ()
		for k in range (0, bc.nsection ()): print (bc.section_elem (k))
		print (tuple (bc.phrase_elem (k) for k in range (0, bc.nphrase  ())))
		print (tuple (bc.segment_elems (k) for k in range (0, bc.nsegment ())))
		print (tuple (bc.bar_elem (k) for k in range (0, bc.nbar ())))
		print ("nbeat: %s" % (bc.nbeat (),))
		#bc.play (av)
		print ("\n\n")
		
		BC = bc
		for hpt in HarmonicProgressionType:
			#tc = random_temporal_cadence (bc)
			#tp = random_temporal_progression (tc)
			fc = random_function_cadences (BC, None, hpt) # tp
			print (" fc: %s" % (fc,))
			print (" fc: %s" % list (fc))
			print ("nfc: %s" % (fc.nfunction_cadence (),))
			print ("nfcs: %s" % (fc.nfunction_cadences (),))
			if hpt == BY_PHRASE_2 or hpt == BY_SEGMENT or hpt == BY_BAR:
				for st in fc.section_types ():
					print ("st: %s" % (st,))
			print ()
			print ("hpt: %s" % (hpt,))
			print ()
			fp = random_function_progressions (fc)
			print (" fp: %s" % (fp,))
			print (" fp: %s" % list (fp))
			print ("nfp: %s" % (fp.nfunction_progression (),))
			print (" np: %s" % (fp.nprogression (),))
			print ("nps: %s" % (fp.nprogressions (),))
			print ()
			
			#mc = random_modulation_cadence (fp)     # fc-level
			#mp = random_modulation_progression (mc)
			#bc = random_borrow_cadence (mp)         # fc-level
			#bp = random_borrow_progression (bc)
			#cc = random_chord_cadence (bp)
			#cp = random_chord_progression (cc)
			# accent pattern
			# poetic meter
			# rhythm
			# CT-NCT, CT-NCT-NCT cadence
			# melody
			# note effects, such as slides, tremelo, etc
			# contrapuntal harmony
			# textures (i.e., which instruments to use)
			
			# timbre, dynamics, texture
			
			print ("\n\n")
	main ()
	
