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
global usermail
global userpassword

logging.basicConfig()
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
devuserid = (configure['userinfo']['devuserid'])
devid = (configure['userinfo']['devid'])
usermail = (configure['userinfo']['usrid'])
userpassword = (configure['userinfo']['pwd'])

root_path = os.path.dirname(os.path.realpath(__file__))

#---------------------------------------------------
allurewiget() # for allure wiget display info

class PWBFunc:

    def __init__(self):
        os.popen("adb devices")
        self.cloudtokenid = None
        self.clouduserid = None
                          
    def homepassicon(self,d):
        # make sure entry to homePass logo
        if d(label="HomePass").exists:
           d(label="HomePass").click()            
           logdef.info("homepass-icon is displayed")
        time.sleep(2)
        if d(label="network connectivity x").exists:
           d(label="network connectivity x").click()   
 
    def entrySignOut(self,d):
        if d.xpath('//*[@label="Tab Bar"]/Button[3]').exists:
           d.xpath('//*[@label="Tab Bar"]/Button[3]').click()
           time.sleep(1)
           d.swipe_up()
           time.sleep(1)
           d.swipe_up()
           time.sleep(1)
        if d(label="Sign out").exists:
           d(label="Sign out").click()
           time.sleep(1)
           # Pop up Signing out
           if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').exists:
              d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').click()
              time.sleep(1)
        
        if d(label="Sign in", name="WelcomeViewController.signInButton").exists:
           logdef.info("Successful to Sign out")


    def Signintest(self,d): # step 1 of Sign in HomePassIOS
        #
        logdef.info('Step 1of Sign in HomePassIOS')
        #
        if d(label="Sign in", name="WelcomeViewController.signInButton").exists:
           d(label="Sign in", name="WelcomeViewController.signInButton").click()
           time.sleep(2)
           # enter your mail address
           if d(label="Your email").exists:
              d.xpath('//*[@label=""]').set_text(usermail)
              time.sleep(1)
              logdef.info('enter your mail address') 
              d.screenshot().save("./pic/usermail.png") 
              allure.attach.file("./pic/usermail.png" , attachment_type=allure.attachment_type.PNG)
              if d(label="Done").exists:
                 d(label="Done").click()
                 # Press next button
                 logdef.info('Press next button')
                 if d(name="EmailEntryAuthenticationViewController.nextButton").exists:
                    d(name="EmailEntryAuthenticationViewController.nextButton").click()
                    time.sleep(2)
                    logdef.info('Switch to Password button')
                    if d(name="MagicLinkAuthenticationViewController.switchToPasswordButton").exists:
                       d(name="MagicLinkAuthenticationViewController.switchToPasswordButton").click()
                       time.sleep(1)

                    # step 2 of Sign in tap password field / input password
                    logdef.info('Step 2 of Sign in tap password field / input password')
                    #
                    d.click(0.456, 0.472)   
                    if d.xpath('//*[@label="Your password"]').exists: 
                       d.xpath('//*[@label=""]').set_text(userpassword)
                       time.sleep(1)
                       d.screenshot().save("./pic/userpassword.png") 
                       allure.attach.file("./pic/userpassword.png" , attachment_type=allure.attachment_type.PNG)                      
                       time.sleep(1)
                    logdef.info('click Done button')
                    d.click(0.86, 0.581)
                    time.sleep(10)
                    if d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]/StaticText[1]').exists:
                       d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]/StaticText[1]').click()
                    
                    if d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]').exists:
                       d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]').click()
                    #Press Sigin
                    logdef.info('Press via xy table')
                    d.click(0.552, 0.8)
                    time.sleep(5)
                    logdef.info('Has been entry HomePass IOS APP') 
                    d.screenshot().save("./pic/Hasbeenenrty.png") 
                    allure.attach.file("./pic/Hasbeenenrty.png" , attachment_type=allure.attachment_type.PNG) 



    def entrySingin(self,d): # step 3 of Sign in
        logdef.info('Step 3 of Sign in to HomePass IOS') 

        if d(name="PasswordEntryAuthenticationViewController.signinButton").exists:
           d(name="PasswordEntryAuthenticationViewController.signinButton").click()
           time.sleep(13)
           logdef.info('Has been entry HomePass IOS APP') 
           d.screenshot().save("./pic/Hasbeenenrty.png") 
           allure.attach.file("./pic/Hasbeenenrty.png" , attachment_type=allure.attachment_type.PNG)             
        elif d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]/StaticText[1]').exists:
           d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]/StaticText[1]').click()   

           time.sleep(13)
           logdef.info('Has been entry HomePass IOS APP') 
           d.screenshot().save("./pic/Hasbeenenrty.png") 
           allure.attach.file("./pic/Hasbeenenrty.png" , attachment_type=allure.attachment_type.PNG)
        else:
           pass    

    def allowfunc(self,d):
        # Allow notification
        logdef.info("Trying to Detect HomePass Would Like to Send You Notifications")
        time.sleep(5)
        if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[1]/Other[1]/StaticText[1]').exists:
            d.screenshot().save("./pic/allowfunc.png") 
            allure.attach.file("./pic/allowfunc.png" , attachment_type=allure.attachment_type.PNG)              
            time.sleep(3)
            if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').exists:
               d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').click()
               logdef.info('Allow function has been created') 
               

class TestAPI(TestAPIWrap):
 
    def test_beacon_func(self):

        # Cloud first 
        logdef.info("# ---------------------------------------------------------------- #)\n")
        """   
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

        #Bundle IDs for native iPhone and iPad apps

        #https://support.apple.com/guide/deployment/bundle-ids-for-native-iphone-and-ipad-apps-depece748c41/web
        """

    
        wda.DEBUG = False # default False
        #wda.HTTP_TIMEOUT = 10.0 # default 60.0 seconds
        #bundle_id = "com.plumewifi.plume.devintegration"  
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

        # Trigger HomePass IOS
        PWBFunc().homepassicon(d)

        # Sigin HomePass 
        PWBFunc().Signintest(d)

        ## step 3 of Sign in HomePass
        PWBFunc().entrySingin(d)

        ## step 4 of the Allow notification
        PWBFunc().allowfunc(d)

        ## Step5 Sig-out HomePass APP
        PWBFunc().entrySignOut(d)

        
        d.home()
        logdef.info("Test completed")
        d.screenshot().save("./pic/Testcompleted.png") # Good
        allure.attach.file("./pic/Testcompleted.png" , attachment_type=allure.attachment_type.PNG)
        time.sleep(2)        
        #print("Test completed")
        d.home()
        time.sleep(1)
        d.swipe(0.5, 0.1, 0.5, 1.0)  # from top to bottom
        time.sleep(3)
        d.press("home") # Press Home button 
        # Close app
        d.close()
    