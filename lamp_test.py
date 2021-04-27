## LAMP CONTROL TEST
##
## Testing performance/capabilities of using a MOSFET trigger to CONTROL
## a lamp.

import RPi.GPIO as gpio
import time

def toggle():
    if gpio.input(lamp):
        gpio.output(lamp, False)
    else:
        gpio.output(lamp, True)


## Setup
lamp = 4      # pin number that lamp MOSFET is working off of.
interval = .1  # number of seconds to wait before toggling lamp

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(lamp, gpio.OUT)


# Main Loop
while True:
    toggle()
    time.sleep(interval)