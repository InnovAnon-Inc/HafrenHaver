#! /usr/bin/env python3

from server import PlayerChannel, PlayerServer
from artwork import Artwork

class ArtworkChannel (PlayerChannel):
	def __init__ (self, *args, **kwargs): PlayerChannel.__init__ (self, *args, **kwargs)
	#def Network_message (self, data):
    #    self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})

class ArtworkServer (PlayerServer, Artwork):
	channelClass = ArtworkChannel
	def __init__ (self, *args, **kwargs):
		PlayerServer.__init__ (self, *args, **kwargs)
		Artwork     .__init__ (self, *args, **kwargs)
		self.artwork = artwork
	def Connected (self, channel, addr):
		PlayerServer.Connected (self, channel, addr)
		self.SendObserver (channel)
	def SendObserver  (self, player): player.Send      ({"action": "observer", "observer": observer_msg (self.observer)})
	def SendObservers (self):         self  .SendToAll ({"action": "observer", "observer": observer_msg (self.observer)})
	def set_artwork (self, artwork):
		self.artwork = artwork # TODO req ?
		self.SendObservers ()
		 # TODO notiy GUI
		 
if __name__ == "__main__":
	from artwork import default_artwork
	
	def main ():
		g = default_artwork ()
		host, port = "0.0.0.0", 1717
		s = ArtworkServer (g, localaddr=(host, int (port)))
		s.Launch ()
	main ()
	quit ()
