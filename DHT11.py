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
relayPin = 12    # define the relayPin @GPIO18
sensorPin = 11      # define the PIR sensor @GPIO17
debounceTime = 50
GPIO.setwarnings(False)
relayState = False


# Relay
def set_relay(curr_hr):
    ''' function call to initiate the relay to irrigate. param curr_hr takes the hour relay needs to irrigate for '''
    print ('set_relay start...')
    global relayState
    relayState = True
    relay_t = irrigation_time[curr_hr]
    print ('relay set to irrigate for ' + str(relay_t) + ' secs')
    start_t = time.time()

    while True:
	# check end of watering interval
        if time.time()-start_t >= relay_t:
            relayState = False
            break

    	# check for motion sensor
        pir_t = time.time()
        while GPIO.input(sensorPin) == GPIO.HIGH:
            '''need to output to LCD'''
            print ('Motion detected... pause relay')
            if time.time()-pir_t >= 60.0:
                print ('\t1 min max over')
                relayState = True
                break
            relayState = False
            GPIO.output(relayPin, relayState)

        relayState = True
        GPIO.output(relayPin, relayState)
        time.sleep(1.0)
        print(time.time()-start_t)

    print ('end relay')
    GPIO.output(relayPin, relayState)

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

#Convert Celsius to fahrenheit
def CtoF(value):
    return (value * 1.8) + 32

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
        time.sleep(2)
    print("DHT11,OK!")
    if(dht.humidity > 100):
        dht.humidity -= 100
    hr_data_list[cur_hr].add_temp_hum(CtoF(dht.temperature),dht.humidity)
    print ("This hour's ReadCnt is : %d, \t chk    : %d"%(hr_data_list[cur_hr].sum_cnt,chk))
    print("Humidity : %.2f, \t Temperature : %.2f "%(dht.humidity,CtoF(dht.temperature)))
    hr_data_list[cur_hr].print_data()
    set_local_humidity(cur_hr, hr_data_list[cur_hr].ave_temp)
    set_local_temp(cur_hr, hr_data_list[cur_hr].ave_hum)
    dht.humidity = 0
def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(relayPin, GPIO.OUT)   # Set relayPin's mode is output
    GPIO.setup(sensorPin, GPIO.IN)   # Set sensorPin's mode to input
def loop():
    timeCnt = 0              #record how many seconds have passed
    readgap = 1              #every 5 seconds read local temp/hum
    CIMISgap = 5            #every 20 seconds request CIMIS data
    while(True):
        read_hum_temp()
        time.sleep(readgap)       
        timeCnt += readgap
        if(timeCnt % CIMISgap == 0):    
            update_CIMIS_data('75','2019-06-01','2019-06-01') # request CIMIS data and update lists
            get_irrigation_time() #calculate irrigation time
            if(irrigation_time[int(check_time_now()[0:2])])!=None:
                ''' OWEN. THIS IS WHERE IT STARTS TO CALL RELAY FUNCTION '''
                irrigation_time[int(check_time_now()[0:2])] = 15.0
                set_relay(int(check_time_now()[0:2]))

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


