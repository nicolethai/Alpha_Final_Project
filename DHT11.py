#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT

from datetime import datetime
from pytz import timezone

DHTPin = 29    #define the pin of DHT11 - GPIO 5

relayPin = 11    # define the relayPin - GPIO 17
buttonPin = 12    # define the buttonPin - GPIO 18

 

class hr_data:
    
    sum_temp = 0
    sum_hum = 0
    sum_cnt = 0
    ave_temp = 0
    ave_hum = 0
    
    def _init_(self):
        sum_temp = 0
        sum_hum = 0
        sum_cnt = 0
        ave_temp = 0
        ave_hum = 0
    
    def get_ave(self):
        self.ave_temp = self.sum_temp/self.sum_cnt
        self.ave_hum = self.sum_hum/self.sum_cnt
          
    def add_temp_hum(self,newtemp,newhum):
        self.sum_temp += newtemp
        self.sum_hum += newhum
        self.sum_cnt += 1
        self.get_ave()
        
    def print_data(self):
        print("Current Hour has average temp: ", self.ave_temp, " and average humidity: ", self.ave_hum)
        
hr_data_list = [hr_data()] * 24        

def check_time_now():
    # define timezone
    PDT = timezone('America/Los_Angeles')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    loc_dt = datetime.now(PDT)
    cur_time = loc_dt.strftime(fmt)[11:18]
    return cur_time

def setup():
	print ('Program is starting...')
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output
	GPIO.setup(buttonPin, GPIO.IN)


def loop():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    GPIO.output(relayPin,GPIO.HIGH)
    cur_hr = int(check_time_now()[0:2])
    print("Current Hour is ", cur_hr)
    sumCnt = 0              #number of reading times 
    while(True):
        chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
            print("DHT11,OK!")
            sumCnt += 1         #counting number of reading times
            print ("The sumCnt is : %d, \t chk    : %d"%(sumCnt,chk))
            hr_data_list[cur_hr].add_temp_hum(dht.temperature,dht.humidity)
            print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
            hr_data_list[cur_hr].print_data()
            time.sleep(5)  
     
        
def destroy():
    
	GPIO.output(relayPin, GPIO.LOW)     # relay off
    
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        exit()  

