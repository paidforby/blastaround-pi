import RPi.GPIO as GPIO

class PirSensor(object):
	def __init__(self, pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(pin, GPIO.RISING, callback=self.pir_triggered, bouncetime=10)
		self.triggered = False

	def pir_triggered(self, arg):
		self.triggered = True
	

if __name__ == "__main__":
	import time
	pir = PirSensor(17)
	time.sleep(2) # allow sensor to stablize 
	try:
		while True:
			print("wait for sense")
			if pir.triggered:
				print("...play sumthin...")
				pir.triggered = False
			time.sleep(1)
	except KeyboardInterrupt:
		print("end")
		GPIO.cleanup()
