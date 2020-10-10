#! /usr/bin/env python3

import pygame

from map_app import SquareMapApp, random_projection

from circle_app import CircleApp
from square_app import SquareApp
from client import Client
from server import Server

#from stat_chart import StatChart
from math import erf

from circled_circle import AbsoluteCircledCircle

from polygon_app import PolygonApp, EqualPolygonApp
from circled_polygon import CircledPolygon
from polygoned_circle import PolygonedCircle, EqualPolygonedCircle
from text_ring import TextRing

class SquareStatChartInner (SquareApp): pass
class SquareStatChart (SquareApp): pass

from stat_chart import StatChart

from atp import ATP






"""
from pygameplotlib import PyGamePlotLib

class MeterApp (PyGamePlotLib):
	def __init__ (self, min_val, max_val):
		PyGamePlotLib.__init__ (self)
		self.min_val = min_val
		self.max_val = max_val
		self.val     = None
	def notify (self, val):
		self.val = val
		self.compute ()
	def compute_helper (self, fig):
		PyGamePlotLib.compute_helper (self, fig)
		if self.val is None: return
		
		ax  = fig.add_subplot (facecolor='black')
		
		#plt.xticks ([0, 1, 2, 3])
		plt.xlim   ([self.min_val, self.max_val])





class ThermometerApp (PyGamePlotLib):
	def __init__ (self):
		PyGamePlotLib.__init__ (self)
		self.temperature = 0
	def notify (self, temp):
		print ("enter thermometer_app.notify (%s)" % (temp,))
		self.temperature = temp
		self.compute ()
		print ("leave thermometer_app.notify ()")
	#def draw_foreground (self, temp):
	def compute_helper (self, fig):
		print ("enter thermometer_app.compute ()")
		PyGamePlotLib.compute_helper (self, fig)
		return
		# TODO square vs circle
		ax  = fig.add_subplot (facecolor='black')
		#ax.plot (times, temps)
		
		# TODO
		
		print ("leave thermometer_app.compute ()")
		
class SquareThermometerApp (ThermometerApp, SquareApp):
	def __init__ (self, rotation=None, *args, **kwargs):
		SquareApp.__init__ (self, rotation, *args, **kwargs)
		ThermometerApp   .__init__ (self,           *args, **kwargs)
	def start_running (self):
		SquareApp.start_running (self)
		ThermometerApp   .start_running (self)
	def  stop_running (self):
		SquareApp.stop_running (self)
		ThermometerApp   .stop_running (self)
	def set_subsurface (self, ss):
		SquareApp.set_subsurface (self, ss)
		# TODO handle geometries&rotations here
		ThermometerApp   .set_subsurface (self, None, True)
	def draw_cropped_scene (self, temp):
		#MapApp   .draw_scene         (self, temp)
		SquareApp.draw_cropped_scene (self, temp)
		ThermometerApp   .draw_foreground    (self, temp)	
	def positive_space (self, is_root=True): raise Exception ()
	def negative_space (self, is_root=True): raise Exception ()
	def minsz          (self): raise Exception ()
		
		
		
		
class   AltimeterApp (PyGamePlotLib):
	def __init__ (self):
		PyGamePlotLib.__init__ (self)
		self.altitude = 0
	def notify (self, alt):
		print ("enter altimeter_app.notify (%s)" % (alt,))
		self.altitude = alt
		self.compute ()
		print ("leave altimeter_app.notify ()")
	#def draw_foreground (self, temp):
	def compute_helper (self, fig):
		print ("enter altimeter_app.compute ()")
		PyGamePlotLib.compute_helper (self, fig)
		return
		# TODO square vs circle
		ax  = fig.add_subplot (facecolor='black')
		#ax.plot (times, temps)
		
		# TODO
		
		print ("leave altimeter_app.compute ()")

class   BarometerApp (PyGamePlotLib):
	def __init__ (self):
		PyGamePlotLib.__init__ (self)
		self.pressure = 0
	def notify (self, press):
		print ("enter barometer_app.notify (%s)" % (press,))
		self.pressure = press
		self.compute ()
		print ("leave barometer_app.notify ()")
	#def draw_foreground (self, temp):
	def compute_helper (self, fig):
		print ("enter barometer_app.compute ()")
		PyGamePlotLib.compute_helper (self, fig)
		return
		# TODO square vs circle
		ax  = fig.add_subplot (facecolor='black')
		#ax.plot (times, temps)
		
		# TODO
		
		print ("leave barometer_app.compute ()")
"""
class         GPSApp (SquareApp):
	def __init__ (self):
		SquareApp.__init__ (self)
		self.map         = SquareMapApp ()
		#self.altimeter   = SquareAltimeterApp   ()
		#self.thermometer = ThermometerApp ()
		#self.barometer   = BarometerApp   ()
		self.atp = ATP ()
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
		self.atp        .notify (observer.elevation, observer.temp, observer.pressure)
		print ("leave gps_app.set_observer ()")
	def set_subsurface (self, ss=None):
		print ("enter gps_app.set_subsurface (%s)" % (ss,))
		SquareApp.set_subsurface (self, ss)
		ss = self.ss
		if ss is None: return
		x, y, w, h = ss.get_rect ()
		rect0 = x        , y        , w / 2, h
		rect1 = x + w / 2, y        , w / 2, h
		ss0 = ss.subsurface (rect0)
		self.map        .set_subsurface (ss0)
		ss1 = ss.subsurface (rect1)
		self.atp        .set_subsurface (ss1)
		print ("leave gps_app.set_subsurface ()")
	def draw_scene (self, temp=None):
		print ("enter gps_app.draw_foreground (%s)" % (temp,))
		SquareApp.draw_scene (self, temp)
		if temp is None: temp = self.ss	
		x, y, w, h = temp.get_rect ()
		rect0 = x        , y        , w / 2, h
		rect1 = x + w / 2, y        , w / 2, h
		ss0 = temp.subsurface (rect0)
		self.map        .draw_cropped_scene (ss0)
		ss1 = temp.subsurface (rect1)
		self.atp        .draw_scene (ss1)
		print ("leave gps_app.draw_foreground ()")
	# has-a map, has-a selector for projection
	# has-a selector for ClientGPS, AddrGPS, CityGPS
	
	def run_loop (self, events, keys):
		SquareApp.run_loop (self, events, keys)
		if isinstance (self.gps, Client): self.gps.Loop ()
		if isinstance (self.gps, Server): self.gps.Pump ()
		 		 
if __name__ == "__main__":
	from gps_client import GPSClient
	from gps_server import GPSServer
	from gps import AddrGPS
	from hal import HAL9000
	
	def main ():
		a = GPSApp ()
		with HAL9000 (app=a) as G:
			p = random_projection ()
			a.set_projection (p)
			
			h = "localhost"
			p = 1717
			n = a.set_observer
			#def cb (observer):
			#	print ("cb (%s)" % (observer,))
			#	g.is_running = False
			#	G.is_running = False
			#	quit ()
			#n = cb
			g = GPSClient (h, p, n)
			#g = AddrGPS ("7271 Wurzbach Rd, San Antonio, TX 78240")
			#g = CityGPS ("Dallas, TX")
			#host, port = "0.0.0.0", 1717
			#g = GPSServer (g, localaddr=(host, int (port)))
			a.set_gps (g)
			
			G.run ()
	main ()
	quit ()
