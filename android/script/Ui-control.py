#!/usr/bin/env python3
#coding=utf-8
from uiautomator import Device
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
from collections import namedtuple
import threading
import pygatt
import logging
from binascii import hexlify
#import allure # allure report
#import platform
import datetime

global DEV

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
DEV = (configure['userinfo']['androiddev'])
timeout= 20.0  
root_path = os.path.dirname(os.path.realpath(__file__))
class PWBFunc:

    def __init__(self):
        os.popen("adb devices")

    def nRF_app(self,d):
        if d(text="nRF Connect",className="android.widget.TextView").exists:
           d(text="nRF Connect",className="android.widget.TextView").click()   
  
    def SCAN(self,d):

        if d(text="SCAN",className="android.widget.Button").exists:
           d(text="SCAN",className="android.widget.Button").click()
    def TARGET(self,d):

        if d(text="PlumeF-100111220-13-003B",className="android.widget.TextView").right(text="CONNECT",className="android.widget.TextView").exists:

           d(text="PlumeF-100111220-13-003B",className="android.widget.TextView").right(text="CONNECT",className="android.widget.TextView").click()       

class TestAPI(TestAPIWrap):
 
    def test_beacon_func(self):

        """
        BLE beacon scan via Android Phone (Nordic App)

        """
        for x in range(2):
            cmd = 'adb devices'
            command = os.popen(cmd)
            time.sleep(3)
        logdef.info("##################################################################\n")
        logdef.info("#  Test case : ( BLE beacon scan via Android Phone (Nordic App)  #)\n")        
        logdef.info("##################################################################)\n") 
        logdef.info("##################################################################")
        print(f'Scan \"PlumeF\"')
        global checkpoint
        global d    
        # get android phone serial number
        d = Device(DEV)
        print(d.info)
        # backtohome
        d.press.home()
        time.sleep(3)
        # Lanch nRF app
        PWBFunc().nRF_app(d)
        time.sleep(3)
        # Click Scan button
        PWBFunc().SCAN(d)
        time.sleep(3)
        # Search Target and click connect button
        PWBFunc().TARGET(d)        
        
