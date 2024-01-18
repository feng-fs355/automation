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
global is_displayed
global versionversion # real version get from HomePass UI
global LatestVersion # Select latest version
global PreviousVersion    # select previous version



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
PreviousVersion = (configure['HomePas_version'] ['Previous'])

root_path = os.path.dirname(os.path.realpath(__file__))

#---------------------------------------------------
allurewiget() # for allure wiget display info

# 

class PWBFunc:

    def __init__(self):
        os.popen("adb devices")
        self.cloudtokenid = None
        self.clouduserid = None
   
    def remove_homepass(self,d):
        # remove homepass first 
        """
        Open the terminal and run the following command to uninstall the app:
        ideviceinstaller -U com.bundle.identifier
        ideviceinstaller -U com.plumewifi.plume.devintegration
        """

        # HomePass Package name for checking
        package_name = "com.plumewifi.plume.devintegration"

        # Check which package has been installed in the Mobile devices
        adb_output = subprocess.check_output(['ideviceinstaller', '-U', package_name]).split()


    def installpreviuos(self,d):
        # 2023/11/15
        if d.xpath('//Image').exists:
            d.xpath('//Image').click()
            if d.xpath('//ScrollView/Other[1]/Button[3]').exists:
                logdef.info("Prepare to Previous Builds")
                d.xpath('//ScrollView/Other[1]/Button[3]').click()
                time.sleep(10)
        # Previous builds page has been displayed
        if d.xpath('//*[@label="PlumeDevelopment"]').exists:
            logdef.info("Previous page is displayed")

            # 3.129
            if d.xpath('//CollectionView/Cell[2]').exists:
                logdef.info("Press Previous version item")
                d.xpath('//CollectionView/Cell[2]').click()
                if d.xpath('//*[@label="INSTALL"]').exists:
                    logdef.info("Install PreviousVersion button is ready")
                    d.xpath('//*[@label="INSTALL"]').click()
                    logdef.info("Install PreviousVersion is Processing")
                    d.screenshot().save("./pic/PreInstalling.png") 
                    allure.attach.file("./pic/PreInstalling.png" , attachment_type=allure.attachment_type.PNG)               
                    time.sleep(33)
                # pop up Install Older Build?
                if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[1]/Other[1]/StaticText[1]').exists:
                    if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[1]/Other[1]/StaticText[1]').value == 'Install Older Build?':
                        #Press Install
                        d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').click()
                
                # Open Button is displayed    
                logdef.info("Open Button is displayed")
                if d.xpath('//*[@label="OPEN"]').exists:
                    logdef.info("Press OPEN BUTTON")
                    d.xpath('//*[@label="OPEN"]').click()
                    time.sleep(6)
                    logdef.info("Next Button is displayed")
                    d.screenshot().save("./pic/NextButton.png") 
                    allure.attach.file("./pic/NextButton.png" , attachment_type=allure.attachment_type.PNG)
                    time.sleep(5)
                    # Next Button                      
                    if d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[1]').exists: 
                       d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[1]').click()
                       time.sleep(3)
                       # Start Button
                       logdef.info("Start Test is displayed")
                       d.screenshot().save("./pic/Start-testing.png") 
                       allure.attach.file("./pic/Start-testing.png" , attachment_type=allure.attachment_type.PNG)
                if d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[1]/StaticText[1]').exists:
                    if d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[1]/StaticText[1]').value == 'Start Testing':
                       logdef.info("Start Testing")
                       d.click(0.729, 0.873)
                       logdef.info("Button has been click")
                       time.sleep(1)
                       d.screenshot().save("./pic/HomePass_H.png") 
                       allure.attach.file("./pic/HomePass_H.png" , attachment_type=allure.attachment_type.PNG) 
                         

    def homepasslogo(self,d):
        # make sure entry to homePass logo
        if d(name="homepass-logo").exists:
           logdef.info("homepass-logo")
           d.screenshot().save("./pic/homepass-logo.png") 
           allure.attach.file("./pic/homepass-logo.png" , attachment_type=allure.attachment_type.PNG)

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
        logdef.info("#########################################################################\n")
        logdef.info("# API Clous URL (URL:thrive-dog1-usw2-api.data.plume.tech/ #)\n")
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
        # Remove HomePASS IPK first
        PWBFunc().remove_homepass(d)
        # Trigger TestFlight
        if d.xpath('//*[@label="TestFlight"]').exists:
           logdef.info("TestFlight has been trigger") 
           d.xpath('//*[@label="TestFlight"]').click()
           d.screenshot().save("./pic/TestFlight.png") 
           allure.attach.file("./pic/TestFlight.png" , attachment_type=allure.attachment_type.PNG)
        time.sleep(2)

        ## Install IPK previous build
        PWBFunc().installpreviuos(d)

        # Trigger HomePass IOS
        PWBFunc().homepasslogo(d)

        # Sigin HomePass 
        PWBFunc().Signintest(d)

        ## step 3 of Sign in HomePass
        PWBFunc().entrySingin(d)

        ## step 4 of the Allow notification
        PWBFunc().allowfunc(d)

        """
        d.swipe_up()
        time.sleep(1)
        d.swipe_up()
        time.sleep(1)
        d.swipe(0.1, 0.7, 0.6, 0.7)
        time.sleep(1)
        d.swipe(0.6, 0.7, 0.1, 0.7)
        
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
        """
        # Close app
        package_name = 'com.apple.TestFlight'

        # Stop the app
        d.app_stop(package_name)
        d.close()
        