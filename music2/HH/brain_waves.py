#! /usr/bin/python3

from enum import Enum

class Brainwaves (Enum): # measured in hertz
	EPSILON = ( 0,   1)
	DELTA   = ( 1,   4)
	THETA   = ( 4,   8)
	ALPHA   = ( 8,  12)
	BETA    = (12,  40)
	GAMMA   = (40, 100)
	
EPSILON = Brainwaves.EPSILON
DELTA   = Brainwaves.DELTA
THETA   = Brainwaves.THETA
ALPHA   = Brainwaves.ALPHA
BETA    = Brainwaves.BETA
GAMMA   = Brainwaves.GAMMA

import ephem
import datetime  
from solfeggio import get_gps

from bjorklund import bjorklund

SLEEP_CYCLE = tuple ([EPSILON] + [ALPHA, DELTA, THETA,] * 5)

class DayNight (Enum):
	DAY   = 0
	NIGHT = 1
DAY   = DayNight.DAY
NIGHT = DayNight.NIGHT

class Lifestyle (Enum):
	VISHNAIVITE = { NIGHT: SLEEP_CYCLE, DAY: (EPSILON, ALPHA,  BETA, GAMMA, BETA,  ALPHA, BETA, GAMMA, BETA,  ALPHA, BETA,  ALPHA,) }
	SHAIVITE    = { NIGHT: SLEEP_CYCLE, DAY: (EPSILON, ALPHA, THETA, DELTA, THETA, ALPHA, BETA, GAMMA, BETA,  ALPHA, THETA, DELTA,) }
VISHNAIVITE = Lifestyle.VISHNAIVITE
SHAIVITE    = Lifestyle.   SHAIVITE
	
def get_brainwaves (lifestyle, addy=None, city=None, lat=None, lon=None, ct=None): # length of day in modern seconds (used for classical seconds)
	if addy is not None:
		assert city is None
		assert lat  is None
		assert lon  is None
		lat, lon = get_gps (addy)
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
	
	cdaylen = daylen.total_seconds ()
	mdaylen = 24 * 60 * 60 / 2
	
	#if day:   ds = pr
	#if night: ds = ps
	if day:   mns = (ct - pr).total_seconds ()
	if night: mns = (ct - ps).total_seconds ()
	
	#cns = mns * cdaylen / mdaylen
	#hr  = (cns / cdaylen) * 12
	#hr  = (mns / mdaylen) * 12
	
	if day:   dn = DAY
	if night: dn = NIGHT
	c = lifestyle.value[dn]
	hr = int ((mns / mdaylen) * len (c) + .5)
	return c[hr]
		
if __name__ == "__main__":
	city = "Dallas"
	bw = get_brainwaves (   SHAIVITE, None, city)
	print (bw)
	bw = get_brainwaves (VISHNAIVITE, None, city)
	print (bw)
