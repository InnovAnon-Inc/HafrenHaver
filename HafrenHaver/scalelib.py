#! /usr/bin/env python3
#
#  Automatic Game Scaling Library for pygame
#
#  Allows resize of a Window while scaling the game, keeping the aspect ratio.
#
#  Created by Matthew Mitchell on 13/09/2009.
#  Copyright (c) 2009 Matthew Mitchell. All rights reserved.
#
#Import modules
import sys
import pygame
from pygame.locals import *
def get_resolution(screen,ss,gs): 
	gap = float(gs[0]) / float(gs[1])
	sap = float(ss[0]) / float(ss[1])
	if gap > sap:
		#Game aspect ratio is greater than screen (wider) so scale width
		factor = float(gs[0]) /float(ss[0])
		new_h = gs[1]/factor #Divides the height by the factor which the width changes so the aspect ratio remians the same.
		game_scaled = (ss[0],new_h)
	elif gap < sap:
		#Game aspect ratio is less than the screens.
		factor = float(gs[1]) /float(ss[1])
		new_w = gs[0]/factor #Divides the width by the factor which the height changes so the aspect ratio remians the same.
		game_scaled = (new_w,ss[1])
	else:
		game_scaled = screen.get_size()
	return game_scaled		
class ScaledGame(pygame.Surface):
	game_size = None
	first_screen = None
	screen = None
	fs = False #Fullscreen false to start
	clock = None
	resize = True
	game_gap = None
	game_scaled = None
	title = None
	fps = False
	def __init__(self,title,game_size):
		pygame.init()
		self.title = title
		self.game_size = game_size
		screen_info = pygame.display.Info() #Required to set a good resolution for the game screen
		self.first_screen = (screen_info.current_w, screen_info.current_h - 120) #Take 120 pixels from the height because the menu bar, window bar and dock takes space
		self.screen = pygame.display.set_mode(self.first_screen,RESIZABLE) 
		pygame.display.set_caption(self.title)
		pygame.Surface.__init__(self,self.game_size) #Sets up the Surface for the game.
		self.clock = pygame.time.Clock()
		self.game_gap = (0,0)
	def update(self):
		#Updates screen properly
		win_size_done = False #Changes to True if the window size is got by the VIDEORESIZE event below
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit()
			if event.type == VIDEORESIZE:
				ss = [event.w,event.h]
				self.resize = True
				win_size_done = True
		keys = pygame.key.get_pressed() #Get the pressed keys
		if pygame.key.get_mods() == 1024:
			if(keys[K_q] or keys[K_w]):
				sys.exit()
			if keys[K_f]:
				self.screen = pygame.display.set_mode(self.first_screen,RESIZABLE)
				if self.fs == False:
					self.game_scaled = get_resolution(self.screen,[self.screen.get_width(),self.screen.get_height()],self.game_size)
					self.game_gap = [(self.screen.get_width() - self.game_scaled[0])/2,(self.screen.get_height() - self.game_scaled[1])/2]
					self.screen = pygame.display.set_mode((0,0), FULLSCREEN | HWSURFACE  | DOUBLEBUF)
					self.fs = True
				else:
					self.fs = False
					self.resize = True
					self.game_gap = (0,0)
		#Scale game to screen resolution, keeping aspect ratio
		if self.resize == True:
			if(win_size_done == False): #Sizes not gotten by resize event
				ss = [self.screen.get_width(),self.screen.get_height()]
			self.game_scaled = get_resolution(self.screen,ss,self.game_size)
			self.game_scaled = tuple (map (lambda x: int (x), self.game_scaled))
			self.screen = pygame.display.set_mode(self.game_scaled,RESIZABLE)
		self.resize = False #Next time do not scale unless resize or fullscreen events occur
		self.screen.blit(pygame.transform.scale(self,self.game_scaled),self.game_gap) #Add game to screen with the scaled size and gap required.
		pygame.display.flip()
		self.clock.tick(60)
		if self.fps == True:
			pygame.display.set_caption(self.title + " - " + str(int(self.clock.get_fps())) + "fps")

#
#  main.py
#  
#
#  Created by Matthew Mitchell on 15/09/2009.
#  Copyright (c) 2009 Matthew Mitchell. All rights reserved.
#
#from scalelib import *
if __name__ == '__main__': #Run if being run directly and not as a module
	game = ScaledGame("Test",[1280,720])  #1280x720 HD resolution game. Creates an object with the game Surface
	bottom = pygame.Surface((50,50))
	bottom.fill((0,80,180))
	bp = [0,0]
	while 1: #Game loop
		keys = pygame.key.get_pressed()
		if keys[K_UP] and (bp[1] > 0):
			bp[1] -= 3
		if keys[K_DOWN] and (bp[1] +50< game.get_height()):
			bp[1] += 3
		if keys[K_LEFT] and (bp[0] > 0):
			bp[0] -= 3
		if keys[K_RIGHT] and (bp[0] +50 < game.get_width()):
			bp[0] += 3
		game.fill((255,255,255)) #Refresh game with white
		game.blit(bottom,bp)
		game.fps = True #Shows framerate
		game.update() #Updates game
