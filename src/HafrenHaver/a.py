LAMBDA  = (200    ,      )
GAMMA   = ( 26    , 100  )
BETA    = ( 13    ,  32  )
ALPHA   = (  8    ,  13  )
THETA   = (  4    ,   8  )
DELTA   = (  0.500,   4  )
EPSILON = (  0.025,   0.5)

#alpha
#alpha+beta
#alpha+gamma

#theta
#theta+beta
#theta+gamma

#delta
#delta+beta
#delta+gamma
#delta+lambda

#epsilon+lambda

# TODO bf0, bf1, tempo, carrier frequency, harmonic complexity?, ...
import numpy
import math
def test (pitch1, pitch2, carrier):
	bits = 16
	#the number of channels specified here is NOT 
	#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

	pygame.mixer.pre_init(44100, -bits, 2)
	pygame.init()
	size = (1366, 720)
	display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)

    #sin (c * x) + a * sin (x)


	duration = 1.0          # in seconds
	#freqency for the left speaker
	#frequency_l = 440
	#frequency for the right speaker
	#frequency_r = 550

	#this sounds totally different coming out of a laptop versus coming out of headphones
	sample_rate = 44100

	n_samples = int(round(duration*sample_rate))

	#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
	max_sample = 2**(bits - 1) - 1

	def play (pitch):
		frequency_l = pitch
		frequency_r = pitch
		buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
		for s in range(n_samples):
			t = float(s)/sample_rate    # time in seconds

			#grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
			buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
			buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right

		sound = pygame.sndarray.make_sound(buf)
		#play once, then loop forever
		sound.play(loops = 1)


	
	# binary interpolation
	min_pitch = 20
	max_pitch = 20000
	while True:
		pitch = min_pitch + (max_pitch - min_pitch) / 2
		#t1 = Thread (audio.play (pitch))
		#inp = wait ()
		play (pitch)
	pygame.quit()
