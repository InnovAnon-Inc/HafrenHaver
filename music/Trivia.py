from __future__ import division

class Trivia:
	audible_range = (20, 20000)
	binaural_range = (20, 1500)
	binaural_diff = (0, 40)

	tempo = {}
	tempo["larghissimo"] = (0, 24) # 1 ?
	tempo["grave"] = (25, 45)
	tempo["largo"] = (40, 60)
	tempo["lento"] = (45, 60)
	tempo["larghetto"] = (60, 66)
	tempo["adagio"] = (66, 76)
	tempo["adagietto"] = (72, 76)
	tempo["andante"] = (76, 108)
	tempo["andantino"] = (80, 108)
	tempo["marcia moderato"] = (83, 85)
	tempo["andante moderato"] = (92, 112)
	tempo["moderato"] = (102, 120)
	tempo["allegretto"] = (112, 120)
	tempo["allegro moderato"] = (116, 120)
	tempo["allegro"] = (120, 168)
	tempo["vivace"] = (168, 176)
	tempo["vivacissimo"] = (172, 176)
	tempo["allegrissimo"] = (172, 176)
	tempo["allegro vivace"] = (172, 176)
	tempo["presto"] = (168, 200)
	reasonable_max_tempo = 380
	tempo["prestissimo"] = (200, reasonable_max_tempo)

	# when notes are long enough to play offset notes or frequencies:
	brainwaves = {}
	brainwaves["gamma"] = (30, 50) # (40, 100)
	brainwaves["beta"] = (14, 30) # (12, 40)
	brainwaves["smr"] = (12.5, 15.5)
	brainwaves["alpha"] = (8, 14) # (8, 12)
	brainwaves["sigma"] = (12, 14)
	brainwaves["mu"] = (8, 12)
	brainwaves["theta"] = (4, 8) # (4, 8)
	brainwaves["delta"] = (.1, 4) # (1, 4)
	brainwaves["epsilon"] = (0, .1) # (0, 1)