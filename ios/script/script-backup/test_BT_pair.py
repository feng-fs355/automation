#!/usr/bin/env python3
#coding=utf-8
import pexpect
from runnerWrapper import *
import pytest 
import logging 
import random
# 20220814
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
import allure # allure report
import asyncio
from asyncore import loop
from bleak import BleakScanner, BleakClient

deviceName = "ETO"

global scanned_device

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
RET_RES = ""
allurewiget() # for allure widget display info
BTdevName = "PlumeF-100111200-13-003B"
NORDIC_TX = ResponseUUID

class TXCallback:
    def __init__(self, name):
        self.name = name

    def callback(self, sender, data):
        print(f'Receive "{self.name}" get：{data.decode()}')


class PWBFunc:

  def __init__(self):
    self.cloudtokenid = None
    self.clouduserid = None

  @pytest.mark.asyncio	 
  async def main(self,address):
    client = BleakClient(address, loop=loop)
    logdef.info(client)
    dev_name = client
    logdef.info("------------------Prepare BLE connection\n")
    await client.connect()
    logdef.info("------------------BLE connect")
    #await client.unpair()
    #logdef.info("------------------BLE unpair")
    await client.pair(3)
    logdef.info("------------------BLE pair")
    x = await client.is_connected()
    logdef.info("Connected: {0}".format(x))


    for service in client.services:
        logdef.info("[Service] {0}: {1}".format(service.uuid, service.description))
        for char in service.characteristics:
            if "read" in char.properties:
                try:
                    value = bytes(await client.read_gatt_char(char.uuid))
                except Exception as e:
                    value = str(e).encode()
            else:
                value = None
            logdef.info(
                "\t[Characteristic] {0}: ({1}) | Name: {2}, Value: {3} ".format(
                    char.uuid, ",".join(char.properties), char.description, value))

    
    """
    svcs = await client.get_services()
    for service in svcs:
        logdef.info("\tService: {0}".format(service))
        for char in service.characteristics:
            logdef.info("\t\tcharacteristic:")
            logdef.info(char)
            logdef.info(char.description)
            logdef.info(char.properties)
            if "read" in char.properties:
                try:
                    value = bytes(await client.read_gatt_char(char))
                    logdef.info(" value of read charac '{0}'".format(value))
                except:
                    logdef.info("not enough authentication")

    try:
        cb = TXCallback(BTdevName)
        await client.start_notify(
            NORDIC_TX, cb.callback
        )
    except Exception as e:
        print(e)
    """



class TestAPI(TestAPIWrap):

  def test_pairing_func(self):

    """
    BLE func test : Pairing device
    """
    logdef.info("####################################################################\n")
    logdef.info("#  Test case : ( pytest BLE pairing  #)\n")        
    logdef.info("####################################################################)\n") 
    logdef.info("#####################################")		
    asyncio.run(PWBFunc().main(macaddr))
