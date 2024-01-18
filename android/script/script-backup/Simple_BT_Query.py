#!/usr/bin/env python3
#coding=utf-8
from runnerWrapper import *
import logging
import asyncio
import time
from bleak import BleakClient, BleakError
from bleak.uuids import uuidstr_to_str
from bleak import BleakScanner
import pytest 
import random
import os
import re
import calendar
import toml
import shutil
import numpy as np
import subprocess
import sys
import struct
from collections import namedtuple
import threading
from binascii import hexlify
import allure # allure report
import platform
import ble_adv_event_scanner as BleScanAdvEvents
import parser_ring_info as ParserRingInfo
import datetime

root_path = os.path.dirname(os.path.realpath(__file__))


"""
    def __init__(self, uuid='plume'):
        if uuid == 'plume':
            self.customServiceUUID = '0000fd1e-0046-524f-444f-006474700001'
            self.customNotifyDataUUID = '0000fd1e-0046-524f-444f-006474700003'
            self.customNotifyRespUUID = '0000fd1e-0046-524f-444f-006474700002'
        else:
            self.customServiceUUID = '00004652-08c2-11e1-9073-0e8ac72e0011'
            self.customNotifyDataUUID = '00004652-08c2-11e1-9073-0e8ac72e0013'
            self.customNotifyRespUUID = '00004652-08c2-11e1-9073-0e8ac72e0012'


{'path': '/org/bluez/hci0/dev_60_B4_F7_F5_00_3B', 
'props': {'Address': '60:B4:F7:F5:00:3B', 
'AddressType': 'public', 
'Name': 'PlumeF-100111200-13-003B', 
'Alias': 'PlumeF-100111200-13-003B', 
'Paired': True, 
'Trusted': True, 
'Blocked': False, 
'LegacyPairing': False, 
'Connected': False, 
'UUIDs': ['00001800-0000-1000-8000-00805f9b34fb', 
'00001801-0000-1000-8000-00805f9b34fb', 
'0000180a-0000-1000-8000-00805f9b34fb', 
'00002760-08c2-11e1-9073-0e8ac72e1001', 
'00004652-08c2-11e1-9073-0e8ac72e1011', 
'0000fd1e-0046-524f-444f-006474701001', 
'0000fd1e-0046-524f-444f-006f74611001'], 
'Adapter': '/org/bluez/hci0', 
'ManufacturerData': {64798: b'(\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'}, 'ServicesResolved': False, 'RSSI': -66, 'TxPower': 0}}
<class 'bleak.backends.device.BLEDevice'>

"""

root_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
# connection timeout
timeout= 30.0  
#######################################################
GETPOWRERINFO_CMD  = '0700'  # Get Power Info (07)
GETSERIALINFO_CMD = '0201'   # Get Provision Info
GETSERIALINFO_TYPE = '01'   # Get Provision TYPE (1= serial number) 
GETSERIALINFO_TYPE2 = '12'  # Get Provision TYPE (12= serial number) 
##########################################################
M_POWRERINFO = bytearray.fromhex(GETPOWRERINFO_CMD)  # For Battery info
##################################################################
X_GETSERIALINFO_CMD_A = bytearray.fromhex(GETSERIALINFO_CMD)
X_GETSERIALINFO_CMD_B = bytearray.fromhex(GETSERIALINFO_TYPE)
X_GETSERIALINFO_CMD_C = bytearray.fromhex(GETSERIALINFO_TYPE2)
M_SERIALINFO = (X_GETSERIALINFO_CMD_A + X_GETSERIALINFO_CMD_B + X_GETSERIALINFO_CMD_C) # For Serial number info
#############################################################



async def run(address, loop, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        # loop.set_debug(True)
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    devices = await BleakScanner.discover()
    for d in devices:
        print(type(d))
        print(d.details)   

    async with BleakClient(address, loop=loop) as client:
        #paired = await client.pair(3)
        #log.info("Paired: {0}".format(paired))
        #x = await client.is_connected()
        
        #self.connected = await client.is_connected()
        #log.info("Connected: {0}".format(x))
        try:
            self.connected = await self.client.is_connected()
            if self.connected:
                print("Connected to Device")
                self.client.set_disconnected_callback(self.on_disconnect)
                await self.client.start_notify(
                    self.notify_characteristic, self.notify_callback,
                )
                while True:
                    if not self.connected:
                        break
                    await asyncio.sleep(1.0)
            else:
                print(f"Failed to connect to Device")
        except Exception as e:
            print(e)


        
        # await client.read_gatt_char('0000fd1e-0046-524f-444f-006474701001')

        """
        for service in client.services:
            # service.obj is instance of 'Windows.Devices.Bluetooth.GenericAttributeProfile.GattDeviceService'
            log.info(
                "[Service] {0}: {1}".format(service.uuid, service.description)
            )
            print("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                # char.obj is instance of 'Windows.Devices.Bluetooth.GenericAttributeProfile.GattCharacteristic'
                if 'read' in char.properties:
                    value = bytes(await client.read_gatt_char(char.uuid))
                else:
                    value = None
                log.info(
                    "\t[Characteristic] {0}: ({1}) | Name: {2}, Value: {3} ".format(
                        char.uuid, ",".join(char.properties), char.description, value
                    )
                )
                for descriptor in char.descriptors:
                    # descriptor.obj is instance of 'Windows.Devices.Bluetooth.GenericAttributeProfile.GattDescriptor
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    log.info(
                        "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                            descriptor.uuid, descriptor.handle, bytes(value)
                        )
                    )
        """

if __name__ == "__main__":
    address = "60:B4:F7:F5:00:3B"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))