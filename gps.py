#! /usr/bin/env python3

# TODO
GPS_CREDITS = ('geopy.geocoders Nominatim', 'elevation-api')

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
#from ast import literal_eval as make_tuple
def addr2latlon_cacher (addr):
	print ("addr2latlon_cacher (%s)" % (addr,))
	ret = memoized_cacher (addr2latlon, addr)
	#print ("ret: %s" % (ret,))
	#ret = make_tuple (ret)
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


#import requests
#import pandas as pd
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
"""
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
"""

from rest import RESTParamTuple, RESTParamList, RESTParam, IARESTClient

def latlon2elevation (lat, lon, key=None): # https://stackoverflow.com/questions/19513212/can-i-get-the-altitude-with-geopy-in-python-with-longitude-latitude
	print ("latlon2elevation (%s, %s)" % (lat, lon))
	
	f = lambda k: (round (lat, k), round (lon, k))
	r = range (0, 6 + 1)
	r = r[::-1]
	t = map (f, r)
	params = []
	for lat, lon in t:
		param = RESTParamTuple (None, (lat, lon))
		params.append (param)
	params = [RESTParamList ('points', params)]
	if key is not None: params.append (RESTParam ('key', key))
	client = IARESTClient ('https', 'elevation-api.io', 'api/elevation', params)
	r      = client.get ()
	print ("r: %s" % (r,))
	r = r['elevations'] # list
	print ("r: %s" % (r,))
	r = r[0] # most accurate
	print ("r: %s" % (r,))
	elevation = r['elevation']
	print ("elevation: %s" % (elevation,))
	return elevation, client.cred
def latlon2elevation_cacher (lat, lon, key=None):
	print ("latlon2elevation_cacher (%s, %s, %s)" % (lat, lon, key))
	ret = memoized_cacher (latlon2elevation, lat, lon, key)
	#print ("ret: %s" % (ret,))
	ret, cred = ret
	ret = float (ret)
	#print ("ret: %s" % (ret,))
	return ret, cred
def latlon2elevation2 (lat, lon):
	key = memoized_key (latlon2elevation)
	return latlon2elevation_cacher (lat, lon, key)
def addr2latlonalt (addr):
	lat, lon, alt = addr2latlon_cacher (addr)
	if alt == 0:
		alt, cred = latlon2elevation2 (lat, lon) # if Nominatim doesn't have altitude info for this address
	else: cred = None
	return lat, lon, alt, cred

from weatherbit.api import Api
def latlon2temperature (lat, lon):
	creds = 'weatherbit' # TODO
	creds = (creds,)
	return None, creds
	
	# TODO
	lat = float (lat)
	lon = float (lon)
	
	api_key = memoized_key (latlon2temperature)
	
	api = Api (api_key)
	
	# TODO temperature and pressure

	# Set the granularity of the API - Options: ['daily','hourly','3hourly']
	# Will only affect forecast requests.
	api.set_granularity ('hourly')

	# Query by lat/lon
	forecast = api.get_forecast (lat=lat, lon=lon)
	
	# To get a daily forecast of temperature, and precipitation:
	temps = forecast.get_series (['temp'])
	
	# TODO snow, wind, clouds, rain
	print ("temps: %s" % (temps,))
	
	return temps, creds
#def latlon2temperature_cacher (lat, lon): return memoized_cacher (latlon2temperature, lat, lon)
	
def latlonalt2pressure (lat, lon, alt):
	# TODO
	return None
	
def addr2gps (addr):
	lat, lon, alt, cred1 = addr2latlonalt (addr)
	temp, cred2 = latlon2temperature (lat, lon)
	pressure = latlonalt2pressure (lat, lon, alt)
	print ("cred1: %s" % (cred1,))
	print ("cred2: %s" % (cred2,))
	cred = tuple (cred1) + cred2
	return lat, lon, alt, temp, pressure, cred

# TODO also send time ?


import ephem

def gps2observer (lat, lon, alt, temp, pressure, cred):
	lowell           = ephem.Observer ()
	lowell.lon       = lon
	lowell.lat       = lat
	lowell.elevation = alt
	if temp     is not None: lowell.temp      = temp
	if pressure is not None: lowell.pressure  = pressure
	#lowell.date = '1986/3/13'
	return lowell, cred
	
def addr2observer (addr):
	tmp = addr2gps (addr)
	return gps2observer (*tmp)

from rest import InnovAnon

class AddrGPS (GPS, InnovAnon):
	def __init__ (self, addr, *args, **kwargs):
		observer, cred = addr2observer (addr)
		GPS.__init__ (self, observer, *args, **kwargs)
		InnovAnon.__init__ (self, cred=cred, *args, **kwargs)

	
def city2observer_lookup        (city): return ephem.cities.lookup (city)
def city2observer_lookup_cacher (city): return memoized_cacher (city2observer_lookup, city)
def city2observer (city):
	try:    ret = ephem.city                  (city)
	except: ret = city2observer_lookup_cacher (city)
	return ret
def city2observer2 (city):
	observer      = city2observer (city)
	temp, cred = latlon2temperature (observer.lat, observer.lon)
	if temp is not None: observer.temp = temp
	pressure      = latlonalt2pressure (observer.lat, observer.lon, observer.elevation)
	if pressure is not None: observer.pressure = pressure
	return observer, cred
class CityGPS (GPS, InnovAnon):
	def __init__ (self, city, *args, **kwargs):
		observer, cred = city2observer2 (city)
		GPS.__init__ (self, observer, *args, **kwargs)
		InnovAnon.__init__ (self, cred=cred, *args, **kwargs)
		 
		 
if __name__ == "__main__":
	def main ():
		g = AddrGPS ("7271 Wurzbach Rd, San Antonio, TX 78240")
		print (g)
		g.credits ()
		print ()
		
		lat = g.observer.lat
		lon = g.observer.lon
		print (latlon2temperature (lat, lon))
		
		g = CityGPS ("Dallas")
		print (g)
		g.credits ()
		print ()
		
		g = CityGPS ("San Antonio, Texas") # TODO
		print (g)
		g.credits ()
		print ()
	main ()
	quit ()
