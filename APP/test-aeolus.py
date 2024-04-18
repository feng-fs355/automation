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
from allure_commons.types import AttachmentType
from asyncore import loop
import platform
import datetime
import string
import cv2 
import pytesseract
global DEV

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
DEV = (configure['userinfo']['androiddev1'])
version_info = (configure['userinfo']['version'])
timeout= 20.0  
root_path = os.path.dirname(os.path.realpath(__file__))

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
print("##################################################################\n")
print("#  Test case : ( aeolus Lanch app unit test  #)\n")        
print("##################################################################)\n") 


class PWBFunc:

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
    def swipeRight(self,d): # big swipe up function for device 1
        print("swipeRight feature\n")
        l=self.device_setting(d)
        width= l[0]
        Height= l[1]    
        print(width)
        print(Height)
        x1 = width * 0.1
        x2 = width * 0.7     
        y1 = Height * 0.6
        y2 = Height * 0.6
        d.swipe(x1, y1, x2, y2)    

    def swipeleft(self,d):  # big swipe swipe function for device 1
        print("swipeleft feature\n")
        l=self.device_setting(d)
        width= l[0]
        Height= l[1]    
        print(width)
        print(Height)
        x1 = width * 0.7
        x2 = width * 0.1     
        y1 = Height * 0.6
        y2 = Height * 0.6
        d.swipe(x1, y1, x2, y2)        
    

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

    def aeolus_instant(self,d):    
        if d(text="Instant",className="android.widget.TextView").exists:
            d(text="Instant",className="android.widget.TextView").click()   
        time.sleep(3)    
        if d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[4]').exists:
            return True

    def generate_password(self,length=10):
  
        characters = string.ascii_letters + string.digits    
        password = ''.join(random.choice(characters) for _ in range(length))
    
        return password
         

class TestAPI(TestAPIWrap):


    global checkpoint
    global d # get android phone serial number
    d = Device(DEV)  

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


    def test_inittest(self):

        print("Test Aeolus has been bring up")
        # adb shell am force-stop com.aeolusbot.instant
        cmd = 'adb shell am force-stop com.aeolusbot.instant'
        command = os.popen(cmd)           
        time.sleep(1)
        d.screen_on()
        time.sleep(1)
        d.press("home")
        print(d.info)    
        # Lanch nRF app
        checkpoint = PWBFunc().aeolus_instant(d)
        if checkpoint != True:
            os.system("adb -s "+(DEV)+" shell am start -n com.aeolusbot.instant/.MainActivity")
            time.sleep(5)
        PWBFunc().swipeleft(d)
        time.sleep(5)    
        assert d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[4]').exists    
        d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[4]').click()
        time.sleep(5)
        # entry e-mail
        if d(text="Email").exists:
           d(text="Email").click()
           cmd = 'adb shell input text "feng038100@gmail.com"'
           command = os.popen(cmd)
        time.sleep(1)   
        # entry password
        password = PWBFunc().generate_password(10)
        print("Generated Password:", password)          
        if d(text="Password").exists:
           d(text="Password").click()
           cmd = 'adb shell input text '+str(password)
           command = os.popen(cmd)
        time.sleep(1)
        # entry server address
        if d(text="Server Address").exists:
           d(text="Server Address").click()
           cmd = 'adb shell input text '+str("8.8.8.8")
           command = os.popen(cmd) 
        time.sleep(3)
        # Login
        if d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').exists:   
           d.xpath('//*[@resource-id="android:id/content"]/android.widget.FrameLayout[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
           time.sleep(1)
           d.screenshot("login.png")
           time.sleep(2)
        if d(text="Login Failed",resourceId="android:id/alertTitle").exists:
           d.screenshot("./login-Fail.png")
           time.sleep(2)
           image = cv2.imread('./login-Fail.png')        
           text = pytesseract.image_to_string(image)
           text = str(text)
           print("pytesseract.image_to_string"+str(image))
           if str('Your server address is incorrect') in text:
              print("Login Failed\n")
              print(text)
             
        print("Done for test")
        logdef.info("test completed")
        # adb shell am force-stop com.aeolusbot.instant
        cmd = 'adb shell am force-stop com.aeolusbot.instant'
        command = os.popen(cmd)        
