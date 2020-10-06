#! /usr/bin/env python3

import pygame

import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

#from mpl_toolkits.basemap import Basemap
#import numpy as np

#import pylab
import matplotlib.pyplot as plt

from square_app import SquareApp

from constants import ORIGIN

import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy

from constants import OPAQUE

# https://stackoverflow.com/questions/13714454/specifying-and-saving-a-figure-with-exact-size-in-pixels
def pygame2matplotlib (w, h): return { 'figsize' : (w, h), 'dpi' : 1 }


projections = [ccrs.PlateCarree(), # https://semba-blog.netlify.app/07/04/2020/mapping-with-cartopy-in-python/
               ccrs.Robinson(),
               ccrs.Mercator(),
               ccrs.Orthographic(),
               ccrs.InterruptedGoodeHomolosine()
              ]

class MapApp (SquareApp):
	def __init__ (self, lat, lon):
		SquareApp.__init__ (self)
		self.lat = lat
		self.lon = lon
	def set_subsurface (self, ss=None): # TODO apps should pre render images here
		SquareApp.set_subsurface (self, ss)
		ss = self.ss
		if ss is None: return
		
		rect = ss.get_rect ()
		x, y, w, h = rect
		dims = pygame2matplotlib (w, h)
		
		central_lon = self.lon
		central_lat = self.lat
		#projection = ccrs.PlateCarree (central_lon, central_lat)
		projection = ccrs.PlateCarree (central_longitude=central_lon) # TODO latitude
		#fig, ax = plt.subplots (**dims, subplot_kw={'projection': projection})

		fig = plt.figure (**dims, facecolor='none', edgecolor='none')
		fig.patch.set_visible (False)
		
		#ax  = fig.add_subplot (1, 1, 1, projection=projection) # nrows, ncols, index
		ax  = fig.add_subplot (projection=projection)
		ax.set_global    ()
		
		ax.stock_img     ()
		ax.add_feature   (cartopy.feature.LAND)
		ax.add_feature   (cartopy.feature.OCEAN)
		ax.add_feature   (cartopy.feature.COASTLINE)
		ax.add_feature   (cartopy.feature.BORDERS, linestyle='dotted')
		ax.add_feature   (cartopy.feature.LAKES, alpha=0.5)
		ax.add_feature   (cartopy.feature.RIVERS)
		ax.gridlines     ()
		#ax.coastlines  ()
		
		ax.plot (self.lon, self.lat, 'ro')
		#ax.plot (self.lon, self.lat, 'ro', transform=projection)
		
		canvas = agg.FigureCanvasAgg (fig) # https://stackoverflow.com/questions/48093361/using-matplotlib-in-pygame
		canvas.draw ()		
		renderer = canvas.get_renderer ()
		raw_data = renderer.buffer_rgba () # tricky bitch
		self.raw_data = raw_data
		self.size     = canvas.get_width_height ()
	def draw_foreground (self, temp): # TODO apps should merely blit pre rendered images here
		SquareApp.draw_foreground (self, temp)
		raw_data = self.raw_data
		size     = self.size
		surf = pygame.image.frombuffer (raw_data, size, "RGBA")
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
