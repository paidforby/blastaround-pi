import os
import time
import vlc

def create_player(mode, output, playlist):

	if mode == "pulse":
		os.environ["PULSE_SINK"] = output
		interface=vlc.Instance('--aout=pulse')
	elif mode == "alsa":
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

if __name__ == "__main__":
	#config
	DIR = "/home/pi/DirectoryA/"	# directory for headphone media
	DIR_B = "/home/pi/DirectoryB/"	# directory for headphone media
	OUTPUT = "1"			# "hw:1,0" corresponds to "cat proc/asound/cards"
	OUTPUTB = "hw:1,0"		# "hw:1,0" corresponds to "cat proc/asound/cards"

	playing = True			# initial state of headphone media

	# get playlist from directory
	playlist = [DIR + i for i in os.listdir(DIR)]
	playlistB = [DIR_B + i for i in os.listdir(DIR_B)]

	# create headphones and speaker outputs, 
	headphones = create_player("pulse", OUTPUT, playlist)
	speaker = create_player("alsa", OUTPUTB, playlistB)
	speaker.play()

	if playing:
		headphones.play()
	else:
		headphones.pause()
	
	while True:
		print("...playing...")	
		time.sleep(1)



