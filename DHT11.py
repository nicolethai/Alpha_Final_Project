#########################################################################
# I used pytz library which is not installed on Pi in default, to install:
# sudo easy_install pip
# sudo pip3 install pytz
#########################################################################

import RPi.GPIO as GPIO
import time
import Freenove_DHT as DHT
from CIMISapi import *

#define GPIO pins
DHTPin = 29    #define the pin of DHT11 - GPIO 5

relayPin = 11    # define the relayPin - GPIO 17
buttonPin = 12    # define the buttonPin - GPIO 18

#data class for local temp/hum
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
        print("ave_humidity: ", self.ave_hum,"\t ave_temp: ", self.ave_temp,  "\n")

#Global variables
hr_data_list = [hr_data()] * 24       # a list of 24 hrs local data  

def check_time_now():
    # define timezone
    PDT = timezone('America/Los_Angeles')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    loc_dt = datetime.now(PDT)
    cur_time = loc_dt.strftime(fmt)[11:18]
    return cur_time

def read_hum_temp():
    dht = DHT.DHT(DHTPin)   #create a DHT class object
    cur_hr = int(check_time_now()[0:2])
    print("Current Hour is ", cur_hr)
    chk = dht.readDHT11()
    while(chk is not dht.DHTLIB_OK):
        chk = dht.readDHT11()
    print("DHT11,OK!")
    hr_data_list[cur_hr].add_temp_hum(dht.temperature,dht.humidity)
    print ("This hour's ReadCnt is : %d, \t chk    : %d"%(hr_data_list[cur_hr].sum_cnt,chk))
    print("Humidity : %.2f, \t Temperature : %.2f "%(dht.humidity,dht.temperature))
    hr_data_list[cur_hr].print_data()
    set_local_humidity(cur_hr, dht.humidity)
    set_local_temp(cur_hr, dht.temperature)

def setup():
	print ('Program is starting...')
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output
	GPIO.setup(buttonPin, GPIO.IN)

def loop():
    timeCnt = 0              #record how many seconds have passed
    readgap = 5              #every 5 seconds read local temp/hum
    CIMISgap = 20            #every 20 seconds request CIMIS data
    while(True):
        read_hum_temp()
        time.sleep(readgap)       
        timeCnt += readgap
        if(timeCnt % CIMISgap == 0):    
            update_CIMIS_data('75',today(),today()) # request CIMIS data and update lists
            get_irrigation_time() #calculate irrigation time

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

