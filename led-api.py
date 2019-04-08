#!/usr/bin/python

# import dependencies
import os, time
from flask import Flask
from flask import jsonify
from blinkstick import blinkstick
import json

# bootstrap the app
app = Flask(__name__)

# set the port dynamically with a default of 3000 for local development
port = int(os.getenv('PORT', '3000'))


# our base route which just returns a string
@app.route('/')
def hello_world():
    return 'Congratulations! Welcome to the Swisscom Application Cloud.'

@app.route('/random')
def blink_random():
    try:
        for led in blinkstick.find_all():
            time.sleep(0.020)
            led.set_random_color()
    except Exception as e:
        return jsonify(
            status="error",
            message=str(e)
        )
    else:
        return blink_info()

@app.route('/blink')
def blink_blink():
    turn_off()
    leds=blinkstick.find_all()
    time.sleep(0.200)
    try:
        while blinkstick.find_all():
            try:
                leds[0].blink(name="red", delay=100, repeats=1)
                time.sleep(0.020)

                leds[1].blink(name="red", delay=100, repeats=1)
                time.sleep(0.020)

            except Exception as e:
                print str(e)


    except Exception as e:
        return jsonify(
            status="error",
            message=str(e)
        )
    else:
        return jsonify(
            status="success",
            message="all led's could be activated"
        )

@app.route('/info')
def return_info():
    return blink_info()

@app.route('/off')
def turn_off():
    for led in blinkstick.find_all():
        try:
            led.turn_off()
        except Exception:
            print "Failed to communicate with led"

    return "Turend off"


def blink_info():
    serial_list, color_list = [], []

    for led in blinkstick.find_all():
        serial_list.append(led.get_serial())
        color_list.append(led.get_color(color_format="hex"))

    serial_colors = [{"serial": s, "color": c} for s, c in zip(serial_list, color_list)]

    return json.dumps(serial_colors)


# start the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, threaded=False)