#!/usr/bin/env python3
########################################################################
# Filename    : Relay.py
# Description : Button control Relay and LED indicator 
# Author      : 
# modification: 2019/06/05
########################################################################
import RPi.GPIO as GPIO
import time

relayPin = 11    # define the relayPin
debounceTime = 50
GPIO.setwarnings(False)
relayState = False

def setup():
	print ('Program is starting...')
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output

def get_irrigation_time():
    ''' function to calculate the needed time (sec) for watering '''
    gal_per_day_sample = (0.3 * 1.0 * 1500 * 0.62 / 0.75)
    gal_per_day = gal_per_day_sample
    water_debit = 1020
    return (gal_per_day/water_debit)*3600

def set_relay():
    ''' function call to initiate the relay to irrigate '''
    print ('set_relay start...')
    global relayState
    relayState = True
    relay_t = get_irrigation_time()
    print ('relay set to irrigate for ' + str(relay_t) + ' secs')
    relay_t = 15.0
    start_t = time.time()
    
    while True:
        if time.time()-start_t >= relay_t:
            relayState = False
            break
        GPIO.output(relayPin, relayState)
        time.sleep(1.0)
        print(time.time()-start_t)
    
    print ('end relay')
    GPIO.output(relayPin, relayState)

def destroy():
	GPIO.output(relayPin, GPIO.LOW)     # relay off
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
                set_relay()
	#	loop()
	except KeyboardInterrupt:  
		destroy()

