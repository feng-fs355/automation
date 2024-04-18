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
import allure
root_path = os.path.dirname(os.path.realpath(__file__))

def test_clients():
    #/api/gen/clients
    print("Step 1 :  /api/gen/clients")
    return GeneralGet('/api/gen/clients')

def test_clientlanguage():
    # /api/gen/clients/{language}
    print("Step 2 : /api/gen/clients/{language}",None,None)
    language = ('ada', 'android', 'apex')
    for item in language:
        time.sleep(1)
        result = JSONGet(f'/api/gen/clients/{item}',None, None)
        Data = result['sortParamsByRequiredFlag']
        OPT = Data['opt']
        print(f"opt is : {OPT} ")
        DES = Data['description']
        print((f"descrption is : {DES} "))
        TYPE = Data['type']
        print((f"TYPE is : {TYPE} "))
        OPTVAL = Data['optValue']
        print((f"optValue is : {OPTVAL} "))
        DEFAULT = Data['default']
        print((f"default is : {DEFAULT} "))
        ENUM = Data['enum']
        print((f"ENUM is : {ENUM} "))
def test_nasaapod():
    # API : /planetary/apod
    # get config from config.ini
    apikey = (configure['userinfo']['api_key'])
    print(apikey)
    result = JSONGet(f'/planetary/apod',apikey,None)
    print("Picture URL:", result["url"])

def test_nasaMarsWeather():
    #  InSight: Mars Weather Service API
    querykey = '&feedtype=json&ver=1.0'
    apikey = (configure['userinfo']['api_key'])
    result = JSONGet(f'/insight_weather/', apikey, querykey)
    Data = result['validity_checks']
    print(Data)
    