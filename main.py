import time
import os
import random
import vlc 
import pygame
from reed import ReedSwitch
from wheels import NeoPixelStrip
from pir import PirSensor
from blue import *
from media import *
from web import *
import RPi.GPIO as GPIO
import math
from neopixel import *
from multiprocessing import Process, Value, Pool, Manager

def start_script(state):

	#config
	DIR_STANDBY = "/home/pi/media/STANDBY/"	# directory for speaker media
	DIR_RIDING_HEADPHONES = "/home/pi/media/RIDING_HEADPHONES/"	# directory for speaker media
        HEADPHONES_MUSIC_SLOW = "/home/pi/media/RIDING_HEADPHONES/rainforest.wav"
        HEADPHONES_MUSIC_FAST = "home/pi/media/RIDING_HEADPHONES/christmas.wav"

	DIR_RIDING_SPEAKER = "/home/pi/media/RIDING_SPEAKER/"	# directory for speaker media
	DIR_RIDE_OVER_HEADPHONES = "/home/pi/media/RIDE_OVER_HEADPHONES/"	# directory for speaker media
	DIR_RIDE_OVER_SPEAKER = "/home/pi/media/RIDE_OVER_SPEAKER/"	# directory for speaker media
	REPEAT_OVER = 15

	OUTPUT_A = "hw:0,0"			# pacmd list-sinks
	OUTPUT_B = "hw:1,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"

	VOLUME_HEADPHONES = 70
	VOLUME_SPEAKER = 100

	NUMBER_OF_WHEELS = 4
	LEDS_PER_WHEEL = 24
	SCOOTER_COLOR = Color(0, 175, 0)

	REED_PIN = 22 
	RADIUS_OF_WHEEL_IN_M =.1 
	SPEED_LIMIT = .1	# limit for detecting velocity 

	PIR_PIN = 17 

	#blueteeth()

	playlist_standby = [DIR_STANDBY + i for i in os.listdir(DIR_STANDBY)]
	playlist_riding_headphones = [DIR_RIDING_HEADPHONES + i for i in os.listdir(DIR_RIDING_HEADPHONES)]
	playlist_riding_speaker = [DIR_RIDING_SPEAKER + i for i in os.listdir(DIR_RIDING_SPEAKER)]
	playlist_ride_over_headphones = [DIR_RIDE_OVER_HEADPHONES + i for i in os.listdir(DIR_RIDE_OVER_HEADPHONES)]
	playlist_ride_over_speaker = [DIR_RIDE_OVER_SPEAKER + i for i in os.listdir(DIR_RIDE_OVER_SPEAKER)]

	#headphones = MediaPlayer("alsa", "song", OUTPUT_A, VOLUME_HEADPHONES)

	speaker = MediaPlayer("alsa", "song", OUTPUT_B, VOLUME_SPEAKER)

        # TODO add to media.py as object
        #set up the mixer
        freq = 44100     # audio CD quality
        bitsize = -16    # unsigned 16 bit
        channels = 2     # 1 is mono, 2 is stereo
        buffer = 2048    # number of samples (experiment to get right sound)
        pygame.mixer.init(freq, bitsize, channels, buffer)

        #Create sound object for each Audio
        audio1 = pygame.mixer.Sound(HEADPHONES_MUSIC_SLOW)
        channel1 = pygame.mixer.Channel(1)
        audio1.set_volume(0.8) # Reduce volume of first audio to 80%
        channel1.play(audio1)
                            
        audio2 = pygame.mixer.Sound(HEADPHONES_MUSIC_FAST)
        channel2 = pygame.mixer.Channel(2)
        audio2.set_volume(0.3) # Reduce volume of first audio to 80%
        channel2.play(audio2)

	wheels = NeoPixelStrip(NUMBER_OF_WHEELS, LEDS_PER_WHEEL, SCOOTER_COLOR)

	velocity = .001
	reed_switch = ReedSwitch(REED_PIN, RADIUS_OF_WHEEL_IN_M) 
	last_update = time.time()

	pir = PirSensor(PIR_PIN)

	start_time = time.time()
	last_play = time.time()
	moving = False
	current_state = None
	headphones.load(playlist_riding_headphones[0])
	headphones.play()

	while True:

		wheels.run()	
		velocity = reed_switch.get_velocity()

		# STATE 1: RIDING

		if moving:
			# SPINNING WHEELS
			wheels.update_speed(1/(50*velocity))
			if velocity < SPEED_LIMIT:
				wheels.update_speed(.5)
				wheels.update_mode(0)
				#headphones.pause()
                                audio1.set_volume(.9)
                                audio2.set_volume(.2)
				moving = False
		
		else:	# NOT moving
			# BLINKING WHEELS
			if velocity > SPEED_LIMIT:
				wheels.update_speed(.001)
				wheels.update_mode(1)
				#headphones.play()
                                audio1.set_volume(.1)
                                audio2.set_volume(.9)
				moving = True 

		if pir.triggered:
			speaker.play_random(playlist_standby)
			pir.triggered = False
		
		if headphones.player.is_playing() == 0:
			headphones.play_random(playlist_riding_headphones)

		#if (time.time() - start_time) > 270:
			# AFTER 4.5 mins
		#	state.value = 2
				

		
# beginning of time, start script and flask processes
script = Process(target=start_script, args=(current_mode,))
script.start()
server = Process(target=start_server, args=(current_mode,))
server.start()
script.join()

