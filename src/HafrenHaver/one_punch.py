#! /usr/bin/env python3

from itertools import cycle

class OnePunch:
	def __init__ (self, artwork): self.artwork = artwork
	def req (self, *queries):
		k = self.artwork.req (*queries)
		return cycle (k)
		
if __name__ == "__main__":
	from artwork import default_artwork

	def main (): # TODO write a program that terminates
		def cb (r):
			p  = r.req (n=2, qs=('test',))
			
			print (p)
			print ()
			for h in p:
				print (h)
				print ()
			
			p  = r.req (n=2, qs=('test',))
			print (len (tuple (p)))
			
		r = default_artwork (cb)
		o = OnePunch (r)
		print ("o: %s" % (o,))
	main ()
	quit ()
