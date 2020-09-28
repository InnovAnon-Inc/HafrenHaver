"""InnovAnon Inc. Proprietary"""

class Ranges:
	"""https://en.wikipedia.org/wiki/Visible_spectrum"""
	#visible_light = (430, 770) THz.
	
	"""http://www.physlink.com/Education/AskExperts/ae2.cfm"""
	colors = {
		("red" => (780, 622)), # nm
		("orange" => (622, 597)), # nm
		("yellow" => (597, 577)), # nm
		("green" =>	(577, 492)), # nm
		("blue" => (492, 455)), # nm
		("violet" => (455, 390)) # nm
	}
	
	"""https://en.wikipedia.org/wiki/Audio_frequency"""
	audible_sound = (20, 20000)
	
	"""https://en.wikipedia.org/wiki/Binaural_beats"""
	binaural_sound = (20, 1500)
	binaural_diff = (0, 40)