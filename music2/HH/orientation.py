#! /usr/bin/env python3

from enum import Enum

class Orientation (Enum):
	NORTH = 0
	EAST  = 1 # "est"
	SOUTH = 2
	WEST  = 3 # "weest"
NORTH = Orientation.NORTH
EAST  = Orientation.EAST
SOUTH = Orientation.SOUTH
WEST  = Orientation.WEST
