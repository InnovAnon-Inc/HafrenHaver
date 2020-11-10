#! /usr/bin/env python3

from client  import Client
from artwork import Artwork

def results_msg (results): return results

class ArtworkClient (Client, Artwork):
	def __init__ (self, *args, **kwargs):
		Client .__init__ (self, *args, **kwargs)
		Artwork.__init__ (self, *args, **kwargs)
	def Network_results (self, data):
		print("*** results: " + data['results'])
		results      = data['results']
		results      = results_msg (results)
		self.results = results
		assert results is not None
		# TODO notify GUI
		self.notify (results)
		#self.is_running = False
		 
if __name__ == "__main__":
	def main ():
		host = "localhost"
		port = 1717
		def cb (results):
			print ("cb (%s)" % (results,))
			for result in results: print (result)
			c.is_running = False
		n = cb
		c = ArtworkClient (host, port, n)
		c.run ()
	main ()
	quit ()
