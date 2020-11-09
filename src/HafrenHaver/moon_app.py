#! /usr/bin/env python3

from app import App
from constants import DEFAULT_BACKGROUND, SECONDARY_BACKGROUND
from cropping_app import CroppingApp
from constants import OPAQUE


import pygame

from gui import GUI, BLACK






	
	
	
from constants import ORIGIN
from circle_app import CircleApp
from client import Client
from server import Server
from math import radians as rad,degrees as deg  
"""
import numpy as np
def filled_arc (center, r, theta1, theta2): # https://stackoverflow.com/questions/30642391/how-to-draw-a-filled-arc-in-matplotlib
	# Range of angles
	phi = np.linspace (theta1, theta2, 100)

	# x values
	x = center[0] + r * np.sin (np.radians (phi))

	# y values. need to correct for negative values in range theta=90--270
	yy = np.sqrt (r - x ** 2)
	yy = [-yy[i] if phi[i] > 90 and phi[i] < 270 else yy[i] for i in range (len (yy))]

	y = center[1] + np.array (yy)

	# Equation of the chord
	m = (y[-1] - y[0]) / (x[-1]  -x[0])
	c = y[0] - m * x[0]
	y2 = m * x + c

	# Plot the filled arc
	ax.fill_between (x, y, y2, color=col[theta1 / 45])
"""

import math
from math import pi

import matplotlib.pyplot as plt
import matplotlib as mpl

from constants import ORIGIN

"""
def dual_half_circle(center, radius, angle=0, ax=None, colors=('w','k'),
                     **kwargs):
    ""
    Add two half circles to the axes *ax* (or the current axes) with the 
    specified facecolors *colors* rotated at *angle* (in degrees).
    ""
    if ax is None:
        ax = plt.gca()
    theta1, theta2 = angle, angle + 180
    w1 = Wedge(center, radius, theta1, theta2, fc=colors[0], **kwargs)
    w2 = Wedge(center, radius, theta2, theta1, fc=colors[1], **kwargs)
    for wedge in [w1, w2]:
        ax.add_artist(wedge)
    return [w1, w2]
"""

# TODO alpha values suck
def arc_patch (ax, lunacity): # https://stackoverflow.com/questions/58263608/fill-between-arc-patches-matplotlib
	ax.grid (False)
	xmin = -85
	xmax = +85
	xrng = xmax - xmin
	ymin = -85
	ymax = +85
	yrng = ymax - ymin
	ax.set_xlim (xmin, xmax)
	ax.set_ylim (ymin, ymax)
	
	# Use a predefined colormap
	colormap = []
	
	# Draw multiple ellipses with different colors and style. All are perfectly superposed
	ellipse = mpl.patches.Ellipse (  # Base one, with big black line for reference
		ORIGIN, xrng, yrng,
		color='k', fill=False, zorder=3) # TODO what is zorder ?

	# Define some clipping paths
	# One for each area
	#clips = [
	#	mpl.patches.Arc (  # One covering right half of your ellipse
	#		ORIGIN, xrng, yrng, theta1=0, theta2=360,
	#		visible=False  # We do not need to display it, just to use it for clipping
	#	),
	#]
	clips = []
	#colormap.append ('purple')
	
	X, Y = ORIGIN
	ll = xmin, ymin
	w, h = xrng / 2, yrng
	lrect = ll, w, h
	ll = xmin + w, ymin
	rrect = ll, w, h
	
	if lunacity < .25:       # 0   ,  .25 => new moon, first quarter moon
		print ("q0-q1")
		
		lun = lunacity * 4   # 0   , 1.
		lun = 1 - lun        # 1   , 0.
		
		rx, ry = xrng * lun, yrng
		
		# dark left, dark middle, light right
		light_patch = mpl.patches.Rectangle ( # right half
			*rrect, visible=False)
		dark_patch = mpl.patches.Ellipse ( # center
			ORIGIN, rx, ry, visible=False)
		dark_patch2 = mpl.patches.Rectangle ( # left half
			*lrect, visible=False)
		colormap.append ('black')
		colormap.append ('white')
		colormap.append ('black')
		clips.append ( dark_patch2)
		clips.append (light_patch)
		clips.append ( dark_patch)
		
	elif lunacity < .5:       #  .25,  .5  => first quarter moon, full moon
		print ("q1-q2")
		
		assert .25 <= lunacity
		lun = lunacity - .25 # 0.  ,  .25
		assert lun >= 0
		assert lun < .25
		lun = lun * 4        # 0.  , 1.
		assert lun >= 0
		assert lun < 1
		
		rx, ry = xrng * lun, yrng
		
		# dark left, light middle, light right
		light_patch2 = mpl.patches.Rectangle (  # right
			*rrect, visible=False)
		dark_patch = mpl.patches.Rectangle (  # left
			*lrect, visible=False)
		light_patch = mpl.patches.Ellipse (  # middle
			ORIGIN, rx, ry, visible=False)
		colormap.append ('white')
		colormap.append ('black')
		colormap.append ('white')
		clips.append (light_patch2)
		clips.append ( dark_patch)
		clips.append (light_patch)
	elif lunacity < .75:     #  .5 ,  .75 => full moon, third quarter moon
		print ("q2-q3")
		
		assert .5 <= lunacity
		lun = lunacity - .5  # 0.  ,  .25
		assert lun >= 0
		assert lun < .25
		lun = lun * 4        # 0.  , 1.
		assert lun >= 0
		assert lun < 1
		lun = 1 - lun        # 1.  , 0.
		assert lun > 0
		assert lun <= 1
		rx, ry = xrng * lun, yrng
	
		# light left, light middle, dark right
		light_patch2 = mpl.patches.Rectangle (  # left
			*lrect, visible=False)
		dark_patch = mpl.patches.Rectangle (  # right
			*rrect, visible=False)
		light_patch = mpl.patches.Ellipse (  # middle
			ORIGIN, rx, ry, visible=False)
		colormap.append ('white')
		colormap.append ('black')
		colormap.append ('white')
		clips.append (light_patch2)
		clips.append ( dark_patch)
		clips.append (light_patch)
	elif lunacity < 1.0:     #  .75, 1.   => third quarter moon, full moon
		print ("q3-q4")

		assert .75 <= lunacity
		lun = lunacity - .75 # 0.  ,  .25
		assert lun >= 0
		assert lun < .25
		lun = lun * 4        # 0.  , 1.
		assert lun >= 0
		assert lun < 1
		
		rx, ry = xrng * lun , yrng
		
		# light left, dark middle, dark right
		dark_patch2 = mpl.patches.Rectangle (  # right
			*rrect, visible=False)
		light_patch = mpl.patches.Rectangle (  # left
			# apparently +90 to +270 is the same as +0 to +360 in matplotlib.
			*lrect, visible=False)
		# because matplotlib doesn't understand angles, drawing patch3 will hide light_patch
		#dark_patch3 = mpl.patches.Arc (  # right
		#	ORIGIN, xrng, yrng, theta1=-90, theta2=+90, visible=False)
		dark_patch = mpl.patches.Ellipse (  # middle
			ORIGIN, rx, ry, visible=False)
		colormap.append ('black')
		colormap.append ('white')
		#colormap.append ('black')
		colormap.append ('black')
		clips.append ( dark_patch2)
		clips.append (light_patch)
		#clips.append ( dark_patch3)
		clips.append ( dark_patch)
	
	n = len (clips)
	# Ellipses for your sub-areas.
	# Add more if you want more areas
	# Apply the style of your areas here (colors, alpha, hatch, etc.)
	areas = [
		mpl.patches.Ellipse (
			ORIGIN, xrng, yrng,  # Perfectly fit your base ellipse
			color=colormap [i], fill=True, alpha=1.0,  # Add some style, fill, color, alpha
			zorder=i)
		for i in range (n)  # Here, we have 3 areas
	]

	# Add all your components to your axe
	ax.add_patch (ellipse)
	for area, clip in zip (areas, clips):
		ax.add_patch (area)
		ax.add_patch (clip)
		area.set_clip_path (clip)  # Use clipping paths to clip you areas



from pygameplotlib import PyGamePlotLib
import datetime
from datetime import timedelta
import ephem

moon_name_db = ('wolf', 'snow', 'worm', 'pink', 'flower', 'strawberry', 'buck', 'sturgeon', 'corn', 'harvest', "hunter's", 'beaver', 'cold', 'blue')
def get_moon_name_helper (moon_no):
	if moon_no is None: name = 'blue'
	else:               name = moon_name_db[moon_no]
	name = "%s moon" % (name,)
	return name
class MoonApp (PyGamePlotLib):
	def __init__ (self, observer=None, *args, **kwargs):
		PyGamePlotLib.__init__ (self, *args, **kwargs)
		self.name = None
		self.set_time (compute=False)
	def notify (self, time=None): self.set_time (time)
	def set_time (self, time=None, compute=True):
		if time is None: time = datetime.datetime.utcnow ()
		self.time = time
		if compute: self.compute ()
	def compute_helper (self, fig):
		PyGamePlotLib.compute_helper (self, fig)
		
		time     = self.time
		if time is None: return
		
		self.phase = self.get_moon_phase ()
		
		#ax  = fig.add_subplot (facecolor='black')
		ax  = fig.add_subplot ()
		ax.get_xaxis ().set_visible (False)
		ax.get_yaxis ().set_visible (False)
		ax.patch.set_visible (False)
		arc_patch (ax, self.phase)
		
		"""
		if self.phase < .25:
			# TODO waxing crescent
			x = w / 2
			y = h / 2
			start_angle = SOUTH.radians ()
			stop_angle  = NORTH.radians ()
			color = (200, 200, 200)
			for r in range (1, inf):
				pygame.gfxdraw.arc (self.ss, x, y, r, start_angle, stop_angle, color)
			pass
		elif self.phase == .25:
			# TODO first quarter
			pass
		elif self.phase < .5:
			# TODO waxing gibbous
			pass
		elif self.phase == .5:
			# TODO full moon
			pass
		elif self.phase < .75:
			# TODO waning gibbous
			pass
		elif self.phase == .75:
			# TODO third quarter
			pass
		elif self.phase < 1:
			# TODO waning crescent
			pass
		else:
			# TODO new moon
			pass
		"""
		
		
	def get_moon_phase (self): # https://michelanders.blogspot.com/2011/01/moon-phases-with-pyephem.html
	#	g = self.observer
		time = self.time
		time = ephem.Date (time)
		nnm = ephem.next_new_moon (time)  
		pnm = ephem.previous_new_moon (time)  
		# for use w. moon_phases.ttf A -> just past  newmoon,  
		# Z just before newmoon  
		# '0' is full, '1' is new  
		# note that we cannot use m.phase as this is the percentage of the moon  
		# that is illuminated which is not the same as the phase!  
		lunation = (time - pnm) / (nnm - pnm)  
		return lunation
	"""
	def set_subsurface (self, ss):
		CircleApp.set_subsurface (self, ss)
		self.compute ()
	def draw_scene (self, temp=None):
		CircleApp.draw_scene (self, temp)
		if temp is None: temp = self.ss
		if self.computed_image is None: self.compute ()
		if self.computed_image is None: return
		temp.blit (self.computed_image, ORIGIN)
	"""
	"""
	def run_loop (self, events, keys): # TODO move this to the GUI ?
		if isinstance (self.gps, Client): self.gps.Loop ()
		if isinstance (self.gps, Server): self.gps.Pump ()
		self.set_time ()
		PyGamePlotLib.run_loop (self, events, keys)
	"""
	"""
	def run_loop (self, events, keys): # TODO move this to the GUI ?
		#if isinstance (self.gps, Client): self.gps.Loop ()
		#if isinstance (self.gps, Server): self.gps.Pump ()
		time = self.time
		time = time + timedelta (hours=9)
		self.set_time (time)
		PyGamePlotLib.run_loop (self, events, keys)
	"""
	#def set_gps (self, gps):
	#	self.gps = gps
	#	self.set_observer (gps.observer)
	
	def get_moon_name (self): return self.get_moon_names ()[-1]
	def get_moon_names (self):
		times = self.get_full_moon_times ()
		moon_no = 0
		name    = get_moon_name_helper (moon_no)
		names   = [name]
		time    = times[0]
		month   = time.month
		for time in times[1:]:
			month2 = time.month
			if month == month2: name = get_moon_name_helper (None)
			else:
				moon_no = moon_no + 1
				name    = get_moon_name_helper (moon_no)
			names.append (name)
			month = month2
		names = tuple (names)
		print ("names: %s" % (tuple (zip (names, times)),))
		return names		
		
	def get_full_moon_times (self):
		time = self.time
		ny   = time.replace (month=1, day=1, hour=0, minute=0, second=0)
		assert time > ny
		#time = ephem.Date (time)
		#ny   = ephem.Date (ny)
		nfm  = ephem.    next_full_moon (time).datetime ()
		
		times = [nfm]
		while True: # >= ?
			pfm = ephem.previous_full_moon (time).datetime ()
			if pfm <= ny: break
			time = pfm
			times.append (time)
		assert pfm  <= ny
		assert time >= ny
		
		times = times[::-1]
		times = tuple (times)
		return times

from circle_app import CircleApp
	
def blit_alpha (target, source, location, opacity): # https://nerdparadise.com/programming/pygameblitopacity
	x, y = location
	temp = pygame.Surface ((source.get_width (), source.get_height ())).convert ()
	temp.blit (target, (-x, -y))
	temp.blit (source, ORIGIN)
	temp.set_alpha (opacity)        
	target.blit (temp, location)
	
#def get_pic_name (name): # use name as query param, return URL of resource ?
#	return "shiva.png"
	
class CircleMoonApp (CircleApp, MoonApp):
	# TODO compute moon name, fetch background
	def __init__ (self, notify_art=None, rotation=None, *args, **kwargs):
		CircleApp.__init__ (self, rotation, *args, **kwargs)
		MoonApp   .__init__ (self,           *args, **kwargs)
		self.pic_name = None
		self.raw_pic  = None
		self.pic      = None
		self.notify_art = notify_art
	def start_running (self):
		CircleApp.start_running (self)
		MoonApp   .start_running (self)
	def  stop_running (self):
		CircleApp.stop_running (self)
		MoonApp   .stop_running (self)
	def set_subsurface (self, ss):
		CircleApp.set_subsurface (self, ss)
		# TODO handle geometries&rotations here
		MoonApp   .set_subsurface (self, None, True)
	def compute (self):
		MoonApp.compute (self)
		
		name = self.name
		self.name = self.get_moon_name ()
		#pic_name = self.pic_name
		if name != self.name:
			if self.notify_art is not None: self.notify_art (self.name) # notify troller
			#self.pic_name = get_pic_name (self.name)                # use self.name as query param to get resource
		#raw_pic = self.raw_pic
		#if pic_name != self.pic_name:
		#	self.raw_pic = pygame.image.load (self.pic_name)             # load resource
		#	self.raw_pic = self.raw_pic.convert_alpha ()
		#	self.set_background (self.pic_name)
		#pic = self.pic
		#if raw_pic != self.raw_pic:
		#	self.pic     = pygame.transform.scale (self.raw_pic, (w, h)) # prepare resource for blitting
	def notify_bg (self, pic_name):
		if pic_name == self.pic_name: return
		self.pic_name = pic_name
		self.set_background (self.pic_name)
	#def draw_cropped_scene (self, temp):
	#	#MapApp   .draw_scene         (self, temp)
	#	CircleApp.draw_cropped_scene (self, temp)
	#	
	#	size = temp.get_size ()
	#	moon = pygame.Surface (size)
	#	MoonApp   .draw_scene    (self, moon)
	#	opacity = 100
	#	blit_alpha (temp, moon, ORIGIN, opacity)
	def draw_foreground (self, temp):
		CircleApp.draw_foreground (self, temp)
		
		size = temp.get_size ()
		moon = pygame.Surface (size)
		MoonApp   .draw_foreground (self, moon)
		opacity = 255 / 2
		blit_alpha (temp, moon, ORIGIN, opacity)
	def positive_space (self, is_root=True): raise Exception ()
	def negative_space (self, is_root=True): raise Exception ()
	def minsz          (self): raise Exception ()

if __name__ == "__main__":
	#from gps_client import GPSClient
	#from artwork_client import ArtworkClient
	from hal import HAL9000

	def main ():
		a = CircleMoonApp ()
		n = a.notify_bg # cb for artwork client to set background of moon app
		b = ArtworkClient (n)
		#a.notify_art = b.notify_request # cb for moon app to request background from artwork client
		def new_loop (events, keys):
			self = a
			time = self.time
			time = time + timedelta (hours=9)
			self.set_time (time)
			PyGamePlotLib.run_loop (self, events, keys)
		a.run_loop = new_loop
		with HAL9000 (app=a) as G:
			#h = "localhost"
			#p = 1717
			#n = a.set_observer
			#g = GPSClient (h, p, n)
			#a.set_gps (g)
			G.run ()
	main ()
	quit ()
