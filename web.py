from flask import Flask, render_template
import datetime
from wheels import NeoPixelStrip
from neopixel import *

mode = 3
R = 0 
G = 255
B = 0
SCOOTER_COLOR = Color(0, 255, 0)
app = Flask(__name__)
wheels = NeoPixelStrip(4, 24, SCOOTER_COLOR)

@app.route('/')
def hello_world():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %H:%M")
	templateData = {
		'title' : 'HELLO!',
		'time': timeString
	}
	return render_template('main.html', **templateData)

@app.route('/mode')
def get_mode():
	message = "mode = %d" % mode
    	return message 

if __name__ == '__main__':
	wheels.run()
      	app.run(debug=True, host='0.0.0.0')
