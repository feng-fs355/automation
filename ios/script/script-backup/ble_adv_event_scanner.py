'''
//*****************************************************************************
//
//! @file ble_adv_event_scanr.py
//!
//! @brief BLE devices advertisment event information scanner
//!
//*****************************************************************************

//*****************************************************************************
//
// Copyright (c) 2022, Plume Design Inc.
// All rights reserved.
//
//*****************************************************************************
'''
import asyncio
import sys
import platform
import time
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import binascii  # Min add 20220912

MF_KEY = 64798
scanList = []
SCAN_PERIOD = 9.0

def arr_to_uint32(arr):
     if (len(arr) < 4):
         return 0
     else:
         return ((arr[0]) + (arr[1]<<8) + (arr[2]<<16) + (arr[3]<<24))

def ble_scan_adv_callback(device: BLEDevice, advertisement_data: AdvertisementData):
    global scanList

    if (advertisement_data.local_name != None):
        existed = 0
        for i, sublist in enumerate(scanList):
            if device.address == sublist['bd_addr']:
                existed = 1
                break

        if (existed == 0) \
            and (advertisement_data.local_name != None) \
            and (MF_KEY in advertisement_data.manufacturer_data):
            scanList.append({'bd_addr': device.address, 'rssi': device.rssi, 'local_name': advertisement_data.local_name, 'mf_data': advertisement_data.manufacturer_data[MF_KEY]})

async def ble_start_scan(service_uuids):
    global SCAN_PERIOD
    global scanList
    scanList.clear()
    scanner = BleakScanner(ble_scan_adv_callback, service_uuids)

    await scanner.start()
    await asyncio.sleep(SCAN_PERIOD)
    await scanner.stop()
    
    return scanList

def ble_get_scan_list(key, pattern):
    if (pattern != []) :
        ret_list = []
        if platform.system()=='Windows':
            dev_list = asyncio.run(ble_start_scan([]))
        else:
            loop = asyncio.get_event_loop()
            future = asyncio.ensure_future(ble_start_scan([]))
            dev_list = loop.run_until_complete(future)

        for i, sublist in enumerate(dev_list):
            if sublist[key].startswith(pattern):
                ret_list.append(sublist)

        return ret_list
    
def ble_advname_parser(name):
    if (name != []):
        ring_size   = int(name[7:9])
        ship_region = int(name[9:11])
        ppg_type    = int(name[11])
        flash_type  = int(name[12])
        ring_color  = int(name[13])
        hw_ver      = int(name[17:19])
        mac_4digits = name[20:24]
        return {'local_name': name, 'ring_size': ring_size, 'ship_region': ship_region, 'ppg_type': ppg_type, 'flash_type': flash_type, 'ring_color': ring_color, 'hw_ver': hw_ver, 'mac_4digits': mac_4digits}

def ble_mf_parser(data):
    print("MF Has been trigger\n")
    print("Will print MF data")
    print("#################")
    print(data)
    print("#################")
    print(data.decode("utf-8")) 
    print("#################")

    # b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


    if (data[1] != 0):
        event_type = data[1]
        d_timestamp = arr_to_uint32(data[2:6])

        # battery
        if event_type == 0xA2:
            warn_type = data[6]
            batt_lvl = data[7]
            print("Has been trigger mf battery\n")
            return {'event_type': 'BATT', 'timestamp': d_timestamp, 'warn_type': warn_type, 'batt_lvl': batt_lvl}

        # HR
        elif event_type == 0xA3:
            warn_type = data[6]
            hr = data[7]
            hr_threshold =  data[8]
            print("Has been trigger mf HR\n")
            return {'event_type': 'HR', 'timestamp': d_timestamp, 'warn_type': warn_type, 'hr': hr, 'hr_threshold': hr_threshold}

        # SpO2
        elif event_type == 0xA4:
            warn_type = data[6]
            spo2 = data[7]
            spo2_threshold =  data[8]
            print("Has been trigger mf SpO2\n")
            return {'event_type': 'SPO2', 'timestamp': d_timestamp, 'warn_type': warn_type, 'spo2': spo2, 'spo2_threshold': spo2_threshold}

        # Activity
        elif event_type == 0xA5:
            warn_type = data[6]
            if (warn_type == 1):
                fall_risk_lvl = data[7]
                fall_threshold =  data[8]
                fall_hr =  data[9]
                fall_rest_hr =  data[10]
                return {'event_type': 'ACTIVITY', 'timestamp': d_timestamp, 'warn_type': warn_type, 'fall_risk_lvl': fall_risk_lvl, 'fall_threshold': fall_threshold, 'fall_hr': fall_hr, 'fall_rest_hr': fall_rest_hr}

            elif (warn_type == 2):
                activity_state = data[7]
                return {'event_type': 'ACTIVITY', 'timestamp': d_timestamp, 'warn_type': warn_type, 'activity_state': activity_state}

class BLE_AdvEventScan(object):

    def getAdvEventScanInfo(self, key, pattern):
        sublist = ble_get_scan_list(key, pattern)

        if (sublist != []):
            rings_info = []
            for i, devs in enumerate(sublist):
                ring_info = {'bd_addr': devs["bd_addr"]}

                ring_name_info = ble_advname_parser(devs["local_name"])
                ring_mf_event = ble_mf_parser(devs["mf_data"])

                if (ring_name_info != None):
                    ring_info |= ring_name_info

                if (ring_mf_event != None):
                    ring_info |= ring_mf_event

                rings_info.append(ring_info)

            return rings_info

