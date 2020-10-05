#! /usr/bin/env python3

import pygame

import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

#from mpl_toolkits.basemap import Basemap
#import numpy as np

import pylab

from square_app import SquareApp

from constants import ORIGIN

import geopandas as gpd

class MapApp (SquareApp):
	def __init__ (self, lat, lon):
		SquareApp.__init__ (self)
		self.lat = lat
		self.lon = lon
	def set_subsurface (self, ss=None): # TODO apps should pre render images here
		SquareApp.set_subsurface (self, ss)
		ss = self.ss
		if ss is None: return
		
		lon_0 = self.lon
		lat_0 = self.lat
		
		#m = Basemap (width=width, height=width, projection='aeqd',
        #    lat_0=lat_0, lon_0=lon_0)
		#m.drawmapboundary (fill_color='aqua')              # fill background.
		#m.drawcoastlines (linewidth=0.5)                   # draw coasts and fill continents.
		#m.fillcontinents (color='coral', lake_color='aqua')
		#m.drawparallels (np.arange (-80, 81, 20))          # 20 degree graticule.
		#m.drawmeridians (np.arange (-180, 180, 20))
		#xpt, ypt = m (lon_0, lat_0)                        # draw a black dot at the center.
		#m.plot ([xpt], [ypt], 'ko')
		#fig = m
		
		fig = pylab.figure (figsize=[4, 4], # Inches
		                    dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
		                   )
		#ax = fig.gca ()
		plt = fig.gca ()
		#ax.plot ([1, 2, 4])
		
		canvas = agg.FigureCanvasAgg (fig)
		canvas.draw ()		
		renderer = canvas.get_renderer ()
		raw_data = renderer.tostring_rgb ()
		self.raw_data = raw_data
		self.size     = canvas.get_width_height ()
	def draw_foreground (self, temp): # TODO apps should merely blit pre rendered images here
		SquareApp.draw_foreground (self, temp)
		raw_data = self.raw_data
		size     = self.size
		surf = pygame.image.fromstring (raw_data, size, "RGB")
		temp.blit (surf, ORIGIN) 
	def notify (self, lat, lon):
		self.lat = lat
		self.lon = lon
		self.set_subsurface ()

from circle_app import CircleApp

class ThermometerApp (SquareApp): pass
class   AltimeterApp (CircleApp): pass
class   BarometerApp (CircleApp): pass
class         GPSApp (SquareApp):
	# has-a thermometer
	# has-a altimeter
	# has-a barometer
	# has-a map
	pass
		 
if __name__ == "__main__":
	from gps_client import GPSClient
	from hal import HAL9000
	
	def main ():
		a = MapApp (0, 0)
		h = "localhost"
		p = 1717
		n = a.notify
		g = GPSClient (h, p, n)
		with HAL9000 (app=a) as g: g.run ()
	main ()
	quit ()
