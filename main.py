import time
import os
import random
import vlc 
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
	DIR_RIDING_SPEAKER = "/home/pi/media/RIDING_SPEAKER/"	# directory for speaker media
	DIR_RIDE_OVER_HEADPHONES = "/home/pi/media/RIDE_OVER_HEADPHONES/"	# directory for speaker media
	DIR_RIDE_OVER_SPEAKER = "/home/pi/media/RIDE_OVER_SPEAKER/"	# directory for speaker media
	REPEAT_OVER = 15

	OUTPUT_A = "hw:1,0"			# pacmd list-sinks
	OUTPUT_B = "hw:0,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"

	VOLUME_HEADPHONES = 90
	VOLUME_SPEAKER = 50

	NUMBER_OF_WHEELS = 4
	LEDS_PER_WHEEL = 24
	SCOOTER_COLOR = Color(0, 255, 0)

	REED_PIN = 22 
	RADIUS_OF_WHEEL_IN_M =.3429 
	SPEED_LIMIT = 1			# limit for detecting velocity 

	PIR_PIN = 17 

	#blueteeth()

	playlist_standby = [DIR_STANDBY + i for i in os.listdir(DIR_STANDBY)]
	playlist_riding_headphones = [DIR_RIDING_HEADPHONES + i for i in os.listdir(DIR_RIDING_HEADPHONES)]
	playlist_riding_speaker = [DIR_RIDING_SPEAKER + i for i in os.listdir(DIR_RIDING_SPEAKER)]
	playlist_ride_over_headphones = [DIR_RIDE_OVER_HEADPHONES + i for i in os.listdir(DIR_RIDE_OVER_HEADPHONES)]
	playlist_ride_over_speaker = [DIR_RIDE_OVER_SPEAKER + i for i in os.listdir(DIR_RIDE_OVER_SPEAKER)]

	headphones = MediaPlayer("alsa", "playlist", OUTPUT_A, VOLUME_HEADPHONES)

	speaker = MediaPlayer("alsa", "song", OUTPUT_B, VOLUME_SPEAKER)

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

	while True:

		wheels.run()	
		velocity = reed_switch.get_velocity()
		#if (time.time() - last_update) > .2:
		#	print velocity
		#	last_update = time.time()
		
		# STATE 0: STANDBY
                if state.value == 0:
			if current_state != state.value:
				wheels.update_mode(state.value)
				wheels.update_speed(.5)
				current_state = state.value
			if pir.triggered:
				speaker.play_random(playlist_standby)
				pir.triggered = False
			

		# STATE 1: RIDING
                elif state.value == 1:

			if current_state != state.value:
				start_time = time.time()
				moving = False
				current_state = state.value
		
			if moving:
				# SPINNING WHEELS
				wheels.update_speed(1/(50*velocity))
				if velocity < SPEED_LIMIT:
					wheels.update_speed(.5)
					wheels.update_mode(0)
					headphones.pause()
					moving = False
			
			else:	# NOT moving
				# BLINKING WHEELS
				if velocity > SPEED_LIMIT:
					wheels.update_speed(.001)
					wheels.update_mode(1)
					headphones.play()
					moving = True 

			if pir.triggered:
				speaker.play_random(playlist_riding_speaker)
				pir.triggered = False

			if (time.time() - start_time) > 270:
				# AFTER 4.5 mins
				state.value = 2
				

		# STATE 2: RIDE_OVER
                elif state.value == 2:
			if current_state != state.value:
				wheels.update_mode(state.value)
				wheels.update_speed(.3)
				current_state = state.value

			if time.time()-last_play > REPEAT_OVER: 
				speaker.load(playlist_ride_over_speaker[0])
				speaker.play()
				headphones.load(playlist_ride_over_headphones[0])
				headphones.play()
				last_play = time.time()

		
# beginning of time, start script and flask processes
script = Process(target=start_script, args=(current_mode,))
script.start()
server = Process(target=start_server, args=(current_mode,))
server.start()
script.join()

