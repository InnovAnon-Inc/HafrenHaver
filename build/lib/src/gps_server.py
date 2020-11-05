#! /usr/bin/env python3

from server import PlayerChannel, PlayerServer
from gps import GPS

class GPSChannel (PlayerChannel):
	def __init__ (self, *args, **kwargs): PlayerChannel.__init__ (self, *args, **kwargs)
	#def Network_message (self, data):
    #    self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})

def observer_msg (observer):
	epoch     = observer.epoch
	lat       = observer.lat
	lon       = observer.lon
	elevation = observer.elevation
	temp      = observer.temp
	pressure  = observer.pressure
	ret       = epoch, lat, lon, elevation, temp, pressure
	ret       = str (ret)
	return ret

class GPSServer (PlayerServer, GPS):
	channelClass = GPSChannel
	def __init__ (self, gps, *args, **kwargs):
		PlayerServer.__init__ (self, *args, **kwargs)
		GPS.__init__ (self, gps.observer)
		self.gps = gps
	def Connected (self, channel, addr):
		PlayerServer.Connected (self, channel, addr)
		self.SendObserver (channel)
	def SendObserver  (self, player): player.Send      ({"action": "observer", "observer": observer_msg (self.observer)})
	def SendObservers (self):         self  .SendToAll ({"action": "observer", "observer": observer_msg (self.observer)})
	def set_gps (self, gps):
		self.gps = gps
		self.SendObservers ()
		 # TODO notiy GUI
		 
if __name__ == "__main__":
	from gps import AddrGPS, CityGPS
	def main ():
		g = AddrGPS ("7271 Wurzbach Rd, San Antonio, TX 78240")
		#g = CityGPS ("Dallas, TX")
		host, port = "0.0.0.0", 1717
		s = GPSServer (g, localaddr=(host, int (port)))
		s.Launch ()
	main ()
	quit ()
