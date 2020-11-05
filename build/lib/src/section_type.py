#! /usr/bin/env python3

from enum      import Enum
#from numba     import jit

class SectionType (Enum):
	VERSE  = 0
	CHORUS = 1
	BRIDGE = 2
	INTRO  = 3
	OUTRO  = 4
	PRE    = 5
VERSE  = SectionType.VERSE
CHORUS = SectionType.CHORUS
BRIDGE = SectionType.BRIDGE
INTRO  = SectionType.INTRO
OUTRO  = SectionType.OUTRO
PRE    = SectionType.PRE

#@jit
def  long_section (st): return st.value in (0, 1, 2)
#@jit
def short_section (st): return st.value in (3, 4, 5)
	
