#! /usr/bin/env python3

from PodSixNet.Connection import connection, ConnectionListener

class Client (ConnectionListener):
	def __init__ (self, host, port):
		self.is_connected = None
		self.is_running = None
		self.Connect ((host, port))
		
		#connection.Send({"action": "nickname", "nickname": stdin.readline().rstrip("\n")})
		
		
	def Loop (self):	
		connection.Pump ()
		self      .Pump ()
	"""
	def InputLoop(self):
		# horrid threaded input loop
		# continually reads from stdin and sends whatever is typed to the server
		while 1:
			connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})
	"""

	# built in stuff

	def Network_connected (self, data):
		print ("You are now connected to the server")
		self.is_connected = True
	def Network_error (self, data):
		print ('error:', data['error'][1])
		connection.Close ()
		self.is_connected = False
	def Network_disconnected (self, data):
		print ('Server disconnected')
		self.is_connected = False
		#exit()
		
	def run (self):
		#while self.is_connected is None or self.is_connected == True:
		self.is_running = True
		while self.is_running:
			self.Loop    ()
			self.do_tick ()
	def do_tick (self):
		#self.clock.tick (DEFAULT_TICK_SPEED)
		pass
		
if __name__ == "__main__":
	def main ():
		host = "localhost"
		port = 1717
		c    = Client (host, int (port))
		#while c.is_connected:
		#	c.Loop ()
		#	sleep (0.001)
		c.run ()
	main ()
	quit ()
