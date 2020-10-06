#! /usr/bin/env python3

import pygame

from map_app import MapApp, random_projection

from circle_app import CircleApp
from square_app import SquareApp
from client import Client

class ThermometerApp (SquareApp): pass
class   AltimeterApp (CircleApp): pass
class   BarometerApp (CircleApp): pass
class         GPSApp (SquareApp):
	def __init__ (self):
		SquareApp.__init__ (self)
		self.map         = MapApp ()
		#self.altimeter   = AltimeterApp   ()
		#self.thermometer = ThermometerApp ()
		#self.barometer   = BarometerApp   ()
	def set_projection (self, projection):
		print ("enter gps_app.set_projection (%s)" % (projection,))
		self.map.set_projection (projection)
		print ("leave gps_app.set_projection ()")
	def set_gps (self, gps):
		print ("enter gps_app.set_gps (%s)" % (gps,))
		self.gps = gps
		self.set_observer (gps.observer)
		print ("leave gps_app.set_gps ()")
	def set_observer (self, observer):
		print ("enter gps_app.set_observer (%s)" % (observer,))
		if observer is None: return
		#epoch     = observer.epoch
		self.map        .notify (observer.lat, observer.lon)
		#self.altimeter  .notify (observer.elevation)
		#self.thermometer.notify (observer.temp)
		#self.barometer  .notify (observer.pressure)
		print ("leave gps_app.set_observer ()")
	def set_subsurface (self, ss=None):
		print ("enter gps_app.set_subsurface (%s)" % (ss,))
		SquareApp.set_subsurface (self, ss)
		ss = self.ss
		if ss is None: return
		x, y, w, h = ss.get_rect ()
		rect0 = x        , y        , w / 2, h / 2
		rect1 = x + w / 2, y        , w / 2, h / 2
		rect2 = x        , y + h / 2, w / 2, h / 2
		rect3 = x + w / 2, y + h / 2, w / 2, h / 2
		ss0 = ss.subsurface (rect0)
		ss1 = ss.subsurface (rect1)
		ss2 = ss.subsurface (rect2)
		ss3 = ss.subsurface (rect3)
		self.map        .set_subsurface (ss0)
		#self.altimeter  .set_subsurface (ss1)
		#self.thermometer.set_subsurface (ss2)
		#self.barometer  .set_subsurface (ss3)
		print ("leave gps_app.set_subsurface ()")
	def draw_foreground (self, temp):
		print ("enter gps_app.draw_foreground (%s)" % (temp,))
		SquareApp.draw_foreground (self, temp)	
		x, y, w, h = temp.get_rect ()
		rect0 = x        , y        , w / 2, h / 2
		rect1 = x + w / 2, y        , w / 2, h / 2
		rect2 = x        , y + h / 2, w / 2, h / 2
		rect3 = x + w / 2, y + h / 2, w / 2, h / 2
		ss0 = temp.subsurface (rect0)
		ss1 = temp.subsurface (rect1)
		ss2 = temp.subsurface (rect2)
		ss3 = temp.subsurface (rect3)
		self.map        .draw_foreground (ss0)
		#self.altimeter  .draw_foreground (ss1)
		#self.thermometer.draw_foreground (ss2)
		#self.barometer  .draw_foreground (ss3)
		print ("leave gps_app.draw_foreground ()")
	# has-a map, has-a selector for projection
	# has-a selector for ClientGPS, AddrGPS, CityGPS
	
	def run_loop (self, events, keys):
		SquareApp.run_loop (self, events, keys)
		if isinstance (self.gps, Client): self.gps.Loop ()
		 		 
if __name__ == "__main__":
	from gps_client import GPSClient
	from hal import HAL9000
	
	def main ():
		a = GPSApp ()
		with HAL9000 (app=a) as G:
			p = random_projection ()
			a.set_projection (p)
			
			h = "localhost"
			p = 1717
			n = a.set_observer
			g = GPSClient (h, p, n)
			a.set_gps (g)
			
			G.run ()
	main ()
	quit ()
