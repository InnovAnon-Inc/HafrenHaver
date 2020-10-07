#! /usr/bin/env python3

#from numba  import jit
from random import choice

segments_db = [
	[0],
	
	[0, 0],
	[0, 1],
	[0, 0],
	[0, 1],
	
	[0, 0, 0],
	[0, 0, 1],
	[0, 1, 1],
	[0, 1, 2],
	
	[0, 1, 1, 2],
	[0, 0, 0, 1],
	[0, 0, 1, 2],
	[0, 1, 0, 1],
	[0, 1, 0, 2],
	[0, 1, 2, 2],
]
#@jit
class SegmentOrder:
	def __init__ (self, bars):
		self.bars = bars
		self.uniq = list (set (bars))
def random_segment_order (nsegment):
	# 2-4-9
	# 4-2-1
	if   nsegment >  9: bars = segments_db[0]
	elif nsegment <= 3: bars = choice (segments_db[5:])
	else:               bars = choice (segments_db[1:5])
	return SegmentOrder (bars)
	
class Segment:
	@staticmethod
	def init_map_1 (phrases, nsegment, seg_ndx):
		mappings1 = []
		segno     = 0
		for phrase_no in range (0, len (phrases)):
			phrase   = phrases[phrase_no]
			nsegment = phrase.uniq[-1] + 1
			temp = []
			for segment_no in range (0, nsegment):
				temp = temp + [seg_ndx[segno]]
				segno = segno + 1
			mappings1 = mappings1 + [temp]
	@staticmethod
	def init_map_2 (segments, nbar, bar_ndx):
		mappings2 = []
		barno     = 0
		for seg_no in range (0, len (segments)):
			segment =  segments[seg_no]
			nbar = segment.uniq[-1] + 1
			temp = []
			for bar_no in range (0, nbar):
				temp = temp + [bar_ndx[barno]]
				barno = barno + 1
			mappings2 = mappings2 + [temp]
	def __init__ (self, phrases, segments, nsegment, seg_ndx, bars, nbar, bar_ndx):
		self.phrases  = phrases
		self.segments = segments
		self.bars     = bars
		self.map1     = Segment.init_map_1 (phrases, nsegment, seg_ndx)
		self.map2     = Segment.init_map_2 (segments, nbar, bar_ndx)
def random_segment (section, phrases, segments=None, seg_ndx=None, bars=None, bar_ndx=None):
	nphrase = len (phrases)
	nsegment = nphrase + sum ((phrase.uniq[-1] for phrase in phrases))
	
	if not segments:
		tot = 0
		for phrase_no in section.phrases:
			phrase = phrases[phrase_no]
			tot = tot + len (phrase.segments)
			
		segments = [random_segment_order (tot) for _ in range (0, nsegment)]
		
	nbar = nsegment + sum ((segment.uniq[-1] for segment in segments))
	
	if not bars:	
		tot = 0
		for phrase_no in section.phrases:
			phrase = phrases[phrase_no]
			for segment_no in phrase.segments:
				segment = segments[segment_no]
				tot = tot + len (segment.bars)
		bars = [random_bar (tot) for _ in range (0, nbar)]
	
	if not seg_ndx:
		seg_ndx = list (range (0, nsegment))
		shuffle (seg_ndx)	
	if not bar_ndx:
		bar_ndx = list (range (0, nbar))
		shuffle (bar_ndx)
	
	return Segment (section, phrases, segments, nsegment, seg_ndx, bars, nbar, bar_ndx)
	
"""
def apply_segment (section, phrases):
	nphrase = len (phrases)
	nsegment = nphrase + sum ((phrase.uniq[-1] for phrase in phrases))
	
	tot = 0
	for phrase_no in section.phrases:
		phrase = phrases[phrase_no]
		tot = tot + len (phrase.segments)
		
	segments = [random_segment (tot) for _ in range (0, nsegment)]
	
	nbar = nsegment + sum ((segment.uniq[-1] for segment in segments))

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
"""
