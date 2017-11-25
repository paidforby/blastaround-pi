# Monitor for and connect to bluetooth device
# written by Jason Woodruff
import os
import sys
import subprocess
import time

def blueteeth():
    status = subprocess.call('ls /dev/input/event0 2>/dev/null', shell=True)
    while status == 0:
        print("Bluetooth UP")
        print(status)
        #time.sleep(15)
        status = subprocess.call('ls /dev/input/event0 2>/dev/null', shell=True)
	return 0	
    else:
        waiting()

def waiting():
    subprocess.call('killall -9 pulseaudio', shell=True)
    time.sleep(3)
    subprocess.call('pulseaudio --start', shell=True)
    time.sleep(2)
    status = subprocess.call('ls /dev/input/event0 2>/dev/null', shell=True)  
    while status == 2:
        print("Bluetooth DOWN")
        print(status)
        subprocess.call('./autopair.sh', shell=True)
        time.sleep(10)
        status = subprocess.call('ls /dev/input/event0 2>/dev/null', shell=True)
    else:
        blueteeth() 

if __name__ == "__main__":
	blueteeth()
