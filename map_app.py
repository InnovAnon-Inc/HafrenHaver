#! /usr/bin/env python3

import cartopy.crs as ccrs
import cartopy

projections_db = ( # https://scitools.org.uk/cartopy/docs/latest/crs/projections.html
	lambda lon, lat: ccrs.PlateCarree                (central_longitude=lon),
	lambda lon, lat: ccrs.AlbersEqualArea            (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.AzimuthalEquidistant       (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.EquidistantConic           (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.LambertConformal           (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.LambertCylindrical         (central_longitude=lon),
	lambda lon, lat: ccrs.Mercator                   (central_longitude=lon, min_latitude=lat-80.0, max_latitude=lat+84.0),
	lambda lon, lat: ccrs.Miller                     (central_longitude=lon),
	lambda lon, lat: ccrs.Mollweide                  (central_longitude=lon),
	lambda lon, lat: ccrs.Orthographic               (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.Robinson                   (central_longitude=lon),
	lambda lon, lat: ccrs.Sinusoidal                 (central_longitude=lon),
	lambda lon, lat: ccrs.Stereographic              (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.TransverseMercator         (central_longitude=lon, central_latitude=lat),
	# TODO UTM
	lambda lon, lat: ccrs.InterruptedGoodeHomolosine (central_longitude=lon),
	lambda lon, lat: ccrs.RotatedPole                (pole_longitude=lon, pole_latitude=lat + 90.0, central_rotated_longitude=0.0), # TODO learn cartography
	# TODO OSGB
	# TODO EuroPP
	lambda lon, lat: ccrs.Geostationary              (central_longitude=lon),
	lambda lon, lat: ccrs.NearsidePerspective        (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.EckertI                    (central_longitude=lon),
	lambda lon, lat: ccrs.EckertII                   (central_longitude=lon),
	lambda lon, lat: ccrs.EckertIII                  (central_longitude=lon),
	lambda lon, lat: ccrs.EckertIV                   (central_longitude=lon),
	lambda lon, lat: ccrs.EckertV                    (central_longitude=lon),
	lambda lon, lat: ccrs.EckertVI                   (central_longitude=lon),
	lambda lon, lat: ccrs.EqualEarth                 (central_longitude=lon),
	lambda lon, lat: ccrs.Gnomonic                   (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.LambertAzimuthalEqualArea  (central_longitude=lon, central_latitude=lat),
	lambda lon, lat: ccrs.NorthPolarStereo           (central_longitude=lon),
	# TODO OSNI
	lambda lon, lat: ccrs.SouthPolarStereo           (central_longitude=lon),
	)
from random import choice
def random_projection (): return choice (projections_db)

from pygameplotlib import PyGamePlotLib

class MapApp (PyGamePlotLib):
	def __init__ (self,):
		PyGamePlotLib.__init__ (self)
		self.lat        = 0
		self.lon        = 0
		self.projection = None
	def set_subsurface (self, ss=None): # TODO apps should pre render images here
		print ("enter map_app.set_subsurface (%s)" % (ss,))
		PyGamePlotLib.set_subsurface (self, ss)
		print ("leave map_app.set_subsurface ()")
	def compute_helper (self, fig):
		print ("enter map_app.compute ()")
		PyGamePlotLib.compute_helper (self, fig)
		
		projection = self.projection (self.lon, self.lat)
		#ax  = fig.add_subplot (1, 1, 1, projection=projection) # nrows, ncols, index
		ax  = fig.add_subplot (projection=projection)
		ax.set_global    ()
		
		ax.stock_img     ()
		ax.add_feature   (cartopy.feature.LAND, edgecolor='black') # TODO why don't these show up
		ax.add_feature   (cartopy.feature.OCEAN)
		ax.add_feature   (cartopy.feature.COASTLINE, edgecolor='black')
		ax.add_feature   (cartopy.feature.BORDERS, linestyle='dotted', edgecolor='black')
		ax.add_feature   (cartopy.feature.LAKES, alpha=0.5)
		ax.add_feature   (cartopy.feature.RIVERS)
		ax.gridlines     ()
		#ax.coastlines  ()
		
		ax.plot (self.lon, self.lat, 'ro') # plot the user's position (this dot is literally the point of the whole app)
		#ax.plot (self.lon, self.lat, 'ro', transform=projection)
		
		print ("leave map_app.compute ()")
	def notify (self, lat, lon):
		print ("enter map_app.notify (%s, %s)" % (lat, lon))
		self.lat = lat
		self.lon = lon
		self.compute ()
		print ("leave map_app.notify ()")
	def set_projection (self, projection):
		print ("enter map_app.set_projection (%s)" % (projection,))
		self.projection = projection
		self.compute ()
		print ("leave map_app.set_projection ()")
		 		 
if __name__ == "__main__":
	from gps_client import GPSClient
	from hal import HAL9000
	
	def main ():
		a = MapApp ()
		with HAL9000 (app=a) as G:
			p = random_projection ()
			a.set_projection (p)
			
			h = "localhost"
			p = 1717
			n = lambda observer: a.notify (observer.lat, observer.lon)
			g = GPSClient (h, p, n)
			
			G.run ()
	main ()
	quit ()
