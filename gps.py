#! /usr/bin/env python3

class GPS:
	def __init__ (self, observer): self.observer = observer

# TODO temperature and pressure

from cache import cacher
from constants import DEFAULT_USER_AGENT

from geopy.geocoders import Nominatim
	
def addr2gps (addr):
	geolocator = Nominatim (user_agent=DEFAULT_USER_AGENT)
	location   = geolocator.geocode (addr)
	ret        = (location.latitude, location.longitude, location.altitude)
	return ret
def addr2gps_cacher (addr): return cacher (addr2gps, addr)

import ephem

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

class AddrGPS (GPS):
	def __init__ (self, addr):
		observer = addr2observer (addr)
		GPS.__init__ (self, observer)


	
def city2observer_lookup        (city): return ephem.cities.lookup (city)
def city2observer_lookup_cacher (city): return cacher (city2observer_lookup, city)
def city2observer (city):
	try:    ret = ephem.city                  (city)
	except: ret = city2observer_lookup_cacher (city)
	return ret
class CityGPS (GPS):
	def __init__ (self, city):
		observer = city2observer (city)
		GPS.__init__ (self, observer)
		 
		 
		 
if __name__ == "__main__":
	def main ():
		g = AddrGPS ("7271 Wurzbach Rd, San Antonio, TX 78240")
		print (g)
		g = CityGPS ("Dallas")
		print (g)
		g = CityGPS ("San Antonio") # TODO
		print (g)
	main ()
	quit ()
