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




class TextRing (CircledPolygon): # circled polygon with polygon'd circle # number of sides of polygon based on text
	def __init__ (self, text, font=None, child):
		if not isinstance (child, PolygonedCircle):
			assert isinstance (child, CircleApp)
			child = PolygonedCircle.__init__ (self, None, child)
		CircledPolygon.__init__ (self, child)
		self.text = text
		self.font = font
	def set_subsurface (self, ss):
		CircledPolygon.set_subsurface (self, ss)
		if self.font is None:
			df        = pygame.font.get_default_font ()
			font      = pygame.font.Font (df, 8)
			self.font = font
		texts, tw, th, minn, maxn, x, y, w, h = self.compute_sizes ()
		# TODO handle change in sizes
		self.texts    = texts
		self.tw       = tw
		self.th       = th
		self.minn     = minn
		self.maxn     = maxn
		self.x        = x
		self.y        = y
		self.w        = w
		self.h        = h
		#self.next_cycle ()
	def compute_sizes (self):
		text = self.text
		print ("text: %s" % (text,))
		N = len (text)
		print ("N: %s" % (N,))
		font = self.font
		
		crfg = (0, 255, 0, 255)
		f = lambda c: (font.render (c, True, crfg), *font.size (c))
		g = lambda c: str (c)
		texts = map (g, text)
		texts = map (f, texts)
		texts = tuple (texts) # image, w, h

		f = lambda iwh: iwh[1] 
		tw = max (texts, key=f)[1]
		f = lambda iwh: iwh[2]
		th = max (texts, key=f)[2]
		print ("tw: %s, th: %s" % (tw, th))
		
		# each char of text is rotated => text is a polygon, circle is inscribed
		X, Y, W, H = self.inner_rect ()                                   # outer radii
		print ("(X, Y): (%s, %s) (W: %s, H: %s)" % (X, Y, W, H))
		#w, h = W - 2 * tw, H - 2 * th                                   # make room for text aligned at axes
		x, y, w, h = X + tw / 2, Y + th / 2, W - tw, H - th # text center
		print ("w: %s, h: %s" % (w, h))
		# text is rendered between outer and inner radii
		
		minn   = 3                                                      # min number of chars that will look "arcane"
		n      = minn
		while True: # TODO if the formula doesn't work, at least use an interpolated binary search
			n      = n + 1
			i      = 0
			theta1 = (i + 0) / n * 2 * pi
			theta2 = (i + 1) / n * 2 * pi
			dx     = cos (theta2) - cos (theta1)
			dy     = sin (theta2) - sin (theta1)
			sl     = sqrt (pow (W * dx, 2) + pow (H * dy, 2))           # side length of polygon
			if sl < tw: break
		maxn = n - 1
		print ("maxn: %s" % (maxn,))
		assert maxn >= minn * (minn + 1)                                # lower bound is minn^2, and the numbers must be different
		
		return texts, tw, th, minn, maxn, x, y, w, h
	
	def transform_helper (self, text, w, h, angle):
		intermediate_alpha_surface = pygame.Surface ((w, h), flags=pygame.SRCALPHA)
		intermediate_alpha_surface.fill (pygame.Color (*OPAQUE))
		text_rect = text.get_rect ()
		text_rect.center = (w / 2, h / 2)
		intermediate_alpha_surface.blit (text, text_rect, special_flags=pygame.BLEND_RGBA_MIN)
		
		# when angle is   0    , rad is - pi / 2
		# when angle is +pi / 2, rad is 0
		# when angle is  pi    , rad is + pi / 2
		# when angle is -pi / 2, rad is 0
		#if 0 <= angle and angle <= pi: rad = angle
		#else:                          rad = angle - pi
		rad = angle	- pi / 2
		#orientation = NORTH
		
		degrees = to_degrees (rad)
		#degrees = 0
		xform = pygame.transform.rotate (intermediate_alpha_surface, degrees)
		#xform = pygame.transform.rotate (text, angle)
		return xform
	def get_transforms (self):
		texts  = self.texts # image, w, h
		angles = self.angles
		# TODO might have to blit onto a temp surface
		f = lambda text, angle: self.transform_helper (*text, angle)
		ntext  = len (texts)
		nangle = len (angles)
		#assert ntext == nangle, "ntext: %s, nangle: %s" % (ntext, nangle)
		k = zip (cycle (texts), angles)
		xforms = starmap (f, k)
		xforms = tuple (xforms)
		return xforms
		
	# def minsz: minsz of inner circle... + tw, th => minsz of outer
	# 3 * 4 = 12 points on polygon...  
	#def draw_foreground (self, temp):
	def draw_cropped_scene (self, temp):
		print ("circular_matrix_text.draw_foreground ()")
		#CircleApp.draw_foreground (self, temp)
		CircledPolygon.draw_cropped_scene (self, temp)
		xforms = self.xforms # image, w, h
		n      = self.n
		ndx    = self.sectioni
		pts    = self.pts
		angles = self.angles		
		print ("nsection: %s, ndx: %s" % (len (self.sections), ndx))
		#k, section = self.sections[ndx]
		section = self.sections[ndx]
		#for i in range (0, n, k):
		for i in section:
			theta = angles[i]
			xform = xforms[i]
			pt    = pts[i]

			#rect  = text.get_rect ()
			rect = xform.get_rect ()
			rect.center = (round (pt[0]), round (pt[1]))
			temp.blit (xform, rect)			
			
		self.increment_section_index () # TODO move this to the troller
# TODO after TextRing, rewrite MagicCircle


















class CircleStatChartInner (CircledPolygon): # polygon radii as a function of stats
	def __init__ (self, n):
		CircledPolygon.__init__ (self, n)
class CircleStatChart (TextRing): # labelled stat chart inner
	def __init__ (self, labels):
		n = len (labels)
		TextRing.__init__ (self, n, CircleStatChartInner (n))
		
class SquareStatChartInner (SquareApp): pass
class SquareStatChart (SquareApp): pass



class ATP (StatChart):
	def __init__ (self):
		StatChart.__init__ (self, ('altitude', 'temperature', 'pressure'))
	def set_inner_background (self, background): self.child.set_background (background)
	def get_radius (self, raw): # https://stackoverflow.com/questions/42140347/normalize-any-value-in-range-inf-inf-to-0-1-is-it-possible
		if raw is None: return 0
		radius   = (erf (raw) + 1) / 2
		return radius
	
	def get_altitude_radius    (self, alti): return self.get_radius (alti)
	def get_temperature_radius (self, temp): return self.get_radius (temp)
	def get_pressure_radius    (self, pres): return self.get_radius (pres)
		
	def set_altitude (self, alt):
		self.rads['altitude'] = (alt, self.get_altitude_radius (alt))
		self.compute ()
	def set_temperature (self, temp):
		self.rads['temperature'] = (temp, self.get_temperature_radius (temp))
		self.compute ()
	def set_pressure (self, press):
		self.rads['pressure'] = (press, self.get_pressure_radius (press))
		self.compute ()
	








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
		self.atp = AngleATP ()
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
		self.thermometer.notify (observer.temp)
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
		self.thermometer.set_subsurface (ss2)
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
		self.thermometer.draw_foreground (ss2)
		#self.barometer  .draw_foreground (ss3)
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
			g = GPSClient (h, p, n)
			#g = AddrGPS ("7271 Wurzbach Rd, San Antonio, TX 78240")
			#g = CityGPS ("Dallas, TX")
			#host, port = "0.0.0.0", 1717
			#g = GPSServer (g, localaddr=(host, int (port)))
			a.set_gps (g)
			
			G.run ()
	main ()
	quit ()
