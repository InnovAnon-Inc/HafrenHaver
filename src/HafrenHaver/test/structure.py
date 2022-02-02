#! /usr/bin/env python3

from enum      import Enum, unique
from itertools import starmap
from operator  import le
from random    import choice, random, randrange

@unique
class Section(Enum):
    INTRO  = 1
    VERSE  = 2
    PRE    = 3
    CHORUS = 4
    BRIDGE = 5
    OUTRO  = 6
	#           nbar, nvoice
	#INTRO  = ((1, 4), (1, 2))
	#VERSE  = ((4, 8), (3, 5))
	#PRE    = ((1, 2), (1, 5))
	#CHORUS = ((4, 8), (3, 5))
	#BRIDGE = ((4, 8), (3, 5))
	#OUTRO  = ((1, 4), (1, 5))
class SongStructure(Enum):
	JAZZ   = (Section.VERSE,                                             Section.VERSE,              Section.BRIDGE, Section.VERSE)
	FOLK1  = (Section.VERSE,                             Section.CHORUS, Section.VERSE,              Section.CHORUS, Section.VERSE,              Section.CHORUS)
	FOLK1p = (Section.VERSE,                Section.PRE, Section.CHORUS, Section.VERSE, Section.PRE, Section.CHORUS, Section.VERSE, Section.PRE, Section.CHORUS)
	FOLK2  = (Section.VERSE,                             Section.CHORUS, Section.VERSE,              Section.CHORUS, Section.VERSE,              Section.CHORUS, Section.CHORUS)
	FOLK2p = (Section.VERSE,                Section.PRE, Section.CHORUS, Section.VERSE, Section.PRE, Section.CHORUS, Section.VERSE, Section.PRE, Section.CHORUS, Section.CHORUS)
	POP    = (Section.VERSE, Section.VERSE,              Section.CHORUS, Section.VERSE,              Section.CHORUS, Section.BRIDGE,             Section.CHORUS)
	POPp   = (Section.VERSE, Section.VERSE, Section.PRE, Section.CHORUS, Section.VERSE, Section.PRE, Section.CHORUS, Section.BRIDGE,             Section.CHORUS)
songtypes = (
		(SongStructure.JAZZ,),
		(SongStructure.FOLK1, SongStructure.FOLK1p, SongStructure.FOLK2, SongStructure.FOLK2p,),
		(SongStructure.POP,   SongStructure.POPp),
)
def random_songtype(): return choice(songtypes)
intro_epsilon = 0.5
outro_epsilon = 0.5
def random_songstructure(songtype=None):
	if songtype is None: songtype = random_songtype()
	songstruct = choice(songtype)
	print("songstruct: %s" % (songstruct,))
	songstruct = songstruct.value
	print("songstruct: %s" % (songstruct,))
	if random() < intro_epsilon: songstruct = (Section.INTRO, *songstruct)
	if random() < outro_epsilon: songstruct = (*songstruct,   Section.OUTRO)
	print("songstruct: %s" % (songstruct,))
	return songstruct

class VerseStructure(Enum):
	TYPE1 = ((1, 2),
		 	 (1, 2))
	TYPE2 = ((1, 2),
		 	 (1, 3))
	TYPE3 = ((1, 2),
		 	 (3, 2))

#def random_versestructures(songstruct)
#    versestructs = {}
#    for section in songstruct:
#        if section in versestructs: continue
#        versestructs[section] = 

# TODO count uniq song sections, decide # different verse structures

