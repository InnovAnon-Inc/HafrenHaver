#! /usr/bin/env python3

from PodSixNet.Server import Server as PSNServer
	
class Server (PSNServer):
	#channelClass = Channel
	
	def __init__ (self, *args, **kwargs):
		PSNServer.__init__ (self, *args, **kwargs)
		print ('Server launched')
		self.is_running = True
	
	def Launch (self):
		while self.is_running:
			self.Pump ()
			#sleep (0.0001)
			self.do_tick ()
	def do_tick (self): pass

from PodSixNet.Channel import Channel

class PlayerChannel (Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__ (self, *args, **kwargs):
        #self.nickname = "anonymous"
        Channel.__init__ (self, *args, **kwargs)
    
    def Close (self):
        self._server.DelPlayer (self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################
    """
    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "who": self.nickname})
    
    def Network_nickname(self, data):
        self.nickname = data['nickname']
        self._server.SendPlayers()
	"""
	

from weakref import WeakKeyDictionary	

class PlayerServer (Server):
	#channelClass = PlayerChannel
	
	def __init__ (self, *args, **kwargs):
		Server.__init__ (self, *args, **kwargs)
		self.players = WeakKeyDictionary ()
		
	def Connected (self, channel, addr):
		self.AddPlayer (channel)
	
	def AddPlayer (self, player):
		print ("New Player" + str (player.addr))
		self.players[player] = True
	#    self.SendPlayers ()
		print ("players", [p for p in self.players])
	
	def DelPlayer (self, player):
		print ("Deleting Player" + str (player.addr))
		del self.players[player]
	#    self.SendPlayers ()
	
	#def SendPlayers (self):
	#    self.SendToAll ({"action": "players", "players": [p.nickname for p in self.players]})
	
	def SendToAll (self, data): [p.Send (data) for p in self.players]
	










		
		# need to be able to adjust solfeggio and send to server
		# display sine wave graph
		# play pure tone
		
		# gui controls server
		# clients have ro access to server

if __name__ == "__main__":
	def main ():
		"""
		for port in random_default_ports ():
			try:
				with HHServer (port=port) as s: s.Launch ()
				break
			except PermissionError as e: print ("port: %s, e: %s" % (port, e))
		"""
		host, port = "0.0.0.0", 1717
		s = PlayerServer (localaddr=(host, int (port)))
		s.Launch ()
	main ()
	quit ()
