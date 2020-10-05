#! /usr/bin/env python3

from app import App
from constants import DEFAULT_BACKGROUND, SECONDARY_BACKGROUND
from cropping_app import CroppingApp
from constants import OPAQUE


import pygame

from gui import GUI, BLACK


import pygame
import pygame.gfxdraw


from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp
from angle_app import AngleApp

from circled_square import CircledSquare
from squared_circle import SquaredCircle
from angled_circle import AngledCircle
from circled_angle import CircledAngle

from orientation import NORTH, SOUTH, EAST, WEST



from geometry import cercle_circonscrit, cercle_inscrit
	
	

		


class  AngledSquare ( AngleApp, CompositeApp): pass
class SquaredAngle  (SquareApp, CompositeApp): pass







from recursive_composite import RecursiveComposite

# using poetic cadences, grammar models, synonym dictionaries => wizard swears (take colorful input and produce musical output)			

		
# how to manage concentrations of positive vs negative space ?

# need subclasses of main connector apps for providing recursion points and reducing negative space

# use base frequency + scale for color palette
# get average color of internet images (from keyword search), then map to color palette ^^^
	
	
	
	
		
# perfect varieties of squares and circles, for compositing

# compositing:
# circles in circle (ring, cluster)
# circles in square
# squares in circle
# squares in square (grid, lines)

# nested apps should recurse with copies of themselves in used slots... need pixel-perfect minsz... copies need to not be clickable

# aesthetic composites:
# golden ratio ? for square layouts with main section et al
# golden ratio ? for circle in circle containers
		


# animated containers...
# jiggle back and forth / up and down (1 pixel)
# jiggle rotation back and forth (1 degree ?)
# pulse (scale down by 1 pixel, then back up)
# fading (alpha)

# some sort of hilbert curve + cadence => how to vary animations of all containers on screen
# need to account for ratios of positive space vs. negative space



# TODO use special music and colors for synchronizing users engaging in diversions... like tetris
def cacher (f, *args):
	fname = "%s-%s.cache" % (str (f), str (args))
	my_file = Path (fname)
	if my_file.is_file ():
		with open (fname, "r") as f: mylist = tuple (map (make_tuple, f))
		assert len (mylist) == 1
		mylist = mylist[0]
		#assert len (mylist) == 2
		return mylist	
	ret = f (*args)
	with open (fname, "w") as f: f.write (str (ret))
	return ret
	
def addr2gps (addr):
	geolocator = Nominatim (user_agent="Hafren Haver")
	location   = geolocator.geocode (addr)
	ret        = (location.latitude, location.longitude, location.altitude)
	return ret
def addr2gps_cacher (addr): return cacher (addr2gps, addr)

def gps2observer (lat, lon, alt):
	lowell           = ephem.Observer()
	lowell.lon       = lon
	lowell.lat       = lat
	lowell.elevation = alt
	#lowell.date = '1986/3/13'
	return lowell
	
def addr2observer (addr):
	tmp = addr2gps_cacher (addr)
	return gps2observer (*tmp)
	
def city2observer_lookup        (city): return cities.lookup (city)
def city2observer_lookup_cacher (city): return cacher (city2observer_lookup, city)
def city2observer (city):
	try:    ret = ephem.city                  (city)
	except: ret = city2observer_lookup_cacher (city)
	return ret

class GPS:
	def __init__ (self, observer): self.observer = observer
class CityGPS (GPS):
	def __init__ (self, city):
		observer = city2observer (city)
		GPS.__init__ (self, observer)
class AddrGPS (GPS):
	def __init__ (self, addr):
		observer = addr2observer (addr)
		GPS.__init__ (self, observer)
class GPSClient (Client, GPS):
	def __init__ (self, host, port):
		Client.__init__ (self, host, port)
		GPS   .__init__ (self, None)
	def Network_observer (self, data):
		print("*** observer: " + data['observer'])
		self.observer = data['observer']
		# TODO notify GUI
		#self.is_running = False
class GPSChannel (PlayerChannel):
	def __init__ (self, *args, **kwargs): PlayerChannel.__init__ (self, *args, **kwargs)
	#def Network_message (self, data):
    #    self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})
class GPSServer (PlayerServer, GPS):
	channelClass = GPSChannel
	def __init__ (self, gps, *args, **kwargs):
		PlayerServer.__init__ (self, *args, **kwargs)
		GPS.__init__ (self, gps.observer)
		self.gps = gps
	def Connected (self, channel, addr):
		PlayerServer.Connected (self, channel, addr)
		self.SendObserver (channel)
	def SendObserver  (self, player): player.Send      ({"action": "observer", "observer": self.observer})
	def SendObservers (self):         self  .SendToAll ({"action": "observer", "observer": self.observer})
	def set_gps (self, gps):
		self.gps = gps
		self.SendObservers ()
		 # TODO notiy GUI
		 
	
	
class ClassicalClock:
	def __init__ (self, gps, time=None):
		self.gps      = gps
		self.update_time (time)
		self.sun      = ephem.Sun  ()
		self.moon     = ephem.Moon ()
	def update_time (self, time=None):
		if time is None: time = datetime.datetime.utcnow ()
		self.gps.observer.date = time
		self.sun .compute (self.observer)
		self.moon.compute (self.observer)
	def get_time (self):
		self.get_hour ()
		self.get minute ()
		self.get_second ()
		self.get_day_or_night () # determines bright or dark
		self.get_day_of_week () # determines color and symbol
		self.get_moon_phase ()
		self.get_moon_position ()
		self.get_season ()
		self.get_position_of_sun ()
	def get_length_of_second (self): pass
	
	
	
# pre alpha	(codename: nirvana)
# solfeggio, chromatic, tetrachords, scales, modes => color manager
# fractalizer, matrix text => layout manager

# alpha (codename: nexus)
# network, chat
# yantra visualizations

# beta (codename: black tantra)
# most music layers
# subliminal programming
# IDE
	


from pyephem_sunpath.sunpath import sunpos
from datetime import datetime

thetime = datetime (2018, 5, 23, 13)
lat = 28.6
lon = 77.2
tz = 0

alt, azm = sunpos (thetime, lat, lon, tz, dst=False)



from skyfield import api

timescale = api.load.timescale ()
class PointInTime:
	def __init__ (self, observer, datetime):
		self.observer = observer
		self.datetime = datetime
	def get_position_of_sun (self):
		pass
	def get_position_of_sun  (self, datetime=None): # position of sun relative to earth
		dt = self.get_datetime (datetime)
		
	# get position of sun  in sky ?
	# get position of moon in sky ?
		
	def get_position_of_moon (self, datetime=None): pass 
	def get_wheel            (self, datetime=None): pass # wheel of the year, only update computations when time has passed
	def get_time_of_day      (self, datetime=None): pass # day, night, twilight
	def get_day_of_week      (self, datetime=None): pass # beginning after sundown ?
	def get_moon_phase       (self, datetime=None): pass #
	def get_length_of_day    (self, datetime=None): pass # length of day/night in seconds
	def get_second_of_day    (self, datetime=None): pass

class TimeModel:
	def __init__ (self, observer, datetime=None):
		self.observer = some_gps_voodoo # position of user (lat, lon, alt), either from client or server
	def get_datetime (self, datetime=None):
		if datetime is None: datetime = timescale.now ()
		else:                datetime = timescale.from_datetime (datetime)
		return datetime
	def get_observer (self): pass
	def get_model (self, datetime=None):
		observer = self.get_observer ()
		datetime = self.get_datetime ()
		return PointInTime (observer, datetime)
		
		
	

class TimeController: # tells the app when to update, based on isochronic pulses + frame rate + audio sample rate
	def get_tick (self): return 7.83 # TODO

# TODO use flatlib for horoscopes/astrology... bitches love sun signs, and computing entire charts for entire congregrations on the daily... well... there might be some possibilities in that


# has-a pos_of_sun + woy, pos_of_moon + moonphase, dow, clock, timer, tod
class TimeApp (CircleApp): # gets data from model, renders it on screen
	def __init__ (self):
		CircleApp.__init__ (self)
	def run_loop (self, events, keys):
		#CenteredApp.run_loop (self, keys)
		pass

# show splash text re: lovecraftian stars aligning
# day/night indicator... red during sunriset, no blue during night, bright during day (greenish?), dark at night
# wheel of the year... can indicate position of sun in sky ?
# moon phases... can indicate position of moon in sky ?
# day of week indicator... switch symbols at sundown
# classical time... analog clock with a hand for the procession of the equinox (i.e., eon hand) ?		
# countdown clock / alarm that can trigger by the stars
# TODO procession of the equinox, positions of other planets... universe man has a clock with an aeon hand


# TODO small animations, such as slightly wavy lines, slight brightening and dimming, slight oscillation, slight expansion/contraction
# ... to make things a little less static without being distracting
#class QuarterTab (Animation):
#




# TODO FinuxSpeak:
# can write in functional or imperative language... use src2src translation
# db of algorithms... automated selection of algorithm for workload
# jit + partial evaluation + pgo
# ... the goal is to be able to specify very generalized and abstract versions of solutions, and have them automatically replaced with special-case versions

# TODO FinuxOS
# microkernel design to facilitate clustering of all system services


if __name__ == "__main__":
	from rotation import ANGLED, STRAIGHT
	from orientation import NORTH, SOUTH, EAST, WEST
	
	def main ():
		if False:
			j = AngleApp     (orientation=NORTH)
			i = CircledAngle (j, background=SECONDARY_BACKGROUND)
			h = AngledCircle (i, orientation=WEST)
			g = CircledAngle (h, background=SECONDARY_BACKGROUND)
			f = AngledCircle (g, orientation=SOUTH)
			e = CircledAngle (f, background=SECONDARY_BACKGROUND)
			d = AngledCircle (e, orientation=EAST)
			c = CircledAngle (d, background=SECONDARY_BACKGROUND)
			b = AngledCircle (c, orientation=NORTH)
			a = CircledAngle (b, background=SECONDARY_BACKGROUND)
		elif False:
			#d = SquareApp     (background=DEFAULT_BACKGROUND)
			d = None
			c = CircledSquare (d, rotation=STRAIGHT)
			b = SquaredCircle (c, background=SECONDARY_BACKGROUND)
			a = RecursiveComposite (b)
			#a = b
		else:
			a = CircularMatrixText ()
		#a = RecursiveCompositeTest ()
		with GUI (app=a, exit_on_close=False) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
