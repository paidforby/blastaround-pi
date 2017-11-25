import RPi.GPIO as GPIO
import math
import time

class ReedSwitch(object):

	def __init__(self, pin, radius):	

		GPIO.setmode(GPIO.BCM)

		self.pin = pin
		self.circumference = 2*math.pi*radius 
		self.switch = False
		self.time_of_last_pass = time.time() 
		self.time_of_current_pass = time.time()
		self.velocity = .00001

		GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(pin, GPIO.RISING, callback=self.sensed, bouncetime = 100)
		# bouncetime should not be higher than top speed

	def update_velocity(self):
		if self.switch:
			self.time_of_last_pass = self.time_of_current_pass
			self.time_of_current_pass = time.time()
			dt = self.time_of_current_pass - self.time_of_last_pass
			self.velocity = self.circumference/dt
			self.switch = False 

	def sensed(self, arg):
		self.switch = True
		self.update_velocity()	

	def get_velocity(self):
		if (time.time() - self.time_of_last_pass) > 3:
			self.velocity = .001
		return self.velocity

if __name__ == "__main__":

	pin = 22 
	radius_of_tire_in_m = .3429 # = 13.5in

	reed_switch = ReedSwitch(pin, radius_of_tire_in_m)

	while True:		

		print "velocity at time %.0f: %.3f" % (time.time(), reed_switch.get_velocity())
		time.sleep(.1)

