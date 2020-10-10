#! /usr/bin/env python3

import pygame

#from map_app import SquareMapApp, random_projection

from client import Client

from math import erf

from stat_chart import StatChart

class ATP (StatChart):
	def __init__ (self, *args, **kwargs):
		labels = ('altitude', 'temperature', 'pressure')
		StatChart.__init__ (self, labels, *args, **kwargs)

	def set_inner_background (self, background): self.child.set_background (background)

	def get_radius (self, raw): # https://stackoverflow.com/questions/42140347/normalize-any-value-in-range-inf-inf-to-0-1-is-it-possible
		if raw is None: return 0
		radius   = (erf (raw) + 1) / 2
		return radius
	def get_scaled_radius (self, raw, raw_min, raw_max):
		raw_rng = raw_max - raw_min + 1
		raw_rng = raw_rng / 2 # TODO use a real offset
		ret = raw / raw_rng
		ret = self.get_radius (ret)
		return ret
		
	def get_altitude_radius (self, alt): # meters
		alt_min = -12262 # Kola Superdeep Borehole
		alt_max = + 8848 # Mount Everest 
		ret = self.get_scaled_radius (alt, alt_min, alt_max)
		return ret
	def get_temperature_radius (self, temp): # celsius
		temp_min = -273.15 # absolute zero
		temp_max = +100    # boiling point of water
		ret = self.get_scaled_radius (temp, temp_min, temp_max)
		return ret
	def get_pressure_radius (self, press): # mBar ???
		press_min = 0
		press_max = 10000 # TODO learn chemistry or physics or whatever
		ret = self.get_scaled_radius (press, press_min, press_max)
		ret = (ret + 1) / 2
		return ret
		
	def set_radius (self, index, value, compute):
		rads = self.get_radii ()
		rads[index] = value
		self.set_radii (rads)
		#if compute: self.compute ()
	def set_altitude (self, alt, compute=True):
		alt = self.get_altitude_radius (alt)
		self.set_radius (0, alt, compute) # TODO scaling ?
	def set_temperature (self, temp, compute=True):
		temp = self.get_temperature_radius (temp)
		self.set_radius (1, temp)
	def set_pressure (self, press, compute=True):
		press = self.get_pressure_radius (press)
		self.set_radius (2, press)
	def notify (self, alt, temp, press):
		print ("notify (%s, %s, %s)" % (alt, temp, press))
		#self.set_altitude    (alt,   False)
		#self.set_temperature (temp,  False)
		#self.set_pressure    (press, True)
		alt   = self.get_altitude_radius (alt)
		temp  = self.get_temperature_radius (temp)
		press = self.get_pressure_radius (press)
		rads  = alt, temp, press
		self.set_radii (rads)
		#quit ()
 		 
if __name__ == "__main__":
	from gps_client import GPSClient
	from hal import HAL9000
	from random import uniform
	
	def main ():
		a = ATP ()
		with HAL9000 (app=a) as G:
			h = "localhost"
			p = 1717
			#n = lambda observer: a.notify (observer.elevation, observer.temp, observer.pressure)
			#n = lambda observer: quit ()
			def cb (observer):
				print ("cb (%s)" % (observer,))
				g.is_running = False
				G.is_running = False
				quit ()
			n = cb
			g = GPSClient (h, p, n)			
			"""
			n = 3
			assert n >= 3
			rng  = range (1, n + 1)
			rng  = tuple (rng)
			assert len (rng) == n
			f    = lambda k: uniform (0, 1)
			rads = map (f, rng)
			a.notify (*rads)
			"""
			G.run ()
	main ()
	quit ()
