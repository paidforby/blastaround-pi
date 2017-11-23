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

#config
DIR_A = "/home/pi/DirectoryA/"	# directory for headphone media
DIR_B = "/home/pi/DirectoryB/"	# directory for speaker media
OUTPUT_A = "1"			# pacmd list-sinks
OUTPUT_B = "hw:1,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"
				
playingA = True			# initial state of headphone media
playingB = False		# initial state of speaker media 

randomness = .2			# percent chance that speakers are playing media
random_delay = 20		# seconds of delay between speaker sounds +/- delay_range	
delay_range = 10
random_sound = 10		# seconds to play a speaker sound +/- play_range 
play_range = 5

start_limit = 1			# lower limit for detecting acceleration in m^2/s
stop_limit = 1			# lower limit for detecting deceleration in m^2/s
easing = .8			# response of acceleration reading, 0 = slower, 1 = faster

NUMBER_OF_WHEELS = 4
LEDS_PER_WHEEL = 24
SCOOTER_COLOR = Color(0, 255, 0)

RADIUS_OF_WHEEL_IN_M =.1016 
REED_PIN = 17
PIR_PIN = 23

blueteeth()

# get playlist from directory
playlistA = [DIR_A + i for i in os.listdir(DIR_A)]

playlistB = [DIR_B + i for i in os.listdir(DIR_B)]

headphones = create_player("pulse", OUTPUT_A, playlistA)

if playingA:
	headphones.play()
else:
	headphones.pause()

speaker = create_player("alsa", OUTPUT_B, playlistB)
speaker.pause()

wheels = NeoPixelStrip(NUMBER_OF_WHEELS, LEDS_PER_WHEEL, SCOOTER_COLOR)
last_update = time.time()
 
reed_switch = ReedSwitch(REED_PIN, RADIUS_OF_WHEEL_IN_M) 

pir = PirSensor(PIR_PIN)
prevTime = time.time()
random_play = random.randint(random_sound - 5, random_sound + 5)

def start_script(state):
	while True:
		global playingA
		global playingB
		global last_update 
		global prevTime 
		global random_play

		velocity = reed_switch.get_velocity()

		wheels.run()	
                wheels.update_mode(state.value)
                if state.value == 0:
                        wheels.update_speed(.5)
                elif state.value == 1:
                        wheels.update_speed(.001)
                elif state.value == 2:
                        wheels.update_speed(.3)

		if playingA:
			wheels.update_speed(1/(100*velocity))
			if (time.time() - last_update) > .1:
				print(velocity)
				last_update = time.time()

			if velocity < stop_limit:
				wheels.update_speed(.5)
				wheels.update_mode(0)
				headphones.pause()
				playingA = False 
		else:	
			if velocity > start_limit:
				wheels.update_mode(1)
				headphones.play()
				playingA = True 

		
		if playingB:
			if (time.time()-prevTime) > random_play:
				print("pause speaker")
				speaker.pause()
				playingB = False 
				prevTime = time.time()
		else:	
			if pir.triggered: 
				print("play speaker")
				speaker.play()
				playingB = True 
				pir.triggered = False
				random_play = random.randint(random_sound - play_range, random_sound + play_range)
				prevTime = time.time()


manager = Manager()
start_time = time.time()

current_mode = manager.Value('i', 0)

script = Process(target=start_script, args=(current_mode,))
script.start()
server = Process(target=start_server, args=(current_mode,))
server.start()
script.join()

