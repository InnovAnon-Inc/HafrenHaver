from __future__ import division

class GuiUtil:
	@staticmethod
	def normalize_window_point (point, win):
		x = (point[0] + 1) * win.getWidth () / 2
		y = (point[1] + 1) * win.getHeight () / 2
		return Point (x, y)
	@staticmethod
	def normalize_window_polygon (pgon, win):
		return Polygon ([normalize_window_point (p, win) for p in pgon])
	@staticmethod
	def display_points (points, win):
		for p in points:
			pt = normalize_window_point (p, win)
			pt.draw (win)
	@staticmethod
	def bjorklund_polygon (scale, points):
		for sp in zip (scale, points):
			(s, p) = sp
			if s is not 0: yield p
	@staticmethod
	def display_polygon (pgon, win):
		normalize_window_polygon (pgon, win).draw (win)
	@staticmethod
	def display_constellation (points, win):
		center = normalize_window_point ((0, 0), win)
		for p in points:
			pt = normalize_window_point (p, win)
			#pt.draw (win)
			l = Line (center, pt)
			l.draw (win)
	@staticmethod
	def display_bjorklund (scale):
		win = GraphWin ()
		pts = list (points (normalize_radians (
			equal_spacing (len (scale)))))
		#display_points (pts, win)
		display_constellation (pts, win)
		pgon = list (bjorklund_polygon (scale, pts))
		display_constellation (pgon, win)
		display_polygon (pgon, win)
		#win.promptClose ()
	@staticmethod
	def display_bjorklund_scale (scale, bjork):
		win = GraphWin ()
		pts = list (points (normalize_radians (
			normalize_frequency (normalize_octave (scale)))))
		#display_constellation (pts, win)
		display_polygon (pts, win)
		pgon = list (bjorklund_polygon (bjork, pts))
		display_constellation (pgon, win)
		display_polygon (pgon, win)
		#win.promptClose ()
	@staticmethod
	def display_scale (scale):
		win = GraphWin ()
		pts = list (points (normalize_radians (
			normalize_frequency (normalize_octave (scale)))))
		#display_points (pts, win)
		display_constellation (pts, win)
		display_polygon (pts, win)
		#win.promptClose ()
		#win.close ()