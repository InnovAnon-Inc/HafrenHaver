


ratios_db = [
	[],
]

ratios = ratios_db[0]

def pitch (ratios, index, octave): return ratios[index] * Math.pow (2, octave)

key = 0

def keyPitch (ratios, index, octave, key):
	index  = index + key
	octave = index // len (ratios) + octave
	index  = index %  len (ratios)
	return pitch (ratios, index, octave)

tetrachords_db = [
	[],
]

lower_tetrachord = tetrachords_db[0]
upper_tetrachord = tetrachords_db[0]

scale = make_scale (lower_tetrachord, upper_tetrachord)

def scalePitch (ratios, index, octave, key, scale):
	index  = scale[index]
	octave = index // len (scale) + octave
	return keyPitch (ratios, index, octave, key)

mode = 0

def modePitch (ratios, index, octave, key, scale, mode):
	index  = index + mode
	octave = index // len (scale) + octave
	index  = index %  len (scale)
	return scalePitch (ratios, index, octave, key, scale)

chords_db = [
	[],
]

chord_progression_db = [
	[],
]

modulation_db = [
	[],
]



intervals_db = {
	# semitones, scale degree
	( 0, 0): "P1",
	( 1, 0): "A1",
	( 0, 1): "d2",
	( 1, 1): "m2",
	( 2, 1): "M2",
	( 3, 1): "A2",
	( 2, 2): "d3",
	( 3, 2): "m3",
	( 4, 2): "M3",
	( 5, 2): "A3",
	( 4, 3): "d4",
	( 5, 3): "P4",
	( 6, 3): "A4",
	( 6, 4): "d5",
	( 7, 4): "P5",
	( 8, 4): "A5",
	( 7, 5): "d6",
	( 8, 5): "m6",
	( 9, 5): "M6",
	(10, 5): "A6",
	( 9, 6): "d7",
	(10, 6): "m7",
	(11, 6): "M7",
	(12, 6): "A7",
	(11, 7): "d8",
	(12, 7): "P8",
}




def darken_key    (key, octave, ratios):
	key    = key - (len (ratios) // 2 - 1)
	if key < 0: octave = octave - 1
	key    = key % len (ratios)
	return (key, octave)
def brighten_key  (key, octave, ratios):
	key    = key + (len (ratios) // 2 + 1)
	octave = key // len (ratios) + octave
	key    = key %  len (ratios)
	return (key, octave)
def darken_mode   (key, octave, ratios, scale, mode):
	if mode == len (scale) - 1:
		key    = key - 1
		if key < 0: octave = octave - 1
		key    = key % len (ratios)
	mode   = mode - (len (scale) // 2)
	if mode < 0: octave = octave - 1
	mode   = mode % len (scale)
	return (key, octave, mode)
def brighten_mode (key, octave, ratios, scale, mode):
	if mode == len (scale) // 2:
		key    = key + 1
		octave = key // len (ratios) + octave
		key    = key %  len (ratios)
	mode   = mode + (len (scale) // 2)
	octave = mode // len (scale) + octave
	mode   = mode % len (scale)
	return (key, octave, mode)

# TODO generate chord progression and/or modulation sequence
# TODO get meter
# TODO poetic feet
# TODO rhythms... 1 note, 1/2 note, 1/4 note, 1/8 note
# TODO CT-NCT, CT-NCT-NCT... accented vs unaccented
# TODO generate motif
# TODO get repetition pattern
