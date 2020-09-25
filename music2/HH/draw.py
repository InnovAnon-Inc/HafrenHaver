# https://towardsdatascience.com/animations-with-matplotlib-d96375c5442c

import matplotlib.pyplot as plt 
import matplotlib.animation as animation 
import numpy as np 


class Graphics:
	def __init__ (self):
		plt.style.use ('dark_background')
		self.fig = plt.figure () 		
		# setting a title for the plot 
		plt.title ('Creating a growing coil with matplotlib!') 
		# hiding the axis details 
		plt.axis ('off') 
		
		self.frame_rate = 60
		self.animation  = Animation ()
		self.anims      = []
	def append (self, duration_milliseconds=1000):
		frm = 1 / self.frame_rate * 1000  # number of frames per millisecond
		fs  = frm * duration_milliseconds # total number of frames
		frm = int (frm) # TODO
		fs  = int (fs)
		animate = lambda i: self.animation.animate (fs, i)
		
		# call the animator 
		anim = animation.FuncAnimation (self.fig, animate, init_func=self.animation.init, 
							frames=fs, interval=frm, blit=True)
		self.anims.append (anim)
	def save (self, fname='test.gif'):
		# save the animation as mp4 video file 
		self.anims[0].save (fname, writer='imagemagick', extra_anim=self.anims[1:]) 		

class Animation:
	def __init__ (self):		
		ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50)) 
		self.line, = ax.plot([], [], lw=2) 
		
		# lists to store x and y axis points 
		self.xdata, self.ydata = [], [] 

	# initialization function 
	def init(self): 
		# creating an empty plot/frame 
		line.set_data([], []) 
		return line, 

	# animation function 
	def animate(self,fs, i): 
		# t is a parameter 
		#t = 0.1*i 
		t = i / fs
		
		# x, y values to be plotted 
		x = t*np.sin(t) 
		y = t*np.cos(t) 
		
		# appending new points to x, y axes points list 
		self.xdata.append(x) 
		self.ydata.append(y) 
		self.line.set_data(xdata, ydata) 
		return line, 
	



