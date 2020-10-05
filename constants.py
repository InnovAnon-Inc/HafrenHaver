#! /usr/bin/env python3

from math import pi
import pygame

from network import random_default_port
    
DEFAULT_ROTATION = pi / 2

DEFAULT_TITLE     = "Hafren Haver: InnovAnon"
DEFAULT_ICONTITLE = "HH IA"
DEFAULT_ICON      = "logo.png"

RUNNING_TITLE     = "Hafren Haver: Free Code for a Free World!"
RUNNING_ICONTITLE = "HH FFF"

CLOSING_TITLE     = "Hafren Haver: Innovations Anonymous"
CLOSING_ICONTITLE = "HH InnovAnon"

DEFAULT_CREDITS   = ('InnovAnon', 'S. Faust', 'Terry A. Davis', 'A. Severn', 'Zantedeschia')
DEFAULT_SUBLIMINAL_THRESHOLD = 16.7 # milliseconds

BLACK    = (  0, 0, 0)
IA_BLACK = (  0, 5, 0)
IA_RED   = (247, 0, 3)

DEFAULT_SCREEN_MODE = pygame.HWSURFACE | pygame.DOUBLEBUF

DEFAULT_ISOCHRONIC  = 7.83 # hz
DEFAULT_SCALE       = (1/1, 3/2) # TODO randomize or something

DEFAULT_MAX_SAMPLE_RATE = 44100 # hz
DEFAULT_SAMPLE_RATE     = DEFAULT_MAX_SAMPLE_RATE
#reasonable_minmax_int_pitch (DEFAULT_ISOCHRONIC, DEFAULT_SCALE, 0, DEFAULT_MAX_SAMPLE_RATE)[1]
#DEFAULT_ISOCHRONIC * pow (2, (log (DEFAULT_MAX_SAMPLE_RATE) - log (DEFAULT_ISOCHRONIC)) / log (2))
#DEFAULT_SAMPLE_RATE     = ceil (DEFAULT_SAMPLE_RATE)

DEFAULT_MAX_FRAME_RATE  = 60 # fps
#DEFAULT_MAX_FRAME_RATE  = 1 # fps
#DEFAULT_FRAME_RATE      = DEFAULT_ISOCHRONIC * pow (2, (log (1 / DEFAULT_MAX_FRAME_RATE) - log (DEFAULT_ISOCHRONIC)) / log (2))
DEFAULT_FRAME_RATE      = DEFAULT_MAX_FRAME_RATE
# reasonable_minmax_int_pitch (DEFAULT_ISOCHRONIC, DEFAULT_SCALE, 0, 1 / DEFAULT_MAX_FRAME_RATE)[0]
#DEFAULT_TICK_SPEED      = min (DEFAULT_FRAME_RATE, DEFAULT_SAMPLE_RATE) * 1000 # ms
#DEFAULT_TICK_SPEED      = DEFAULT_FRAME_RATE / 1000 # x frames / 1 second * 1 second / 1000 ms => x frames / 1000 ms
DEFAULT_TICK_SPEED      = DEFAULT_FRAME_RATE


DEFAULT_EXIT_TIMEOUT = 3



OPAQUE = (255, 255, 255, 255) # TODO I think this should be called TRANSPARENT

# TODO DEFAULT_HOST        => client param: domain name or ip of server
# TODO DEFAULT_PORT        => client param: port              of server
# TODO DEFAULT_LISTEN_ADDR => server param:
# TODO DEFAULT_LISTEN_PORT => server param:
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = random_default_port ()
DEFAULT_USER_AGENT = "HafrenHaver" # TODO maybe leak your info


DEFAULT_BACKGROUND   = "background.png"
SECONDARY_BACKGROUND = "shiva.png"

ORIGIN = (0, 0)
