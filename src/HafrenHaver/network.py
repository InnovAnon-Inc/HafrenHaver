#! /usr/bin/env python3

from numerology import numerology
from random import shuffle
	
def is_valid_port (k):
	k = int (k)
	if k <= 0:        return False
	if k > (1 << 15): return False
	return True
def default_ports ():
	ns = numerology ()
	ports     = filter (is_valid_port, ns)
	# TODO check root and port range
	# TODO filter out commonly used ports
	ports     = tuple (ports)
	return ports
def random_default_ports ():
	ports = default_ports ()
	ports = list (ports)
	shuffle (ports)
	return tuple (ports)
def random_default_port (): return random_default_ports ()[0]

if __name__ == "__main__":
	def main ():
		print (random_default_ports ())
	main ()
	quit ()
