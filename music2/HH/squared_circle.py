#! /usr/bin/env python3

from composite_app import CompositeApp
from circle_app import CircleApp
from square_app import SquareApp
	
class SquaredCircle (SquareApp, CompositeApp):
	def __init__ (self, child, *args, **kwargs):
		SquareApp   .__init__ (self,        *args, **kwargs)
		CompositeApp.__init__ (self, child, *args, **kwargs)
		assert isinstance (child, CircleApp)
	def set_subsurface (self, ss):
		SquareApp   .set_subsurface (self, ss)
		CompositeApp.set_subsurface (self, self.ss)
		ss = self.ss
		rect = self.bounds
		ss2 = ss.subsurface (rect)
		self.inner_bounds = rect
		self.child.set_subsurface (ss2)
	def draw_cropped_scene (self, temp):
		SquareApp.draw_cropped_scene (self, temp)
		rect = self.bounds
		ss2 = temp.subsurface (rect)
		self.child.set_subsurface (ss2)
		#self.child.draw_cropped_scene (ss2)
		self.child.draw_scene (ss2)

if __name__ == "__main__":
	from app import SECONDARY_BACKGROUND
	from gui import GUI
	
	def main ():
		b = CircleApp (background=SECONDARY_BACKGROUND)
		a = SquaredCircle (b)
		with GUI (app=a) as g:
			#g.setApp (a)
			g.run ()
	main ()
	quit ()
