from runnerWrapper import *
import pytest
import logging
import os
import time
import toml
import shutil
import allure
import webbrowser

root_path = os.path.dirname(os.path.realpath(__file__))
###########################################################

@pytest.fixture()
def apikey_data():
  # get config from config.ini
  print(f"Get API Key from Config.ini / Call Nasa func", end="")
  apikey = (configure['userinfo']['api_key'])
  return apikey

def test_nasaapod(apikey_data):
  # API : /planetary/apod
  result = JSONGet(f'/planetary/apod', apikey_data, None)
  print("Picture URL:", result["url"])
  # Open image through Web-Browser
  webbrowser.open(result["url"])

def test_nasaMarsWeather(apikey_data):
  #  InSight: Mars Weather Service API
  querykey = '&feedtype=json&ver=1.0'
  result = JSONGet(f'/insight_weather/', apikey_data, querykey)
  Data = result['validity_checks']
  print(Data)
#Use the Person class to create an object, and then execute the printname method:


##################################################################
"""
def test_clients():
    #/api/gen/clients
    # https://api.openapi-generator.tech/api/gen/clients
    print("Step 1 :  /api/gen/clients")
    assert GeneralGet('/api/gen/clients')

def test_clientlanguage():
    # /api/gen/clients/{language}
    #https://api.openapi-generator.tech/api/gen/clients/apex
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

@pytest.mark.parametrize('user, password',
                         [('min', 'abcdefgh'),
                          ('tom', 'a123456a'),
                          ('luke', "21880377"),
                          ('zeno-number1', "a4fruch11")])
def test_passwd_md5(user, password):
    # command example : echo -n a4fruch11 | md5sum
    db = {
        'min': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503',
        'luke': 'f544e1cd917e141842393d9d6a2874c4',
        'zeno-number1': 'c0ff63591a87ad0d45d8ab93fdaa67fa'
    }
    import hashlib
    assert hashlib.md5(password.encode()).hexdigest() == db[user]
"""


