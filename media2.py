import pygame
from media import *
import time

def checkifComplete(channel):
    while channel.get_busy():  #Check if Channel is busy
        pygame.time.wait(800)  #  wait in ms
    channel.stop()             #Stop channel

if __name__ == "__main__":

    music_file1 = "/home/pi/media/RIDING_HEADPHONES/rainforest.wav"
    music_file2 = "/home/pi/media/RIDING_HEADPHONES/christmas.wav"

    #set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 2048    # number of samples (experiment to get right sound)
    pygame.mixer.init(freq, bitsize, channels, buffer)

    #Create sound object for each Audio
    audio1 = pygame.mixer.Sound(music_file1)
    channel1 = pygame.mixer.Channel(1)
    audio1.set_volume(0.3) # Reduce volume of first audio to 80%
    channel1.play(audio1)
    #checkifComplete(channel1) #Check if Audio1 complete

    audio2 = pygame.mixer.Sound(music_file2)
    channel2 = pygame.mixer.Channel(2)
    audio2.set_volume(0.9) # Reduce volume of first audio to 80%
    channel2.play(audio2)
    #checkifComplete(channel2)

    DIR = "media/STANDBY/" # directory for headphone media
    OUTPUTB = "hw:0,0"      # "hw:1,0" corresponds to "cat proc/asound/cards"
    playlist = [DIR + i for i in os.listdir(DIR)]
    
    headphones = MediaPlayer("alsa", "song", OUTPUTB, 80)
    headphones.load(playlist[0])
    headphones.play()

    while True:
        print "...playing..."
        time.sleep(1)
