#! /usr/bin/env python3

#from numba  import jit
from random import choice

# by bar (horizontal):
# a b a c
# or (vertical)
# a  b  c  d
# a  e  c  g
# or (both)
# a  b  a  c
# a  d  a  e

# by segment (horizontal):
# a b a b
# or (vertical)
# a b c d
# a b e f
# or (both)
# a b c a b
# a b d a b

# by phrase:
# a b c d
# a b c d

# by segment 2:
# a a b a b
# a b c a b

# a b a a b
# a b c a b

# a b a b b
# a b c a b
# a b a b c

# by segment 2 (horizontal)
# a a b a b

# a b a b c

# a b c a b

# [[3, 3], [3, 4]]
# [[3, 3], [3, 4]]
# [[3, 3], [3, 1, 1, 2]]

# (a a) (a b) => vary seg0, repeat seg00, vary seg01
# (a a) (a c c d) => repeat seg0, vary seg1, repeat seg10, split seg11

phrases_db = [
	[0],
	[0],
	[0],
	[0],
	
	[0, 0],
	[0, 1],
	[0, 0],
	[0, 1],
	
	[0, 0, 0],
	[0, 0, 1],
	[0, 1, 1],
	[0, 1, 2],
	
	#[0, 1, 1, 2],
	#[0, 0, 0, 1],
	#[0, 0, 1, 2],
	#[0, 1, 0, 1],
	#[0, 1, 0, 2],
	#[0, 1, 2, 2],
]
#@jit
class Phrase:
	def __init__ (self, segments):
		self.segments = segments
		self.uniq     = list (set (segments))

def random_phrase (nphrase):
	if   nphrase <= 2: segments = choice (phrases_db[4:])
	else:              segments = choice (phrases_db[:8])
	return Phrase (segments)
	
def apply_phrase (section):
	nphrase = section.uniq[-1] + 1
	#print ("nphrase=%s" % nphrase, end="\n")
	#phrases = []
	#for phrase_no in range (0, nphrase):
	#	phrases[phrase_no] = random_phrase ()
	phrases = [random_phrase (nphrase) for _ in range (0, nphrase)]
	#print ("phrases=%s" % phrases, end="\n")
	
	tot = 0
	for phrase_no in section.phrases:
		phrase = phrases[phrase_no]
		tot = tot + len (phrase.segments)
		
	segments = apply_segment (section, nphrase, phrases, tot)
	
	tot = 0
	for phrase_no in section.phrases:
		phrase = phrases[phrase_no]
		for segment_no in phrase.segments:
			segment = segments[segment_no]
			tot = tot + len (segment.bars)
	#print ("tot=%s" % tot, end="\n")
		
	#bars = []
	#for bar_no in range (0, nbar):
	#	bars[bar_no] = random_bar ()
	#bars = [random_bar (len (section.phrases) * nbar) for _ in range (0, nbar)]
	bars = [random_bar (tot) for _ in range (0, nbar)]
	#print ("bars=%s" % bars, end="\n")
	
	mappings1 = []
	segno     = 0
	seg_ndx   = list (range (0, nsegment))
	shuffle (seg_ndx)
	#print ("seg_ndx=%s" % seg_ndx, end="\n")
	
	for phrase_no in range (0, len (phrases)):
		phrase   = phrases[phrase_no]
		nsegment = phrase.uniq[-1] + 1
		temp = []
		for segment_no in range (0, nsegment):
			temp = temp + [seg_ndx[segno]]
			segno = segno + 1
		mappings1 = mappings1 + [temp]
	
	mappings2 = []
	barno     = 0
	bar_ndx   = list (range (0, nbar))
	shuffle (bar_ndx)
	#print ("bar_ndx=%s" % bar_ndx, end="\n")
	
	for seg_no in range (0, len (segments)):
		segment =  segments[seg_no]
		nbar = segment.uniq[-1] + 1
		temp = []
		for bar_no in range (0, nbar):
			temp = temp + [bar_ndx[barno]]
			barno = barno + 1
		mappings2 = mappings2 + [temp]
		
	return phrases, segments, bars, mappings1, mappings2

