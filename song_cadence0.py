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
# which sections have the same meter
class SongCadence0 (Pattern):
	def __init__ (self, sc): Pattern.__init__ (self, sc)
	def __repr__ (self): return "SC0 [%s]" % Pattern.__repr__ (self)
	#def sections (self): return self.uniq.items () # TODO test
	#def section_type (self, i): return Cadence.pattern (self, i)
	#def section_type (self, i): return self.pattern (i)
	# TODO or max ?
	#def ns (self): return len (self.uniq)
	#def nuniq (self): return len (set (self.uniq))
	def nsection (self): return len (self)
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
	if nsection == 0: return SongCadence0 (())
	temp  = sc0_db[nsection - 1]
	#temp  = sc0_db[nsection]
	assert temp is not None
	sc    = choice (temp)
	assert sc is not None
	assert type (sc) is tuple, nsection
	#min_n = max (sc) + 1
	#min_n = len (set (sc))
	#max_n = min_n
	m = len (set (sc))
	#assert max_n <= nsection, "max n: %s, n section: %s" % (max_n, nsection)
	assert m <= nsection
	#n     = randrange (min_n, max_n + 1)
	## TODO map from cardinalities nsection to n
	#temp0 = range (0, nsection)
	#temp1 = (randrange (0, nsection) for _ in range (0, nsection - n)) # TODO maybe just increment-modulo by a relatively prime amount
	#temp  = list (chain (temp0, temp1)) 
	#shuffle (temp)
	#temp = reduce_map (nsection, min_n, max_n)
	#temp = reduce_map (nsection, m, m)
	return SongCadence0 (sc)
