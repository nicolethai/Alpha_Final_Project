import RPi.GPIO as GPIO
import time
import DHT11
from time import sleep
from Adafruit_LCD1602 import Adafruit_CharLCD
from PCF8574 import PCF8574_GPIO

from datetime import datetime


def display(string):

 PCF8574_address = 0x27 # I2C address of the PCF8574 chip.
 PCF8574A_address = 0x3F # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
 try:
     mcp = PCF8574_GPIO(PCF8574_address)
 except:
  try:
     mcp = PCF8574_GPIO(PCF8574A_address)
  except:
     print('I2C Address Error !')
  exit(1)
# Create LCD, passing in MCP GPIO adapter.
 lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
 lcd.clear()
 mcp.output(3,1) # turn on LCD backlight
 lcd.begin(16,2) # set number of LCD lines and columns
 lable = 0
 mcp.output(3,1)
 lcd.begin(16,2)
 
 lcd.setCursor(0,1)
 lcd.message(string)
 sleep(0.5)
 lcd.clear()

def scrolling(txt):

 PCF8574_address = 0x27 # I2C address of the PCF8574 chip.
 PCF8574A_address = 0x3F # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
 try:
     mcp = PCF8574_GPIO(PCF8574_address)
 except:
  try:
     mcp = PCF8574_GPIO(PCF8574A_address)
  except:
     print('I2C Address Error !')
  exit(1)
# Create LCD, passing in MCP GPIO adapter.
 lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
 lcd.clear()
 mcp.output(3,1) # turn on LCD backlight
 lcd.begin(16,2) # set number of LCD lines and columns
 lable = 0
 txt = txt.strip() + ' '
 if len(txt) < 17:
    txt = txt + (16 * ' ' )
 for i in range(len(txt)-16):
     lcd.setCursor(0, 0)
     lcd.message(txt[:16])
     lcd.setCursor(0, 1)
     lcd.message(datetime.now().strftime('%b %d  %H:%M:%S'))
     time.sleep(0.2)
     txt = txt[1:] + txt[0]
 lcd.clear()



'''def getAllsensorData():
 humid, temp = DHT11.getHumidityTemp()
 print(humid)
 print(temp)'''

