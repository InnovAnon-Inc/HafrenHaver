#base = 100
"""print pitches (harmonics (10), base)
print pitches (scale1 (10, 10), base)
print pitches (indian_scale1, base)
print pitches (just_scale, base)
print pitches (indian_scale2, base)
print pitches (pythagorean_scale, base)"""
"""
print pitches (harmonics20 (10), base)
print pitches (harmonics21 (10), base)
print pitches (harmonics22 (10), base)
print harmonics2 (10)
print pitches (harmonics2 (10), base)
"""
"""
print pitches (scale2 ({(2, 2), (3, 2), (5, 2)}), base)
print pitches (scale2 ({(2, 3), (3, 2), (5, 1), (7, 1)}), base)
print pitches (scale2 ({(2, 1), (3, 1), (5, 1), (8, 1), (13, 1)}), base)
print pitches (scale2 ({(2, 20), (3, 20)}), base)
"""
"""
print scale2 ([(b, 1) for b in harmonics2all (1)])
print scale2 ([(b, 1) for b in harmonics2all (2)])
print scale2 ([(b, 1) for b in harmonics2all (3)])
print scale2 ([(b, 1) for b in harmonics2 (4)])
"""
"""
print scale2 ([(b, 2) for b in harmonics2all (1)])
print scale2 ([(b, 2) for b in harmonics2all (2)])
print scale2 ([(b, 2) for b in harmonics2all (3)])
print scale2 ([(b, 2) for b in harmonics2 (4)])
"""
"""
for p in xrange (3):
	for k in xrange (6):
		print sorted (scale3 (harmonics2 (k + 1), p + 1))
"""
"""
for p in xrange (3):
	for k in xrange (6):
		print sorted (scale3 (harmonics2all (k + 1), p + 1))
"""
"""
print pitches (scale2 ([(b, 1) for b in harmonics2 (3)]), base)
print pitches (scale2 ([(b, 2) for b in harmonics2 (3)]), base)
print pitches (scale2 ([(b, 1) for b in harmonics2 (4)]), base)
print pitches (scale2 ([(b, 2) for b in harmonics2 (4)]), base)
"""
"""
print pitches (sorted (scale3 ([(1 + pow (5, .5)) / 2], 6)), base)
print pitches (sorted (scale3 ([
	2/3, 3/2,
	4/5, 5/4,
	4/7, 7/4,
	5/7, 7/5,
	8/9, 9/8,
	9/10, 10/9], 3)), base)
"""
"""
print pitches (sorted (scale3 (harmonics21 (10), 1)), 100)
print pitches (sorted (scale4 (harmonics3 (4))), 100)
print pitches (sorted (harmonics4inv2 (8)), 100)
"""
"""
pick melody from "chord"
chord progression based on that
melody notes based on chords within chord progression

pick number of measures
divide that by a sequence. i.e., 2+3+2 2+3+2
generate rhythm that repeats

melody should repeat... follow A A B A song structure?

melody generating helper functions: scales + arpeggios + repetition + alternating

left hand:  | a b a a  | a b a a  |
right hand: |  c c c b |  c c c b |
third hand: |  12 1  3    12 1  3
1: |a-c|
2: |b-c|
3: |a-b|
simple repetition + alternating, trinary scale, two parts, one part is rotated by a couple notes

legato, staccato, crescendo, descendo, ritard

different musicians can play at different tempos

modulation: key siggy changes, even mid-measure

cell:
2-3 notes + rhythm + accent
^^^ a couple times => phrase (e.g., 2-3 measures)

should have intra-cell modulation?

AABA or AABB phrases => verse (e.g., 12 bar blues)

AABA or AABB verses or ABACABA or AA1BA2CA3BA4 or ABABCB => song

song + variations => song cycle ?

sections:
intro, verse, pre-chorus, chorus/refrain, bridge, outro/coda
exposition, recapitulation, conclusion, interlude

sequence:
2-4 segments
usually in one direction (e.g., going higher or lower in pitch)
continue by same interval distance

figure/motif/cell => phrase => melody/period/section

phrase ~ 4 bars
period ~ 2-4 phrases

riff vs fill
riff: often repeated
fill: played between riffs
- can be standard motifs
- can be improv'd

transformations:
- retrograde: reverse melody and/or rhythm
- transposition
- inversion?
- multiplication?

melodic motion:
- ascending
- descending
- undulating/pendulum
- tile/terrace/cascading
- rise or musical plateau

modal frame:
- floor note
- ceiling note
- central note
- upper/lower focus (i.e., skew)
"""
"""
tempo_changes["rallentando"] = gradually slowing down
tempo_changes["ritardando"] = gradually slowing down (but not as much)
tempo_changes["ritenuto"] = immediately slowing down
tempo_changes["stringendo"] = gradually speeding up (slowly)
tempo_changes["accelerando"] = gradually speeding up (quickly)

tempo_changes["allargando"] = growing broader, decreasing tempo
tempo_changes["calando"] = going slower (and usually softer)
tempo_changes["doppio movimento"] = double speed
tempo_changes["doppio piu mosso"] = double speed
tempo_changes["doppio piu lento"] = half speed
tempo_changes["lentando"] = gradual slowing and softer
tempo_changes["meno mosso"] = less movement or slower
tempo_changes["mosso"] = movement, more lively or quicker... less extreme than piu mosso
tempo_changes["piu mosso"] = more movement or faster
tempo_changes["precipitando"] = hurrying, going faster/forward
tempo_changes["rubato"] = free adjustment of tempo
tempo_changes["stretto"] = faster tempo
tempo_changes["tardando"] = slowing down gradually
"""
#euclid for rhythm pattern
#select number of notes in scale
#euclid for choosing arpeggio notes
####scale is alphabet
####create conditional probability table for bigrams (or variable length sequences)
####sequences of letters, sequence of words, sequences of sentences

# common patterns:
# fibonacci
# euclid
# alternating
# increasing/decreasing
# peaks/valleys
# cascade
# +k  (mod m)
# *k  (mod m)
# **k (mod m)
# railfence & other transposition ciphers

# how to measure entropy of music?
# keep track of current entropy level and previously played sequences
# re-use previously played sequences in order to moderate entropy
# track entropy of phrase, verse, song, etc

# other channels must track which frequencies are being played at which times
#    and remove dissonant frequencies from the scale when generating their melodies

# types of notes:
# rest
# whole (measure)
# dotted half
# half triplet
# half
# triplet
# dotted quarter
# quarter (1 beat)
# dotted eighth
# eighth
# dotted sixteenth
# sixteenth

# music divided into measures
# ...with repeats and other structure
# songs usually have a standard number of measures?
# measures divided into beats

# rhythm
# alternation, repetition, strong vs. weak beats, beats vs. rest
# predictable rhythm, possible syncopation

# melody = pitch + duration + rhythm

# time siggys - simple, compound, complex, mixed, additive, fractional, irrational



#print sorted (chain (solfeggios ()))

#hs = [harmonic + 1 for harmonic in xrange (10)]
#hs = [harmonic + 1 for harmonic in xrange (6)]
#hs = [1] + sorted ([(h + 1) / h for h in hs])
#hs = sorted ([(h + 1) / h for h in hs])

#for h in xrange (len (hs)):
	#for k in xrange (h):
		#for p in euclid (h, k, hs):
		#	print p
		#print "euclid (", hs[h], ",", hs[k], ")=", euclid (h, k, list (hs))
#l = []
#map (l.extend, [euclid (h, k, list (hs)) for h in xrange (len (hs)) for k in xrange (h)])
#l = sorted (set (l))		
"""
11100000
10 10 10 00
100 100 10
100 10 100 ?

abcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg
100101001001010010010100100101001001010010010100100101001001010010010100
a  d f  b  e g  c  f a  d  g b  e  a c  f  b d  g  c e  a  d f  b  e g
adfbegcfadgbeacfbdgce adfbeg

22222 10010100
21 20 20 21 20 100 ?
211 200 200 21 20
211 21 200 20 200

22222 10 01 01 00
2 10 2 01 2 01 2 00 2

2112 1200 2020 0 3333
2113 2123 0023 0
21123 12203 20203

111110000000
10 10 10 10 10 00
100 100 10 10 10
100 10 100 10 10

111112222333
12 12 12 12 13 33
123 123 12 12 13
123 12 123 12 13
123 12 13 123 12 ?

111111111111 00000000
01 01 01 01 01 01 01 01 1111
011 011 011 011 01 01 01 01
011 01 011 01 011 01 011 01

111222333444 55667788
51 51 61 62 72 72 83 83 3444
513 514 614 624 72 72 83 83
513 72 514 72 614 83 624 83 ?
"""
"""
def melody (scale):
	length = len (scale)
	return melody2 (length * length, scale)
def melody2 (length, scale):
	return [scale[randint (0, len (scale) - 1)] for _ in xrange (length)]
"""
"""for a in xrange (8):
	b = Bjorklund (8, a + 1)
	b.bjorklund ()
	print b.sequence
b = Bjorklund (13, 5)
b.bjorklund ()
print b.sequence"""

#display_scale (pitches ([1] + list (equal_temperament_scale (12)), 440))
"""
k = sorted ([min_max_normalize (m, 147, 963) for m in solfeggios ()])
print k
display_scale (pitches (k, 1))
"""
#h = list (harmonics5 (10))
#h2 = h.index (2)
#for i in xrange (len (h)):
#	if i != h2:
#		display_scale ([1] + euclid (h2, i, h))

#select_number_of_channels ()
# ^^^ includes harmonies/chords, other rhythms, other tempos
# select_brainwave_freq () ?
#select_tempo ()
#select_key_siggy ()
#select_time_siggy ()
#select_base_freq ()
#select_scale ()

#select_song_structure ()
#select_verse_structures ()
#select_phrase_structures ()
#select_cells ()

#choose time siggy: number of beats per 2-4 bars
#choose number of beats to go into bar of that length
#^^^ => phrase structure... need number of phrases... 2-4?... multiple types?
#^^^ => verse structure... need number of verses... 2-8?... multiple types
# chord progression?
"""
cps = generate_coprime_pairs (16)
#print cps
cp = choice (list (cps))
print cp
"""
#phrase = cp[0] * cp[1]
#print phrase
"""
b = Bjorklund (cp[0], cp[1])
b.bjorklund ()
print b.sequence
display_bjorklund (b.sequence)
"""
#display_scale (pitches ([1] + list (equal_temperament_scale (12)), 440))
#display_scale ([1] + list (harmonics5 (12)))
#sleep (30)
#exit

#b = Bjorklund (12, 7)
#b.bjorklund ()
#print b.sequence
#display_bjorklund (b.sequence)
#sleep (30)
#exit

#b = Bjorklund (8, 5)
#b.bjorklund ()
#print b.sequence
#display_bjorklund (b.sequence)
#sleep (30)
#exit
"""
for k in xrange (2, 10):
	s = sorted ([1] + list (set (harmonics7 (k))))
	print len (s)
	for v in [4, 6, 8, 12, 20]:
		if v > len (s): continue
		b = Bjorklund (len (s), v)
		b.bjorklund ()
		display_bjorklund_scale (s, b.sequence)
		sleep (2)
"""
"""
def bjorklund_complete (n, p, r):
	b = Bjorklund (n, p)
	b.bjorklund ()
	s = b.sequence
	s.rotate (r)
	return s
"""
"""
class SongCycle:
	def __init__ (self, songs, pattern, mode):
		self.songs = songs
		self.seq = bjorklund_complete (len (songs), pattern, mode)
class Song:
	def __init__ (self, verses, pattern, mode):
		self.verses = verses
		self.seq = bjorklund_complete (len (verses), pattern, mode)
class Verse:
	def __init__ (self, phrases, pattern, mode):
		self.phrases = phrases
		self.seq = bjorklund_complete (len (phrases), pattern, mode)
class Phrase:
	def __init__ (self, cells, pattern, mode):
		self.cells = cells
		self.seq = bjorklund_complete (len (cells), pattern, mode)
		# need melody and "rhythm" for chord changes
class Cell:
	def __init__ (self,
		scale, key, mode,
		chord, chpattern, chmode,
		beats, pulses, bpmode):
		self.channels = 1
		self.scale = bjorklund_complete (len (scale), key, mode)
		self.chord = bjorklund_complete (key, chpattern, chmode)
		self.rhythm = bjorklund_complete (beats, pulses, bpmode)
		#TODO generate multi-order stochastic table ?
		
		# bass line         100 10 100 100 10 100
		# melody durations  3   2  3   3   2  3
		
		# hidden            10  10  100 10 10 10 10 100 10 10
		# beat pattern      1/2 1/2 1/3 1/2 ?
		
		# hidden            10 100 10 10 100 10
		# melody notes      1  3   3  2  1   1

		# hidden            100 10 100 10  100 100 10 100 10 100 100 10 100 10 100
		# number of bars    3   2  3   2   3   3   2  3   2  3   3   2  3   2  3
		# chord progression 1   4  5   1   4   5   1  4   5  1   4   5  1   4  5
		
		# hidden
		# ...some sort of rhythm of cell changes ?
"""
# 100 10 100 100 10 100 100 10 100 100 10 100
# tff tf tff tff tf tff tff tf tff tff tf tff
# hlm hl mhl mhl mh lmh lmh lm hlm hlm hl mhl
# hhmmmlllhhhm
# now need durations

# ranges, chakras => base frequency

#0  5   10   15
#0 3 6 9  12 15
"""
class SkipIter:
	def __init__ (self, bjork, seq):
		(a, b, c) = lcm_pair (sum (bjork), len (seq))
		self.bjork = cycle (
			#repeat (
				bjork
			#, a)
		)
		self.seq = cycle (
			#repeat (
				seq
			#, b)
		)
		self.length = c
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		bj = self.bjork.next ()
		seq = self.seq.next ()
		if bj is 1: return seq
		return self.next ()
class SkipIter2:
	def __init__ (self, bjork, seq):
		self.length = sum (bjork)
		(a, b, c) = lcm_pair (self.length, len (seq))
		self.bjork = cycle (bjork)
		self.seq = cycle (seq)
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		bj = self.bjork.next ()
		seq = self.seq.next ()
		if bj is 1: return seq
		return self.next ()
"""
#1001010010100 10010100101001001010010100
#1  3 2  3 2   3  3 2  3 2  3  3 2  3 2
"""
class ChangeIter:
	def __init__ (self, bjork, seq):
		self.length = sum (bjork.seq)
		(a, b, c) = lcm_pair (self.length, len (seq))
		self.bjork = cycle (bjork)
		self.seq = cycle (seq)
		self.seq_cur = seq.next ()
	def __len__ (self):
		return self.length
	def __iter__ (self):
		return self
	def next (self):
		bj = self.bjork.next ()
		ret = self.seq_cur
		if bj is 1: self.seq_cur = seq.next ()
		return ret
"""
"""
class BeatChordIter:
	def __init__ (self, beats, chords

class Cell2:
	def __init__ (self, beats, rhythms, chords, chbeats):
		self.beats = beats
		self.rhythms = rhythms
		self.chords = chords
		self.chbeats = chbeats
		# get next beat(s)
		# get next chord, play for that many beats
		
		beat = self.beats.next ()
		chord = self.chords.next ()
		chbeat = self.chbeats.next ()
		
		next_beat = self.beats.next ()
		next_chord = self.chords.next ()
		next_chbeat = self.chbeats.next ()
		
		m = min (beat, chbeat)
		a = [chord] * m
		b = modulate (chord, next_chord) * (beat - i)
		c = [next_chord] * (chbeat - i)
		
		i = 0
		while i < beat and i < chbeat:
			#notes come from chord
		while i < beat:
			#notes come from modulate (chord, next_chord)
		while i < chbeat:
			#notes come from next_chord
		beat = next_beat
		chord = next_chord
		# play for beat * rhythm
		
		#10010100101001001010010100
		#  c  f g  c f  g  c f  g c
		
		#10101101101011011010110110
		#c f gc fg c fg cf g cf gc
		#  c  f g  c f  g  c f  g c

		#10010100101001001010010100
		#c f gc fg c fg cf g cf gc
		#c qfpccqg c qg pf g pf gp
		#111000000111000111000000111000111000
		#ccccccqqqfffpppccccccqqqggg
		#q=modulate(c,f)
		#p=modulate(c,g)
		
		#ccqfp ccqgg ccqgg pffgg pffgp

		#                          CFG CF GCF GCF GC FGC
		# periods of so many beats 323 23 323 323 23 323
		# divide each period by equal numbers 1/2 1/3 1/5
		# each subdivisions of the period will follow bjork pattern
"""
"""
class Cell3:
	def __init__ (self, beat, melody, rhythm, rests, volume):
		# repeat, variation, new
		# 3 beats, 1/5 rhythm, which beat*rhythms to skip
		self.beat = beat
		self.melody = melody
		self.rhythm = rhythm
		self.rests = rests
		self.volume = volume

		notes = [None] * lcm (rhythm, len (rests))
		note_duration = beat / rhythm
		for i in xrange (len (notes)):
			if not rests[i]:
				notes[i] = melody.next ()
"""
"""
class Bjorklund2 (Bjorklund):
	def __init__ (self, lengthOfSeq, pulseAmt, rotateAmt):
		Bjorklund.__init__ (self, lengthOfSeq, pulseAmt)
		#super (Bjorklund2.__class__, self).__init__ (lengthOfSeq, pulseAmt)
		self.bjorklund ()
		self.rotate (rotateAmt)
beatIter = CountIter (Bjorklund2 (13, 5, 0))
"""
"""
class Bjorklund3:
	def __init__ (self, lengthOfSeq, pulseAmt, rotateAmt):
		bjork = Bjorklund (lengthOfSeq, pulseAmt)
		bjork.bjorklund ()
		bjork.rotate (rotateAmt)
		self.seq = bjork.sequence
		self.pulseAmt = pulseAmt
"""

























# TODO SkipIter should use amt relatively prime to len rhythms
#rhythmIter = SkipIter2 (Bjorklund3 (11, 3, 0).seq, rhythms)
#for k in rhythmIter: print k

#rhythmIter = SkipIter2 (Bjorklund3 (len (rhythms), 3, 0).seq, rhythms)
#for k in rhythmIter: print k
"""
class SyncopatIter:
	def __init__ (self, b):
		self.b = b
		a = list (xrange (1, b + 1))
		self.a = SkipIter2 (Bjorklund3 (len (a) + b, b, 0).seq, a)
	def __iter__ (self): return self
	def next (self):
		#return [self.a.next () for i in xrange (self.b)]
		ret = self.a.next ()
		return ret
class InterleavIter:
	def __init__ (self, interval, seq):
		self.interval = interval
		self.seq = Bjorklund3 (interval, seq, 0).seq
	def __iter__ (self): return self
	def next (self):
		return self.seq
class RhythmIter:
	def __init__ (self, ar):
		self.ar = ar
	def __iter__ (self): return self
	def next (self):
		r = self.ar.next ()
		return r, SyncopatIter (r)
#rhythmIter2 = RhythmIter (rhythmIter)
for r, k in rhythmIter2:
	j = 0
	for p in k:
		if j == 10: break
		j += 1
		interleavIter = InterleavIter (r, p)
		for i in xrange (5):
			print interleavIter.next ()
"""
"""
range iterator
chakra iterator
=> solfeggio (base freq) iterator

beat iterator

scale
key is subset of scale

noteNums length <= key length
noteNumKey is subset of noteNums

for each length in noteNumKey
	chord[length] is subset of key

rhythms
rhythmKey is subset of rhythms
rhythmProg[

silence[rhythm] is [0..rhythm]
silenceKey[rhythm] is subset of silence[rhythm]


fundyIter is subset of key
chords[noteNum] is subset of key
noteNumIter is subset of noteNumKey
rhythmIter is subset of rhythmKey
silenceIter[rhythm] is subset of rhythm

for each beat:
melodyIter[chord, noteNum, rhythm, silences] is subset of chords[noteNum] and has rhythm-silences notes
"""

# 1 a 1.0
# 2 b 1.125
# 3 c 1.185185185
# 4 d 1.33333333333
# 5 e 1.5
# 6 f 1.58024691358
# 7 g 1.77777777777

#000000000111
#000100010001
#100010001000 100010001000 100010001000 100010001000 1
#abcdefgabcde fgabcdefgabc defgabcdefga bcdefgabcdef g
#a   e   b    f   c   g    d   a   e    b   f   c    g

#aebfcgd

#1000 1000 * 7
#abcd efga * 4

#0000 111

#1234567 1234567 1234567 1234567
#abcdefg abcdefg abcdefg abcdefg
#1000000 0001000 0000100 0000000
#979 979 979

#9+9=18=>20
#7+7=14=>16
#9+7=16=>18
#9+7+9=25=>28

#1001100
#abcdefg

# 1.0
# 1.33333
# 1.5























# shits on Bj[x,0,z]
#for k in xrange (8 + 1):
#	print Bjorklund3 (8, 8 - k, 0).seq
#print "TEST"
#print "a=",list (Bjorklund3 (8, 8, 0).seq)
#print "b=",list (SkipIter (Bjorklund3 (8, 8, 0), xrange (1,9)))
#print "END TEST"

#silenceBjork
#melodyBjork
#(melodyChord,chord)
#sort and iter rhythms
#   iter silencebjork
#      note = skiperator
#      if silence: continue
#      if melodybjork.next
#        note



















# TODO replace rhythmProgIter with silProgIter
# ... foreach rhythm
#             /|\
#             0sil 1sil 2sil... rhythmsil
# rhythmProg * silences
#rhythmProgression = list (ProdIter (rhythmProgIter, rhythmNoteNumProgIter))
#print "rhythmProgression=",rhythmChordProgression

##### 

#class BeatChordIter:
#	def __init__ (self, rhythmChordProgression):
#		self.seq = rhythmChordProgression
#		self.__len__ = 
#beatChordProgression = list ([sorted ([(k/r, 1/r) for r in rhythmChord for k in xrange (r)]) for rhythmChord in rhythmChordProgression])








# noteNum * rhythm-silence => arpeggio
#print "chordProgression=", chordProgression

#print list (rhythmProgression)



























	


#print list (CountIter (Bjorklund3 (7, 5, 0)))
#print "PISS=",list (CountIter (Bjorklund3 (7, 5, 0)))
#print len (ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5))))
#for k in ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5))):
#	print k
#print ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5)))
#print "SHIT=",list (ChangeIter (Bjorklund3 (7, 5, 0), list (xrange (5))))
#i = list (ChangeIter (Bjorklund3 (b, c, 0), chord))
#print "ASDFASDF"
#sleep (5)


#for k in xrange (1,9):
#	print k, list (CountIter (Bjorklund3 (8, k, 0)))
#sleep (5)


























"""
class ExpandBCPIter:
	def __init__ (self, bcp):
		bcp = bcp[::-1]
		self.bcp = bcp.__iter__ ()
		self.length = len (bcp)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		last = (None, 1)
		for n, r in notesRhythms:
			l = last[1]
			last = n, r
			yield n, r, l - r
expandBCPIter = ExpandBCPIter (beatChordProgression)
print list
"""































"""
class BeatChordMaskIterAdapter:
	def __init__ (self, bcIter):
		self.length = sum ([len (bc) for bc in bcIter])
		print list (bcIter)
		self.bcIter = chain (bcIter)
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self): return self.bcIter.next ()
"""
"""
class MaskIter:
	def __init__ (self, bjork, seq):
		self.length = len (seq)
		self.bjork = bjork
		self.seq = seq
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		self.seq.next ()
"""	

# MUST MULTIPLY BY DURATION before EXPANDING bcIter and DROPPING notes



















































"""
class ExpandBcIterHelper:
	def __init__ (self, nr):
		print 'A'
		self.nr = nr.__iter__ ()
		print 'B'
		self.length = len (nr)
		print 'C'
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		print 'D'
		last = (None, 1)
		print 'E'
		for n, r in notesRhythms:
			print 'F'
			print last[1] - r
			yield n, last[1] - r
			print 'G'
			last = n, r
			print 'H'
class ExpandBcIter:
	def __init__ (self, bcIter):
		print 'a'
		self.bcIter = bcIter.__iter__ ()
		print 'b'
		# TODO expand length
		self.length = len (bcIter)
		print 'c'
	def __len__ (self): return self.length
	def __iter__ (self): return self
	def next (self):
		print 'd'
		duration, z = self.bcIter.next ()
		print 'e'
		#print duration, z
		#print list (z)
		#print list (z)[::-1]
		last = (1, None)
		print 'f'
		for r, n in z[::-1]:
			print 'g'
			yield r, last[0] - r, n
			print 'h'
			last = r, n
		print 'k'
		#n, r = list (ExpandBcIterHelper (notesRhythms[::-1]))
		#print 'f'
		#print (r * duration, n)
			# start at r
			# hold for next_r - r
			# tail_r = duration
		# multiply each rhythm by duration
		# (rhythm := start time of note)
print "god damn it=",list (BeatChordIter (bcIter))
for duration, z in BeatChordIter (bcIter):
	print duration
	for r, n in z:
		print r, n
print "NEXT"
e = ExpandBcIter (list (BeatChordIter (bcIter)))
print len (e)
for E in e: print E
print list (e)
"""













































#maxRhythm = 5
#rhythms = sorted ([1] + list (set ([n / d
#	for d in xrange (1, maxRhythm)
#		for n in xrange (1, d)])))
#rhythms = list (xrange (1, 10))


#for (b, (p, n)) in zip (beatIter, chordProgression):
#	print b, fundyChord (key, p, chords[noteNumKey[n]])

#rangeIter = SkipIter (Bjorklund.factory (10, 9, 0), ranges)
#chakraIter = SkipIter (Bjorklund.factory (15, 13, 0), chakras)
#for k in BaseFreqIter (rangeIter, chakraIter, solfeggio): print k


#for b, p, n in zip (beatIter, rhythmProgIter, rhythmNoteNumProgIter):
#for (b, (p, n)) in zip (beatIter, rhythmChordProgression):
#	print b, fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])

"""
silProgs = [None] * (max (rhythmKey) + 1)
#rs = [None] * (max (rhythmKey) + 1)
melodies = [None] * (max (rhythmKey) + 1)
#for k in xrange (1, max (rhythmKey) + 1):
#	melodies[k] = list (SkipIter (Bjorklund3 (max (noteNum, rhythmKey[k]), min (rhythmKey[k], noteNum), 0), chords[noteNum]))
	#print melodies[k]
for rhythm in rhythmKey:
	silScale = list (xrange (1, rhythm + 1)) #[0, rhythm]
	silScaleType = 5
	silScaleType = min (silScaleType, len (silScale))
	silScaleType = max (silScaleType, 1)
	# TODO maybe don't use subset:
	silKey = list (KeyIter (silScale, silScaleType, 0))
	silProgIter = list (ProgIter (xrange (len (silKey)), 29, 2, 0))
	silProgs[rhythm] = silProgIter
"""
#	"""
#	print ("rhythm=",rhythm,
#		"silScale=",list (silScale),
#		"silScaleType=",silScaleType,
#		"silKey=",list (silKey))
#	"""
#	#print len (list (SkipIter (Bjorklund3 (len (silScale), silScaleType, 0), silScale)))
#	
#	"""rs[rhythm] = [None] * (max (silKey) + 1)
#	melodies[rhythm] = [None] * (max (silKey) + 1)
#	for sil in silKey:
#		rs[rhythm][sil] = Bjorklund3 (rhythm, sil, 0).seq
#
#		melodies[rhythm][sil] = [None] * (max (noteNumKey) + 1)
#		for noteNum in noteNumKey:
#			melodies[rhythm][sil][noteNum] = list (SkipIter (Bjorklund3 (max (noteNum, rhythm), min (rhythm, noteNum), 0), chords[noteNum]))
#			#print melodies[rhythm][sil][noteNum]
#	"""
#for b, p, n in zip (beatIter, rhythmProgIter, rhythmNoteNumProgIter):
#	print b, fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])

#chordProgression = list (ProdIter (progIter, noteNumProgIter))

#for p, n in chordProgression:
#	print fundyChord (key, p, chords[noteNumKey[n]])
#for p, n in rhythmChordProgression:
#	print fundyChord (rhythmKey, p, rhythmChords[rhythmNoteNumKey[n]])

# TODO add silence to scale

# TODO expand here
#beatChordProgression = 
#print fundChordProgression
#for bc in beatChordProgression: print bc

#bcIter = list (ProdIter (beatChordProgression, chordProgression))
#bcIter = list (ProdIter (beatChordProgression, fundChordProgression))
#silBjork = Bjorklund.factory (13, 5, 0)
#bcIter = list (ProdIter (beatIter, ProdIter (MaskIter (silBjork, beatChordProgression), fundChordProgression)))
#bcIter = list (ProdIter (beatIter, ProdIter (beatChordProgression, fundChordProgression))

#for bc in BeatChordIter (bcIter): print "bc=",bc