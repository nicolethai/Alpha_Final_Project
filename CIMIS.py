import json
from urllib.request import urlopen
from datetime import date
#
def today():
    return str(date.today())

def CIMIS_request(zip_OR_target, start_date, end_date):
    request_target = 'http://et.water.ca.gov/api/data?appKey=b0d0abe6-53d6-49e5-94ad-9ffd6d43e166&targets='
    request_items = '&dataItems=hly-eto,hly-rel-hum,hly-air-tmp'
    request_startdate = '&startDate='
    request_enddate = '&endDate='
    request = request_target + zip_OR_target + request_startdate + start_date + request_enddate + end_date + request_items
    return urlopen(request)

def update_lists(records,CIMIS_ET_list,CIMIS_temp_list,CIMIS_hum_list):
    CIMIS_ET_list.clear()
    CIMIS_temp_list.clear()
    CIMIS_hum_list.clear()
    for x in records:
        CIMIS_ET_list.append(x['HlyEto']['Value'])
        CIMIS_temp_list.append(x['HlyAirTmp']['Value'])
        CIMIS_hum_list.append(x['HlyRelHum']['Value'])
    

def update_CIMIS_data(zip_OR_target, start_date, end_date):
    response = CIMIS_request(zip_OR_target,start_date,end_date)
    #response = urlopen('http://et.water.ca.gov/api/data?appKey=b0d0abe6-53d6-49e5-94ad-9ffd6d43e166&targets=92619&dataItems=hly-eto&startDate=2019-06-01&endDate=2019-06-01')
    str_response = response.read().decode('utf-8')
    obj = json.loads(str_response)
    records = obj['Data']['Providers'][0]['Records']
    CIMIS_ET_list = []
    CIMIS_temp_list = []
    CIMIS_hum_list = []
    update_lists(records,CIMIS_ET_list,CIMIS_temp_list,CIMIS_hum_list)
    return CIMIS_ET_list, CIMIS_temp_list, CIMIS_hum_list

#75 is the ID of CIMIS Station at Irvine
#today() returns a string of today's date

CIMIS_ET_list,CIMIS_temp_list,CIMIS_hum_list = update_CIMIS_data('75',today(),today())
print("ET/Temp/Humidity value of", today())
print(CIMIS_ET_list)
print(CIMIS_temp_list)
print(CIMIS_hum_list)
