# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
#
# heavily modified by Grant Gallo

import time
from threading import Thread

from neopixel import *


# LED strip configuration:
LED_RING_COUNT  = 24      # Number of LED pixels.
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest

LED_COUNT      = 4*LED_RING_COUNT
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 1       # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering


class NeoPixelStrip(Thread): 

	def __init__(self, number_of_rings, leds_per_ring, color):	
		super(NeoPixelStrip, self).__init__()
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
		self.strip.begin()
		self.wheel = [ NeoPixelRing(i, leds_per_ring) for i in range(number_of_rings) ]		
                self.color = color
		self.color_flip = True
		self.current_led = 0 
		self.previousUpdate = time.time()
		self.delay = .01
                self.mode = 0
		self.cancelled = False

	def spinning_lights(self):
		if self.color_flip:   
			for i in range(4):
				self.wheel[i].colorWipe(self.strip, self.color)  # Green wipe
			self.current_led += 1
			if self.current_led > 24:
				self.color_flip = False
				self.current_led = 0
			       
		else: 
			for i in range(4):
			      self.wheel[i].colorWipe(self.strip, Color(255, 255, 255))  # white wipe
			self.current_led +=1
			if self.current_led > 24:
				self.color_flip = True
				self.current_led = 0

        def blinky_lights(self)
		if self.color_flip:   
			for i in range(4):
				self.wheel[i].colorSolid(self.strip, self.color)  # Green blink 
			self.current_led += 1
			if self.current_led > 24:
				self.color_flip = False
				self.current_led = 0
			       
		else: 
			for i in range(4):
			      self.wheel[i].colorSolid(self.strip, Color(255, 255, 255))  # White blink 
			self.current_led +=1
			if self.current_led > 24:
				self.color_flip = True
				self.current_led = 0


	def run(self):
		while not self.cancelled:
		        if(time.time() - self.previousUpdate) > self.delay:
                            self.previousUpdate = time.time()
                            if self.mode == 0:
                                    self.blinky_lights() 
                            if self.mode == 1:
				    self.spinning_lights() 
			    

	def cancel(self):
		self.cancelled = True

	def update_speed(self,delay):
		self.delay = delay

        def update_mode(self, mode):
                self.mode = mode

class NeoPixelRing(object):
	def __init__(self, ring_number, led_count):
		self.startLED = ring_number*led_count 
		self.stopLED = self.startLED+led_count
		self.currentLED = self.startLED 

	# Define functions which animate LEDs in various ways.
	def colorWipe(self, strip, color):
		"""Wipe color across display a pixel at a time."""
		if self.currentLED in range(self.startLED, self.stopLED):
			strip.setPixelColor(self.currentLED, color)
			strip.show()
			self.currentLED += 1
		else: 
			self.currentLED = self.startLED 

	def colorSolid(self, strip, color):
		"""Wipe color across display a pixel at a time."""
		for self.currentLED in range(self.startLED, self.stopLED):
			strip.setPixelColor(self.currentLED, color)
			strip.show()
		self.currentLED = self.startLED 

	def theaterChase(self, strip, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		for j in range(iterations):
			for q in range(3):
				for i in range(self.startLED, self.stopLED, 3):
					strip.setPixelColor(i+q, color)
				strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(self.startLED, self.stopLED, 3):
					strip.setPixelColor(i+q, 0)


# Main program logic follows:
if __name__ == '__main__':

	wheels = NeoPixelStrip(4, 24)
	wheels.start()
	start_time = time.time()

	print ('Press Ctrl-C to quit.')
	while True:
		print("...threading...")	
		if (time.time() - start_time) > 10 :	
			wheels.update(.0001)
		if (time.time() - start_time) > 20 :	
			wheels.cancel()
			exit()

		time.sleep(1)
