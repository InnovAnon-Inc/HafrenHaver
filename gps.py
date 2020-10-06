#! /usr/bin/env python3

class GPS:
	def __init__ (self, observer): self.observer = observer
	def __repr__ (self): return str (self.observer)

# TODO temperature and pressure

from cache import memoized_cacher, memoized_key
from constants import DEFAULT_USER_AGENT

from geopy.geocoders import Nominatim
	
def addr2latlon (addr):
	geolocator = Nominatim (user_agent=DEFAULT_USER_AGENT)
	location   = geolocator.geocode (addr)
	ret        = (location.latitude, location.longitude, location.altitude)
	return ret
from ast import literal_eval as make_tuple
def addr2latlon_cacher (addr):
	print ("addr2latlon_cacher (%s)" % (addr,))
	ret = memoized_cacher (addr2latlon, addr)
	print ("ret: %s" % (ret,))
	ret = make_tuple (ret)
	print ("ret: %s" % (ret,))
	lat, lon, alt = ret
	assert type (lat) is float
	assert type (lon) is float
	assert type (alt) is float
	return ret

"""
import geocoder
def elevation_cacher (arg):    return cacher (geocoder.elevation, arg)
def   addr2elevation (addr):   return elevation_cacher (addr)
def latlon2elevation (latlon): return elevation_cacher (latlon)

def addr2gps (addr):
	lat, lon, alt = addr2latlon_cacher (addr)
	if alt == 0: alt = addr2elevation (addr)
	return lat, lon, alt
"""


import requests
import pandas as pd
"""
# script for returning elevation from lat, long, based on open elevation data
# which in turn is based on SRTM
def latlon2elevation (lat, lon): # https://stackoverflow.com/questions/19513212/can-i-get-the-altitude-with-geopy-in-python-with-longitude-latitude
	print ("latlon2elevation (%s, %s)" % (lat, lon))
	f = lambda k: "%s,%s" % (round (lat, k), round (lon, k))
	r = range (0, 6 + 1)
	r = r[::-1]
	t = map (f, r)
	s = '|'.join (t)
	print ("s: %s" % (s,))
	query = ('https://api.open-elevation.com/api/v1/lookup?locations=%s' % (s,))
	print ("query: %s" % (query,))
	r = requests.get (query)
	#r = requests.post (query)
	print ("r: %s" % (r,))
	if r.status_code != 200:
		print ("error")
		quit ()
	r = r.json ()  # json object, various ways you can extract value
	print ("r: %s" % (r,))
	r = r[0]
	print ("r: %s" % (r,))
	# one approach is to use pandas json functionality:
	elevation = pd.io.json.json_normalize (r, 'results')['elevation'].values
	print ("elevation: %s" % (elevation,))
	elevation = elevation[0]
	print ("elevation: %s" % (elevation,))
	return elevation
"""
# script for returning elevation from lat, long, based on open elevation data
# which in turn is based on SRTM
def latlon2elevation (lat, lon, key=None): # https://stackoverflow.com/questions/19513212/can-i-get-the-altitude-with-geopy-in-python-with-longitude-latitude
	print ("latlon2elevation (%s, %s)" % (lat, lon))
	f = lambda k: "(%s,%s)" % (round (lat, k), round (lon, k))
	r = range (0, 6 + 1)
	r = r[::-1]
	t = map (f, r)
	s = ','.join (t)
	print ("s: %s" % (s,))
	if key is not None: s = "%s&key=%s" % (s, key)
	query = ('https://elevation-api.io/api/elevation?points=%s' % (s,))
	print ("query: %s" % (query,))
	r = requests.get (query)
	#r = requests.post (query)
	print ("r: %s" % (r,))
	if r.status_code != 200:
		print ("error")
		quit ()
	r = r.json ()  # json object, various ways you can extract value
	print ("r: %s" % (r,))
	r = r['elevations'] # list
	print ("r: %s" % (r,))
	r = r[0] # most accurate
	print ("r: %s" % (r,))
	elevation = r['elevation']
	print ("elevation: %s" % (elevation,))
	return elevation
def latlon2elevation_cacher (lat, lon, key=None):
	print ("latlon2elevation_cacher (%s, %s, %s)" % (lat, lon, key))
	ret = memoized_cacher (latlon2elevation, lat, lon, key)
	print ("ret: %s" % (ret,))
	ret = float (ret)
	print ("ret: %s" % (ret,))
	return ret
def latlon2elevation2 (lat, lon):
	key = memoized_key (latlon2elevation)
	return latlon2elevation_cacher (lat, lon, key)
def addr2gps (addr):
	lat, lon, alt = addr2latlon_cacher (addr)
	if alt == 0: alt = latlon2elevation2 (lat, lon) # if Nominatim doesn't have altitude info for this address
	return lat, lon, alt


# TODO temperature and pressure


import ephem

def gps2observer (lat, lon, alt):
	lowell           = ephem.Observer ()
	lowell.lon       = lon
	lowell.lat       = lat
	lowell.elevation = alt
	#lowell.date = '1986/3/13'
	return lowell
	
def addr2observer (addr):
	tmp = addr2gps (addr)
	return gps2observer (*tmp)

class AddrGPS (GPS):
	def __init__ (self, addr):
		observer = addr2observer (addr)
		GPS.__init__ (self, observer)


	
def city2observer_lookup        (city): return ephem.cities.lookup (city)
def city2observer_lookup_cacher (city): return memoized_cacher (city2observer_lookup, city)
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
