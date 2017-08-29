from __future__ import division
from Util import *

class Solfeggio:
	@staticmethod
	def solfeggios ():
		for seq in [
			[1, 4, 7],
			[5, 2, 8],
			[3, 6, 9]]:
			for perm in permutations (seq):
				yield list_to_number (perm)
	@staticmethod
	def chrang (chakra, rang):
		return solfeggio[rang, chakra]
	ranges = ["low", "med", "hi"]
	chakras = ["red", "orange", "yellow", "green", "blue", "purple"]

	solfeggio = {}
	solfeggio["low", "red"] = 174
	solfeggio["low", "orange"] = 147
	solfeggio["low", "yellow"] = 285
	solfeggio["low", "green"] = 369
	solfeggio["low", "blue"] = 396
	solfeggio["low", "purple"] = 258
	solfeggio["med", "red"] = 417
	solfeggio["med", "orange"] = 471
	solfeggio["med", "yellow"] = 528
	solfeggio["med", "green"] = 693
	solfeggio["med", "blue"] = 639
	solfeggio["med", "purple"] = 582
	solfeggio["hi", "red"] = 741
	solfeggio["hi", "orange"] = 714
	solfeggio["hi", "yellow"] = 852
	solfeggio["hi", "green"] = 936
	solfeggio["hi", "blue"] = 963
	solfeggio["hi", "purple"] = 825