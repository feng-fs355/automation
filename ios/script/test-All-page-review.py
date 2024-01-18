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
apiNameGetReadinessInsightSummary = 'GetReadinessInsightSummary'

apiNameGetDailyReadinessInsightList = 'GetDailyReadinessInsightList'

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


 
class TestAPI(TestAPIWrap):
 
    def test_beacon_func(self):


        wda.DEBUG = False # default False
        #wda.HTTP_TIMEOUT = 10.0 # default 60.0 seconds
        bundle_id = "com.plumewifi.plume.devintegration"  
        #d = wda.Client('http://192.168.1.111:8100')
        d = wda.USBClient("00008110-001405601129801E", port=8100)
        # IOS status    
        logdef.info(d.status())
        status = d.status()
    
        # Extract the IP address from the status
        device_ip = status['value']['ip']
        logdef.info(device_ip)       
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
        d.screenshot().save("./pic/4.png") # Good
        allure.attach.file("./pic/4.png" , attachment_type=allure.attachment_type.PNG)    
 

        logdef.info("Test completed")
        d.home()
        time.sleep(1)
        #d.swipe(0.5, 0.1, 0.5, 1.0)  # from top to bottom
        #time.sleep(3)
        #d.press("home") # Press Home button 
        # Close app
        d.close()
