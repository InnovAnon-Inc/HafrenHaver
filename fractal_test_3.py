#! /usr/bin/env python3

from cropping_app import CroppingApp


import pygame

from geom import SQUARE, DIAMOND, CIRCLE, ANGLE_N, ANGLE_E, ANGLE_S, ANGLE_W
from recursive_composite import RecursiveComposite

if __name__ == "__main__":
	from rotation import ANGLED, STRAIGHT
	from orientation import NORTH, SOUTH, EAST, WEST
	from circled_square import CircledSquare
	from squared_circle import SquaredCircle
	from circled_angle import CircledAngle
	from angled_circle import AngledCircle
	from app import App
	from constants import DEFAULT_BACKGROUND, SECONDARY_BACKGROUND
	from gui import GUI
	from constants import BLACK
	from square_app import SquareApp
	from hal import HAL9000
	
	def main ():
		d = None
		r = ANGLED
		r = STRAIGHT
		c = SquaredCircle (d, rotation=r)
		b = CircledSquare (c, background=SECONDARY_BACKGROUND)
		a = RecursiveComposite (b)
		with HAL9000 (app=a) as g:
			g.run ()
	main ()
	quit ()
