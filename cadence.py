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
#from song_structure import SongStructure

class Cadence (Pattern):
	def __init__ (self, uniq, order):
		Pattern.__init__ (self, order)
		self.uniq = uniq
	def __repr__ (self): return "Cadence [%s, uniq=%s]" % (Pattern.__repr__ (self), self.uniq)
	#@jit
	def __getitem__ (self, i):
		#v = self.pattern (i)
		#return self.uniq[v]
		return self.uniq[i]
	def pattern (self, i): return Pattern.__getitem__ (self, i)
	#@jit
	#def all (self): return (self.u (v) for v in Pattern.all (self))
	#def all (self): return (self.uniq[v] for v in Pattern.all (self))
	#@jit
	#def v (self, v): return v
	#@jit
	#def u (self, v):
	#	v = self.v (v)
	#	return self.uniq[v]
	# TODO indices for which elem() is k	
	#def nuniq ()
	
	
	def nuniq (self):
		assert len (self.uniq) == Pattern.nuniq (self)
		return len (self.uniq)
	def uniq_elements (self):
		#assert Pattern.uniq_elements (self) == tuple (self.uniq), "%s, %s, %s" % (Pattern.uniq_elements (self), self.uniq, self)
		return self.uniq

	def __iter__     (self):       return (self[i] for i in Pattern.__iter__ (self))
	def __reversed__ (self):       return (self[i] for i in Pattern.__reversed__ (self))
	def __contains__ (self, item): return item in self.uniq
