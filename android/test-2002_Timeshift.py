# coding=utf-8
from runnerWrapper import *
import pytest 
import logging 
import random
import os
import re
import calendar
import time
import toml
import shutil
import allure # allure report
root_path = os.path.dirname(os.path.realpath(__file__))
allurewiget() # for allure wiget display info
class PWBFunc:

    def __init__(self):
        self.cloudtokenid = None
        self.clouduserid = None  

    def LoadJSONFile(self):
        global desrinationfile  # Target json file
        listtemp = 0
        listtemp = int(listtemp)  # for how much steps
        findays = 0
        finhours = 0
        finsecs = 0
        try:
            adddays =  (configure['unixtime']['adddays'])
            addhours =  (configure['unixtime']['addhours'])
            addsecs =  (configure['unixtime']['addsecs'])

        except ValueError:
            logdef.info("*******Config file error ,please check config.ini")
    
        findays = adddays * 86400

        logdef.info(findays)

        
        finhours = addhours * 3600
        logdef.info(finhours)

        finsecs = addsecs * 3600
        logdef.info(finsecs)
        

        # How much times(day) would like to shift

        fintimes =  findays + finhours + finsecs
        
        """
        What is epoch time?
        The Unix epoch (or Unix time or POSIX time or Unix timestamp) is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap seconds (in ISO 8601: 1970-01-01T00:00:00Z). Literally speaking the epoch is Unix time 0 (midnight 1/1/1970), but 'epoch' is often used as a synonym for Unix time. Some systems store epoch dates as a signed 32-bit integer, which might cause problems on January 19, 2038 (known as the Year 2038 problem or Y2038). The converter on this page converts timestamps in seconds (10-digit), milliseconds (13-digit) and microseconds (16-digit) to readable dates.

        Human-readable time     Seconds
        1 hour  3600 seconds
        1 day   86400 seconds
        1 week  604800 seconds
        1 month (30.44 days)    2629743 seconds        
        1 year (365.24 days)     31556926 seconds        

        """    
        current_GMT = time.gmtime()
        logdef.info(current_GMT)
        logdef.info("\n\n")
        time_stamp = calendar.timegm(current_GMT)
        logdef.info("************************************************\n\n")
        #sourcefile = 'CI_CLOUD_Example.json'
        sourcefile = 'dogfood_cloud-example_1018.json'

        with open(sourcefile,'r+') as file:
            data = json.load(file)            
            logdef.info("\n\n")
            for index in data:
               if 'timestamp' in index:
                  listtemp = listtemp + 1 
            logdef.info(listtemp)  # Step of the timestamp
            logdef.info("\n")

        
        data1 = data    
        # First timestamp is 9 
        for i in range(9,listtemp):
            timeslot = (data1[i]['timestamp'])

            data1[i]['timestamp'] = timeslot + (fintimes) 

            logdef.info(str(data1[i]['timestamp']) +" = "+str(timeslot)+ "+" +str(fintimes)) 

            logdef.info("\n")
            
        # Target json file generate
        ID =  (configure['userinfo']['devuserid']) 
        DUTID = (configure['userinfo']['devid']) 
        desrinationfile = str(ID)+'-'+str(DUTID)+'-android-'+str(time_stamp)+'.json'
        with open(desrinationfile, 'w') as f:
            json.dump(data1, f)
                              
class TestAPI(TestAPIWrap):
 
    def test_timeshift_func(self):

        """
        Please modify this address before test script
        """
        logdef.info("####################################################################\n")
        logdef.info("#  Timeshift  (thrive-ci-usw2-api.data.plume.tech/ #)\n")
        logdef.info("# ---------------------------------------------------------------- #)\n")
        logdef.info("#  Test case : ( Via Timeshift / Generate new JSON File #)\n")        
        logdef.info("####################################################################)\n") 
        logdef.info("#####################################")

        PWBFunc().LoadJSONFile()
        

