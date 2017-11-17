import time
import os
import random
import vlc 
from reed import ReedSwitch
from wheels import NeoPixelStrip
from pir import PirSensor
#from mpu6050 import mpu6050
#from kalman import KalmanFilter
import RPi.GPIO as GPIO
import math
from neopixel import *

#config
DIR_A = "/home/pi/DirectoryA/"	# directory for headphone media
DIR_B = "/home/pi/DirectoryB/"	# directory for speaker media
OUTPUT_A = "hw:0,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"
OUTPUT_B = "hw:1,0"

playingA = False		# initial state of headphone media
playingB = False		# initial state of speaker media 

#volumeA = 80
#volumeB = 30

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

RADIUS_OF_WHEEL_IN_M =.3429 
REED_PIN = 17
PIR_PIN = 23

def create_player(output, playlist):

	interface=vlc.Instance('--aout=alsa', '--alsa-audio-device=' + output)

	#add song
	#media = interface.media_new(playlistA)
	#player=interface.media_player_new()
	#player.set_media(mediaA)
	
	#add playlist
	mediaList = interface.media_list_new()
	for music in playlist:
	    mediaList.add_media(interface.media_new(music))
	player = interface.media_list_player_new()
	player.set_media_list(mediaList)
	player.set_playback_mode(vlc.PlaybackMode.loop)

	return player

# get playlist from directory
playlistA = [DIR_A + i for i in os.listdir(DIR_A)]

playlistB = [DIR_B + i for i in os.listdir(DIR_B)]

# create headphones and speaker outputs, 
headphones = create_player(OUTPUT_A, playlistA)

if playingA:
	headphones.play()
else:
	headphones.pause()

speaker = create_player(OUTPUT_B, playlistB)
speaker.pause()

# create wheel LEDs object and start its thread
wheels = NeoPixelStrip(NUMBER_OF_WHEELS, LEDS_PER_WHEEL, SCOOTER_COLOR)
last_update = time.time()

# create accelerometer and get initial values
reed_switch = ReedSwitch(REED_PIN, RADIUS_OF_WHEEL_IN_M) 

# create PIR sensor
pir = PirSensor(PIR_PIN)
prevTime = time.time()
random_play = random.randint(random_sound - 5, random_sound + 5)

#sensor = mpu6050(0x68)
#data = sensor.get_accel_data()

# kalman filter for smoothing data
# replace kalman filter with complementary filter per http://www.pieter-jan.com/node/11


while True:

	velocity = reed_switch.get_velocity()

	wheels.run()	

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
