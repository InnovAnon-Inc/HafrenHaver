"""

from numba import jit

def frequency (ratios, index, octave):
    return ratios[index] * Math.pow (2, octave)

ratios = {
    P1: 1/1,
    d2:
    m2:
    M2:
}
key    = 0

intervals = {
    0:  [P1, d2],
    1:  [A1, m2],
    2:  [M2, d3],
    3:  [A2, m3],
    4:  [M3, d4],
    5:  [A3, P4],
    6:  [A4, TT, d5],
    7:  [P5, d6],
    8:  [A5, m6],
    9:  [M6, d7],
    10: [A6, m7],
    11: [M7, d8],
    12: [A7, P8],
}

def intervalToRatio (key, interval):
    ratios[interval - key]
    # TODO
    pass


def degreeToInterval (degree):
    scale[mode + degree]
    # TODO
    pass

scale = [P1, M2, M3, P4, P5, M6, M7]

mode = ???
"""

P1 =  0
P4 =  1
P5 =  2
P8 =  3

d2 =  4
d3 =  5
d4 =  6
d5 =  7
d6 =  8
d7 =  9
d8 = 10

A1 = 11
A2 = 12
A3 = 13
A4 = 14
A5 = 15
A6 = 16
A7 = 17

m2 = 18
M2 = 19
m3 = 20
M3 = 21
m6 = 22
M6 = 23
m7 = 24
M7 = 25

# key = 0  P1    m2   M2    m3   M3   P4    A4    d5   P5    m6   M6    m7   M7
# key = 1  M7    P1   m2    M2   m3   M3    P4    A4   d5    P5   m6    M6   m7
# key = 2  m7    M7   P1    m2   M2   m3    M3    d4   P4 A4/d5   P5    m6   M6
# key = 3  M6    m7   M7    P1   m2   M2    m3    m3              d5    P5   m6
# key = 4  m6    M6   m7    M7   P1   m2    M2    M2   m3    M3   P4 A4/d5   P5
#           0     1    2     3    4    5     6     7    8     9   10    11   12
ratios = ["C", "C#", "D", "D#", "E", "F", "F#", "Gb", "G", "G#", "A", "A#", "B"]
intervals = {
    P1:  0, d2:  0,
    A1:  1, m2:  1,
    M2:  2, d3:  2,
    A2:  3, m3:  3,
    M3:  4, d4:  4,
    A3:  5, P4:  5,
    A4:  6, d5:  7,
    P5:  8, d6:  8,
    A5:  9, m6:  9,
    M6: 10, d7: 10,
    A6: 11, m7: 11,
    M7: 12, d8: 12,
    A7: 13, P8: 13,
}
def ratio (interval, key):
    index = intervals[interval]
    index = index + key
    index = index % len (ratios)
    return ratios[index]

for key in range(0, len (ratios)):
    print ("key=%s" % key, end="\n")
    for interval in [P1, M2, M3, P4, P5, M6, M7]:
        print ("%2s" % ratio (interval, key), end=" ")
    print (end="\n")



def intervals (scale, mode):
    previous = 0
    for degree in range (0, len (scale)):
        current = scale[mode + degree]
        if previous == current: yield P1
        else:










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
