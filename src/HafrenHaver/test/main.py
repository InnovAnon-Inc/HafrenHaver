#! /usr/bin/env python3

from chroma      import random_limit, random_chromatic, random_base_frequency

limit  = random_limit()
chroma = random_chromatic(limit)



from key         import random_key

key    = random_key(chroma)



from interpolate import BrainWave, Tempo, interpolate, tempo1, AUDIBLE, REFRESH, color, wavelength_to_rgb
from random      import choice

brain1  = choice((BrainWave.LAMBDA, BrainWave.GAMMA, BrainWave.BETA,))                     #    audible drone
brain2  = choice((BrainWave.ALPHA,  BrainWave.THETA, BrainWave.DELTA, BrainWave.EPSILON,)) # subaudible drone + occasional fast notes in high register
brain1  = brain1.value
brain2  = brain2.value

basef = random_base_frequency()

brains1 = interpolate(basef, key, brain1)
assert len(brains1) > 0
brains2 = interpolate(basef, key, brain2)
assert len(brains2) > 0
tempos  = interpolate(basef, key, tempo1) 
assert len(tempos)  > 0
audible = interpolate(basef, key, AUDIBLE)
assert len(audible) > 0
# TODO expand audible range
refresh = interpolate(basef, key, REFRESH)
assert len(refresh) > 0
colors  = interpolate(basef, key, color)
assert len(colors)  > 0

print("brains1:  %s" % (brains1,))
print("brains2:  %s" % (brains2,))
print("tempos:   %s" % (tempos,))
print("audible:  %s" % (audible,))
print("refresh:  %s" % (refresh,))
print("colors:   %s" % (colors,))





























from variances import random_variances, VarianceType

variances           = random_variances()

harmonic_variance   = variances[VarianceType.HARMONIC]
modulation_variance = variances[VarianceType.MODULATION]
borrow_variance     = variances[VarianceType.BORROW]
accent_variance     = variances[VarianceType.ACCENT]
dynamics_variance   = variances[VarianceType.DYNAMICS]
meter_variance      = variances[VarianceType.METER]
tempo_variance      = variances[VarianceType.TEMPO]

print("harmonic_variance  : %s" % (harmonic_variance,))
print("modulation_variance: %s" % (modulation_variance,))
print("borrow_variance    : %s" % (borrow_variance,))
print("accent_variance    : %s" % (accent_variance,))
print("dynamics_variance  : %s" % (dynamics_variance,))
print("meter_variance     : %s" % (meter_variance,))
print("tempo_variance     : %s" % (tempo_variance,))



from structure import random_songstructure

songstruct          = random_songstructure()
print("songstruct: %s" % (songstruct,))

class Song: # map sections
    def __init__(self, songstruct):
        self.songstruct = songstruct
        

class Meter(Song):
    def __init__(self):
        pass




"""
sections = {}
for section in songstruct:
    if section in sections: continue
    s = Section()
    sections[section] = s
"""




from scale import random_scale

scale  = random_scale(key)
ratios = tuple((scale[i] for i in range(0, len(scale))))
print("ratios: %s" % (ratios,))



"""
def get_section_mapping(songstruct, random_section):
    nsection = len(set(songstruct))
    nuniq    = randrange(nsection)
    # TODO short sections and long sections
    sections = (random_section() for section in range(nuniq))
    mapping  = {}
    for section in songstruct:
        if section in mapping: continue
        mapping[section] = sections.next()
    assert sections is empty
    return mapping
#    
#def get_phrase_mapping(songstruct):
#    # TODO
#def get_measure_mapping(songstruct):
#    # TODO
#def get_beat_mapping(songstruct):
#    # TODO

# TODO meter & measures
if   meter_variance == VarianceType.SONG:
    # TODO pick one scale degree / meter
    meter = choice((2, 3, 4))
elif meter_variance == VarianceType.SECTION:
    # TODO pick variances by section
    # TODO get uniq section types, reduce variety
    # same measure length for whole section, may vary by section
    # or same measure length pattern for whole section, varies between sections
    motif    = get_section_mapping(songstruct, lambda: choice((2, 3, 4)))
    #meter    = choice((2, 3, 4))
    
elif meter_variance == VarianceType.PHRASE: # ~16 beats
    # TODO pick variances by phrase
    # TODO get uniq section types, reduce variety
    # same measure length for whole phrase, may vary by phrase
    # or same measure length pattern for whole phrase, varies between phrases
elif meter_variance == VarianceType.MEASURE:
    # TODO pick variances by measure
    # TODO get uniq section types, reduce variety
    # varies by measure ?
    # or measure length pattern by phrase?
    meter = choice((1, 2, 3, 4))







"""



# TODO tempo

# TODO harmonic (chord cadences)
# TODO modulations
# TODO borrowed chords

# TODO accent (bjorklund)
# TODO dynamics

# number of chord changes, number of modulations, number of borrowed chords
# consonance cadence, brightness cadence
# TODO meter, accents, rhythms

# 

# TODO count uniq song sections, decide # different verse structures

# dynamics
# 1: per section
# 2: per phrase
# 3: within phrases

# mode/key changes
# 1: none
# 2: per section
# 3: per phrase
# 4: within phrases

# tempo modulations
# 1-4

# t-s-d harmonic cadence
# 1-4

# secondary/borrowed cadence & chords

# bjorklund accent patterns
# 1-4

# rhythm cadence & rhythms
# whole, half, quarter, eighth, sixteenth, triplets


# ct-nct cadence

# chords
# melody
# countermelodies







#from numba  import jit

import pygame
from pygame.locals import *

import math
from math import log

from datetime import datetime

#brains1 = [basef * 2**octave * scale[index] for index, octave in brains1]
#brains2 = [basef * 2**octave * scale[index] for index, octave in brains2]
#tempos = [basef * 2**octave * scale[index] for index, octave in tempos]
#audible = [basef * 2**octave * scale[index] for index, octave in audible]
#refresh = [basef * 2**octave * scale[index] for index, octave in refresh]
#colors = [basef * 2**octave * scale[index] for index, octave in colors]
brains1 = [basef * 2**octave * scale.chroma[index] for index, octave in brains1]
brains2 = [basef * 2**octave * scale.chroma[index] for index, octave in brains2]
tempos = [basef * 2**octave * scale.chroma[index] for index, octave in tempos]
audible = [basef * 2**octave * scale.chroma[index] for index, octave in audible]
refresh = [basef * 2**octave * scale.chroma[index] for index, octave in refresh]
colors = [basef * 2**octave * scale.chroma[index] for index, octave in colors]

c      = 2.99792458 * 10**17
colors2 = [wavelength_to_rgb(c / color) for color in colors]

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
	return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
colors2 = '\n'.join((get_color_escape(*color) + str(color) + RESET for color in colors2))
print("colors2:   %s" % (colors2,))

pitch1  = choice(brains1)
pitch2  = choice(brains2)
#pitch3  = choice(tempos) / 60
pitch3  = choice(tempos)
# TODO
#pitch1 = 432
#pitch2 = 20
#pitch3 = 1
print("pitches: %s, %s, %s" % (pitch1, pitch2, pitch3,))

duration = 10.0          # in seconds

from audio import Audio
from sound import Sound

if __name__ == "__main__":
	#from time import sleep

	def main ():
		sample_rate = 44100
		bits        = 16
		duration    = 10
		audio = Audio(sample_rate, bits)
		sound = Sound(audio, duration)

		#for k in range(duration): sound.sine_wave(432, 0.5, k)

		#buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
		#arr = stereo_sine_wave(0, n_samples, n_samples, pitch1)
		#print("arr: %s" % (arr,))
		#buf = buf + arr

		#pitch1 = 432
		#pitch2 = 7.83 / 2
		#pitch3 = 1
		sound.add_wave(sound.sine_wave, pitch3, duration, 1.0,  0)
		sound.add_wave(sound.sine_wave, pitch2, duration, 0.5,  0)
		#sound.add_waves(sound.sine_waves_1, pitch2, duration, 1.0, 0)
		sound.add_wave(sound.sine_wave, pitch1, duration, 0.25, 0)
		#for k in range(int(round(duration * pitch1))): sound.add_waves(sound.sine_waves_1, 432.0 * 3 / 2, 0.5 / pitch1, 0.25, float(k) / pitch1)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_2, 432,           0.5 / pitch3, 0.25, float(k) / pitch3)
		#sound.add_waves(sound.sine_waves_2, pitch1, duration, 1.0, 0)
		#sound.add_waves(sound.sine_waves_1, pitch1, duration, 1.0, 0)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_1, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch3))): sound.add_waves(sound.sine_waves_2, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch3))): sound.add_wave(sound.sine_wave, pitch1, 0.5 / pitch3, 1.0, k / pitch3)

		#for k in range(int(round(duration * pitch3))): sound.add_wave(sound.sine_waves_1, pitch1, 0.5 / pitch3, 1.0, k / pitch3)
		#for k in range(int(round(duration * pitch2))): play(buf, pitch2, 0.5 / pitch2, k / pitch2)

		#sound = pygame.sndarray.make_sound(buf)
		#play once, then loop forever
		#sound.play(loops = 1)

		sound.play_sound()
		#sleep(0.1)
		#sleep(duration)
		#pygame.time.delay(1000)
		while pygame.mixer.music.get_busy(): pygame.time.Clock().tick()

		#pygame.quit()
	main ()
