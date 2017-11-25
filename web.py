from flask import Flask, render_template
import time
import datetime
from wheels import NeoPixelStrip
from neopixel import *
from multiprocessing import Process, Value, Pool, Manager

app = Flask(__name__)
manager = Manager()
current_mode = manager.Value('i', 0) 

# Create a dictionary of possible modes:
modes = { 
	0 : {'name': 'STANDBY'}, 
	1 : {'name': 'RIDING'}, 
	2 : {'name': 'RIDE_OVER'}
	}

@app.route('/')
def main():
	templateData = {
		'current_mode' : current_mode.value,	
		'modes' : modes
	}
	return render_template('main.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changeToMode>")
def action(changeToMode):
	current_mode.value = int(changeToMode)
	templateData = {
		'current_mode': current_mode.value,
		'modes' : modes
	}
	return render_template('main.html', **templateData)


def start_lights(state):
	while True:
		wheels.run()
		wheels.update_mode(state.value)
		if state.value == 0:
			wheels.update_speed(.5)
		elif state.value == 1:
			wheels.update_speed(.001)
		elif state.value == 2:
			wheels.update_speed(.3)

def start_server(state):
	app.run(debug=True, use_reloader=False, host='0.0.0.0')


if __name__ == '__main__':
	SCOOTER_COLOR = Color(0, 255, 0)
	wheels = NeoPixelStrip(4, 24, SCOOTER_COLOR)
	start_time = time.time()

	script = Process(target=start_lights, args=(current_mode,))
	script.start()  
	server = Process(target=start_server, args=(current_mode,))
	server.start()
	script.join()

