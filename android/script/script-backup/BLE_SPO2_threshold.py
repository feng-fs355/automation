#!/usr/bin/env python3
#coding=utf-8
import numpy as np
import subprocess
import sys
import threading
import re
import pygatt
import logging
from binascii import hexlify
import time
import calendar
import os
import struct
from time import sleep
from collections import namedtuple
import platform
import ble_adv_event_scanner as BleScanAdvEvents
import parser_ring_info as ParserRingInfo
import datetime

from runnerWrapper import *

bleScan = BleScanAdvEvents.BLE_AdvEventScan()
ringInfo = ParserRingInfo.PARSER_name()
eventInfo = ParserRingInfo.PARSER_events()


logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
# connection timeout
timeout= 20.0  
#######################################################


def bleak_query():

    print(f'Scan \"PlumeF\"')
    info = bleScan.getAdvEventScanInfo('local_name', 'PlumeF')


    if (info != None):
        for i, dev in enumerate(info):
            print(dev)
            print(f'Adv Name   : {dev["local_name"]}')
            print(f'BD addr    : {dev["bd_addr"]}')
            print(f'Size       : {dev["ring_size"]}')
            print(f'Color      : {ringInfo.get_ring_color(dev["ring_color"])}')
            print(f'Ship region: {ringInfo.get_ship_region(dev["ship_region"])}')
            print(f'PPG_type   : {ringInfo.get_ppg_type(dev["ppg_type"])}')
            print(f'Flash_type : {ringInfo.get_flash_type(dev["flash_type"])}')
            print(f'HW ver     : {dev["hw_ver"]}')
            
            if ('event_type' in dev):
                print(f'Event type : {dev["event_type"]}')
                print(f'time       : {datetime.datetime.fromtimestamp(dev["timestamp"])}')
                
                if dev["event_type"] == 'BATT':
                    print(f'Warn type  : {eventInfo.get_batt_warn_type(dev["warn_type"])}')
                    print(f'BATT level : {dev["batt_lvl"]}')

                if dev["event_type"] == 'HR':
                    print(f'Warn type  : {eventInfo.get_hr_warn_type(dev["warn_type"])}')
                    print(f'HR         : {dev["hr"]}')
                    print(f'Threshold  : {dev["hr_threshold"]}')

                if dev["event_type"] == 'SPO2':
                    print(f'Warn type  : {eventInfo.get_spo2_warn_type(dev["warn_type"])}')
                    print(f'SpO2       : {dev["spo2"]}')
                    print(f'Threshold  : {dev["spo2_threshold"]}')

                if dev["event_type"] == 'ACTIVITY':
                    print(f'Warn type  : {eventInfo.get_activity_warn_type(dev["warn_type"])}')
                    if dev["warn_type"] == 1:
                        print(f'Risk Level : {dev["fall_risk_lvl"]}')
                        print(f'Threshold  : {dev["fall_threshold"]}')
                        print(f'Fll HR     : {dev["fall_hr"]}')
                        print(f'Rest HR    : {dev["fall_rest_hr"]}')

                    if dev["warn_type"] == 2:
                        print(f'State      : {dev["activity_state"]}')


            print('\n')


"""
Require as below:

Please set the hr high threshold to 60 or the low spo2 threshold to 99 to trigger warning notification
"""
# SpO2 Warning Threshold (13)

SETTHRESHOLD_CMD  = '13'  
SETLEN_CMD = '02'   # LEN
SETMODE = '01'   # Mode 01 = SET

"""
0: Reset to default
1: Set
SPO2_L_TH
Configure the SpO2 low warning threshold. If SpO2 is smaller than threshold, device sends BLE warning message notification to mobile. The value ranges from 70~100(BPM), the default value is 90.

2: Read


"""
##http://www.unitconversion.org/numbers/base-10-to-base-16-conversion.html
#base-10 = 99  
#base-16 = 63

SETSPO2_L_TH = '63'
##########################################################
X_SETTHRESHOLD_CMD = bytearray.fromhex(SETTHRESHOLD_CMD)
X_SETLEN_CMD = bytearray.fromhex(SETLEN_CMD)
X_SETMODE = bytearray.fromhex(SETMODE)
X_SETSPO2_L_TH = bytearray.fromhex(SETSPO2_L_TH)
M_SETTHRESHOLD_INFO= (X_SETTHRESHOLD_CMD + X_SETLEN_CMD + X_SETMODE + X_SETSPO2_L_TH)
####################################################

# HR Warning Threshold (12)
# Configure Heart Rate and SpO2 warning threshold.
SETTHR_CMD  = '12'  
SETHRLEN = '02'   # LEN
SETMODE = '01'   # Mode 01 = SET

HR_L_TH = '32'
#base-10 = 50
#base-16 = 32

HR_REST_TH = '3C'
#base-10 = 60
#base-16 = 3C

HR_ACTIVITY_TH = 'B4'
#base-10 = 180
#base-16 = B4

#MODE
#0: Reset to default
#1: Set
#HR_L_TH
#Configure the heart rate low warning threshold. If the HR level is smaller than the threshold, the device sends a BLE warning message notification to mobile. The value ranges from 0~50(BPM), the default value is 50.

#HR_REST_TH
#Configure the rest heart rate at a high warning threshold. If HR is greater than threshold, the device sends BLE warning message notification to mobile. The value ranges from 40~220(BPM), the default value is 100.

#HR_ACTIVITY_TH
#Configure the activity heart rate at a high warning threshold. If HR is greater than threshold, the device sends a BLE warning message notification to mobile. The value ranges from 40~220(BPM), the default value is 180.

 
#RET_CODE
#0x00: SUCCESS                           0x01: FAIL

# All = 0x12 + LEN + MODE +HR_L_TH + HR_REST_TH + HR_ACTIVITY_TH

X_SETTHR_CMD = bytearray.fromhex(SETTHR_CMD)
X_SETHRLEN = bytearray.fromhex(SETHRLEN)
X_SETMODE = bytearray.fromhex(SETMODE)
X_HR_L_TH = bytearray.fromhex(HR_L_TH)
X_HR_REST_TH = bytearray.fromhex(HR_REST_TH)
X_HR_ACTIVITY_TH = bytearray.fromhex(HR_ACTIVITY_TH)

ALL_HR_Paramter = (SETTHR_CMD + SETHRLEN + SETMODE + HR_L_TH + HR_REST_TH + HR_ACTIVITY_TH)


def main(url, num):
    print("######################")
    print('Thread', num)
    print("######################")

def data_handler_cb(handle, value):

    current_GMT = time.gmtime()
    logdef.info(current_GMT)
    logdef.info("\n\n")
    time_stamp = calendar.timegm(current_GMT)
    logdef.info("\n") 
    logdef.info("**************************************\n")
    logdef.info("Data: {}".format(value.hex()))
    logdef.info("Handle: {}".format(handle))
    logdef.info("\n") 
    logdef.info("**************************************\n")
    respCmd, respLen, respres = (value[0], value[1], value[2])
    res ={'cmd': respCmd,'return': respres}
    respCmd= hex(respCmd)    
    #res['battLevel'] = value[3]
    #res['vbatt'] = struct.unpack('<H', value[4:6])[0]
    #res['chgStat'] = value[6]
    #res['chgInStat'] = value[7]
    #res['vchg'] = struct.unpack('<H', value[8:10])[0]
    #res['ichg'] = struct.unpack('<H', value[10:12])[0]
    #res['powerlvl'] = value[12]
    logdef.info("\n") 
    logdef.info("**************************************\n")
    logdef.info(res)
    logdef.info("**************************************\n")
    path = './BLE_output.txt'
    f = open(path, 'a+b')
    f.write(value)
    f.close()
    return handle


def SUBSCRIBE():
    while True:      
        try: 
            sleep(2)
            device.subscribe(ResponseUUID,callback=data_handler_cb,wait_for_response=False)
            break
        except:
            logdef.info("subscribe Fail and re-subscribr\n")
            pass

def WRITECMD():
    while True:
        try:
            sleep(2)
            logdef.info("Trying to Set SPO2 THRESHOLD_INFO\n")
            print("Next Command 1")     
            device.char_write(Commanduuid, M_SETTHRESHOLD_INFO, wait_for_response=False)
            break
        except:
            logdef.info("Write Fail and re-write\n")
            pass

def WRITECMD2():
    while True:
        try:
            sleep(5)
            logdef.info("Trying to Set HR THRESHOLD_INFO\n")
            device.char_write(Commanduuid, ALL_HR_Paramter, wait_for_response=False)
            print("Next Command 2")
            break
        except:
            logdef.info("Write Fail and re-write\n")
            pass 


def UNSUBSCRIBR():
    while True:    
        try:
            sleep(2)
            device.unsubscribe(ResponseUUID,wait_for_response=False)
            break
        except:
            logdef.info("unsubscribe Fail and re-unsubscribe\n")
            pass


adapter = pygatt.GATTToolBackend(search_window_size=2048)
adapter.start()
sleep(3)
while True:
    try:
        sleep(2)
        device = adapter.connect(macaddr,timeout=timeout)
        break    
    except:
        logdef.info("Connection Fail and re-connect again\n")
        pass    


t1 = threading.Thread(target=main, args=(SUBSCRIBE(), 1))
t2 = threading.Thread(target=main, args=(WRITECMD(), 2))

#-------------------
t1.start()
sleep(8)
t2.start()
t1.join()
t2.join()
#-------------------
sleep(3)
UNSUBSCRIBR()
sleep(5)
adapter.stop()
sleep(3)

bleak_query()


