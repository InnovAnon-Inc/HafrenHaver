#print list (BeatChordIter (bcIter))
		
#beatChordProgression = list ([sorted ([(k/r, 1/r) for r in rhythmChord for k in xrange (r)]) for rhythmChord in rhythmChordProgression])
bcIter = ProdIter (beatChordProgression, chordProgression)
#bcIter = ProdIter (rhythmChordProgression, chordProgression)
for beat, ch in bcIter:
	prog, noteNumProg = ch
	chord = chords[noteNumKey[noteNumProg]]
	b = len (beat)
	c = len (chord)
	#print chord
	
	#print "beat=",beat
	#print "chord=", chord
	
	if b > c:
		#print Bjorklund3 (b, c, 0).seq
		i = list (ChangeIter (Bjorklund3 (b, c, 0), chord))
		#i = None
		#print "changeIter=", i
	else:
		i = list (SkipIter (Bjorklund3 (c, b, 0), chord))
		#print "skipIter=",i
	#print "i=",i
	#list (SkipIter (Bjorklund3 (max (b, c), min (c, b), 0)*, chords[noteNum]))

#for (rhythmChord, chord) in ProdIter (rhythmChordProgression, chordProgression):
#	rhythmNotes = sorted ([(k/r, 1/r) for r in rhythmChord for k in xrange (r)])

#ProdIter (beatIter, progIter, noteNumProgIter, rhythmProgIter, rhythmNoteNumProgIter)
print "DONE"

















#for k in ChordIter (ProdIter (rsProgIter, rhythmNoteNumIter), key): print k
#for k in ChordIter (ProdIter (rhythmProgIter, rhythmNoteNumIter), rhythmKey): print k
sleep (5)

# beat    beat    beat
# chord   chord   chord
# rhythms rhythms rhythms
# /|\
#rhythm   rhythm   rhythm
#silences silences silences
#melody   melody   melody
#
#for each (beat, chord, rhythmChord)
#   foreach rhythm in rhythmChord
#      nnote = bjork (rhythm, silenceIters[rhythm].next)
#      melody(chord, nnote)?


#class RhythmIter:
	
sleep (5)






class NestIter:
	def __init__ (self, itr):
		self.itr = SkipIter (itr)
		
	def __iter__ (self): return self
	def next (self): return self.itr.next ()










"""class SilenceIter:
	def __init__ (self, rang):
		self.rang = xrange (1, rang)
		self.it = SkipIter2 (Bjorklund3 (31, 23, 0).seq, self.rang)
		for i in xrange (10):
			print self.it.next ()
	def __iter__ (self):
		return self
	def next (self):
		return self.it.next ()

class ArhythmIter:
	def __init__ (self, rhythmIter):
		self.rhythmIter = rhythmIter
	def __iter__ (self):
		return self
	def next (self):
		rhythm = rhythmIter.next ()
		#print rhythm
		return rhythm, SilenceIter (rhythm)
arhythmIter = ArhythmIter (rhythmIter)
for k, p in arhythmIter:
	print k
	print list (p)

class RhythmIter:
	def __init__ (self, ar):
		self.ar = ar
	def __iter__ (self): return self
	def next (self):
		ar, se = arhythmIter.next ()
		s = se.next ()
		return Bjorklund3 (ar, s, 0).seq
rhythmIter2 = RhythmIter (arhythmIter)"""

rangeIter = SkipIter2 (Bjorklund3 (10, 9, 0).seq, ranges)
#for k in rangeIter: print k

chakraIter = SkipIter2 (Bjorklund3 (15, 13, 0).seq, chakras)
#for k in chakraIter: print k

baseFreqIter = ZipIter (rangeIter, chakraIter, solfeggio)
#for k in baseFreqIter: print k

# 4,5 - 8
scaleType = 7
scaleMode = 0
scale = list (pythagorean_scale)
scale.remove (2)
# key:
keyIter = SkipIter2 (Bjorklund3 (len (scale), scaleType, scaleMode).seq, scale)
#for k in keyIter: print k
key = list ([keyIter.next () for k in xrange (scaleType)])
#print key
progIter = SkipIter2 (Bjorklund3 (19, 15, 0).seq, xrange (len (key)))
#for k in progIter: print k

# number of notes in chord: 3 to len(keyIter) - 1
noteNums = list ([n for n in xrange (2, len (key))])
noteNumIter = SkipIter2 (Bjorklund3 (16, 5, 0).seq, noteNums)
#for k in noteNumIter: print k

# TODO rotate key by progIter.next ()
#chordBjork = Bjorklund (len (keyIter2), noteNumIter.next ())
#chordBjork.bjorklund ()
#chordBjork.rotate (0)
#chordIter = SkipIter (chordBjork.sequence, keyIter2)
#for k in chordIter: print k

class ChordIter:
	def __init__ (self, progIter, noteNumIter, key):
		self.progIter = progIter
		self.noteNumIter = noteNumIter
		self.key = key
	def __iter__ (self):
		return self
	def next (self):
		prog = self.progIter.next ()
		noteNum = self.noteNumIter.next ()
		return SkipIter2 (Bjorklund3 (len (self.key), noteNum, prog).seq, self.key)
chordIter = ChordIter (progIter, noteNumIter, key)

class CellIter:
	def __init__ (self, beatIter, arhythmIter, chordIter):
		self.beatIter = beatIter
		self.arhythmIter = arhythmIter
		self.chordIter = chordIter
	def __iter__ (self):
		return self
	def next (self):
		beat = self.beatIter.next ()
		div, arhythm = self.arhythmIter.next ()
		chordIter = self.chordIter.next ()
		
		b = beat / div
		n = arhythm
		#n = [chordIter.next () for i in xrange (div)]
		
		return (b, n)
cellIter = CellIter (beatIter, rhythmIter2, chordIter)
#for k in cellIter:
#	print k

#beatBjork = Bjorklund (13, 5)
#beatBjork.bjorklund ()
#beatBjork.rotate (0)
#beatIter = CountIter (beatBjork.sequence)
#for k in beatIter: print k

#rhythmBjork = Bjorklund (22, 13)
#rhythmBjork.bjorklund ()
#rhythmBjork.rotate (0)
#rhythms = sorted (list (set ([n / d
#	for n in xrange (1, 5)
#		for d in xrange (1, 5)])))
#print len (rhythms)
#rhythmIter = SkipIter2 (rhythmBjork.sequence, rhythms)
#for k in rhythmIter: print k

"""rhythmSelect = list ([n for n in xrange (1, len (rhythmIter))])
rhythmSelectBjork = Bjorklund (len (rhythmSelect), 3)
rhythmSelectBjork.bjorklund ()
rhythmSelectBjork.rotate (0)
rhythmSelectIter = SkipIter (rhythmSelectBjork.sequence, rhythmSelect)
print rhythmSelect
#print rhythmSelectBjork.sequence
#for k in rhythmSelectIter: print k
"""
"""
rhythmBjork2 = Bjorklund (len (rhythmIter), 3)
rhythmBjork2.bjorklund ()
rhythmBjork2.rotate (0)
rhythmIter2 = SkipIter2 (rhythmBjork2.sequence, rhythmIter)
for k in rhythmIter2: print k
"""
#rangeBjork = Bjorklund (7, 5)
#rangeBjork.bjorklund ()
#rangeBjork.rotate (0)
#rangeIter = SkipIter2 (rangeBjork.sequence, ranges)
#for k in rangeIter: print k

#chakraBjork = Bjorklund (15, 6)
#chakraBjork.bjorklund ()
#chakraBjork.rotate (0)
#chakraIter = SkipIter2 (chakraBjork.sequence, chakras)
#for k in chakraIter: print k

#baseFreqIter = ZipIter (rangeIter, chakraIter, solfeggio)
#for k in baseFreqIter: print k

# 4,5 - 8
#scaleType = 7
#scaleMode = 0
#scale = list (pythagorean_scale)
#scale.remove (2)
# key:
#scaleBjork = Bjorklund (len (scale), scaleType)
#scaleBjork.bjorklund ()
#scaleBjork.rotate (scaleMode)
#print scaleBjork.sequence
#print sum (scaleBjork.sequence)
#print len (scale)
#keyIter1 = SkipIter2 (scaleBjork.sequence, scale)
#keyIter2 = SkipIter2 (scaleBjork.sequence, scale)
#scaleIter
#for k in keyIter1: print k


def scale_key (scale, scaleType, scaleMode):
	scaleBjork = Bjorklund (scale, scaleType, scaleMode)
	scaleBjork.bjorklund ()
	scaleBjork.rotate (scaleMode)
	scaleIter = SkipIter2 (scaleBjork.sequence, scale)
	return scaleIter
"""def key_chord (key, chordType, chordPhrasing):
	chordBjork = Bjorklund (key, chordType, chordPhrasing)
	chordBjork.bjorklund ()
	chordBjork.rotate (chordPhrasing)
	chordIter = SkipIter2 (chordBjork.sequence, key)
def key_progression (key, progType, progMode):
	progBjork = Bjorklund (key, progType, progMode)
	progBjork.bjorklund ()
	progBjork.rotate (progMode)
	progIter = SkipIter2 (progBjork.sequence, key)
"""

#print scaleBjork.sequence
#print scale
#print keyIter1.length

# root progression
#progBjork = Bjorklund (len (keyIter1), 3)
#progBjork.bjorklund ()
#progBjork.rotate (0)
# clone keyIter
#progIter = SkipIter (progBjork.sequence, keyIter1)
#for k in progIter: print k

# number of notes in chord: 3 to len(keyIter) - 1
#noteNums = list ([n for n in xrange (2, len (keyIter2))])
#noteNumBjork = Bjorklund (len (noteNums), 3)
#noteNumBjork.bjorklund ()
#noteNumBjork.rotate (0)
#noteNumIter = SkipIter (noteNumBjork.sequence, noteNums)
#for k in noteNumIter: print k

# TODO rotate key by progIter.next ()
#chordBjork = Bjorklund (len (keyIter2), noteNumIter.next ())
#chordBjork.bjorklund ()
#chordBjork.rotate (0)
#chordIter = SkipIter (chordBjork.sequence, keyIter2)
#for k in chordIter: print k







print "yes"
sleep (5)
exit



key = 7
mode = 0
chord = 0
chpattern = 3
chmode = 0
beats = 8
pulses = 5
bpmode = 0

phrase_pattern = 2
phrase_mode = 0

verse_pattern = 3
verse_mode = 0

song_pattern = 2
song_mode = 0

cycle_pattern = 1
cycle_mode = 0

"""print len (scale)

def random_permutation (iterable, r=None):
	"Random selection from itertools.permutations(iterable, r)"
	pool = tuple (iterable)
	r = len (pool) if r is None else r
	return tuple (random.sample (pool, r))

sample_rate = 44100
pygame.mixer.pre_init (sample_rate, -16, 1) # 44.1kHz, 16-bit signed, mono
pygame.init ()
length = int (round (500/4))
wait = int (round (1000/4))
for s in random_permutation (solfeggios ()):
	for c in scale:
		print "s=",s,"*","c=",c,"=",s * c
		fundy = fundamental (s * c, sine_wave)
		print "fundy=", fundy
		play_for (fundy, length)
		pygame.time.delay (wait)"""
		
cells = [
	Cell (scale, key, mode, chord, chpattern, chmode, beats, pulses, bpmode),
	Cell (scale, key, mode, chord, chpattern, chmode, beats, pulses, bpmode),
	Cell (scale, key, mode, chord, chpattern, chmode, beats, pulses, bpmode)
]
phrases = [
	Phrase (cells, phrase_pattern, phrase_mode),
	Phrase (cells, phrase_pattern, phrase_mode),
	Phrase (cells, phrase_pattern, phrase_mode),
	Phrase (cells, phrase_pattern, phrase_mode)
]
verses = [
	Verse (phrases, verse_pattern, verse_mode),
	Verse (phrases, verse_pattern, verse_mode),
	Verse (phrases, verse_pattern, verse_mode)
]
songs = [
	Song (verses, song_pattern, song_mode),
	Song (verses, song_pattern, song_mode)
]
cycle = SongCycle (songs, cycle_pattern, cycle_mode)


# select scale, i.e., 12 note
# select key, 1-12 euclidean subset
# select mode, rotate key... doesn't have the same effect with equal temperament
# select chord progression
# create melody within chord progression

#print sorted ([1] + list (harmonics5 (7)))
#display_scale ([1] + list (harmonics5 (7)))
"""
for k in xrange (2, 15):
	s = sorted ([1] + list (set (harmonics6 (k))))
	print len (s)
	display_scale (s)
	sleep (1)
"""
"""
for k in xrange (2, 15):
	s = sorted ([1] + list (set (harmonics6 (k))))
	#print len (s), [(i + 1) / i for i in xrange (2, k + 1)]
	for v in [4, 6, 8, 12, 20]:
		if v > k: continue
		b = Bjorklund (len (s), v)
		b.bjorklund ()
		display_bjorklund_scale (s, b.sequence)
		sleep (1)
"""

# TODO aspects, constraint solving, mpi, opencl

sleep (30)
exit








# hz
tempo = 1
ts_top = 4 # beats per measure
ts_bottom = 4 # quarter note = 1 beat
dot = 1.5

beats = []
beats["dotted whole note"] = ts_bottom * 4 * dot
beats["whole note"] = ts_bottom * 4
beats["dotted half note"] = ts_bottom * 2 * dot
beats["half note"] = ts_bottom * 2
beats["dotted quarter note"] = ts_bottom * dot
beats["quarter note"] = ts_bottom
beats["dotted eighth note"] = ts_bottom / 2 * dot
beats["eighth note"] = ts_bottom / 2
beats["half triplet"] = ts_bottom * 4 / 3
beats["dotted triplet"] = ts_bottom * 2 / 3 * dot
beats["triplet"] = ts_bottom * 2 / 3
beats["eighth triplet"] = ts_bottom / 3
beats["fivlet"] = ts_bottom * 2 / 5

def time_signature (top, bottom):
	# TODO
	return null












ranges_scale = [(rang, note)
	for rang in ranges for note in scale]
chakras_ranges = [(chakra, rang) for chakra in chakras for rang in ranges]
chakras_scale = [(chakra, note) for chakra in chakras for note in scale]

shuffle (ranges)
shuffle (chakras)
shuffle (scale)
shuffle (ranges_scale)
shuffle (chakras_ranges)
shuffle (chakras_scale)

"""ranges_1_chakras_1_scale_1 = [(rang, chakra, note) for rang in ranges for chakra in chakras for note in scale]
ranges_1_scale_1_chakras_1 = [(rang, chakra, note) for rang in ranges for note in scale for chakra in chakras]
chakras_1_ranges_1_scale_1 = [(rang, chakra, note) for chakra in chakras for rang in ranges for note in scale]
chakras_1_scale_1_ranges_1 = [(rang, chakra, note) for chakra in chakras for note in scale for rang in ranges]
scale_1_ranges_1_chakras_1 = [(rang, chakra, note) for note in scale for rang in ranges for chakra in chakras]
scale_1_chakras_1_ranges_1 = [(rang, chakra, note) for note in scale for chakra in chakras for rang in ranges]

ranges_1_chakras_scale_2 = [(rang, chakra, note) for rang in ranges for chakra, note in chakras_scale]
chakras_1_ranges_scale_2 = [(rang, chakra, note) for chakra in chakras for rang, note in ranges_scale]
scale_1_chakras_ranges_2 = [(rang, chakra, note) for note in scale 	for chakra, rang in chakras_ranges]
chakras_scale_2_ranges_1 = [(rang, chakra, note) for chakra, note in chakras_scale for rang in ranges]
ranges_scale_2_chakras_1 = [(rang, chakra, note) for rang, note in ranges_scale for chakra in chakras]
chakras_ranges_2_scale_1 = [(rang, chakra, note) for chakra, rang in chakras_ranges for note in scale]

movements = [
	ranges_1_chakras_1_scale_1, ranges_1_scale_1_chakras_1,
	chakras_1_ranges_1_scale_1, chakras_1_scale_1_ranges_1,
	scale_1_ranges_1_chakras_1, scale_1_chakras_1_ranges_1,

	ranges_1_chakras_scale_2, chakras_1_ranges_scale_2, scale_1_chakras_ranges_2,
	chakras_scale_2_ranges_1, ranges_scale_2_chakras_1, chakras_ranges_2_scale_1]
shuffle (movements)"""

scale_melody = melody (scale)
chakras_melody = melody (chakras)
ranges_melody = melody (ranges)
chakras_scale_melody = melody (chakras_scale)
ranges_scale_melody = melody (ranges_scale)
chakras_ranges_melody = melody (chakras_ranges)

ranges_1_chakras_1_scale_1_melody = [(rang, chakra, note) for rang in ranges_melody for chakra in chakras_melody for note in scale_melody]
ranges_1_scale_1_chakras_1_melody = [(rang, chakra, note) for rang in ranges_melody for note in scale_melody for chakra in chakras_melody]
chakras_1_ranges_1_scale_1_melody = [(rang, chakra, note) for chakra in chakras_melody for rang in ranges_melody for note in scale_melody]
chakras_1_scale_1_ranges_1_melody = [(rang, chakra, note) for chakra in chakras_melody for note in scale_melody for rang in ranges_melody]
scale_1_ranges_1_chakras_1_melody = [(rang, chakra, note) for note in scale_melody for rang in ranges_melody for chakra in chakras_melody]
scale_1_chakras_1_ranges_1_melody = [(rang, chakra, note) for note in scale_melody for chakra in chakras_melody for rang in ranges_melody]

ranges_1_chakras_scale_2_melody = [(rang, chakra, note) for rang in ranges_melody for chakra, note in chakras_scale_melody]
chakras_1_ranges_scale_2_melody = [(rang, chakra, note) for chakra in chakras_melody for rang, note in ranges_scale_melody]
scale_1_chakras_ranges_2_melody = [(rang, chakra, note) for note in scale_melody 	for chakra, rang in chakras_ranges_melody]
chakras_scale_2_ranges_1_melody = [(rang, chakra, note) for chakra, note in chakras_scale_melody for rang in ranges_melody]
ranges_scale_2_chakras_1_melody = [(rang, chakra, note) for rang, note in ranges_scale_melody for chakra in chakras_melody]
chakras_ranges_2_scale_1_melody = [(rang, chakra, note) for chakra, rang in chakras_ranges_melody for note in scale_melody]

movements_melody = [
	ranges_1_chakras_1_scale_1_melody, ranges_1_scale_1_chakras_1_melody,
	chakras_1_ranges_1_scale_1_melody, chakras_1_scale_1_ranges_1_melody,
	scale_1_ranges_1_chakras_1_melody, scale_1_chakras_1_ranges_1_melody,

	ranges_1_chakras_scale_2_melody, chakras_1_ranges_scale_2_melody, scale_1_chakras_ranges_2_melody,
	chakras_scale_2_ranges_1_melody, ranges_scale_2_chakras_1_melody, chakras_ranges_2_scale_1_melody]
shuffle (movements_melody)

"""for movement in movements:
	for rang, chakra, note in movement:
		print play (chrang (chakra, rang), note), " 1"
"""
for movement in movements_melody:
	for rang, chakra, note in movement:
		print play (chrang (chakra, rang), note), " 1"