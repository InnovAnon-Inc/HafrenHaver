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

from pattern import Pattern

	
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
# which section types, which order
class SongStructure (Pattern):
	def __init__ (self, ss): Pattern.__init__ (self, ss)
	def __repr__ (self): return "SongStructure [%s]" % Pattern.__repr__ (self)
	
	def section_type        (self, i): return self[i]
	def nsection            (self): return len (self)
	def nuniq_section       (self): return self.nuniq ()
	def uniq_sections       (self): return self.uniq_elements ()
	def nshort_section      (self): return len (tuple (filter (short_section, self)))
	def  nlong_section      (self): return len (tuple (filter (long_section,  self)))
	
	def nuniq_short_section (self): return len (self.uniq_short_sections ())
	def nuniq_long_section  (self): return len (self.uniq_long_sections ())
	def uniq_short_sections (self): return tuple (filter (short_section, self.uniq_elements ()))
	def uniq_long_sections  (self): return tuple (filter (long_section,  self.uniq_elements ()))
	
	#def nuniq (self): return len (self. uniq ())
	#def nsc (self): return len (set (filter (short_section, Pattern.all (self))))
	#def nlc (self): return len (set (filter ( long_section, Pattern.all (self))))
	
	#@jit
	#def elem (self, i):
	#	v = Pattern.elem (self, i)
	#	return v.value ()
	#@jit
	#def all (self): return (v.value () for v in Pattern.all (self))
def random_song_structure ():
	ss = choice (song_structure_db)
	return SongStructure (ss)
