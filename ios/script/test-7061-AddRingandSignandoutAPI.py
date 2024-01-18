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
from subprocess import Popen, PIPE
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
global sn
global devid
global sourcefile

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
sn = (configure['userinfo']['sn'])
devid = (configure['userinfo']['devid'])

root_path = os.path.dirname(os.path.realpath(__file__))

#---------------------------------------------------
allurewiget() # for allure wiget display info

# For unregister py file
sourcefile = 'test-ios_Unregister_Device.py'



class PWBFunc:

    def __init__(self):
        os.popen("adb devices")
        self.cloudtokenid = None
        self.clouduserid = None

    def device_setting(self,d):   # device setting page for device 1
        #info=d.info
        info=d.window_size()
        logdef.info(info)
        pattern = r"Size\(width=(\d+), height=(\d+)\)"
        match = re.search(pattern, str(info))
        # check match condition
        if match:

            width = match.group(1)
            height = match.group(2)

            logdef.info(f"Width: {width}, Height: {height}")
        else:
            logdef.info("Didnt get value")

        #Size(width=390, height=844)
        width=int(width)
        height=int(height)
        return width,height        
    def swipeUp(self,d): # big swipe up function for device 1
        print("swipeUp feature\n")
        l=self.device_setting(d)
        width= l[0]
        Height= l[1]    
        print(width)
        print(Height)
        x1 = width * 0.5 // 1   
        y1 = Height * 0.9 // 1 
        y2 = Height * 0.1 // 1       
        logdef.info(x1)
        logdef.info(y1)
        logdef.info(y2)
        #s.swipe(0.5, 0.5, 0.5, 1.0)  # swipe middle to bottom
        ##d.swipe(0.6, 0.7, 0.1, 0.7) # from bottom right to bottom left
        for x in range(0, 5): 
            d.swipe(0.5, 0.3, 0.5, 0.1) 
            time.sleep(1) 
                          
    def homepassicon(self,d):
        # make sure entry to homePass logo
        if d(label="HomePass").exists:
           d(label="HomePass").click()            
           logdef.info("homepass-icon is displayed")
        time.sleep(1)

        if d(label="network connectivity x").exists:
           d(label="network connectivity x").click()  
        time.sleep(1)

        if d(label="network connectivity x").exists:
           d(label="network connectivity x").click() 

        time.sleep(1)

        if d(label="network connectivity x").exists:
           d(label="network connectivity x").click()                       


    def Unregister(self):

        num_of_inputs = len(sys.argv)
        #collection = sys.argv[1]
        collection = str(sourcefile+" --alluredir=./allure-results")
        environment = None
        global_vars = None

        if num_of_inputs > 2:
            environment = sys.argv[2]
        if num_of_inputs > 3:
            golbals = sys.argv[3]

        command = "python3 -m pytest -vv "+collection
        #if environment:
        #    command += " -e "+environment
        #if global_vars:
        #    command += " -g "+global_vars
       

        command = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = command.communicate()
        logdef.info(output)
        print(output)

        if error:
            email_body = "Error while running the command"
            logdef.info(email_body)
            print(email_body)
        else:
            email_body = output.decode('utf-8')
            logdef.info(email_body)
            print(email_body)


    def AddThriveRing(self,d):
        # Add ring via home Pass
        if d.xpath('//*[@label="Tab Bar"]/Button[3]').exists:
           d.xpath('//*[@label="Tab Bar"]/Button[3]').click()
           #time.sleep(1)
           #d.swipe_up()
           #time.sleep(1)
           d.screenshot().save("./pic/AddThriveRing.png") 
           allure.attach.file("./pic/AddThriveRing.png" , attachment_type=allure.attachment_type.PNG) 
           time.sleep(3)
        if d(label="Add Plume Ring").exists:
           d(label="Add Plume Ring").click()   
           time.sleep(1)
        if d.xpath('//Window[1]/Other[2]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[2]/StaticText[1]').exists:
           d.xpath('//Window[1]/Other[2]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[2]/StaticText[1]').click()
           time.sleep(1)
        if d(name="icon-64-ring").exists:
           d(name="icon-64-ring").click()
           time.sleep(1) 

        ## Accept 
        
        if d.xpath('//Window/Other[2]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[2]').exists:
           d.xpath('//Window/Other[2]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[2]').click()   
        time.sleep(3)

        if d.xpath('//Window/Other[2]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[2]').exists:
           d.xpath('//Window/Other[2]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Button[2]').click() 
        time.sleep(3)         
        ###    Now let's connect your ring
        # Press Next 
        if d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[4]/Button[1]').exists:
           d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[4]/Button[1]').click()
        # Alow bluetooth enable
        if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').exists:
           d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').click()   

        # Press add Ring
        if d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/CollectionView[1]/Cell[3]/Other[1]/Other[1]/Other[2]/CollectionView[1]/Cell[4]').exists:
           d.xpath('//Window[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/Other[1]/CollectionView[1]/Cell[3]/Other[1]/Other[1]/Other[2]/CollectionView[1]/Cell[4]').click()
           
        # Wait for sec
        time.sleep(10) # wait for 10 sec
        d.screenshot().save("./pic/ADDRing.png") 
        allure.attach.file("./pic/ADDRing.png" , attachment_type=allure.attachment_type.PNG) 
        time.sleep(3)


    def selectRingtoAdd(self,d):
         if d.xpath('//*[@label="Size 10 SN KD909A0084"]').exists:

           # connect
           if d.xpath('//Window/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]').exists:
              d.xpath('//Window/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]').click()
              time.sleep(10)
              d.screenshot().save("./pic/Connecting.png") 
              allure.attach.file("./pic/Connecting.png" , attachment_type=allure.attachment_type.PNG)
              time.sleep(3)

    def SetupYourself(self,d):
         # Select Year of Birth
         if d.xpath('//Table/Cell[1]/Button[1]').exists:
             d.xpath('//Table/Cell[1]/Button[1]').click()

             time.sleep(2)
             #s.swipe(0.5, 0.5, 0.5, 1.0)  # swipe middle to bottom
             ##d.swipe(0.6, 0.7, 0.1, 0.7) # from bottom right to bottom left
             d.swipe(0.5, 0.5, 0.5, 0.1) 
             time.sleep(1)
             d.swipe(0.5, 0.4, 0.5, 0.1) 
             time.sleep(1)
             d.click(0.49, 0.44) # Press 2007
             d.click(0.49, 0.44) # Press 2007
             time.sleep(1)
             logdef.debug("Set Year of birth successfully")
         else:
             logdef.debug("Failed to set Year of birth")
     

         ## For Gender
         if d.xpath('//Table/Cell[3]/Button[1]/StaticText[1]').exists:
             d.xpath('//Table/Cell[3]/Button[1]/StaticText[1]').click()
             time.sleep(2)
             # Select Male
             #s.swipe(0.5, 0.5, 0.5, 1.0)  # swipe middle to bottom
             ##d.swipe(0.6, 0.7, 0.1, 0.7) # from bottom right to bottom left
             d.swipe(0.5, 0.5, 0.5, 0.1) 
             time.sleep(1)
             d.swipe(0.5, 0.4, 0.5, 0.1) 
             time.sleep(1)
             d.swipe(0.5, 0.3, 0.5, 0.1) 
             time.sleep(1)             
             d.click(0.494, 0.5) # Press Male
             d.click(0.494, 0.5) # Press Male
         else:
             logdef.debug("Failed to set the Gender")

         # Usual sleep time   
         if d.xpath('//Table/Cell[4]/Button[1]/StaticText[1]').exists:
             d.xpath('//Table/Cell[4]/Button[1]/StaticText[1]').click()
             time.sleep(2)
             #s.swipe(0.5, 0.5, 0.5, 1.0)  # swipe middle to bottom
             ##d.swipe(0.6, 0.7, 0.1, 0.7) # from bottom right to bottom left
             d.swipe(0.5, 0.5, 0.5, 0.1) 
             time.sleep(1)
             d.swipe(0.5, 0.6, 0.5, 0.1) 
             #d.click(0.798, 0.564)
             logdef.debug("Set Usual sleep time successfully")

         else:
             logdef.debug("Failed to set Usual sleep time") 

         # next
         if d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Button[1]/StaticText[1]').exists:
             d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Button[1]/StaticText[1]').click()
             logdef.debug("Click Next button successfully")
             time.sleep(2)
         else:
             logdef.debug("Failed to click Next button")

         # Enable notification # 20231204 add
 
         if d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]').exists:
            d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[2]/Other[1]/Button[1]').click()

         if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').exists:
            d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').click()  

         time.sleep(3)
         # I understand
         if d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[3]/Button[1]').exists:  
            d.xpath('//Window[1]/Other[2]/Other[1]/Other[1]/Other[1]/Other[1]/Other[3]/Button[1]').click()

         time.sleep(2)
         # Complete
         if d.xpath('//Button/StaticText[1]').exists:
            d.xpath('//Button/StaticText[1]').click() 
              
         # Ring has been added
         logdef.info('Ring has been added') 
         d.screenshot().save("./pic/Ringadded.png") 
         allure.attach.file("./pic/Ringadded.png" , attachment_type=allure.attachment_type.PNG)
         time.sleep(1)
      
    
    def entrySignOut(self,d):
        # Detect network notification
        if d(label="network connectivity x").exists:
           d(label="network connectivity x").click()
        time.sleep(1)
           
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
            #d.screenshot().save("./pic/allowfunc.png") 
            #allure.attach.file("./pic/allowfunc.png" , attachment_type=allure.attachment_type.PNG)              
            time.sleep(1)
            if d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').exists:
               d.xpath('//Alert/Other[1]/Other[1]/Other[2]/ScrollView[2]/Other[1]/Other[1]/Other[3]').click()
               logdef.info('Allow function has been created') 
           

    def closeHomePass(self,d):
        time.sleep(1)
        # Close app
        package_name = 'com.plumewifi.plume.devintegration'
        # Stop the app
        d.app_stop(package_name)    
        time.sleep(1)


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


        
        # Close HomePass
        PWBFunc().closeHomePass(d)


        # Trigger HomePass IOS
        PWBFunc().homepassicon(d)

 
        PWBFunc().device_setting(d)

        # Sigin HomePass 
        PWBFunc().Signintest(d)

        ## step 3 of Sign in HomePass
        PWBFunc().entrySingin(d)

        ## step 4 of the Allow notification
        PWBFunc().allowfunc(d)


        ## step 5 Add Ring process 1
        PWBFunc().AddThriveRing(d)

        ## step 6 Add Ring process 2
        PWBFunc().selectRingtoAdd(d)

        ## Step 7 Add Ring process 3 
        PWBFunc().SetupYourself(d)

        ## Step 8 Unregister
        PWBFunc().Unregister()

        time.sleep(10)

        # Close HomePass
        PWBFunc().closeHomePass(d)


        
        
    
        # Trigger HomePass again
        PWBFunc().homepassicon(d)
        time.sleep(15)
        ##if d.xpath('//*[@label="Your network is offline. Tap here for troubleshooting tips."]').exists:
        #   d.xpath('//*[@label="network connectivity x"]').click()
        ## Step9 Sig-out HomePass APP
        PWBFunc().entrySignOut(d)


        d.home()
        logdef.info("Test completed")
        d.screenshot().save("./pic/Testcompleted.png") # Good
        allure.attach.file("./pic/Testcompleted.png" , attachment_type=allure.attachment_type.PNG)
        time.sleep(2)        
        #print("Test completed")
        d.home()
        time.sleep(1)
        # Close HomePass
        PWBFunc().closeHomePass(d)


        d.close()
    