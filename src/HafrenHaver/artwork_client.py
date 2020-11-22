#! /usr/bin/env python3

from PodSixNet.Connection import connection

from client  import Client
from artwork import Artwork

from ast import literal_eval as make_tuple

def results_msg (results): return make_tuple (results)

class ArtworkClient (Client, Artwork):
	def __init__ (self, host, port, cb, *args, **kwargs):
		Client .__init__ (self, host, port, *args, **kwargs)
		Artwork.__init__ (self, None, *args, **kwargs)
	def Network_results (self, data):
		print("*** results: " + data['results'])
		results      = data['results']
		results      = results_msg (results)
		self.results = results
		assert results is not None
		# TODO notify GUI
		self.notify (results)
		#self.is_running = False
	def sendQueries (self, *queries):
		#f = lambda n, kwargs: self.recycler.req (n, **kwargs)
		#return starmap (f, queries)
		connection.Send ({"action": "queries", "queries": str (queries)})
	#def sendQuery   (self, n=1, **kwargs): connection.Send ({"action": "queries", "n": str (n), "query": str (kwargs)})
		 
if __name__ == "__main__":
	def main ():
		host = "localhost"
		port = 1717
		def cb (p):
			print ("cb (%s)" % (p,))
			c.is_running = False
			
			for h in p:
				print (h)
				print ()
				
		n = cb
		c = ArtworkClient (host, port, n)
		c.sendQueries ({'n':2, 'qs':('test',)})
		#c.sendQuery (n=2, qs=('test',))
		#c.sendQueries ((2, ('test',)))
		#c.sendQueries ((n=2, qs=('test',)))
		c.run ()
	main ()
	quit ()
