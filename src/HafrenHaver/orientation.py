#! /usr/bin/env python3

from math import pi
from enum import Enum

class Orientation (Enum):
	NORTH = 0
	EAST  = 1 # "est"
	SOUTH = 2
	WEST  = 3 # "weest"
	def radians (self):
		if self == NORTH: return pi / +2
		if self == EAST:  return 0
		if self == SOUTH: return pi
		if self == WEST:  return pi / -2
		raise Exception ()
NORTH = Orientation.NORTH
EAST  = Orientation.EAST
SOUTH = Orientation.SOUTH
WEST  = Orientation.WEST
