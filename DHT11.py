#!/usr/bin/env python3
########################################################################
# Filename    : Relay.py
# Description : Button control Relay and LED indicator
# Update	  : PIR Code integrated
# Author      :
# modification: 2019/06/05
########################################################################
import RPi.GPIO as GPIO
import time

relayPin = 12    # define the relayPin @GPIO18
sensorPin = 11      # define the PIR sensor @GPIO17
debounceTime = 50
GPIO.setwarnings(False)
relayState = False

def setup():
	print ('Program is starting...')
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output
	GPIO.setup(sensorPin, GPIO.IN)	 # Set sensorPin's mode to input

def get_irrigation_time(ET0_local):
    ''' function to calculate the needed time (sec) for watering '''
    # Formula to calculate the gallons of irrigation water needed per day: (ET0xPFxSFx0.62)/IE = GallonsofWaterperday
    IE = 0.75
    PF = 1.0	# PF=1.0 for lawns
    SF = 200	# sq. ft. of lawn
    water_debit = 1020	# 1020 gal of water per hr

    gal_per_day_sample = (ET0_local * PF * SF * 0.62 / IE)
    gal_per_day = gal_per_day_sample
    return (gal_per_day/water_debit)*3600

def set_relay(irrigate_period):
    ''' function call to initiate the relay to irrigate. param curr_hr takes the hour relay needs to irrigate for '''
    print ('set_relay start...')
    global relayState
    relayState = True
    relay_t = irrigate_period
    print ('relay set to irrigate for ' + str(relay_t) + ' secs')
    start_t = time.time()
    pause_time = 0 #pause time 
    paused = 0 #pause flag
    while True:
	# check end of watering interval
        
        if time.time()-start_t >= relay_t:
            relayState = False
            break

    	# check for motion sensor
        pir_t = time.time()
        while GPIO.input(sensorPin) == GPIO.LOW:
            '''need to output to LCD'''
            print ('Motion detected... pause relay')
            if time.time()-pir_t >= 60.0:
                print ('\t1 min max over')
                relayState = True
                pause_time = time.time() - pir_t #when exiting the pause loop, minus the start time from current to get the paused time
                paused = 1 #paused set to true.
                break
            relayState = False
            paused = 1 #paused set to true
            GPIO.output(relayPin, relayState)

        if(paused == 1): #pause loop exited, add pause time back
            pause_time = time.time() - pir_t #when exiting the pause loop, minus the start time from current to get the paused time
            relay_t += pause_time # add the paused time back to irrigation time
            pause_time = 0
            paused = 0 #set flag to false
        
        relayState = True
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
            set_relay(0.3)
	#	loop()
	except KeyboardInterrupt:
		destroy()
