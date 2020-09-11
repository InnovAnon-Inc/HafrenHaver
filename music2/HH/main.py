#! /usr/bin/env python3

from mode import random_mode

def main ():
	mode = random_mode ()
	for index in range (0, len (mode.scale.intervals)):
		print (mode.pitch    (index, 0))
		print (mode.function (index))
		print ()

if __name__ == "__main__":
	main ()

