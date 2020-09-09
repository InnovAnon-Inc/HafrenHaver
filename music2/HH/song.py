#! /usr/bin/env python

#from numba  import jit
from random import choice

from section import apply_section, random_section

songs_db = [
	# pop song structures
	   [0, 0,    1, 0,    1, 2, 1],             #   V1 V2   C V3   C B C          0
	[3, 0, 0,    1, 0,    1, 2, 1],             # I V1 V2   C V3   C B C          1
	   [0, 0,    1, 0,    1, 2, 1, 4],          #   V1 V2   C V3   C B C O        2
	[3, 0, 0,    1, 0,    1, 2, 1, 4],          # I V1 V2   C V3   C B C O        3
	   [0, 0, 5, 1, 0, 5, 1, 2, 1],             #   V1 V2 P C V3 P C B C          4
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1],             # I V1 V2 P C V3 P C B C          5
	   [0, 0, 5, 1, 0, 5, 1, 2, 1, 4],          #   V1 V2 P C V3 P C B C O        6
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1, 4],          # I V1 V2 P C V3 P C B C O        7
	
	   [0, 0,    1, 0,    1, 2, 1, 2, 1],       #   V1 V2   C B C V3   C B C      8
	   [0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1],       #                                 9
	[3, 0, 0,    1, 0,    1, 2, 1, 2, 1],       #                                10
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1],       #                                11
	   [0, 0,    1, 0,    1, 2, 1, 2, 1, 4],    #                                12
	   [0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1, 4],    #                                13
	[3, 0, 0,    1, 0,    1, 2, 1, 2, 1, 4],    #                                14
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1, 4],    #                                15
	   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1],    #   V1 V2   C B C V3   C B C C   16
	   [0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1, 1],    #                                17
	[3, 0, 0,    1, 0,    1, 2, 1, 2, 1, 1],    #                                18
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1, 1],    #                                19
	   [0, 0,    1, 0,    1, 2, 1, 2, 1, 1, 4], #                                20
	   [0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1, 1, 4], #                                21
	[3, 0, 0,    1, 0,    1, 2, 1, 2, 1, 1, 4], #                                22
	[3, 0, 0, 5, 1, 0, 5, 1, 2, 1, 2, 1, 1, 4], #                                23

	# TODO I O P for ^^^
	# folk song structures
	   [0, 1,    0, 1,    0, 1, 0, 1],          #                                24
	   [0, 1,    0, 1,    0, 1, 1],             #                                25

	[   0,    1, 0,    1, 2, 1, 0,    1],       #                                26
	[   0, 5, 1, 0, 5, 1, 2, 1, 0, 5, 1],       #                                27
	[3, 0,    1, 0,    1, 2, 1, 0,    1],       #                                28
	[3, 0, 5, 1, 0, 5, 1, 2, 1, 0, 5, 1],       #                                29
	[   0,    1, 0,    1, 2, 1, 0,    1, 4],    #                                30
	[   0, 5, 1, 0, 5, 1, 2, 1, 0, 5, 1, 4],    #                                31
	[3, 0,    1, 0,    1, 2, 1, 0,    1, 4],    #                                32
	[3, 0, 5, 1, 0, 5, 1, 2, 1, 0, 5, 1, 4],    #                                33
]

#@jit
class SongStructure:
	def __init__ (self, sections):
		self.sections = sections
		#self.uniq = []
		#for section in sections:
		#	if section in self.uniq: continue
		#	self.uniq = self.uniq + [section]
def random_song_structure ():
	sections = choice (songs_db)
	return SongStructure (sections)

class Song:
	@staticmethod
	def init_map (sections, song_structure):
		section_ret = []
		for section in sections:
			phrases, segments, bars, mappings1, mappings2 = apply_section (section)
			phrase_ret = []
			for phrase_no in section.phrases:
				phrase = phrases[phrase_no]
				segment_ret = []
				for segment_no in phrase.segments:
					segno = mappings1[phrase_no][segment_no]
					segment = segments[segno]
					bar_ret = []
					for bar_no in segment.bars:
						barno = mappings2[segno][bar_no]
						bar = bars[barno]
						bar_ret = bar_ret + [bar]
					segment_ret = segment_ret + [bar_ret]
				phrase_ret = phrase_ret + [segment_ret]
			section_ret = section_ret + [phrase_ret]
		return [(section, section_ret[section]) for section in song_structure.sections]
	def __init__ (self, sections, song_structure):
		self.sections       = sections
		self.song_structure = song_structure
		self.map            = Song.init_map (sections, song_structure)
def random_song (song_structure=None, sections=None, long_sections=None, short_sections=None):
	if not song_structure: song_structure = random_song_structure ()
	if not sections:
		if not long_sections: long_sections = [random_section (2) for _ in range (0, 3)]
		if not short_sections:
			#min_bar = min (bar.nbeat for phrase in long_sections for segment in phrase.segments for bar in segment.bars)
			#max_bar = max (bar.nbeat for phrase in long_sections for segment in phrase.segments for bar in segment.bars)
			#short_sections = [random_section (1, min_bar, max_bar) for _ in range (0, 3)]
			short_sections = [random_section (1) for _ in range (0, 3)]
		sections = long_sections + short_sections
	return Song (sections, song_structure)

if __name__ == "__main__":
	#for song1 in range (0, len (songs_db)):
	#	for song2 in range (song1 + 1, len (songs_db)):
	#		if songs_db[song1] == songs_db[song2]:
	#			print (song1)
	#			print (song2)
	#			raise Exception ()
	
	#song1 = random_song ()
	#song2 = apply_song (song1)
	song1 = random_song ()
	song2 = song1.map
	for section_type, section in song2:
		if   section_type == 0: section_type = "verse"
		elif section_type == 1: section_type = "chorus"
		elif section_type == 2: section_type = "bridge"
		elif section_type == 3: section_type = "intro"
		elif section_type == 4: section_type = "outro"
		elif section_type == 5: section_type = "pre"
		print (section_type, end="\n")
		for phrase in section:
			for segment in phrase:
				for bar in segment:
					print ("%1s" % bar.nbeat, end=" ")
				print (end="    ")
			print (end="\n")
		print (end="\n")
	print (end="\n")
	
	##verse  = random_section (2)
	##chorus = random_section (2)
	##bridge = random_section (2)
	##sections = [verse, verse, chorus, verse, chorus, bridge, chorus]
	##for section in sections:
	#for section in song2:
	#	phrases, segments, bars, mappings1, mappings2 = apply_section (section)
	#	#print ("phrases=%s"   % phrases,   end="\n")
	#	#print ("segments=%s"  % segments,  end="\n")
	#	#print ("bars=%s"      % bars,      end="\n")
	#	#print ("mappings1=%s" % mappings1, end="\n")
	#	#print ("mappings2=%s" % mappings2, end="\n")
	#	for phrase_no in section.phrases:
	#		phrase = phrases[phrase_no]
	#		for segment_no in phrase.segments:
	#			#print ("phrase_no=%s, segment_no=%s" % (phrase_no, segment_no), end="\n")
	#			segno = mappings1[phrase_no][segment_no]
	#			segment = segments[segno]
	#			for bar_no in segment.bars:
	#				#print ("segno=%s, bar_no=%s" % (segno, bar_no), end="\n")
	#				barno = mappings2[segno][bar_no]
	#				bar = bars[barno]
	#				print ("%s" % bar.nbeat, end=" ")
	#			print (end="   ")
	#		print (end="\n")
	#	print (end="\n")
