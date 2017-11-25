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
	DIR_A = "/home/pi/DirectoryA/"	# directory for headphone media
	DIR_B = "/home/pi/DirectoryB/"	# directory for speaker media
	OUTPUT_A = "1"			# pacmd list-sinks
	OUTPUT_B = "hw:0,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"
					

	NUMBER_OF_WHEELS = 4
	LEDS_PER_WHEEL = 24
	SCOOTER_COLOR = Color(0, 255, 0)

	REED_PIN = 22 
	RADIUS_OF_WHEEL_IN_M =.3429 
	SPEED_LIMIT = 1			# limit for detecting velocity 

	PIR_PIN = 17 

	blueteeth()

	playlistA = [DIR_A + i for i in os.listdir(DIR_A)]

	playlistB = [DIR_B + i for i in os.listdir(DIR_B)]

	headphones = MediaPlayer("pulse", OUTPUT_A, playlistA)
	headphones.pause()

	speaker = MediaPlayer("alsa", OUTPUT_B, playlistB)
	speaker.pause()

	wheels = NeoPixelStrip(NUMBER_OF_WHEELS, LEDS_PER_WHEEL, SCOOTER_COLOR)

	velocity = .001
	reed_switch = ReedSwitch(REED_PIN, RADIUS_OF_WHEEL_IN_M) 
	last_update = time.time()

	pir = PirSensor(PIR_PIN)
	prev_detect = time.time()

	start_time = time.time()
	current_state = None

	while True:

		wheels.run()	
		velocity = reed_switch.get_velocity()
		if (time.time() - last_update) > .2:
			print velocity
			last_update = time.time()
		
		# STATE 0: STANDBY
                if state.value == 0:
			if current_state != state.value:
				wheels.update_mode(state.value)
				wheels.update_speed(.5)
				current_state = state.value
			if pir.triggered: 
				speaker.play_next()
				pir.triggered = False
			

		# STATE 1: RIDING
                elif state.value == 1:

			if (time.time() - start_time) > 270:
				state.value = 2

			if current_state != state.value:
				wheels.update_mode(state.value)
				wheels.update_speed(.001)
				start_time = time.time()
				headphones.play()
				current_state = state.value

			elif headphones.playing == True:
				wheels.update_speed(1/(100*velocity))
				if velocity < SPEED_LIMIT:
					wheels.update_speed(.5)
					wheels.update_mode(0)
					headphones.pause()

			elif headphones.playing == False:	
				if velocity > SPEED_LIMIT:
					wheels.update_mode(1)
					headphones.play()


		# STATE 2: RIDE_OVER
                elif state.value == 2:
                	wheels.update_mode(state.value)
                        wheels.update_speed(.3)

		
		#if playingB:
		#	if (time.time()-prevTime) > random_play:
		#		print("pause speaker")
		#		speaker.pause()
		#		playingB = False 
		#		prevTime = time.time()
		#else:	
		#	if pir.triggered: 
		#		print("play speaker")
		#		speaker.play()
		#		playingB = True 
		#		pir.triggered = False


# beginning of time, start script and flask processes
script = Process(target=start_script, args=(current_mode,))
script.start()
server = Process(target=start_server, args=(current_mode,))
server.start()
script.join()

