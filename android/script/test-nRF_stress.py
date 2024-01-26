#!/usr/bin/env python3
#coding=utf-8
from uiautomator2 import Device
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
import numpy as np
import subprocess
import sys
import struct
from time import sleep  # time for sleep
import builtins
from collections.abc import MutableMapping
from collections import namedtuple
import threading
import pygatt
import logging
from binascii import hexlify
import allure # allure report
#from allure_commons.types import AttachmentType
import platform
import datetime

global DEV

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
#DEV = (configure['userinfo']['androiddev1'])
DEV = 'd38c1487'
timeout= 20.0  
root_path = os.path.dirname(os.path.realpath(__file__))

class PWBFunc:

    def __init__(self):
        os.popen("adb devices")
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
    def nRF_app(self,d):
        # Initial nRF APP to BLE scanning 
        if d(text="@nRF Connect",className="android.widget.TextView").exists:
           d(text="@nRF Connect",className="android.widget.TextView").click()
           return True        
        if d(text="nRF Connect",className="android.widget.TextView").exists:
           d(text="nRF Connect",className="android.widget.TextView").click()
           return True

    def SCAN(self,d):
        with allure.step('look for target device'):        
            if d(text="SCAN",className="android.widget.Button",resourceId="no.nordicsemi.android.mcp:id/action_scan_start").exists:
               d.screenshot("SCAN.png") # default format="pil
               allure.attach.file('./SCAN.png' , attachment_type=allure.attachment_type.PNG)        
               d(text="SCAN",className="android.widget.Button",resourceId="no.nordicsemi.android.mcp:id/action_scan_start").click()

    def TARGET(self,d):
        d.screenshot("TARGET.png") # default format="pillow"            
        allure.attach.file('TARGET.png' , attachment_type=allure.attachment_type.PNG)

        text_names = ["PlumeF-945108100-13-04D4", "PlumeF-945108100-13-02FF","PlumeF-000000000-13-05BC","PlumeF-000000000-13-04F4"]

        for text in text_names:

            time.sleep(1.5)
            if d(text=text,className="android.widget.TextView").exists:
               print("Target has been found")
               break                     
        self.STOP_SCAN(d)                    
                   

    def STOP_SCAN(self,d):
        # # press STOP SCANNING button 
        if d(text="STOP SCANNING",className="android.widget.Button",resourceId="no.nordicsemi.android.mcp:id/action_scan_stop").exists:
           d.screenshot("STOP_SCAN.png") # default format="pillow"     
           d(text="STOP SCANNING",className="android.widget.Button",resourceId="no.nordicsemi.android.mcp:id/action_scan_stop").click()
           time.sleep(2)        

        text_names = ["PlumeF-945108100-13-04D4", "PlumeF-945108100-13-02FF","PlumeF-000000000-13-05BC","PlumeF-000000000-13-04F4"]


        for text in text_names:

            elements = d(text=text,className="android.widget.TextView",resourceId="no.nordicsemi.android.mcp:id/display_name").right(text="CONNECT",className="android.widget.TextView",packageName="no.nordicsemi.android.mcp")

            for element in elements:
                if element.exists:
                   element.click()

    def DISCONNECT(self,d):
        # press DISCONNECT button 
        if d(text="DISCONNECT",className="android.widget.Button").exists:
           image = d.screenshot() # default format="pillow"
           image.save("DISCONNECT.jpg")            
           d(text="DISCONNECT",className="android.widget.Button").click()
    def CANCELAD(self,d):
        # press X button 
        if d(resourceId="no.nordicsemi.android.mcp:id/action_close",className="android.widget.ImageButton").exists:
           image = d.screenshot() # default format="pillow"
           image.save("CANCELAD.jpg")            
           d(resourceId="no.nordicsemi.android.mcp:id/action_close",className="android.widget.ImageButton").click()        
    def Scanner_tap(self,d):
        # Tap SCANNER page
        if d(resourceId="android:id/text1",text="SCANNER").exists:
           image = d.screenshot() # default format="pillow"
           image.save("Scanner_tap.jpg")           
           d(resourceId="android:id/text1",text="SCANNER").click() 

class TestAPI(TestAPIWrap):
 
    def test_android_func(self):

        """
        BLE beacon scan via Android Phone (Nordic App)

        """
        # Re-initial adb interface
        cmd = 'adb kill-server'
        #command = subprocess.run([sys.executable, "-c", "print(cmd)"])
        command = os.popen(cmd)
        time.sleep(1.5)
        cmd = 'adb start-server'
        command = os.popen(cmd)
        time.sleep(1.5)        
        cmd = 'adb devices'
        command = os.popen(cmd)
        time.sleep(1.5) 
        logdef.info("##################################################################\n")
        logdef.info("#  Test case : ( BLE beacon scan via Android Phone (Nordic App)  #)\n")        
        logdef.info("##################################################################)\n") 
        logdef.info("##################################################################")
        print(f'Scan \"PlumeF\"')
        global checkpoint
        global d # get android phone serial number
        d = Device(DEV)        
        time.sleep(1)
        d.screen_on()
        time.sleep(1)
        d.press("home")
        print(d.info)    
       
        """
        # Lanch nRF app
        checkpoint = PWBFunc().nRF_app(d)
        if checkpoint != True:
            PWBFunc().swipeUp(d)
            time.sleep(1)
            PWBFunc().swipeUp(d)
        time.sleep(2)
        # Click Scan button
        PWBFunc().SCAN(d)
        time.sleep(150)
        print("Done")
        logdef.info("Done")
        # adb shell am force-stop no.nordicsemi.android.mcp
        cmd = 'adb shell am force-stop no.nordicsemi.android.mcp'
        command = os.popen(cmd)
        """