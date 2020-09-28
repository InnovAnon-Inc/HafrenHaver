#! /usr/bin/env python3

from PodSixNet.Channel import Channel

class ClientChannel (Channel):
	def Network (self, data):
		#print data
		pass
	#def Network_myaction (self, data):
		#print "myaction:", data









from PodSixNet.Server import Server
from weakref import WeakKeyDictionary

from constants import DEFAULT_HOST, DEFAULT_PORT


	
class HHServer (Server):
	channelClass = ClientChannel
	
	def __init__ (self, host=DEFAULT_HOST, port=DEFAULT_PORT, *args, **kwargs):
		Server.__init__(self, *args, localaddr=(host, int (port)), **kwargs)
		self.players = WeakKeyDictionary()
		print ("host: %s, port: %s" % (host, port))
		
	def Connected (self, channel, addr): self.AddPlayer (channel)
    
	def AddPlayer (self, player): self.players[player] = True
		
	def DelPlayer (self, player): del self.players[player]
        
	def SendToAll (self, data):
		for p in self.players: p.Send (data)
		
	def Launch (self):
		while True:
			self.Pump ()
	
		# need to be able to adjust solfeggio
		# need to be able to generate songs
		# duration of song => amount of time to for solfeggio
		
	def recv_solfeggio (self): pass
	def send_solfeggio (self): pass
		
		
		
class ServerGUI:
	def __init__ (self, server, gui):
		self.server = server
		self.gui    = gui
		
		# need to be able to adjust solfeggio and send to server
		# display sine wave graph
		# play pure tone
		
		# gui controls server
		# clients have ro access to server

if __name__ == "__main__":
	def main ():
		for port in random_default_ports ():
			try:
				with HHServer (port=port) as s: s.Launch ()
				break
			except PermissionError as e: print ("port: %s, e: %s" % (port, e))
	main ()
	quit ()
