from __future__ import division
from collections import *
from fractions import *
from functools import *
from itertools import *
from math import *
from operator import mul
from random import *
from time import sleep
"""
from graphics import *
from play_chord import *
"""
from BaseFreqIter import *
from BeatChordIter import *
from Bjorklund import *
from ChangeIter import *
#from FIter import *
from ChordIter import *
from CountIter import *
from GuiUtil import *
from Harmonic import *
from KeyIter import *
from MusicMath import *
from ProdIter import *
from ProgIter import *
from SkipIter import *
from Solfeggio import *
from Trivia import *
from Util import *
from ZipIter import *
#from Util import lcm_pair

pythagorean_scale = Harmonic.pythagorean_scale
ranges = Solfeggio.ranges
chakras = Solfeggio.chakras
solfeggio = Solfeggio.solfeggio
lcm_pair = Util.lcm_pair
lcm = Util.lcm
fundyChord = Util.fundyChord
rhythmChordToBeatChord = Util.rhythmChordToBeatChord

###print "init rangeIter"
#rangeIter = list (SkipIter2 (Bjorklund3 (10, 9, 0).seq, ranges))
rangeIter = list (SkipIter (Bjorklund.factory (10, 9, 0), ranges))
#for k in rangeIter: print k
#print len (rangeIter)
###print rangeIter
###print "rangeIter=",rangeIter
#sleep (1)

###print "init chakraIter"
#chakraIter = list (SkipIter2 (Bjorklund3 (15, 13, 0).seq, chakras))
chakraIter = list (SkipIter (Bjorklund.factory (15, 13, 0), chakras))
#for k in chakraIter: print k
#print len (chakraIter)
###print "chakraIter=",chakraIter
###print chakraIter
#sleep (1)

#print len (ProdIter (rangeIter, chakraIter))
#sleep (1)

#print solfeggio

#for r, c in ProdIter (rangeIter, chakraIter):
#	print r, c
#	print solfeggio[r, c]
#	sleep (1)

#print list ([solfeggio[r, c] for r, c in ProdIter (rangeIter, chakraIter)])

###print "init baseFreqIter"
baseFreqIter = list ([solfeggio[r, c] for r, c in ProdIter (rangeIter, chakraIter)])
#baseFreqIter = list (ZipIter (rangeIter, chakraIter, solfeggio))
#for k in baseFreqIter: print k
###print "baseFreqIter=",baseFreqIter





###print "SEI"

###print "init scale"
scaleType = 7
scaleMode = 0
scale = list (pythagorean_scale)
scale.remove (2)
###print "scale=",scale
###print "init key"
#for k in KeyIter (scale, scaleType, scaleMode): print k
key = list (KeyIter (scale, scaleType, scaleMode))
###print "key=",key
###print "init progIter"
progIter = list (ProgIter (xrange (len (key)), 29, 2, 0))
###print "progIter=",progIter

###print "init noteNums"
noteNums = list ([n for n in xrange (1, len (key))])
###print "noteNums=",noteNums
###print "init noteNumKey"
noteNumKey = list (KeyIter (noteNums, 5 % len (noteNums), 0))
###print "noteNumKey=",noteNumKey
###print "init noteNumProgIter"
noteNumProgIter = list (ProgIter (xrange (len (noteNumKey)), 41, 7, 0))
###print "noteNumProgIter=",noteNumProgIter

#chordIters = list ([list (KeyIter (xrange (len (key)), noteNum, 0)) for noteNum in noteNums])
#noteNumIter = list (SkipIter (Bjorklund3 (16, 5, 0), chordIters))

###print "init chords"
chords = [None] * (max (noteNumKey) + 1)
for noteNum in noteNumKey:
	###print "\tinit chords[noteNum=",noteNum,"]"
	chords[noteNum] = list (
		KeyIter (xrange (len (key)), noteNum, 0))
	###print "\tchords[noteNum=",noteNum,"]=",chords[noteNum]
###print "chords=",chords
#for b, p, n in zip (beatIter, progIter, noteNumProgIter):
#	print b, fundyChord (key, p, chords[noteNumKey[n]])

#for k in ProdIter (progIter, noteNumIter): print k
#for k in ChordIter (ProdIter (progIter, noteNumIter), key): print k

###print "init chordProgression"
chordProgression = list (ProdIter (progIter, noteNumProgIter))
###print "chordProgression=",chordProgression



###print "init rhythmScale"
rhythmScale = list (xrange (1, 10))
###print "rhythmScale=",rhythmScale
rhythmScaleType = 5
###print "init rhythmKey"
rhythmKey = list (KeyIter (rhythmScale, rhythmScaleType, 0))
###print "rhythmKey=",rhythmKey
###print "init rhythmProgIter"
rhythmProgIter = list (ProgIter (xrange (len (rhythmKey)), 37, 5, 0))
###print "rhythmProgIter=",rhythmProgIter

###print "init rhythmNoteNums"
rhythmNoteNums = list ([n for n in xrange (1, len (rhythmKey))])
###print "rhythmNoteNums=",rhythmNoteNums
#rhythmChordIters = list ([list (KeyIter (xrange (len (rhythmKey)), noteNum, 0)) for noteNum in rhythmNoteNums])
#rhythmNoteNumIter = list (SkipIter (Bjorklund3 (16, 5, 0), rhythmChordIters))

#rhythmNoteNums =
###print "init rhythmNoteNumKey"
rhythmNoteNumKey = list (KeyIter (rhythmNoteNums, 7 - len (rhythmNoteNums), 0))
###print "rhythmNoteNumKey=",rhythmNoteNumKey
###print "init rhythmNoteNumProgIter"
rhythmNoteNumProgIter = list (ProgIter (xrange (len (rhythmNoteNumKey)), 31, 3, 0))
###print "rhythmNoteNumProgIter=",rhythmNoteNumProgIter

###print "init rhythmChords"
rhythmChords = [None] * (max (rhythmNoteNumKey) + 1)
for noteNum in rhythmNoteNumKey:
	###print "init rhythmChords[noteNum=",noteNum,"]"
	rhythmChords[noteNum] = list (
		KeyIter (xrange (len (rhythmKey)), noteNum, 0))
	###print "rhythmChords[noteNum=",noteNum,"]=", rhythmChords[noteNum]
###print "init rhythmChordProgression"
rhythmChordProgression = list (ProdIter (rhythmProgIter, rhythmNoteNumProgIter))
###print "rhythmChordProgression=",rhythmChordProgression



###print "init beatIter"
beatIter = list (CountIter (Bjorklund.factory (13, 5, 0)))
###print "beatIter=",beatIter
###print "init beatChordProgression"
beatChordProgression = list ([rhythmChordToBeatChord (fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])) for p, n in rhythmChordProgression])
###print "beatChordProgression=",beatChordProgression
###print "init fundChordProgression"
fundChordProgression = list ([fundyChord (key, p, chords[noteNumKey[n]]) for p, n in chordProgression])
###print "fundChordProgression=",fundChordProgression

###print "init bcIter"
bcIter = list (ProdIter (beatIter, ProdIter (beatChordProgression, fundChordProgression)))
###print "bcIter=",bcIter
###print "init bcI"
bcI = list (BeatChordIter (bcIter))
###print "bcI=",bcI

#for sei in bcI: print sei
#for s, e, i in bcI:
#for s, e, i in repeat (bcI, 2):
#for sei, bf in ProdIter (bcI, baseFreqIter):
	#s, e, i = sei
	#print int (round (i * 174)), " ", int (round (e * 600))
	#print bf
	#print int (round (i * bf)), " ", e
	
# TODO add rests

#print len (baseFreqIter), len (bcI)
g = gcd (len (baseFreqIter), len (bcI))
for bf in chain.from_iterable (repeat (baseFreqIter, int (len (bcI) / g))):
	for sei in chain.from_iterable (repeat (bcI, int (len (baseFreqIter) / g))):
		s, e, i = sei
		#print bf, s, e, i
		print int (round (i * bf)), " ", e