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
global sourcefile
global usermail
global userpassword

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
DEV = (configure['userinfo']['androiddev1'])
usermail = (configure['userinfo']['usrid'])
userpassword = (configure['userinfo']['pwd'])

# APP Package name
## sourcefile = (configure['testapk']['pythonfile'])

timeout= 30.0  
root_path = os.path.dirname(os.path.realpath(__file__))

# TICKET : https://plumedesign.atlassian.net/browse/THRIV-2511


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
        if d(resourceId="com.android.launcher3:id/action_clearall").exists:
           d(resourceId="com.android.launcher3:id/action_clearall").click()

    def Signintest(self,d): # step 1 of Sign in
        #d(resourceId="com.plumewifi.plume.dogfood:id/launch_sign_in_button")
        if d(resourceId="com.plumewifi.plume.dogfood:id/launch_sign_in_button").exists:
            logdef.info("HomePass Sign in button is displayed") 
            d.screenshot("./pic/Signintest.png")
            allure.attach.file("./pic/Signintest.png" , attachment_type=allure.attachment_type.PNG)              
            d(resourceId="com.plumewifi.plume.dogfood:id/launch_sign_in_button").click()
            time.sleep(3)
            if d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/text_input_layout"]/android.widget.FrameLayout[1]').exists:                  
              d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/text_input_layout"]/android.widget.FrameLayout[1]').set_text(usermail)
              sleep(1)
              # Press Next
              if d(resourceId="com.plumewifi.plume.dogfood:id/email_entry_authentication_next_action").exists:
                d(resourceId="com.plumewifi.plume.dogfood:id/email_entry_authentication_next_action").click()
                time.sleep(5)
                #Switch to password 
                # 540,2150 # for sony phone
                os.system("adb -s "+str(DEV)+" shell input tap 540 2150")
                time.sleep(2)          
                if d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/magic_link_authentication_switch_to_password_action"]').exists:   
                   d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/magic_link_authentication_switch_to_password_action"]').click()
            
                if d(resourceId="com.plumewifi.plume.dogfood:id/magic_link_authentication_switch_to_password_action").exists:
                   d(resourceId="com.plumewifi.plume.dogfood:id/magic_link_authentication_switch_to_password_action").click()

    def keyinpassword(self,d): # step 2 of Sign in
        #d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/text_input_layout"]/android.widget.FrameLayout[1]')
        if d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/text_input_layout"]/android.widget.FrameLayout[1]').exists:
           d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/text_input_layout"]/android.widget.FrameLayout[1]').set_text(userpassword)
    
    def entrySingin(self,d): # step 3 of Sign in
        #d(resourceId="com.plumewifi.plume.dogfood:id/password_entry_authentication_sign_in_action")
        if d(resourceId="com.plumewifi.plume.dogfood:id/password_entry_authentication_sign_in_action").exists:
           d(resourceId="com.plumewifi.plume.dogfood:id/password_entry_authentication_sign_in_action").click()
           time.sleep(3)
           if d(resourceId="com.plumewifi.plume.dogfood:id/dialog_base_message_primary_action").exists: 
               d(resourceId="com.plumewifi.plume.dogfood:id/dialog_base_message_primary_action").click()
               time.sleep(20) 
               logdef.info("HomePass has been Sign") 
               d.screenshot("./pic/HOMEPASSInstallOK.png")
               allure.attach.file("./pic/HOMEPASSInstallOK.png" , attachment_type=allure.attachment_type.PNG)            

        ## Add 2023/11/1 since Sony v10 didn't popup those information
        time.sleep(15)                  
        if d(resourceId="com.plumewifi.plume.dogfood:id/dialog_base_message_primary_action").exists:
           d(resourceId="com.plumewifi.plume.dogfood:id/dialog_base_message_primary_action").click()
        elif d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/dialog_base_message_primary_action"]').exists:
           d.xpath('//*[@resource-id="com.plumewifi.plume.dogfood:id/dialog_base_message_primary_action"]').click()  
        else:
            # pixel phone click permission  
            d.click(497, 887)
            time.sleep(2)
            if d.xpath('//*[@text="Permissions"]').exists:
              d.xpath('//*[@text="Permissions"]').click()
              logdef.info("click permission ") 
              d.screenshot("./pic/clickpermission.png")
              allure.attach.file("./pic/clickpermission.png" , attachment_type=allure.attachment_type.PNG)
        ##################################################################################################        
        # Click "While using the app"##  
        if d(textContains="While using the app",resourceId="com.android.permissioncontroller:id/permission_allow_foreground_only_button").exists:
            d(textContains="While using the app",resourceId="com.android.permissioncontroller:id/permission_allow_foreground_only_button").click()
            time.sleep(3)
        else:
            if d(textContains="While using the app").exists:
               d(textContains="While using the app").click()

          
            logdef.info("click While using the app ") 
            d.screenshot("./pic/Whileusingtheapp.png")
            allure.attach.file("./pic/Whileusingtheapp.png" , attachment_type=allure.attachment_type.PNG)
               
            # Pixel "While using the app"  
            d.click(497, 501)   
        # Click allow button   
        if d.xpath('//*[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]').exists:
            logdef.info("Click allow button") 
            d.screenshot("./pic/Clickallowbutton.png")
            allure.attach.file("./pic/Clickallowbutton.png" , attachment_type=allure.attachment_type.PNG)  
            d.xpath('//*[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]').click()                

        if d.xpath('//*[@text="Location"]').exists:
            d.xpath('//*[@text="Location"]').click() 

        if d.xpath('//*[@resource-id="com.android.permissioncontroller:id/allow_foreground_only_radio_button"]').exists:
            d.xpath('//*[@resource-id="com.android.permissioncontroller:id/allow_foreground_only_radio_button"]').click()
            d.xpath('//*[@resource-id="com.android.permissioncontroller:id/allow_foreground_only_radio_button"]').click()    

        # Has been allow and back yo homepage
        d.press("back")
        time.sleep(1) 
        d.press("back")
        time.sleep(1) 
        d.press("back")
        time.sleep(1)
        logdef.info("Back to HOMEPAGE ") 
        d.screenshot("./pic/HOMEPAGE.png")
        allure.attach.file("./pic/HOMEPAGE.png" , attachment_type=allure.attachment_type.PNG)  

        logdef.info("allow access location ") 
        d.screenshot("./pic/accesslocation.png")
        allure.attach.file("./pic/accesslocation.png" , attachment_type=allure.attachment_type.PNG)             
        if d(resourceId="com.android.permissioncontroller:id/permission_allow_foreground_only_button").exists:
           d(resourceId="com.android.permissioncontroller:id/permission_allow_foreground_only_button").click()
           time.sleep(3)
           logdef.info("Final result ") 
           d.screenshot("./pic/Finalresult.png")
           allure.attach.file("./pic/Finalresult.png" , attachment_type=allure.attachment_type.PNG)         

    def LatestDownload(self,d):
        # Start and tested this devices
        # Choice if Latest is ready and Not install + Download
        # we can Download and install
        if d(textContains="Download", resourceId="dev.firebase.appdistribution:id/download_label").exists:
           logdef.info("Press Download HomePass button") 
           d(textContains="Download", resourceId="dev.firebase.appdistribution:id/download_label").click()          
           time.sleep(5)
           # install apk and wait for 20 iterations
           for index in range(20):

                if not d(textContains="Install",resourceId="android:id/button1").exists:
                   # wait for more time
                   time.sleep(30)
                else:
                  break  
                          

           if d(textContains="Install",resourceId="android:id/button1").exists:
              logdef.info("Press Install HomePass button is displayed") 
              d.screenshot("./pic/InstallAPP.png")
              allure.attach.file("./pic/InstallAPP.png" , attachment_type=allure.attachment_type.PNG)              
              time.sleep(3)
              d(textContains="Install",resourceId="android:id/button1").click()
              time.sleep(25)
              # call ifLatestNinstalledNopen module
              self.ifLatestNinstalledNopen(d)
              # Uninstall apk
              ##cmd = "adb -s "+str(DEV)+" uninstall com.plumewifi.plume.dogfood"
              ##command = os.popen(cmd)
              ##time.sleep(1.5)


    def ifLatestNinstalledNopen(self,d):
        # Start and tested this devices
        # if Latest is ready and Installed + Open
        # we can open directly
        if d(textContains="Latest",resourceId="dev.firebase.appdistribution:id/labels_latest_release").exists:
            if d(textContains="Installed",resourceId="dev.firebase.appdistribution:id/labels_installed_release").exists:
                if d(textContains="Open", resourceId="dev.firebase.appdistribution:id/open_button").exists:                    
                   d(textContains="Open", resourceId="dev.firebase.appdistribution:id/open_button").click()
                   time.sleep(12)
                   # Allow HomePass to send you notification ?
                   if d(resourceId="com.android.permissioncontroller:id/permission_allow_button").exists:
                      d(resourceId="com.android.permissioncontroller:id/permission_allow_button").click()
                   time.sleep(2)   
                   d.screenshot("./pic/HomPassinstalled.png")
                   allure.attach.file("./pic/HomPassinstalled.png" , attachment_type=allure.attachment_type.PNG)
                   # Call Homepass test func
                   self.Signintest(d)
                   self.keyinpassword(d)
                   self.entrySingin(d)
                   ###
                   return True

    def TapselectApp(self,d):
        #d(resourceId="dev.firebase.appdistribution:id/row",className="android.view.ViewGroup")
        # Press TestApps
        if d(resourceId="dev.firebase.appdistribution:id/row",className="android.view.ViewGroup").exists:
            d(resourceId="dev.firebase.appdistribution:id/row",className="android.view.ViewGroup").click()
            logdef.debug("Lanch the TapselectApp successfully.")
            return True
        else:
            logdef.debug("Failed to lanch the TapselectApp")
            PWBFunc().captureadblog() # adb log
            return False       
  
    def Apptester(self,d):
        # Lanch HomePass app
        if d(textContains="App Tester",className="android.widget.TextView").exists:
            d(textContains="App Tester",className="android.widget.TextView").click()
            logdef.debug("Lanch the App Tester APP successfully.")

            return True
        else:
            logdef.debug("Failed to lanch the App Tester APP!")
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
 
    def test_firebase_func(self):

        """
        pip install numpy
        pip install pyautogui
        pip install opencv-python
        pip install pytest-repeat

        """
        global TODAY

        # HomePass Package name for checking
        package_name = "com.plumewifi.plume.dogfood"

        device_serial = str(DEV)
        
        # Check which package has been installed in the Mobile devices
        adb_output = subprocess.check_output(['adb', '-s', device_serial, 'shell', 'pm', 'list', 'packages']).split()

        # 
        for package in adb_output:
            if package.decode("utf-8") == "package:" + package_name:
                logdef.info("Package found and will do uninstall") 
                time.sleep(1)
                ## com.plumewifi.plume.dogfood
                cmd = "adb -s "+str(DEV)+" uninstall com.plumewifi.plume.dogfood"
                command = os.popen(cmd)
                time.sleep(1.5)     
                logdef.info("For HomePass Uninstall")                 
                break
        else:
            logdef.info("HomePass Package not found.")
            pass

        time.sleep(3)
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
        logdef.info("################################################################################################\n")
        logdef.info("#  Test case : THRIV-2580 :  [Thrive Automation][script] Trigger FireBase in the Android phone #     (FireBase App)  #)\n")        
        logdef.info("################################################################################################)\n") 
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
        d.screenshot("./pic/home.png") # default format="pil
        time.sleep(2)
        allure.attach.file('./pic/home.png' , attachment_type=allure.attachment_type.PNG)  
        time.sleep(3)
        # Press recent button
        # uiautomator2
        d.press("recent")
        time.sleep(2)        
        d.screenshot("./pic/recent.png") # default format="pil
        allure.attach.file('./pic/recent.png' , attachment_type=allure.attachment_type.PNG)           
        time.sleep(3)
        PWBFunc().CleanAPP(d)
        logdef.info("STOP Appter First")
        #dev.firebase.appdistribution/dev.firebase.appdistribution.main.MainActivity
        cmd = "adb -s "+str(DEV)+"  shell am force-stop dev.firebase.appdistribution"
        command = os.popen(cmd)
        time.sleep(5)
        print(d.info)  
        # Lanch Apptester app
        logdef.info("Lanch Apptester app")        
        PWBFunc().Apptester(d)   
        time.sleep(20)
        # Lanch HomePass app via cmd
        cmd = "adb -s "+str(DEV)+" shell am start -n dev.firebase.appdistribution/dev.firebase.appdistribution.main.MainActivity"
        command = os.popen(cmd) 
        time.sleep(20)
        d.screenshot("./pic/Apptester.png") # default format="pil
        allure.attach.file('./pic/Apptester.png' , attachment_type=allure.attachment_type.PNG)            
        time.sleep(5)
        #############
        # Tap and Select TestApps 
        logdef.info("Tap and Select TestApps ")
        PWBFunc().TapselectApp(d)
        time.sleep(10)
        ##############
        if d(textContains="Latest",resourceId="dev.firebase.appdistribution:id/labels_latest_release").exists:
            if d(textContains="Installed",resourceId="dev.firebase.appdistribution:id/labels_installed_release").exists:
               logdef.info("Choice if Latest is ready and Installed + Open")
               PWBFunc().ifLatestNinstalledNopen(d)

               # Start and tested this devices
               # Choice if Latest is ready and Installed + Open
               # we can open directly
            else:
               logdef.info("Choice if Latest is ready and HomePass Not install + Download button is displayed")                
               PWBFunc().LatestDownload(d)   
               # Start and tested this devices
               # Choice if Latest is ready and Not install + Download
               # we can Download and install
        d.press("back") # press the back key, with key name
        # small back key
        if d.xpath('//*[@resource-id="dev.firebase.appdistribution:id/back_arrow"]').exists:
           d.xpath('//*[@resource-id="dev.firebase.appdistribution:id/back_arrow"]').click()
           time.sleep(3)
           logdef.info("return to Tap and Select TestApps page")
           d.screenshot("./pic/Returntopage.png") # default format="pil
           allure.attach.file('./pic/Returntopage.png' , attachment_type=allure.attachment_type.PNG)         
        ############################################################################################       
        time.sleep(5)
        logdef.info("STOP App tester")
        cmd = "adb -s "+str(DEV)+" shell am force-stop dev.firebase.appdistribution"
        command = os.popen(cmd)
        time.sleep(1.5)     
        logdef.info("For Trigger Apptester --> STOP")
        # backtohome
        d.press("home")           
        logdef.info("Test completed")
    
          