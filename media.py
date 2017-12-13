import os
import time
import vlc
import random

class MediaPlayer(object):
	
	def __init__(self, mode, switch, output, volume):

		if mode == "pulse":
			os.environ["PULSE_SINK"] = output
			self.interface=vlc.Instance('--aout=pulse')
		elif mode == "alsa":
			self.interface=vlc.Instance('--aout=alsa', '--alsa-audio-device=' + output)
		
		if switch == "song":
			self.player = self.interface.media_player_new()
			self.player.audio_set_volume(volume)
			self.current_track = 0

		if switch == "playlist":
			self.player = self.interface.media_list_player_new()
			self.player.set_playback_mode(vlc.PlaybackMode.loop)	
	
	def load_playlist(self, playlist):
		mediaList = self.interface.media_list_new()
		for music in playlist:
			mediaList.add_media(self.interface.media_new(music))
		self.player = self.interface.media_list_player_new()
		self.player.set_media_list(mediaList)
		self.player.set_playback_mode(vlc.PlaybackMode.loop)	

	def load(self, song):
		media = self.interface.media_new(song)
		self.player = self.interface.media_player_new()
		self.player.set_media(media)
	
	def play(self):
		self.player.play()

	def pause(self):
		self.player.pause()

	def play_next(self, playlist):
		self.current_track += 1
		if self.current_track > (len(playlist)-1):
			self.current_track == 0
		media = self.interface.media_new(playlist[self.current_track])
		self.player = self.interface.media_player_new()
		self.player.set_media(media)
		self.player.play()

	def play_random(self, playlist):
		self.current_track = random.randint(0, len(playlist)-1)
		media = self.interface.media_new(playlist[self.current_track])
		self.player = self.interface.media_player_new()
		self.player.set_media(media)
		self.player.play()


if __name__ == "__main__":

	from blue import *

	#config
	DIR = "/home/pi/media/STANDBY/"	# directory for headphone media
	DIR_B = "/home/pi/DirectoryB/"	# directory for headphone media
	OUTPUT = "hw:0,0"			# "hw:1,0" corresponds to "cat proc/asound/cards"
	OUTPUTB = "hw:1,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"

	# get playlist from directory
	playlist = [DIR + i for i in os.listdir(DIR)]
	playlistB = [DIR_B + i for i in os.listdir(DIR_B)]
	
	#blueteeth()

	# create headphones and speaker outputs, 
	headphones = MediaPlayer("alsa", "song", OUTPUT, 80)
	headphones.load(playlist[0])
	headphones.play()
	speaker = MediaPlayer("alsa", "playlist", OUTPUTB, 40)
	speaker.load_playlist(playlistB)
	speaker.play()
	
	while True:
	
		print("...playing...")	
		time.sleep(1)
		
		if headphones.player.is_playing() == 0:
			print("...play next sample...")
			time.sleep(5)
			headphones.play_random(playlist)
			


