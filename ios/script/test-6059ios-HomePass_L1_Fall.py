#!/usr/bin/env python3
#coding=utf-8
import appium
from appium import webdriver
import os
import sys
import wda # facebook api
import time
import os
import os
import sys
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
import glob   
import numpy as np
import subprocess
import sys
import struct
from time import sleep  # time for sleep
from collections.abc import MutableMapping
import threading
import pygatt
import logging
from binascii import hexlify
import allure # allure report
import platform
import datetime
from datetime import datetime, timedelta
from datetime import date
from PIL import Image
import pytesseract
import math
global DEV

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
timeout= 20.0  
root_path = os.path.dirname(os.path.realpath(__file__))

############################################################
# Should Use Authorize process first

# API1 (For Authorize / Per session base)

apiNameCloudLogin = 'PlumeCloudLogin'

apiNameAuthPlumeToken = 'AuthenticateWithPlumeToken'

# API3

#GetFallEventSummary
#for numbers
#GetFallEventList
#for times
apiNameGetFallEventSummary= 'GetFallEventSummary'

apiNameGetFallEventList= 'GetFallEventList'

#---------------------------------------------------
allurewiget() # for allure wiget display info

class PWBFunc:

    def __init__(self):
        os.popen("adb devices")
        self.cloudtokenid = None
        self.clouduserid = None

    def Authtoken(self,cloudtokenid,clouduserid):

        # Step 2 :  /pwb/AuthenticateWithPlumeToken   

        return authtokenpost(apiNameAuthPlumeToken, cloudtokenid, clouduserid)

    def CloudLoginProcess(self):

        # Step 1 :  /pwb/PlumeCloudLogin

        return CloudLoginpost(apiNameCloudLogin)

    def GetFallEventSummary(self,finaltokenid,clouduserid,startTime,endTime):

        logdef.info(startTime)
        logdef.info(endTime)
        #Step 4 : Test API /pwb/GetFallEventSummary
        #curl -k -H "Content-Type:application/json" -d '{"pingTest": {"action": 1,"ipVersion": 4,"host": "10.10.10.100","count": 3,"size": 64,"timeout": 60,"interval": "1",}}' -u admin:password https://10.10.10.8:8443/api/v1/ping_test_start
        # 
 
        return ToGetFallEventSummary(apiNameGetFallEventSummary, finaltokenid, startTime, endTime)


    def GetFallEventList(self,finaltokenid,clouduserid,startTime,endTime):

        logdef.info(startTime)
        logdef.info(endTime)
        #Step 4 : Test API /pwb/GetFallEventList
        #curl -k -H "Content-Type:application/json" -d '{"pingTest": {"action": 1,"ipVersion": 4,"host": "10.10.10.100","count": 3,"size": 64,"timeout": 60,"interval": "1",}}' -u admin:password https://10.10.10.8:8443/api/v1/ping_test_start
        # 

        return ToGetFallEventList(apiNameGetFallEventList, finaltokenid, startTime, endTime)        
 
class TestAPI(TestAPIWrap):
 
    def test_beacon_func(self):

        ## Ticket number THRIV-1452
        ## https://plumedesign.atlassian.net/browse/THRIV-1452 

        ## facebook-wda IOS

        wda.DEBUG = False # default False
        #wda.HTTP_TIMEOUT = 10.0 # default 60.0 seconds
        bundle_id = "com.plumewifi.plume.devintegration"  
        #d = wda.Client('http://192.168.1.111:8100')
        d = wda.USBClient("00008110-001405601129801E", port=8100)
        # IOS status    
        logdef.info(d.status())
    
        # Wait WDA ready
        d.wait_ready(timeout=3000) 
        d.home()
        # Hit healthcheck
        d.healthcheck()
        # Get page source
        d.source() # format XML
        d.source(accessible=True) # default false, format JSON        
        d.home()
        logdef.info(d.window_size())
        d.swipe_left()
        d(label="HomePass").click()
        d.swipe_up()
        time.sleep(1)
        d.swipe_up()
        time.sleep(1)
        d.swipe_up()
        time.sleep(1)
        d.swipe_up()
        time.sleep(1)                
        d.swipe(0.1, 0.7, 0.6, 0.7)
        time.sleep(1)
        d.swipe(0.1, 0.7, 0.6, 0.7)
        time.sleep(1)
        d.swipe(0.1, 0.7, 0.6, 0.7)
        time.sleep(1)        
        d.swipe(0.1, 0.7, 0.6, 0.7)
        time.sleep(1)   
        d.screenshot().save("./pic/1.png") # Good
        allure.attach.file("./pic/1.png" , attachment_type=allure.attachment_type.PNG) 
        d.swipe(0.6, 0.7, 0.1, 0.7)
        d.screenshot().save("./pic/2.png") # Good
        allure.attach.file("./pic/2.png" , attachment_type=allure.attachment_type.PNG)   
        d.swipe(0.6, 0.7, 0.1, 0.7)
        time.sleep(2)
        d.screenshot().save("./pic/3.png") # Good
        allure.attach.file("./pic/3.png" , attachment_type=allure.attachment_type.PNG)    
        d.swipe(0.6, 0.7, 0.1, 0.7)
        time.sleep(2)
        d.screenshot().save("./pic/Redcard.png") # Good
        allure.attach.file("./pic/Redcard.png" , attachment_type=allure.attachment_type.PNG)

        ## API Part
        # Cloud Part 
        self.result = PWBFunc().CloudLoginProcess()
        logdef.info("Step 1 :  PlumeCloudLogin\n")
        Data1 = self.result['data']
        # Get token-id via staging cloud
        cloudtokenid = Data1['id']
        logdef.info(Data1['id'])
        # Get userid via staging
        clouduserid = Data1['user']['id']
        logdef.info(Data1['user']['id'])
        logdef.info("\n")
        logdef.info("Step 2 :  AuthenticateWithPlumeToken\n")        
        self.result2 = PWBFunc().Authtoken(cloudtokenid,clouduserid)
        Data2 = self.result2['data']
        # Get final access-token via staging cloud
        finaltokenid = Data2['accessToken']
        logdef.info(Data2['accessToken'])
        logdef.info("\n")
        global TODAY
        if d(label="Fall detected 0:00 am, yesterday").exists:
            # for yesterday
            logdef.info("Yesterday Fail event has been detected")
            TODAY = datetime.now() - timedelta(days=1)  # - 1 day -> yesterday
            logdef.info(TODAY.year)
            logdef.info(TODAY.month)
            logdef.info(TODAY.day)        
            dtime = datetime(TODAY.year, TODAY.month, TODAY.day, 0)
            logdef.info(dtime)
            Starttimestamp = int(round(dtime.timestamp()))
            Etime = datetime(TODAY.year, TODAY.month, TODAY.day, 23)
            Endtimestamp = int(round(Etime.timestamp()))
            ## For Fallevent yesterday eventtime check point
            logdef.info("Yesterday's Timestamp Range:")
            logdef.info(Starttimestamp)
            logdef.info(Endtimestamp)

            ## API for fallevent
            self.InsightSummary = PWBFunc().GetFallEventList(finaltokenid,clouduserid,Starttimestamp,Endtimestamp)
            GetFallEventList_insightlist = self.InsightSummary['data']
            logdef.info(GetFallEventList_insightlist)
            FalleventtList= GetFallEventList_insightlist['fallEventList']
            logdef.info("####################################")
            logdef.info(FalleventtList) 
            logdef.info("####################################")
            eventtime_API = [i['eventTime'] for i in GetFallEventList_insightlist['fallEventList']]
            logdef.info("The eventTime get from Backend API : ")
            eventtime_num = eventtime_API [0] # eventTime from API
            eventtime_API = [i['eventId'] for i in GetFallEventList_insightlist['fallEventList']]
            num_i = len(eventtime_API)
            logdef.info("The numbers of eventId  : "+str(num_i))
            # 
            timestamp_to_check = eventtime_num

            if Starttimestamp <= timestamp_to_check <= Endtimestamp:
                logdef.info(str(eventtime_num)+" is within yesterday's time range.")
            else:
                logdef.info(str(eventtime_num)+" is not within yesterday's time range.")

            ## Front-end /backend should the same
            try:
                assert Starttimestamp <= timestamp_to_check <= Endtimestamp
                logdef.info("##################################################################\n\n")            
                logdef.info("PASS : L1_Fall event display info -> FrontEnd and Backend are the same\n\n")
                logdef.info("##################################################################\n\n")                
            except AssertionError as err:
                logdef.info("##################################################################\n\n")            
                logdef.info("FAIL : L1_Fall event display info -> FrontEnd and Backend are not equal\n\n")
                logdef.info("##################################################################\n\n")  
                time.sleep(3)
                raise

            #d(label="1 fall today")    
            fall_array = {
                '1 fall today',
                '2 fall today',
                '3 fall today',
                '4 fall today',
                '5 fall today',
                '6 fall today',
                '7 fall today',
                '8 fall today',                                                                                
                '9 fall today',
                '10 fall today',                                                 
            }

            for FALLindex in fall_array:
                if d(label=FALLindex).exists:
                    if str(num_i) in FALLindex:
                       logdef.info("##########################################################")
                       logdef.info("The L1 FALL count get from HomePASS IOS is : "+str(num_i))
                       logdef.info("###########################################################")
                    break
            else:
                logdef.info("Not thing match")


        else:    
            # for today 
            TODAY =  datetime.now()
            logdef.info(TODAY.year)
            logdef.info(TODAY.month)
            logdef.info(TODAY.day)
            dtime = datetime(TODAY.year, TODAY.month, TODAY.day, 0)
            logdef.info(dtime)
            Starttimestamp = int(round(dtime.timestamp()))
            Etime = datetime(TODAY.year, TODAY.month, TODAY.day, 23)
            Endtimestamp = int(round(Etime.timestamp()))
        ##---- 
        self.InsightSummary = PWBFunc().GetFallEventSummary(finaltokenid,clouduserid,Starttimestamp,Endtimestamp)
        FallEventSummary_result = self.InsightSummary['data']
        logdef.info(FallEventSummary_result)
        FallcountList= FallEventSummary_result['fallCountList']
        logdef.info("####################################")
        logdef.info(FallcountList) 
        logdef.info("####################################")
        Fallcount_API = [i['fallCount'] for i in FallEventSummary_result['fallCountList']]
        logdef.info("The fallCount get from Backend API : ")
        logdef.info(Fallcount_API [0])   



        ## Cloud API value and UI/UX value compare , the value should equal
        ## L1 Sleep score
        try:
            assert int(num_i) == int(Fallcount_API [0])
            logdef.info("##################################################################\n\n")            
            logdef.info("PASS : L1_FALL count  -> FrontEnd and Backend are the same\n\n")
            logdef.info("##################################################################\n\n")                
        except AssertionError as err:
            logdef.info("##################################################################\n\n")            
            logdef.info("FAIL : L1_FALL count -> FrontEnd and Backend are not equal\n\n")
            logdef.info("##################################################################\n\n")            
            time.sleep(3)
            raise
  

    
 

        logdef.info("Test completed")
        d.home()
        time.sleep(1)
        #d.swipe(0.5, 0.1, 0.5, 1.0)  # from top to bottom
        #time.sleep(3)
        #d.press("home") # Press Home button 
        # Close app
        d.close()
