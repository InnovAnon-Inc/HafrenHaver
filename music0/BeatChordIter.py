from __future__ import division
from itertools import *

from Bjorklund import *
from ChangeIter import *
from SkipIter import *
from SmoothIter import *

class BeatChordIterHelper:
	def __init__ (self, bcIter):
		# TODO verify correctness
		#self.length = sum ([len (bc) for dur, bc in bcIter])
		self.length = len (bcIter)
		self.bcIter = chain (bcIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): # beat as in rhythm-division... not the other kind (rhythm as in beat-division)
		#beat, ch = self.bcIter.next ()
		#prog, noteNumProg = ch
		#chord = chords[noteNumKey[noteNumProg]]
		duration, (beat, chord) = self.bcIter.next ()
		b = len (beat)
		c = len (chord)
		# TODO try >=
		#print "b=",b
		#print "c=",c
		if c is 1:
			i = list (FIter (Bjorklund.factory (b, c, 0), chord))
		elif b > c:
			i = list (ChangeIter (Bjorklund.factory (b, c, 0), chord))
		else:
			# TODO test
			si = list (SkipIter (Bjorklund.factory (c, b, 0), chord))
			#g = gcd (len (si), c)
			#print "gcd (", len (si),",",c,")=",g
			#i = repeat (si, si / g)
			i = si
		
		#print "chord=", chord
		#print "beat=", beat
		#print "i=",i
		#print zip (beat, i)
		
		se = list (SmoothIter (beat))[::-1]
		#print "se=",se
		s, e = zip (*se)
		#print "s=", s
		#print "e=", e
		#print "i=", i
		#print
		S = [S * duration for S in s]
		E = [E * duration for E in e]
		#return (duration, zip (s, e, i))
		#for s, e in se:
		#	yield (s * duration, e, i)
		return zip (S, E, i)
			
		#ret = fundyChord (key, prog, noteNumProg)
		#print (prog, zip (beat, i))
		#sleep (1)
		#return (prog, zip (beat, i))
		#print "test=",(duration, zip (beat, i))
		#return (duration, zip (beat, i))
		#return zip (beat, [duration * (1 + j) for j in i])
class BeatChordIter:
	def __init__ (self, bcIter):
		helper = BeatChordIterHelper (bcIter)
		self.length = len (helper)
		self.seq = chain.from_iterable (helper)
		#self.seq = helper.__iter__ ()
	# TODO fix length
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		#return self.seq.next ()
		return self.seq.next ()
		#return duration, play