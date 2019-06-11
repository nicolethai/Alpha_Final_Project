# Usage: 
# update_CIMIS_data('75',today(),today()) 
# call this function to update 3 global lists of CIMIS data for each hour
# 75 is the ID of CIMIS Station at Irvine
# today() returns a string of today's date

# get_irrigation_time()
# call this function to update a global list of irrigation for each hour
# irrigation_time[0] will be the time needed to irrigate for the 1st hour of the day

import json
import requests
import urllib
from urllib.request import urlopen
from datetime import datetime
from pytz import timezone
import LCD
import socket

#Gloal variables
CIMIS_ET_list = [None]*24
CIMIS_temp_list = [None]*24
CIMIS_hum_list = [None]*24

local_ET_list = [None]*24
local_temp_list= [None]*24
local_hum_list = [None]*24

irrigation_time = [None]*24
water_amount = [None]*24
CIMIS_water_amt = [None]*24

str_today = None
start_hr = None 

def check_time_now():
    # define timezone
    PDT = timezone('America/Los_Angeles')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    loc_dt = datetime.now(PDT)
    cur_time = loc_dt.strftime(fmt)[11:18]
    return cur_time

def set_start_hr():
    global start_hr
    start_hr = int(check_time_now()[0:2])
    print("Program starts at hour: ", start_hr, "\n")

def today():
    # define timezone
    PDT = timezone('America/Los_Angeles')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    loc_dt = datetime.now(PDT)
    global str_today
    if str_today == None:
        str_today = loc_dt.strftime(fmt)[0:10]
    return str_today

def CIMIS_request(zip_OR_target, start_date, end_date):
    request_target = 'http://et.water.ca.gov/api/data?appKey=b0d0abe6-53d6-49e5-94ad-9ffd6d43e166&targets='
    request_items = '&dataItems=hly-eto,hly-rel-hum,hly-air-tmp'
    request_startdate = '&startDate='
    request_enddate = '&endDate='
    request = request_target + zip_OR_target + request_startdate + start_date + request_enddate + end_date + request_items
    result = None 
    try:
        result = urlopen(request,timeout = 6)
    except socket.timeout as e:
        print(e, "\n")
        pass 
    except urllib.error.URLError as e:
        print(e, "\n")
        pass
    
    return result 
def convert_data(a):
    if (a == 'None' or a == None):
        return None
    else:
        return float(a)

def update_lists(records):
    for i in range(24):
        if(CIMIS_ET_list[i] is None or i < start_hr):
            CIMIS_ET_list[i] = (convert_data(records[i]['HlyEto']['Value']))
            CIMIS_temp_list[i] = (convert_data(records[i]['HlyAirTmp']['Value']))
            CIMIS_hum_list[i] = (convert_data(records[i]['HlyRelHum']['Value']))

def calculate_time(ET):
    PF = 1 #plant factor
    SF = 200 #area to be irrigated
    IE= 0.75 #irrigation efficiency
    irrigation_speed = 1020 #irrigation system delivers 1020 gallons of water per hour
    water = (ET * PF * SF * 0.62) / IE
    time = water / irrigation_speed * 60 * 60
    return time

def calculate_water(ET):
    PF = 1 #plant factor
    SF = 200 #area to be irrigated
    IE= 0.75 #irrigation efficiency
    irrigation_speed = 1020 #irrigation system delivers 1020 gallons of water per hour
    water = (ET * PF * SF * 0.62) / IE
    return water

def set_local_humidity(i, value):
    local_hum_list[i] = value
    
def set_local_temp(i, value):
    local_temp_list[i] = value

def get_irrigation_time():
    print("Average hum and temp average per hour of ", today())
    print(local_hum_list)
    print(local_temp_list)
    for i in range(len(CIMIS_ET_list)):
        if (CIMIS_ET_list[i] == None or local_temp_list[i] == None or local_hum_list[i] == None):
            local_ET_list[i] = None
        else:
            local_ET_list[i] = CIMIS_ET_list[i] * local_temp_list[i] / CIMIS_temp_list[i] * CIMIS_hum_list[i] / local_hum_list[i]
    for i in range(len(local_ET_list)):
        if (local_ET_list[i] != None):
            irrigation_time[i] = calculate_time(local_ET_list[i])
            water_amount[i] = calculate_water(local_ET_list[i])
            CIMIS_water_amt[i] = calculate_water(CIMIS_ET_list[i])
    print("\nIrrigation time of", today())
    print(irrigation_time, "\n")
    print("Water amount to irrigate based on CIMIS data of", today())
    print(CIMIS_water_amt, "\n")
    print("Water amount to irrigate based on modified local data of", today())
    print(water_amount, "\n")
        
def update_CIMIS_data(zip_OR_target, start_date, end_date):
    try:
        response = CIMIS_request(zip_OR_target,start_date,end_date)
        if response==None:
            return
        str_response = response.read().decode('utf-8')
        obj = json.loads(str_response)
        records = obj['Data']['Providers'][0]['Records']
        update_lists(records)
        print("Requesting data from CIMIS website...")
        print("ET/Temp/Humidity value of", today())
        print(CIMIS_ET_list)
        print(CIMIS_temp_list)
        print(CIMIS_hum_list, "\n")
    except json.decoder.JSONDecodeError as e:
        print("CIMIS data json decode error:")
        print(e, "\n")
        pass

        #exit()
    #response = urlopen('http://et.water.ca.gov/api/data?appKey=b0d0abe6-53d6-49e5-94ad-9ffd6d43e166&targets=92619&dataItems=hly-eto&startDate=2019-06-01&endDate=2019-06-01')

################Test###################
#update_CIMIS_data('75','2019-06-04','2019-06-04')

#get_irrigation_time()
