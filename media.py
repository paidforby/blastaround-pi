import os
import time
import vlc

class MediaPlayer(object):
	
	def __init__(self, mode, output, playlist):
		self.current_track = 0
		self.playing = False 
		self.player = self.create_player(mode, output, playlist)
	
	def create_player(self, mode, output, playlist):

		if mode == "pulse":
			os.environ["PULSE_SINK"] = output
			self.interface=vlc.Instance('--aout=pulse')
		elif mode == "alsa":
			self.interface=vlc.Instance('--aout=alsa', '--alsa-audio-device=' + output)

		#add song
		media = self.interface.media_new(playlist[self.current_track])
		player = self.interface.media_player_new()
		player.set_media(media)

		#add playlist
		#mediaList = interface.media_list_new()
		#for music in playlist:
		#    mediaList.add_media(interface.media_new(music))
		#player = interface.media_list_player_new()
		#player.set_media_list(mediaList)
		#player.set_playback_mode(vlc.PlaybackMode.loop)

		return player

	def play(self):
		self.player.play()
		self.playing = True

	def pause(self):
		self.player.pause()
		self.playing = False 

	def play_next(self, playlist):
		self.player.stop()
		current_track += 1
		media = self.interface.media_new(playlist[self.current_track])
		self.player=self.interface.media_player_new()
		self.player.set_media(media)
		


if __name__ == "__main__":

	from blue import *

	#config
	DIR = "/home/pi/DirectoryA/"	# directory for headphone media
	DIR_B = "/home/pi/DirectoryB/"	# directory for headphone media
	OUTPUT = "1"			# "hw:1,0" corresponds to "cat proc/asound/cards"
	OUTPUTB = "hw:1,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"

	# get playlist from directory
	playlist = [DIR + i for i in os.listdir(DIR)]
	playlistB = [DIR_B + i for i in os.listdir(DIR_B)]
	
	blueteeth()

	# create headphones and speaker outputs, 
	headphones = MediaPlayer("pulse", OUTPUT, playlist)
	headphones.play()
	speaker = MediaPlayer("alsa", OUTPUTB, playlistB)
	speaker.pause()
	
	while True:
		print("...playing...")	
		time.sleep(1)



