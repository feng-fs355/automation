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
# Releate to pytest.fixture
from math_utils import add, subtract


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



@pytest.fixture
def user_data():
    return {
        'username': 'johndoe',
        'email': 'johndoe@example.com',
        'password': 'password123'
    }


# 测试函数使用 user_data fixture
def test_user_registration(user_data):
    # 在测试函数中可以直接使用 user_data
    assert 'username' in user_data
    assert 'email' in user_data
    assert 'password' in user_data

# 另一个测试函数也可以使用 user_data fixture
def test_user_login(user_data):
    username = user_data['username']
    password = user_data['password']
    # 模拟登录过程进行测试
    assert login(username, password) == True

def login(user,passwrd):
    return True