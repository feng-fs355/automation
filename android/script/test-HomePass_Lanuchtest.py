#!/usr/bin/env python3
#coding=utf-8
import uiautomator2 as Device
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
#import numpy as np
import subprocess
import sys
import struct
from time import sleep  # time for sleep
from collections import namedtuple
import threading
import pygatt
import logging
from binascii import hexlify
import allure # allure report
import platform
import datetime
from datetime import datetime
from datetime import date
global DEV

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
DEV = (configure['userinfo']['androiddev1'])
timeout= 20.0  
root_path = os.path.dirname(os.path.realpath(__file__))

# TICKET : https://plumedesign.atlassian.net/browse/THRIV-1311


############################################################

# Should Use Authorize process first

# API1 (For Authorize / Per session base)

apiNameCloudLogin = 'PlumeCloudLogin'

apiNameAuthPlumeToken = 'AuthenticateWithPlumeToken'

# API3
# /pwb/GetDailySleepInsightList
# API to get L1 sleep info by user, time period and interval.
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

    def captureadblog(self):
        #########################################
        current_GMT = time.gmtime()
        logdef.info(current_GMT)
        logdef.info("\n\n")
        time_stamp = calendar.timegm(current_GMT)
        TODAY =  datetime.now()
        logdef.info(TODAY.year)
        logdef.info(TODAY.month)
        logdef.info(TODAY.day)
        dtime = datetime(TODAY.year, TODAY.month, TODAY.day, 0)        
        adbtimestamp = int(round(dtime.timestamp()))
        logdef.info("************************************************\n\n")

        # adb log file name
        desrinationfile = './adblog/adblog-'+str(adbtimestamp)+'.txt'
        r = d.shell("logcat", stream=True)
        # r: requests.models.Response
        deadline = time.time() + 30 # run maxium 30s
        try:
            for line in r.iter_lines(): # r.iter_lines(chunk_size=512, decode_unicode=None, delimiter=None)
                if time.time() > deadline:
                    break
                with open(desrinationfile, 'a') as f:
                    data1 = line.decode("utf-8", "ignore")
                    json.dump(data1, f)
        finally:
            r.close() # this method must be called


    def reboot_device(self):
        # Reboot the device
        RESULT = os.popen("adb -s "+str(DEV)+" reboot",'r',1)
        logdef.info(RESULT)

    def check_connection(self):
        # Check if the device is connected
        result = subprocess.run(["adb", 'devices'], capture_output=True, text=True)
        output = result.stdout.strip()
        if DEV in output:
            print("Device is connected.")
            return True
        else:
            print("Device is not connected.")
            return False

    def mobile_reboot(self):
        # 
        RESULT = os.popen("adb -s "+str(DEV)+" reboot",'r',1)
        logdef.info(RESULT)

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

    def device_setting(self,d):   # device setting page for device 1
        info=d.info
        width=info['displayWidth']
        Height=info['displayHeight']
        return width,Height        
    def swipeUp(self,d): # big swipe up function for device 1
        print("swipeUp feature\n")
        l=self.device_setting(d)
        width= l[0]
        Height= l[1]    
        print(width)
        print(Height)
        x1 = width * 0.5    
        y1 = Height * 0.9  
        y2 = Height * 0.1        
        d.swipe(x1, y1, x1, y2)
    def swipeDown(self,d):  # big swipe swipe function for device 1
        print("swipeDown feature\n")
        l=self.device_setting(d)
        width= l[0]
        Height= l[1]    
        print(width)
        print(Height)
        x1 = width * 0.5      
        y1 = Height * 0.25
        y2 = Height * 0.75
        d.swipe(x1, y1, x1, y2)

    def swipeleft(self,d):  # big swipe swipe function for device 1
        print("swipeleft feature\n")
        l=self.device_setting(d)
        width= l[0]
        Height= l[1]    
        print(width)
        print(Height)
        x1 = width * 0.7
        x2 = width * 0.1     
        y1 = Height * 0.4
        y2 = Height * 0.4
        d.swipe(x1, y1, x2, y2)        
    
    def CleanAPP(self,d):
        # Clean all APP on background
        if d(text="Close all",className="android.widget.Button").exists:
            d(text="Close all",className="android.widget.Button").click()

    def HomePass(self,d):
        # Lanch HomePass app
        if d(textContains="HomePass",className="android.widget.TextView").exists:
            d(textContains="HomePass",className="android.widget.TextView").click()
            logdef.debug("Lanch the HomePass APP successfully.")

            return True
        else:
            logdef.debug("Failed to lanch the HomePass® APP!")
            PWBFunc().captureadblog() # adb log
            return False


    def Adapt(self,d):
        # Lanch Thrive HomePage
        # resourceId="com.plumewifi.plume.dogfood:id/home_section_title" 

        if d(text="Your network is offline. Tap here for troubleshooting tips.",resourceId="com.plumewifi.plume.dogfood:id/snackbar_text").exists:
            d(text="Your network is offline. Tap here for troubleshooting tips.",resourceId="com.plumewifi.plume.dogfood:id/snackbar_text").sibling(resourceId="com.plumewifi.plume.dogfood:id/snackbar_action").click()

        if d(resourceId="com.plumewifi.plume.dogfood:id/partner_home_logo_brand").exists:
            logdef.debug("Trigger HomePage successfully.")
            time.sleep(3)
            self.swipeUp(d)
            time.sleep(3)
            self.swipeUp(d)
            d.screenshot("./pic/Adapt.png")
            allure.attach.file("./pic/Adapt.png" , attachment_type=allure.attachment_type.PNG) 
            if d(text="Thrive",resourceId="com.plumewifi.plume.dogfood:id/home_section_title").exists:
               self.swipeUp(d)
               time.sleep(3)
               d.screenshot("./pic/L1_Activity.png")
               allure.attach.file("./pic/L1_Activity.png" , attachment_type=allure.attachment_type.PNG) 
            return True
        else:
            logdef.debug("Trigger HomePage Failed")
            d.screenshot("./pic/FAIL-HOMEPAGE.png")
            allure.attach.file("./pic/FAIL-HOMEPAGE.png" , attachment_type=allure.attachment_type.PNG)
            if d(resourceId="com.plumewifi.plume.dogfood:id/dialog_base_message_title").exists:
                d(resourceId="com.plumewifi.plume.dogfood:id/dialog_base_message_primary_action").click()
                PWBFunc().captureadblog() # adb log
                return False                
            else:
                PWBFunc().captureadblog() # adb log
                return False
                               
class TestAPI(TestAPIWrap):
 
    def test_beacon_func(self):

        """
        Android Phone HomePass APP

        But for Sleep score , the frontend / backend is not consistent. So far, would like to file another automation bug for that.
        
        API Clous URL (URL:thrive-dog1-usw2-api.data.plume.tech

        https://testrail.sso.plume.tech/index.php?/cases/view/2317742

        THRIV-1396
        
        create test-6057-HomePass_L1_Sleep into Jenkins

        {
            "data": {
                "userId": "62a2d6708a13a8000a1b40b9",
                "startTime": 1686499200,
                "endTime": 1686582000,
                "dailySleepInsightList": [
                    {
                        "userId": "62a2d6708a13a8000a1b40b9",
                        "sleepDate": 1686585600,
                        "sleepScore": 6,
                        "deepSleepTime": 5400,
                        "awakeTime": 607,
                        "remTime": 4800,
                        "lightSleepTime": 7800,
                        "totalSleepTime": 18000,
                        "startTime": 1686506473,
                        "endTime": 1686525080,
                        "wakeUpTimes": 2,
                        "maxHr": 123,
                        "avgHr": 65,
                        "minHr": 53,
                        "maxSpo2": 100,
                        "avgSpo2": 99,
                        "minSpo2": 98,
                        "timeZone": "Asia/Brunei",
                        "utcOffset": 8,
                        "sleepSessionId": "8501c6ae1fb068bf766b8d5a847f7bca"
                    }
                ]
            },
            "result": {
                "code": 201000,
                "message": "Successfully."
            }        
         

        """
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
        cmd = 'adb kill-server'
        command = os.popen(cmd)
        time.sleep(1.5)
        cmd = 'adb start-server'
        command = os.popen(cmd) 
        time.sleep(1.5)        
        cmd = 'adb devices'
        command = os.popen(cmd)
        time.sleep(1.5)
        # Force to stop the HomePass APP
        cmd = "adb -s "+str(DEV)+" shell am force-stop com.plumewifi.plume.dogfood"
        command = os.popen(cmd)
        time.sleep(1.5)
        logdef.info("##############################################################################################\n")
        logdef.info("#  Test case : ( THRIV-1369: test-6057-HomePass_L1_Sleep into jenkins        (HomePass App)  #)\n")        
        logdef.info("##############################################################################################)\n") 
        print(f'Scan \"PlumeF\"')
        global checkpoint
        global d 
        global device   
        # get android phone serial number
        d = Device.connect(DEV)
        time.sleep(3)
        print(d.info)
        # uiautomator2
        d.screen_on() # turn on the screen
        time.sleep(1.5)
        # swipe up to unlock the screen
        d.swipe(530,2150,630,1080)
        time.sleep(3)
        # backtohome
        d.press("home")
        #d.screenshot("./pic/home.png") # default format="pil
        #time.sleep(2)
        #allure.attach.file('./pic/home.png' , attachment_type=allure.attachment_type.PNG)  
        time.sleep(3)
        # Press recent button
        # uiautomator2
        d.press("recent")
        time.sleep(2)        
        d.screenshot("./pic/recent.png") # default format="pil
        allure.attach.file('./pic/recent.png' , attachment_type=allure.attachment_type.PNG)           
        time.sleep(3)
        PWBFunc().CleanAPP(d)
        cmd = "adb -s "+str(DEV)+"  shell am force-stop com.plumewifi.plume.dogfood"
        command = os.popen(cmd)
        time.sleep(5)
        print(d.info)  
        # Lanch HomePass app
        PWBFunc().HomePass(d)   
        time.sleep(20)
        # Lanch HomePass app via cmd
        cmd = "adb -s "+str(DEV)+" shell am start -n com.plumewifi.plume.dogfood/com.plume.residential.ui.main.MainActivity"
        command = os.popen(cmd) 
        time.sleep(20)
        d.screenshot("./pic/HomePass.png") # default format="pil
        allure.attach.file('./pic/HomePass.png' , attachment_type=allure.attachment_type.PNG)            
        time.sleep(3)
        RESULT = PWBFunc().Adapt(d)
        if RESULT != True:
            logdef.info("Status is wrong and will Mobile reboot") 
            PWBFunc().reboot_device() # Reboot the device
            # Wait for the device to reboot
            # Add any necessary delay here based on your device
            # Check the connection
            time.sleep(60)
            CHECKConnection= PWBFunc().check_connection()
            if CHECKConnection != False:
               TestAPI().test_beacon_func()
            else:
               logdef.info("Adb check_connection fail after adb reboot, please check testbed")
               sys.exit(1)    
        #global SCORE
        """
        if d(resourceId="com.plumewifi.plume.dogfood:id/daily_fitness_activity_summary_step_count", packageName="com.plumewifi.plume.dogfood").exists:
            #swipleft
            d(resourceId="com.plumewifi.plume.dogfood:id/daily_fitness_activity_summary_step_count", packageName="com.plumewifi.plume.dogfood").swipe("left", steps=15)
            time.sleep(1)                          
            d.screenshot("./pic/swipeleft.png") # default format="pil
            allure.attach.file('./pic/swipeleft.png' , attachment_type=allure.attachment_type.PNG)                  
       
        if d(text="Readiness today",resourceId="com.plumewifi.plume.dogfood:id/today_readiness_summary_day_label").exists:
            d(text="Readiness today",resourceId="com.plumewifi.plume.dogfood:id/today_readiness_summary_day_label").swipe("left", steps=20)
            time.sleep(1)                          
            d.screenshot("./pic/swipeleft.png") # default format="pil
            allure.attach.file('./pic/swipeleft.png' , attachment_type=allure.attachment_type.PNG) 
        else:
            logdef.info("didn't swipe to exaclty page ,please double check script or HomePass APP")
            PWBFunc().captureadblog() # adb log
            # Force to stop the HomePass APP
            cmd = "adb -s "+str(DEV)+" shell am force-stop com.plumewifi.plume.dogfood"
            command = os.popen(cmd)             
            time.sleep(1)
            sys.exit(1) 
        """ 
          
        # Open notification and verify it
        d.open_notification()
        time.sleep(3)    
        d.screenshot("./pic/notification.png") # default format="pil
        allure.attach.file('./pic/notification.png' , attachment_type=allure.attachment_type.PNG)        
        # Force to stop the HomePass APP
        cmd = "adb -s "+str(DEV)+" shell am force-stop com.plumewifi.plume.dogfood"
        command = os.popen(cmd)
        time.sleep(1.5)     
        logdef.info("For Time asleep , the Frontend / Backend are equal --> PASS")
        # backtohome
        d.press("home")        
        logdef.info("Test completed")
        logdef.info("Test completed")
        