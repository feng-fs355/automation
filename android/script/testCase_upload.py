from runnerWrapper import *
import pytest 
import random
import os
import calendar
import time
import toml
import shutil
import glob   
import numpy as np
import subprocess
import struct
from collections import namedtuple
import pygatt
import logging
from binascii import hexlify
import allure # allure report
import platform
import datetime
from datetime import datetime
from datetime import date
from tkinter import *
import asyncio
import sys
import platform
import time
import re
import logging
from threading import Thread
import bleak
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from queue import Queue
from huffman import *

SECURITY_MODE = 1   #1: Huffman     2: Encrypt  3: Encrypt default key

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
# get config from config.ini
Commanduuid = (configure['userinfo']['Commanduuid'])
Datauuid = (configure['userinfo']['Datauuid'])
ResponseUUID = (configure['userinfo']['ResponseUUID'])
macaddr = (configure['userinfo']['mac'])
DEV = (configure['userinfo']['androiddev1'])
timeout= 20.0  
root_path = os.path.dirname(os.path.realpath(__file__))
    
# TICKET : https://plumedesign.atlassian.net/browse/THRIV-1311
#            

root_path = os.path.dirname(os.path.realpath(__file__))


BD_ADDRESS = macaddr

class AsyncTester(Thread):
    def __init__(self, testfun, bdaddr, timeout):
        global log
        super().__init__()
        
        self.tester = testfun
        self.bdaddr = bdaddr
        self.timeout = timeout

    def run(self):
        asyncio.run(self.tester(self.bdaddr, self.timeout))

class TestCase_upload_Main(object):
    def __init__(self):
        self.ul_state = 'Init'

        # Init - handler
        self.huffman = HuffmanCode()
        self.block_index = 0xFF
        self.UUID_CMD = "00004652-08c2-11e1-9073-0e8ac72e0011"
        self.UUID_RSP = "00004652-08c2-11e1-9073-0e8ac72e0012"
        self.UUID_DAT = "00004652-08c2-11e1-9073-0e8ac72e0013"
        
        # Init - variables
        self.test_run = 1
        self.disconnected_event = None
        self.securityMode = 3

        self.compressed_buf         = [0] * 65536
        self.compressed_len         = 0
        self.compressed_buf_tail    = 0
        self.decompressed_len       = 0
        self.decompressed_buf_tail  = 0

        self.is_first_packet        = True
        self.is_data_uploading      = True

    async def control_pannel_init(self):
        await self.test_cmd(self.client)
        self.is_data_uploading == True
        await self.send_ble_raw_cmd(self.client, '52 01 FF')

    async def test_cmd(self, client):
#--------------------------------------------------
#   Test
#--------------------------------------------------
        await asyncio.sleep(10)
        self.is_data_uploading == True
        await self.send_ble_raw_cmd(self.client, '52 01 FF')
        pollingcnt = 0
        for i in range(1000):
            if (self.is_data_uploading == True):
                await asyncio.sleep(10)
                print(pollingcnt)
                pollingcnt += 1
                continue

            await self.send_ble_raw_cmd(self.client, "52 01 FF")
            
            for j in range(20):
                await asyncio.sleep(60)
                print(pollingcnt)
                pollingcnt += 1

#--------------------------------------------------
#   Command
#--------------------------------------------------
    async def send_ble_raw_cmd(self, client, cmd):
        try:
            oriCmd = bytearray.fromhex(cmd)
            print(f"TX: {''.join('{:02X}'.format(x) for x in oriCmd)}")

            if (SECURITY_MODE == 3):
                await client.write_gatt_char(self.UUID_CMD, self.enc.encrypt(oriCmd))
            else:
                await client.write_gatt_char(self.UUID_CMD, oriCmd)
        except:
            print(f'!!!Unknow command - {cmd}!!!')

    async def notification_handler(self, characteristic: BleakGATTCharacteristic, data: bytearray):
#--------------------------------------------------
#   Response parser
#--------------------------------------------------
        print(f"RX: {''.join('{:02X}'.format(x) for x in data)}")

        if (data[0] == 0x52):
            if (data[1] == 2) and (data[2] == 1) and (data[3] == 1):
                print("--Success--\n")
                self.is_data_uploading  = False
                self.block_index            = 0
                    
        if (data[0] == 0x52) or (data[0] == 0x53):
            ret = self.huffman.parser(data)

            if (ret != ''):
                await self.send_ble_raw_cmd(self.client, "52 01 " + '{:02X}'.format(self.block_index))
                if (self.block_index >= 0xFF) or (self.block_index == 0xF):
                    self.block_index = 0
                else:
                    self.block_index += 1     
            
    def disconnected_callback(self, client):
        print("Disconnected callback called!")
        #if self.disconnected_event.is_set():
        self.disconnected_event.set()

    async def run_test_init(self, client):
        print(f'Exit run_test_init\n')

    async def run_test(self, client):
        while self.test_run == 1:
            print(f'\nwait self.q.get()')
            cmd = await self.q.get()
            print(f'Got self.q.get({cmd})')

            if cmd == 'disconnect':
                print(f'Disconnect break')
                break
            elif cmd == 'Init':
                continue
            else:
                await self.send_ble_cmd(client, cmd)

        self.test_run = 0
        print(f'Exit run_test\n')

    async def dev_disconnect(self, client):
        print(f'dev_disconnect()')
        await self.send_ble_cmd(client, 'disconnect')
        self.test_run = 0

    async def register_notification(self, client):
        await asyncio.sleep(2.0)

        print(f'start_notify {self.UUID_RSP}')
        await client.start_notify(self.UUID_RSP, self.notification_handler)
        await asyncio.sleep(1.0)

        print(f'start_notify {self.UUID_DAT}')
        await client.start_notify(self.UUID_DAT, self.notification_handler)
        await asyncio.sleep(1.0)

    async def unregister_notification(self, client):
        print(f'stop_notify {self.UUID_RSP}')
        await client.stop_notify(self.UUID_RSP)
        await asyncio.sleep(1.0)

        print(f'stop_notify {self.UUID_DAT}')
        await client.stop_notify(self.UUID_DAT)
        await asyncio.sleep(1.0)

    async def MainRun(self, bdaddr, scantime):

        print(f"MainRun({bdaddr}, {scantime})")
        try:
            async with BleakClient( bdaddr,
                                    timeout = scantime,
                                    disconnected_callback = self.disconnected_callback) as client:
                print("---Start---")
                print(f"Connected: {client.is_connected}")
                print(f"BD address: {client.address}")
                print(f"mtu_size: {client.mtu_size}")

                self.client = client

                self.q = asyncio.Queue()

                self.disconnected_event = asyncio.Event()

                await self.register_notification(client)

                await self.control_pannel_init()

                try:
                    await asyncio.gather(self.run_test_init(client, self.q), self.run_test(client, self.q))
                except :
                    pass

                await self.disconnected_event.wait()
                await self.dev_disconnect(client);
                print(f"Connected = {client.is_connected}")
                quit

        except bleak.exc.BleakError as e:
            print(f"Connect error : {e}")
            await asyncio.sleep(3)

if __name__ == "__main__":
    tester = TestCase_upload_Main()
    asyncio.run(
        tester.MainRun(BD_ADDRESS, 15.0)
    )
