#!/usr/bin/env python3
#coding=utf-8
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from appium import webdriver as appdriver
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
from collections.abc.Mapping import namedtuple
#from collections import namedtuple
import threading
import pygatt
import logging
from binascii import hexlify
#import allure # allure report
#import platform
import datetime

root_path = os.path.dirname(os.path.realpath(__file__))


class PWBFunc:

    def __init__(self):
        os.popen("adb devices")
        self.START()
        nRF_Connect_activity = 'no.nordicsemi.android.mcp/no.nordicsemi.android.mcp.MainActivity'
        self.Android_Shell(deviceName=self.deviceName, text='shell am start -W -n ' + nRF_Connect_activity+ ' -S', prn=1)
        adv_name = 'a'
        print('Android Phone : Filter "' + adv_name + '" on nRF_connect')
        self.UI_locate(By.ID, 'no.nordicsemi.android.mcp:id/filter_header', 'click')
        time.sleep(3)
        self.app_driver.find_element(By.ID, 'no.nordicsemi.android.mcp:id/filter').send_keys(adv_name)
        self.UI_locate(By.ID, 'no.nordicsemi.android.mcp:id/filter_header', 'click')
        text = self.UI_locate(By.ID, 'no.nordicsemi.android.mcp:id/display_name', 'text')
        print('\n\nThe first BLE Name:' + text)


    def AppiumServer(self):
        print("**** appium -a 127.0.0.1 -p 4723 -bp 4724 --chromedriver-port 9515 --session-override", 'BLACK', 'WHITE')
        AppiumServer = os.popen("appium -a 127.0.0.1 -p 4723 -bp 4724 --chromedriver-port 9515 --session-override")
        while True: 
            try:
                tmp = AppiumServer.buffer.readline().decode('ascii', 'ignore').replace('\r','').replace('\n','')
            except Exception as e:
                print(str(e))
                return
            if self.AppiumIsReady == 0:
                print(tmp)
                if 'listener started on 127.0.0.1' in tmp:
                    self.AppiumIsReady = 1


    def Android_Shell(self, deviceName, text, expected = 'None', prn=1):
        cmd = 'adb -s ' + deviceName + ' ' + text
        print(cmd)
        adb_cmd = os.popen(cmd)
        log_list = []
        while True:
            tmp = adb_cmd.buffer.readline().decode('ascii', 'ignore')
            handle = tmp.replace('\n','').replace('\r','')
            if prn == 1:
                print(handle)
            log_list.append(handle)
            if expected in handle or tmp == '':
                break
        time.sleep(1)
        return log_list[-1]


    def GetDeviceID(self):
        cmd = 'adb devices'
        command = os.popen(cmd)
        while True:
            tmp = command.buffer.readline().decode('ascii', 'ignore')
            if tmp == '':
                print('\nCan not detect Android phone, please check the USB.')
                input("\tInput any key to rerun.")
                command = os.popen(cmd)
            else:
                tmp = tmp.replace('\n','').replace('\r','')
                print(tmp)
            if "device" in tmp and 'List of devices attached' not in tmp:
                PhoneID = tmp.split('\t')
                PhoneID = PhoneID[0]
                command.close()
                return PhoneID


    def UI_locate(self, attribute, value, action):
        for i in range(5):
            elem = self.app_driver.find_elements(attribute, value)
            if len(elem)>0:
                break
            else:
                time.sleep(1)
        if action == 'click':
            elem[0].click()
        elif action == 'text':
            return elem[0].get_attribute('text')

    def START(self):
        print("**** Appium initial ****")
        desired_caps = {}
        self.deviceName = self.GetDeviceID()
        desired_caps['deviceName'] = self.deviceName
        android_ver = self.Android_Shell(self.deviceName, 'shell getprop ro.build.version.release')
        desired_caps['platformVersion'] = android_ver
        desired_caps['unicodeKeyboard']= False
        desired_caps['resetKeyboard'] = False

        self.AppiumIsReady = 0 
        AppiumServer = threading.Thread(target = self.AppiumServer, args=() )
        AppiumServer.daemon = True
        AppiumServer.start()
        while self.AppiumIsReady == 0 :
            time.sleep(1)

        print('Connecting Android...')
        desired_caps['platformName'] = 'Android'
        desired_caps['newCommandTimeout']= '20000'
        desired_caps['unicodeKeyboard']= False
        desired_caps['resetKeyboard'] = False
        desired_caps['noSign']= True
        #desired_caps['autoLaunch'] = False
        desired_caps['automationName'] = 'Uiautomator2'
        for i in range(3):
            try:
                self.app_driver = appdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
            except Exception as e:
                if i < 2:
                    print('Can not access Android Phone, try again...')
                else:
                    print(str(e))
                    print('Failed, Stop the process, please reconnect the USB of Android and run again.')
                    return False
        self.app_driver.implicitly_wait(3)
        self.app_driver.update_settings({"waitForIdleTimeout": 100})
        return self.app_driver


class TestAPI(TestAPIWrap):
 
    def test_beacon_func(self):

        """
        BLE beacon scan via Android Phone (Nordic App) 
        """
        logdef.info("##################################################################\n")
        logdef.info("#  Test case : ( BLE beacon scan via Android Phone (Nordic App)  #)\n")        
        logdef.info("##################################################################)\n") 
        logdef.info("##################################################################")
        print(f'Scan \"PlumeF\"')
        global checkpoint
        PWBFunc().START()
        PWBFunc().AppiumServer()
        PWBFunc().Android_Shell()
        PWBFunc().GetDeviceID()
        PWBFunc().UI_locate()
        #assert checkpoint != False       
