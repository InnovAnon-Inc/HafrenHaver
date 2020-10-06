#! /usr/bin/env python3

from client import Client
from gps import GPS

from ast import literal_eval as make_tuple
import ephem

def observer_msg (observer):
	temp          = make_tuple (observer)
	epoch, lat, lon, elevation, temp, pressure = temp
	ret           = ephem.Observer ()
	ret.epoch     = epoch
	ret.lat       = lat
	ret.lon       = lon
	ret.elevation = elevation
	ret.temp      = temp
	ret.pressure  = pressure
	return ret

class GPSClient (Client, GPS):
	def __init__ (self, host, port, notify):
		Client.__init__ (self, host, port)
		GPS   .__init__ (self, None)
		self.notify = notify
	def Network_observer (self, data):
		print("*** observer: " + data['observer'])
		observer      = data['observer']
		observer      = observer_msg (observer)
		self.observer = observer
		assert observer is not None
		# TODO notify GUI
		self.notify (observer)
		#self.is_running = False
		 
if __name__ == "__main__":
	def main ():
		host = "localhost"
		port = 1717
		c = GPSClient (host, port)
		c.run ()
	main ()
	quit ()
