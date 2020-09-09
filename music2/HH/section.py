#! /usr/bin/env python

#from numba  import jit
from random import choice, shuffle

from bar     import random_bar
from phrase  import random_phrase
from segment import random_segment_order

sections_db = [
	[0],
	
	[0, 0],
	[0, 1],
	
	[0, 0],
	[0, 1],
	
	[0, 0, 0],
	[0, 0, 1],
	[0, 1, 0],
	[0, 1, 1],
]
#@jit
class Section:
	def __init__ (self, phrases):
		self.phrases = phrases
		self.uniq    = list (set (phrases))
def random_section (nsection):
	if nsection == 1: phrase = sections_db[0]
	else:             phrase = choice (sections_db[1:])
	return Section (phrase)
def apply_section (section):
	nphrase = section.uniq[-1] + 1
	#print ("nphrase=%s" % nphrase, end="\n")
	#phrases = []
	#for phrase_no in range (0, nphrase):
	#	phrases[phrase_no] = random_phrase ()
	phrases = [random_phrase (nphrase) for _ in range (0, nphrase)]
	#print ("phrases=%s" % phrases, end="\n")
		
	#nsegment = 0
	#for phrase in phrases:
	#	nsegment = nsegment + 1 + phrase.segments[-1]
	nsegment = nphrase + sum ((phrase.uniq[-1] for phrase in phrases))
	#print ("nsegment=%s" % nsegment, end="\n")
	
	tot = 0
	for phrase_no in section.phrases:
		phrase = phrases[phrase_no]
		tot = tot + len (phrase.segments)
		
	#segments = []
	#for segment_no in range (0, nsegment):
	#	segments[segment_no] = random_segment ()
	segments = [random_segment_order (tot) for _ in range (0, nsegment)]
	#print ("segments=%s" % segments, end="\n")
	
	#nbar = 0
	#for segment in segments:
	#	nbar =  nbar + 1 + segment.bars[-1]
	nbar = nsegment + sum ((segment.uniq[-1] for segment in segments))
	#print ("nbar=%s" % nbar, end="\n")

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
	bars = [random_bar (tot, len (section.phrases)) for _ in range (0, nbar)]
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
