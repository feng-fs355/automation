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
from datetime import datetime
from datetime import date
from PIL import Image
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
# /pwb/GetFitnessInsightSummary
# API to get fitness summary by user, time period and interval.
apiNameGetDailySleepInsightList = 'GetDailySleepInsightList'
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

    def GetDailySleepInsightList(self,finaltokenid,clouduserid,startTime,endTime):

        logdef.info(startTime)
        logdef.info(endTime)
        #Step 4 : Test API /pwb/GetDailySleepInsightList
        #curl -k -H "Content-Type:application/json" -d '{"pingTest": {"action": 1,"ipVersion": 4,"host": "10.10.10.100","count": 3,"size": 64,"timeout": 60,"interval": "1",}}' -u admin:password https://10.10.10.8:8443/api/v1/ping_test_start
        # 
        """
        curl -X 'POST' \
          'https://thrive-dog1-usw2-api.data.plume.tech/pwb/GetDailySleepInsightList' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIzIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6ZTIyMDZiN2QtMDk1YS00M2QxLTgxMzUtODZhMTc5NmI1OTA5IiwiYXVkIjoidXMtd2VzdC0yOjU2YzQyNDM5LWJlMmMtNDUyMy04YmUwLTEwYjU4ODVlYTczMyIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzM6SlVtQnFiMmRxT3lRZFdFS3VSR1hYWnZrN2RMTUEwUmJYaENtOUVHb1gwZW00aHRCWlVCNnZLMkF0cVN6cXVVViJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjoxNDMwODk2MTA0ODI6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzMiLCJleHAiOjE2ODY2MzM0OTcsImlhdCI6MTY4NjU0NzA5N30.FgoFMwJC-kz2WfyTGKbFiz5JkyC8vMlRm8aZMcIpROa8y9TpRmxiNXuShUAvXNEQKcb7-WndcBG7g72DjhJSsLldSewMS8Ck2bgb5G1cLofL6JepcTHrZxEuxJ-9ESLnlOGGYqCZEzJfdqlYkbSutsMwf02D7Dwr2RWVpVgCC8uOSavDQUPJ5OlMPzenBVGGDhbntUdCZiEC1pc6oyj7gK_ndL4m_KigNho9a0WZ00asVzB7qHDJQNpodLx4nvfbf6ZQHNNYn_J9PWZ3TRLTSTjZ8eQTXVjh5i1SM9T50hbkNCFxGxmGEEYFhWoZAEBwndc-KjdS9QbB6Am7448MFA' \
          -H 'Content-Type: application/json' \
          -d '{
          "userId": "62a2d6708a13a8000a1b40b9",
          "startTime": 1686500000,
          "endTime": 1686547498,
          "pageSize": 1,
          "startKey": "",
          "utcOffset": -8
        }'
        """
 
        return ToGetDailySleepInsightList(apiNameGetDailySleepInsightList, finaltokenid, startTime, endTime)

 
class TestAPI(TestAPIWrap):
 
    def test_beacon_func(self):

        """
        IOS Phone HomePass APP
        API Clous URL (URL:thrive-dog1-usw2-api.data.plume.tech
        create test-6057ios-HomePass_L1_Sleep into Jenkins
        TestRail :TBD
        https://plumedesign.atlassian.net/browse/THRIV-1561

        List app bundle refernce as below:
        ideviceinstaller -l
        CFBundleIdentifier, CFBundleVersion, CFBundleDisplayName
        com.plumewifi.plume.devintegration, "1", "HomePass"
        com.facebook.WebDriverAgentRunner.xctrunner, "1", "WebDriverAgentRunner-Runner"

        List device id

        command : tidevice list
        
            UDID                       SerialNumber    NAME            MarketName    ProductVersion    ConnType
            00008110-001405601129801E  L9CX2JF9DM      plume’s iPhone  iPhone 13     16.5.1            ConnectionType.USB


        {
          "platformName": "iOS",
          "appium:automationName": "XCUITest",
          "appium:platformVersion": "16.5",
          "appium:deviceName": "iPhone 13",
          "appium:udid": "00008110-001405601129801E",
          "appium:noRest": true,
          "appium:bundleld": "com.plumewifi.plume.devintegration",
          "appium:unlockType": "pattern",
          "appium:unlockKey": "000000",
          "appium:noReset": "true",
          "appium:fullReset": "false",
          "appium:CaptureScreenshots": "true"
        }

        Bundle IDs for native iPhone and iPad apps

        https://support.apple.com/guide/deployment/bundle-ids-for-native-iphone-and-ipad-apps-depece748c41/web

       Issue reference as below:

       https://plumedesign.atlassian.net/browse/THRIV-1074?atlOrigin=eyJpIjoiNTE4OGVlNTdiYmU1NDQzN2E5YzExMDQ4YjA5YzExYmYiLCJwIjoiamlyYS1zbGFjay1pbnQifQ

       https://plumedesign.atlassian.net/browse/THRIV-1103?atlOrigin=eyJpIjoiODg1MTRhM2I2YzFkNGE2Mzk5OGMwZjEzZDEyYzg2NmQiLCJwIjoiamlyYS1zbGFjay1pbnQifQ

       https://plumedesign.atlassian.net/browse/THRIV-1198?atlOrigin=eyJpIjoiZWIxZTAyMWQxMjJlNGM1ZmI4NGJmNDgxMjMzNDNkNDMiLCJwIjoiamlyYS1zbGFjay1pbnQifQ

       https://plumedesign.atlassian.net/browse/THRIV-1069?atlOrigin=eyJpIjoiYjEzZTJjOTUxYWMyNGM4MmFmNTg0M2Q3ZDlmMTAzY2UiLCJwIjoiamlyYS1zbGFjay1pbnQifQ

        """
        # API Part
        logdef.info("#########################################################################\n")
        logdef.info("# API Clous URL (URL:thrive-dog1-usw2-api.data.plume.tech/ #)\n")
        logdef.info("# ---------------------------------------------------------------- #)\n")
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
        self.reponse = PWBFunc().GetDailySleepInsightList(finaltokenid,clouduserid,Starttimestamp,Endtimestamp)
        SleepInsight = self.reponse['data']
        RES_SleepInsightList= SleepInsight['dailySleepInsightList']
        logdef.info("####################################")
        logdef.info(RES_SleepInsightList) 
        logdef.info("####################################")
        # As talked in thrive channel -> should remTime + deepSleepTime + lightSleepTime
        # https://plumedesign.atlassian.net/browse/THRIV-1557 
        #totalSleepTime_API = [i['totalSleepTime'] for i in SleepInsight['dailySleepInsightList']]
        remTime_API = [i['remTime'] for i in SleepInsight['dailySleepInsightList']]
        deepSleepTime_API = [i['deepSleepTime'] for i in SleepInsight['dailySleepInsightList']] 
        lightSleepTime_API = [i['lightSleepTime'] for i in SleepInsight['dailySleepInsightList']]         
        totalSleepTime_API = remTime_API[0]+ deepSleepTime_API[0]+ lightSleepTime_API[0]
        totalSleepTime_API = str(totalSleepTime_API)      
        logdef.info("The totalSleepTime get from Backend API : ")
        logdef.info(totalSleepTime_API)
        Sleepscore_API = [i['sleepScore'] for i in SleepInsight['dailySleepInsightList']]
        Real_Sleepscore = Sleepscore_API[0]
        logdef.info("The SleepScore get from Backend API : ")
        logdef.info(Real_Sleepscore)        

        # APP Part
        wda.DEBUG = False # default False
        #wda.HTTP_TIMEOUT = 10.0 # default 60.0 seconds
        bundle_id = "com.plumewifi.plume.devintegration"  
        #d = wda.Client('http://192.168.1.111:8100')
        d = wda.USBClient("00008110-001405601129801E", port=8100)
        logdef.info(d.status())
        # Wait WDA ready
        d.wait_ready(timeout=300) 
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
        d.swipe(0.1, 0.7, 0.6, 0.7)
        time.sleep(1)
        # Get Sleep Hours from APP Sides
        if d(label="Sleep today").exists:
            sleep_array = {
                '24 hr': 24,
                '23 hr': 23,
                '22 hr': 22,
                '21 hr': 21, 
                '20 hr': 20,
                '19 hr': 19,
                '18 hr': 18,
                '17 hr': 17,
                '16 hr': 16,
                '15 hr': 15,
                '14 hr': 14,
                '13 hr': 13,
                '12 hr': 12,
                '11 hr': 11,
                '10 hr': 10,
                '9 hr': 9,
                '8 hr': 8,
                '7 hr': 7,
                '6 hr': 6,
                '5 hr': 5,
                '4 hr': 4,
                '3 hr': 3,
                '2 hr': 2,
                '1 hr': 1,
                '0 hr': 0,                                
            }

            for HOUR in sleep_array:
                if d(label=HOUR).exists:
                    REALL1_sleephr = sleep_array[HOUR]
                    logdef.info("#######################################")
                    logdef.info("The L1 Sleep Hours get from HomePASS IOS is : "+str(REALL1_sleephr))
                    logdef.info("#######################################")
                    break
            else:
                logdef.info("Not thing match")
            Time_asleep_sec = int(REALL1_sleephr) * 60 * 60
            logdef.info("#######################################") 
            logdef.info("Total Sec is : "+str(Time_asleep_sec))
            logdef.info("#######################################\n\n")                
            time.sleep(1) 
            d.screenshot().save("./pic/L1-Sleep-HOUR .png") # Good
            allure.attach.file("./pic/L1-Sleep-HOUR .png" , attachment_type=allure.attachment_type.PNG)
            # Get Sleep score from APP Side
            #d(label="Sleep score: 1")
        if d(label="Sleep today").exists:
            sleepscore_array = {
                'Sleep score: 1': 1,
                'Sleep score: 2': 2,
                'Sleep score: 3': 3,                                               
                'Sleep score: 4': 4,
                'Sleep score: 5': 5,                           
            }

            for SCORE in sleepscore_array:
                if d(label=SCORE).exists:
                    REALL1_score = sleepscore_array[SCORE]
                    logdef.info("#######################################")
                    logdef.info("The L1 Sleep SCORE get from HomePASS IOS is : "+str(REALL1_score))
                    logdef.info("#######################################")
                    break
            else:
                logdef.info("Not thing match")
            d.screenshot().save("./pic/L1-Sleep-SCORE .png") # Good
            allure.attach.file("./pic/L1-Sleep-SCORE .png" , attachment_type=allure.attachment_type.PNG) 


        # Back to previous page
        d.swipe(0.6, 0.7, 0.1, 0.7)

        ############################
        time.sleep(1)
        #s.swipe(0.5, 0.5, 0.5, 1.0)  # swipe middle to bottom
        ##d.swipe(0.6, 0.7, 0.1, 0.7) # from bottom right to bottom left
        for x in range(0, 5): 
            d.swipe(0.1, 0.7, 0.6, 0.7) #from bottom left to bottom right
            time.sleep(1) 
        time.sleep(1)          
        d.home()
        d.screenshot().save("./pic/HomePass_H.png") # Good
            
        time.sleep(2)        

    


        ##############
        ## Cloud API value and UI/UX value compare , the value should equal
        ## L1 Time sleep 0 ~10 
        ## https://plumedesign.atlassian.net/browse/MOBY-18220 

        try:
            assert int(Time_asleep_sec) == int(totalSleepTime_API)
            logdef.info("##################################################################\n\n")            
            logdef.info("PASS : L1_Sleep hours / Sec -> FrontEnd and Backend are the same\n\n")
            logdef.info("##################################################################\n\n")            
        except AssertionError as err:
            logdef.info("##################################################################\n\n")            
            logdef.info("FAIL : L1_Sleep hours / Sec -> FrontEnd and Backend are not equal\n\n")
            logdef.info("##################################################################\n\n")   
            d.screenshot("./pic/Sleep-error.png") # default format="pil
            allure.attach.file('./pic/Sleep-error.png' , attachment_type=allure.attachment_type.PNG)            
            time.sleep(3)
            raise
        ##############
        ## Cloud API value and UI/UX value compare , the value should equal
        ## L1 Sleep score
        try:
            assert int(Real_Sleepscore) == int(REALL1_score)
            logdef.info("##################################################################\n\n")            
            logdef.info("PASS : L1_Sleep SCORE -> FrontEnd and Backend are the same\n\n")
            logdef.info("##################################################################\n\n")                
        except AssertionError as err:
            logdef.info("##################################################################\n\n")            
            logdef.info("FAIL : L1_Sleep SCORE -> FrontEnd and Backend are not equal\n\n")
            logdef.info("##################################################################\n\n") 
            d.screenshot("./pic/Sleep-score-error.png") # default format="pil
            allure.attach.file('./pic/Sleep-score-error.png' , attachment_type=allure.attachment_type.PNG)            
            time.sleep(3)
            raise

        #assert int(REALL1_Readiness_score) == int(avgReadinessScore_API [0])
        #print("Test completed")
        logdef.info("Test completed")
        d.home()
        time.sleep(1)
        d.swipe(0.5, 0.1, 0.5, 1.0)  # from top to bottom
        time.sleep(3)
        d.press("home") # Press Home button 
        # Close app
        d.close()        