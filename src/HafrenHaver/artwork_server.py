#! /usr/bin/env python3

from server import PlayerChannel, PlayerServer
from artwork import Artwork

def results_msg (results):
	#(
	#	(883, 500, 'cache/50e7dc454354b108f5d084609629377c123edbe4574c704f752c7bd29e4ec751_1280.jpg', {'https://pixabay.com', 'skeeze'}),
	#	(883, 500, 'cache/54e4d7474b52a914f6da8c7dda79367e1738dfe052556c48732f78d49144c65ab1_1280.jpg', {'https://pixabay.com', 'peejhunt'})
	#)
	#tuple of tuples of int,    int,         filename, set of credits
	#                   vtotal, vtotal_hits, res,      vcreds
	s = []
	for result in results:
		vtotal, vtotal_hits, res, vcreds = result
		t = str (vtotal), str (vtotal_hits), str (res), str (vcreds)
		s.append (t)
	return str (s)
	#return str (results)
	#s = str (tuple (map (lambda s: str (s), results)))
	#print ("s: %s" % (s,))
	#return s

class ArtworkChannel (PlayerChannel):
	def __init__ (self, *args, **kwargs): PlayerChannel.__init__ (self, *args, **kwargs)
	def Network_queries (self, data):
		queries = data['queries']
		queries = tuple (queries)
		self._server.SendResult (self, queries)

class ArtworkServer (PlayerServer, Artwork):
	channelClass = ArtworkChannel
	def __init__ (self, artwork, localaddr, *args, **kwargs):
		PlayerServer.__init__ (self, localaddr=localaddr, *args, **kwargs)
		Artwork     .__init__ (self, artwork.recycler, *args, **kwargs)
		self.artwork = artwork
	def Connected (self, channel, addr):
		PlayerServer.Connected (self, channel, addr)
		#self.SendObserver (channel)
	def SendResult  (self, player, queries):
		#results = self.artwork.req (*queries)
		q = { 'qs' : ('test',) }
		q = (1, q)
		print ("artwork: %s" % (self.artwork,))
		results = self.artwork.req (q)
		results = results_msg (results)
		player.Send ({"action": "results", "results": results})
	#def set_artwork (self, artwork):
	#	self.artwork = artwork # TODO req ?
		#self.SendObservers ()
		 # TODO notiy GUI
		 
if __name__ == "__main__":
	from artwork import default_artwork
	
	def main ():
		def cb (r):
			s.Launch ()
			"""
			p  = r.req (n=2, qs=('test',))
			
			print (p)
			print ()
			for h in p:
				print (h)
				print ()
				
			p  = r.req (n=2, qs=('test',))
			print (len (tuple (p)))
			"""
		g = default_artwork (cb)
		host, port = "0.0.0.0", 1717
		s = ArtworkServer (g, localaddr=(host, int (port)))
	main ()
	quit ()
