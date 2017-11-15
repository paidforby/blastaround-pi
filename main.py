import time
import os
import random
import vlc 
#from mpu6050 import mpu6050
from reed import ReedSwitch
from wheels import NeoPixelStrip
#from kalman import KalmanFilter
import RPi.GPIO as GPIO
import math

#config
dirA = "/home/pi/DirectoryA/"	# directory for headphone media
dirB = "/home/pi/DirectoryB/"	# directory for speaker media
outputA = "hw:0,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"
outputB = "hw:1,0"
playingA = False		# initial state of headphone media
playingB = False		# initial state of speaker media 
volumeA = 80
volumeB = 30
randomness = .2			# percent chance that speakers are playing media
random_delay = 20		# seconds of delay between speaker sounds +/- delay_range	
delay_range = 10
random_sound = 10		# seconds to play a speaker sound +/- play_range 
play_range = 5

start_limit = 1			# lower limit for detecting acceleration in m^2/s
stop_limit = 1			# lower limit for detecting deceleration in m^2/s
easing = .8			# response of acceleration reading, 0 = slower, 1 = faster
number_of_wheels = 4
leds_per_wheel = 24
radius_of_wheel_in_m =.3429 
reed_pin = 17

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
playlistA = [dirA + i for i in os.listdir(dirA)]

playlistB = [dirB + i for i in os.listdir(dirB)]

# create headphones and speaker outputs, 
headphones = create_player(outputA, playlistA)
#headphones.audio_set_volume(volumeA)

if playingA:
	headphones.play()
else:
	headphones.pause()

speaker = create_player(outputB, playlistB)
#speaker.audio_set_volume(volumeB)
speaker.play()

wheels = NeoPixelStrip(number_of_wheels, leds_per_wheel)
wheels.start()
start_time = time.time()
last_update = time.time()

# create accelerometer and get initial values
reed_switch = ReedSwitch(reed_pin, radius_of_wheel_in_m) 

#sensor = mpu6050(0x68)
#data = sensor.get_accel_data()

# kalman filter for smoothing data
# replace kalman filter with complementary filter per http://www.pieter-jan.com/node/11

prevTime = time.time()
random_pause = random.randint(random_delay - 10, random_delay + 10)
random_play = random.randint(random_sound - 5, random_sound + 5)

while True:

	velocity = reed_switch.get_velocity()
	if (time.time() - last_update) > .1:
		wheels.update(1/(100*velocity)) #time between pixel update
		print(velocity)
		last_update = time.time()

	if (time.time()-start_time) > 60 :
		wheels.cancel()
		exit()
	
	if playingA:
		if velocity < stop_limit:
			headphones.pause()
			playingA = False 
	else:	
		if velocity > start_limit:
			headphones.play()
			playingA = True 

	
	if playingB:
		if (time.time()-prevTime) > random_play:
			print("pause speaker")
			speaker.pause()
			playingB = False 
			random_pause = random.randint(random_delay - delay_range, random_delay + delay_range)
			prevTime = time.time()
	else:	
		if (time.time()-prevTime) > random_pause: 
			print("play speaker")
			speaker.play()
			playingB = True 
			random_play = random.randint(random_sound - play_range, random_sound + play_range)
			prevTime = time.time()
