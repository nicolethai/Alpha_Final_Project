import RPi.GPIO as GPIO
import time
import DHT11
import Freenove_DHT as DHT

DHTPin = 11  
def getht():
    dht = DHT.DHT(DHTPin)
    while(True):
        chk = dht.readDHT11()
        print("Humidity : %.2f, \t Temperature : %.2f \n"%(dht.humidity,dht.temperature))
        time.sleep(2)
        

if __name__=='__main__':
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()