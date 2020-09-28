#! /usr/bin/env python3

from enum   import Enum
#from numba  import jit
from random import choice

class SolfeggioType (Enum):
	RED    = 0
	ORANGE = 1
	YELLOW = 2
	GREEN  = 3
	BLUE   = 4
	VIOLET = 5
solfeggio_db = {
	SolfeggioType.RED    : ( 8,  2, 14),
	SolfeggioType.ORANGE : ( 1,  7, 13),
	SolfeggioType.YELLOW : ( 6,  0, 12),
	SolfeggioType.GREEN  : ( 5, 11, 17),
	SolfeggioType.BLUE   : ( 4, 16, 10),
	SolfeggioType.VIOLET : ( 3,  9, 15),
}
solfeggios = (
    528, #  0
    147, #  1
    417, #  2
    258, #  3
    396, #  4
    369, #  5
    285, #  6
    471, #  7
    174, #  8
    582, #  9
    963, # 10
    693, # 11
    852, # 12
    714, # 13
    741, # 14
    825, # 15
    639, # 16
    936, # 17
)


from geopy.geocoders import Nominatim
from pathlib import Path
from ast import literal_eval as make_tuple
def get_gps (addy):
	assert addy is not None
	fname = "%s.txt" % addy
	my_file = Path (fname)
	if my_file.is_file ():
		with open (fname, "r") as f: mylist = tuple (map (make_tuple, f))
		assert len (mylist) == 1
		mylist = mylist[0]
		assert len (mylist) == 2
		return mylist	
	geolocator = Nominatim (user_agent="Hafren Haver")
	location   = geolocator.geocode (addy)
	ret        = (location.latitude, location.longitude)
	with open (fname, "w") as f: f.write (str (ret))
	return ret

import ephem
import datetime  
def get_hz_adjustment (city=None, lat=None, lon=None, ct=None): # length of day in modern seconds (used for classical seconds)
	o      = ephem.Observer ()  
	if ct is None: ct     = datetime.datetime.utcnow ()
	o.date = ct 
	s      = ephem.Sun ()
	if lat is None or lon is None:
		assert lat  is     None
		assert lon  is     None
		assert city is not None
		sf = ephem.city (city)
		s.compute (sf)	
	else:
		assert lat  is not None
		assert lon  is not None
		assert city is     None
		s.compute ()
	#twilight = -12 * ephem.degree
	#print 'Is it light in SF?', s.alt > twilight
	
	pr = o.previous_rising  (s).datetime ()
	ps = o.previous_setting (s).datetime ()
	nr = o.    next_rising  (s).datetime ()
	ns = o.    next_setting (s).datetime ()
	
	#print ("prev rise: %s" % (pr,))
	#print ("prev  set: %s" % (ps,))
	#print ("next rise: %s" % (nr,))
	#print ("next  set: %s" % (ns,))
	
	day   = pr > ps and ns < nr
	night = pr < ps and ns > nr
	if day: # day
		assert not night
		assert pr < ct
		assert ct < ns
		daylen = ns - pr
	if night: # night
		assert not day
		assert ps < ct
		assert ct < nr
		daylen = nr - ps
	
	return daylen.total_seconds ()

def get_solfeggio_offset (city=None, lat=None, lon=None, ct=None):
	o      = ephem.Observer ()  
	if ct is None: ct     = datetime.datetime.utcnow ()
	o.date = ct 
	s      = ephem.Moon ()
	if lat is None or lon is None:
		assert lat  is     None
		assert lon  is     None
		assert city is not None
		sf = ephem.city (city)
		s.compute (sf)	
	else:
		assert lat  is not None
		assert lon  is not None
		assert city is     None
		s.compute ()
	c = ephem.constellation (s)
	print (c)
	#a = s.anorm
	n = len (solfeggio_db)
	i = int (a / (2 * pi) * n)
	return solfeggio_db[i]
	
	
def get_gps_hz_adjustment (addy=None, city=None, lon=None, lat=None, ct=None):
	if lon is not None or lat is not None:
		assert lat  is not None
		assert lon  is not None
		assert city is     None
		assert addy is     None
		return get_hz_adjustment (city, lat, lon, ct)
	assert lon is None
	assert lat is None
	if city is not None:
		assert addy is None
		return get_hz_adjustment (city, lat, lon, ct)
	assert city is     None
	assert addy is not None
	return get_hz_adjustment (None, *get_gps (addy), ct)
def get_gps_solfeggio_offset (addy=None, city=None, lon=None, lat=None, ct=None):
	if lon is not None or lat is not None:
		assert lat  is not None
		assert lon  is not None
		assert city is     None
		assert addy is     None
		return get_solfeggio_offset (city, lat, lon, ct)
	assert lon is None
	assert lat is None
	if city is not None:
		assert addy is None
		return get_solfeggio_offset (city, lat, lon, ct)
	assert city is     None
	assert addy is not None
	return get_solfeggio_offset (None, *get_gps (addy), ct)
def get_solfeggio_adjustment (addy=None, city=None, lon=None, lat=None, ct=None):
	if ct is None: ct = datetime.datetime.utcnow ()
	if addy is not None:
		assert city is None
		assert lon  is None
		assert lat  is None
		lat, lon = get_gps (addy)
	daylen = get_hz_adjustment    (city, lon, lat, ct)
	solfeg = get_solfeggio_offset (city, lon, lat, ct)
	return daylen, solfeg
	
# empirically tune res freq of saline water
# get hz adjustment
# select arbitrary solfeggio
# => solfeggio hz is def'd to be res freq of water


# res freq of water => octaves
# scale + tod => isochronic 



# TODO harmonic frequencies of various elements

# TODO empirically tuning to the resonant frequency of target object

import pygame
from pygame.locals import *
def wait ():
	pygame.event.clear()
	while True:
		#for event in pygame.event.get ():
		event = pygame.event.wait()
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if not event.type == KEYDOWN: continue
		if event.key == K_f: return # -1, 0, +1

import numpy
import math
def tune_base_frequency ():
	bits = 16
	#the number of channels specified here is NOT 
	#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

	pygame.mixer.pre_init(44100, -bits, 2)
	pygame.init()
	size = (1366, 720)
	display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

	duration = 1.0          # in seconds
	#freqency for the left speaker
	#frequency_l = 440
	#frequency for the right speaker
	#frequency_r = 550

	#this sounds totally different coming out of a laptop versus coming out of headphones
	sample_rate = 44100

	n_samples = int(round(duration*sample_rate))

	#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
	max_sample = 2**(bits - 1) - 1

	def play (pitch):
		frequency_l = pitch
		frequency_r = pitch
		buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
		for s in range(n_samples):
			t = float(s)/sample_rate    # time in seconds

			#grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
			buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
			buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right

		sound = pygame.sndarray.make_sound(buf)
		#play once, then loop forever
		sound.play(loops = 1)


	
	# binary interpolation
	min_pitch = 20
	max_pitch = 20000
	while True:
		pitch = min_pitch + (max_pitch - min_pitch) / 2
		#t1 = Thread (audio.play (pitch))
		#inp = wait ()
		#t1.kill ()
		play (pitch)
		inp = wait ()
		if inp ==  0: break
		if inp == -1: max_pitch = pitch
		if inp == +1: min_pitch = pitch
		
	# TODO linear interpolation
	for pitch in range (min_pitch, max_pitch):
		pass
	
	pygame.quit()

class Solfeggio: # solves the problem of tuning the yellow bell
	def __init__ (self, base_frequency): self.base_frequency = base_frequency
	def __repr__ (self): return str ("Solfeggio=[base_frequency=%s]" % self.base_frequency)
#	@jit
	def pitch (self, ratio): return self.base_frequency * ratio
        #def draw (self, screen):
        #    index = solfeggios.indexof
        #    color = 
def random_solfeggio ():
	base_frequency = choice (list (solfeggio_db.values ()))
	base_frequency = choice (base_frequency)
	base_frequency = solfeggios[base_frequency]
	return Solfeggio (base_frequency)
	
mdaylen = 24 * 60 * 60 / 2
def c2m (daylen, hz): return hz * mdaylen /  daylen
def m2c (daylen, hz): return hz *  daylen / mdaylen
	
class SolarSolfeggio (Solfeggio):
	def __init__ (self, base_frequency, daylen):
		Solfeggio.__init__ (self, m2c (daylen, base_frequency))
		self.daylen = daylen
	def to_classical_hertz (self, hz): c2m (hz, self.daylen)
	def to_modern_hertz    (self, hz): m2c (hz, self.daylen)
def random_solar_solfeggio (city):
	base_frequency = choice (list (solfeggio_db.values ()))
	base_frequency = choice (base_frequency)
	base_frequency = solfeggios[base_frequency]
	daylen = get_hz_adjustment (city)
	return SolarSolfeggio (base_frequency, daylen)
	
	
	
	
	
class Solfeggios:
	def draw (self, screen):
            outer.draw (screen)
            inner.draw (screen)
            for s in self.circles: s.draw (screen)
            for s in self.lines:   s.draw (screen)
            
from random import uniform

if __name__ == "__main__":
	def main ():
		#bf = tune_base_frequency ()
		solfeggio = random_solfeggio ()
		print (solfeggio)
		
		solfeggio = random_solar_solfeggio ("Dallas")
		print (solfeggio)
		
		rf = uniform (432, 528)
		solfeggio = Solfeggio (rf)
		print (solfeggio)
		
		#city = "Dallas"
		#print (get_solfeggio_adjustment (addy, None, None, None, None))
	main ()
	
