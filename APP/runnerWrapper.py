import ast
import inspect
import json
import logging
import os
import re
import time
import pytest
import requests
import toml
import subprocess

LOG_LEVEL = logging.DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
root_path = os.path.dirname(os.path.realpath(__file__))
common_formatter = logging.Formatter('%(asctime)s [%(levelname)-7s][ln-%(lineno)-3d]: %(message)s',
                                     datefmt='%Y-%m-%d %H:%M:%S')

logdef = None
logapi = None
logtel = None
handler = None
configure = None
switchinfo = {}
requests_timeout = 120

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def setupLog():
    global logdef, logapi, logtel
    if logdef: return
    filedefprefix = time.strftime('%y%m%d')
    fileapiprefix = time.strftime('%y%m%d%H%M')
    # default console logger
    debug_log_filename = root_path + os.sep + 'Logs' + os.sep + filedefprefix + '_console_outputs.log'
    logdef = setup_logger(debug_log_filename, LOG_LEVEL, 'logcon')

    # logger for API outputs
    api_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    api_outputs_filename = root_path + os.sep + 'Logs' + os.sep + fileapiprefix + '_api_outputs.log'
    logapi = setup_logger(api_outputs_filename, LOG_LEVEL, 'logapi', formatter=api_formatter)


def setupConfig():
    global configure
    if configure: return
    logdef.info('Start to load config file')
    configure = toml.load('config.ini')
    logdef.debug('config.ini: %s' % configure)


def setupRequest():
    global handler
    if handler: return


# Note: To create multiple log files, must use different logger name.
def setup_logger(log_file, level=logging.INFO, name='', formatter=common_formatter):
    """Function setup as many loggers as you want."""
    handler = logging.FileHandler(log_file, mode='a')
    # Or use a rotating file handler
    # handler = RotatingFileHandler(log_file,maxBytes=1024, backupCount=5)          
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def pretty_print_request(request):
    logapi.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )


def pretty_print_request_json(request): 

    #  body = request.body.replace('true', 'True').replace('false', 'False') # for python2 
    #  For python3 as below
    #  Reference : https://stackoverflow.com/questions/33054527/typeerror-a-bytes-like-object-is-required-not-str-when-writing-to-a-file-in
    #  20220809 Min modify
    body = request.body.decode('utf8').replace('true', 'True', 3).replace('false', 'False', 3)
    #------------------------------------------------------------------------------------------
    logapi.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        json.dumps(ast.literal_eval(body), indent=4))
    )

def pretty_print_response_json(response):
    """ pretty print response in json format. 
        If failing to parse body in json format, print in text.
    """
    esec = response.elapsed.total_seconds()
    if esec > 10:
        logdef.warn('rest call costs long time!!')
    try:
        resp_data = response.json()
        resp_body = json.dumps(resp_data, indent=4)
    # if .json() fails, ValueError is raised.
    except ValueError:
        resp_body = response.text
    logapi.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code: %s, elapsed seconds: %s' % (str(response.status_code), esec),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        resp_body
    ))


def httpget(url, auth=None):

    pass
    
def authtokenpost(url, Token=None, Id=None):
    #Step 2
    """
    curl -X 'POST' \
      'https://nordic-ci-usw2-api.data.minfeng.tech/pwb/AuthenticateWithminfengToken' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "accessToken": "wAtLnUgH2Azg5LrfZ14FfpobuR52xx2uL7QOpVbcWUIdvgdWGXuc3Qtq7QnQc9UE",
      "userId": "62a2d6708a13a8000a1b40b9"
    }'
    """
    # 20220811 min add flow 
    # reference data apiDem.ts
          
    json = {"accessToken": Token, "userId": str(Id),}
    
    logdef.info(url)
    
    ###################################################################
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
               'Content-Type': "application/json"}

  
    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

   
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()

    logdef.info(url)

    headers = { 'accept': 'application/json',
               'Content-Type': "application/json"}

    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()    



def CloudLoginpost(url, json=None):
    # Step 1
    """
    curl -X 'POST' \
      'https://nordic-ci-usw2-api.data.minfeng.tech/pwb/minfengCloudLogin' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "action+2@minfeng.com",
      "password": "minfeng1234",
      "ttl": 3600
    }'
    """
    # 20220811 min add flow 
    # reference data apiDem.ts

 
    try:
        userinfo =  (configure['userinfo']['usrid'])
        userpwd =  (configure['userinfo']['pwd'])
    except:
        userinfo =  (configure['userinfo']['usrid'])
        userpwd =  (configure['userinfo']['pwd'])      
 
    json = {"email": userinfo, "password": str(userpwd), "ttl": 3600}
    
    logdef.info(url)
    
    ###################################################################
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
               'Content-Type': "application/json"}

  
    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

   
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()

    logdef.info(url)

    headers = { 'accept': 'application/json',
               'Content-Type': "application/json"}

    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()  

def ToRegdevicepost(url, FinalaccessToken,Cdevid,subscriptionIdnumber): # modify 20230310
    """
    For RegisterDevice
    ##################
    curl -X 'POST' \
      'https://nordic-ci-usw2-api.data.minfeng.tech/pwb/RegisterDevice' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
      -H 'Content-Type: application/json' \
      -d '{
      "userId": "62a2d6708a13a8000a1b40b9",
      "deviceId": "kd8b0002f6",
     }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "deviceId": str(Cdevid)}
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()

    logdef.info(url)

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(clouduserid), "deviceId": str(Cdevid)}

    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()



def ToUNRegdevicepost(url, FinalaccessToken,Cdevid,SN): # modify 20230310
    """
    For UNRegisterDevice
    ##################
    curl -X 'POST' \
      'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/UnregisterDevice' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
      -H 'Content-Type: application/json' \
      -d '{
      "userId": "62a2d6708a13a8000a1b40b9",
      "deviceId": "kd8b0002f6",
     }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "deviceId": str(Cdevid)}
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()

    logdef.info(url)

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(clouduserid), "deviceId": str(Cdevid)}

    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()


def ToGetFallEventList(url, FinalaccessToken,STime,ETime): # modify 20230718
    logdef.info(url)
    """
    For GetFallEventList
    ##################
        curl -X 'POST' \
          'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/GetFallEventList \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIzIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6ZTIyMDZiN2QtMDk1YS00M2QxLTgxMzUtODZhMTc5NmI1OTA5IiwiYXVkIjoidXMtd2VzdC0yOjU2YzQyNDM5LWJlMmMtNDUyMy04YmUwLTEwYjU4ODVlYTczMyIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzM6SlVtQnFiMmRxT3lRZFdFS3VSR1hYWnZrN2RMTUEwUmJYaENtOUVHb1gwZW00aHRCWlVCNnZLMkF0cVN6cXVVViJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjoxNDMwODk2MTA0ODI6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzMiLCJleHAiOjE2ODY2MzM0OTcsImlhdCI6MTY4NjU0NzA5N30.FgoFMwJC-kz2WfyTGKbFiz5JkyC8vMlRm8aZMcIpROa8y9TpRmxiNXuShUAvXNEQKcb7-WndcBG7g72DjhJSsLldSewMS8Ck2bgb5G1cLofL6JepcTHrZxEuxJ-9ESLnlOGGYqCZEzJfdqlYkbSutsMwf02D7Dwr2RWVpVgCC8uOSavDQUPJ5OlMPzenBVGGDhbntUdCZiEC1pc6oyj7gK_ndL4m_KigNho9a0WZ00asVzB7qHDJQNpodLx4nvfbf6ZQHNNYn_J9PWZ3TRLTSTjZ8eQTXVjh5i1SM9T50hbkNCFxGxmGEEYFhWoZAEBwndc-KjdS9QbB6Am7448MFA' \
          -H 'Content-Type: application/json' \
          -d '{
          "userId": "62a2d6708a13a8000a1b40b9",
          "startTime": 1686500000,
          "endTime": 1686547498
        }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "startTime": STime ,"endTime": ETime}
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)

    return resp.json()


def ToGetFallEventSummary(url, FinalaccessToken,STime,ETime): # modify 20230718
    logdef.info(url)
    """
    For ToGetFallEventSummary
    ##################
        curl -X 'POST' \
          'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/GetFallEventSummary' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIzIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6ZTIyMDZiN2QtMDk1YS00M2QxLTgxMzUtODZhMTc5NmI1OTA5IiwiYXVkIjoidXMtd2VzdC0yOjU2YzQyNDM5LWJlMmMtNDUyMy04YmUwLTEwYjU4ODVlYTczMyIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzM6SlVtQnFiMmRxT3lRZFdFS3VSR1hYWnZrN2RMTUEwUmJYaENtOUVHb1gwZW00aHRCWlVCNnZLMkF0cVN6cXVVViJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjoxNDMwODk2MTA0ODI6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzMiLCJleHAiOjE2ODY2MzM0OTcsImlhdCI6MTY4NjU0NzA5N30.FgoFMwJC-kz2WfyTGKbFiz5JkyC8vMlRm8aZMcIpROa8y9TpRmxiNXuShUAvXNEQKcb7-WndcBG7g72DjhJSsLldSewMS8Ck2bgb5G1cLofL6JepcTHrZxEuxJ-9ESLnlOGGYqCZEzJfdqlYkbSutsMwf02D7Dwr2RWVpVgCC8uOSavDQUPJ5OlMPzenBVGGDhbntUdCZiEC1pc6oyj7gK_ndL4m_KigNho9a0WZ00asVzB7qHDJQNpodLx4nvfbf6ZQHNNYn_J9PWZ3TRLTSTjZ8eQTXVjh5i1SM9T50hbkNCFxGxmGEEYFhWoZAEBwndc-KjdS9QbB6Am7448MFA' \
          -H 'Content-Type: application/json' \
          -d '{
          "userId": "62a2d6708a13a8000a1b40b9",
          "startTime": 1686500000,
          "endTime": 1686547498
        }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "startTime": STime ,"endTime": ETime , "interval": "day", "utcTimeOffset": 8 }
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)

    return resp.json()


def ToGetDailySleepInsightList(url, FinalaccessToken,STime,ETime): # modify 20230612
    logdef.info(url)
    """
    For GetDailySleepInsightList
    ##################
        curl -X 'POST' \
          'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/GetDailySleepInsightList' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIzIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6ZTIyMDZiN2QtMDk1YS00M2QxLTgxMzUtODZhMTc5NmI1OTA5IiwiYXVkIjoidXMtd2VzdC0yOjU2YzQyNDM5LWJlMmMtNDUyMy04YmUwLTEwYjU4ODVlYTczMyIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzM6SlVtQnFiMmRxT3lRZFdFS3VSR1hYWnZrN2RMTUEwUmJYaENtOUVHb1gwZW00aHRCWlVCNnZLMkF0cVN6cXVVViJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjoxNDMwODk2MTA0ODI6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzMiLCJleHAiOjE2ODY2MzM0OTcsImlhdCI6MTY4NjU0NzA5N30.FgoFMwJC-kz2WfyTGKbFiz5JkyC8vMlRm8aZMcIpROa8y9TpRmxiNXuShUAvXNEQKcb7-WndcBG7g72DjhJSsLldSewMS8Ck2bgb5G1cLofL6JepcTHrZxEuxJ-9ESLnlOGGYqCZEzJfdqlYkbSutsMwf02D7Dwr2RWVpVgCC8uOSavDQUPJ5OlMPzenBVGGDhbntUdCZiEC1pc6oyj7gK_ndL4m_KigNho9a0WZ00asVzB7qHDJQNpodLx4nvfbf6ZQHNNYn_J9PWZ3TRLTSTjZ8eQTXVjh5i1SM9T50hbkNCFxGxmGEEYFhWoZAEBwndc-KjdS9QbB6Am7448MFA' \
          -H 'Content-Type: application/json' \
          -d '{
          "userId": "62a2d6708a13a8000a1b40b9",
          "startTime": 1686500000,
          "endTime": 1686547498,
          "pageSize": 1,
          "startKey": "",
          "utcOffset": -8
        }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "startTime": STime ,"endTime": ETime ,"pageSize": 1,"startKey": "" , "utcOffset": -8 }
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)

    return resp.json()

def ToGetFitnessActivityList(url, FinalaccessToken,STime,ETime): # modify 20230612
    logdef.info(url)
    """
    For GetFitnessActivityList
    ##################
        curl -X 'POST' \
          'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/GetFitnessActivityList' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIzIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6ZTIyMDZiN2QtMDk1YS00M2QxLTgxMzUtODZhMTc5NmI1OTA5IiwiYXVkIjoidXMtd2VzdC0yOjU2YzQyNDM5LWJlMmMtNDUyMy04YmUwLTEwYjU4ODVlYTczMyIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzM6SlVtQnFiMmRxT3lRZFdFS3VSR1hYWnZrN2RMTUEwUmJYaENtOUVHb1gwZW00aHRCWlVCNnZLMkF0cVN6cXVVViJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjoxNDMwODk2MTA0ODI6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo1NmM0MjQzOS1iZTJjLTQ1MjMtOGJlMC0xMGI1ODg1ZWE3MzMiLCJleHAiOjE2ODY2MzM0OTcsImlhdCI6MTY4NjU0NzA5N30.FgoFMwJC-kz2WfyTGKbFiz5JkyC8vMlRm8aZMcIpROa8y9TpRmxiNXuShUAvXNEQKcb7-WndcBG7g72DjhJSsLldSewMS8Ck2bgb5G1cLofL6JepcTHrZxEuxJ-9ESLnlOGGYqCZEzJfdqlYkbSutsMwf02D7Dwr2RWVpVgCC8uOSavDQUPJ5OlMPzenBVGGDhbntUdCZiEC1pc6oyj7gK_ndL4m_KigNho9a0WZ00asVzB7qHDJQNpodLx4nvfbf6ZQHNNYn_J9PWZ3TRLTSTjZ8eQTXVjh5i1SM9T50hbkNCFxGxmGEEYFhWoZAEBwndc-KjdS9QbB6Am7448MFA' \
          -H 'Content-Type: application/json' \
          -d '{
          "userId": "62a2d6708a13a8000a1b40b9",
          "startTime": 1686500000,
          "endTime": 1686547498,
          "pageSize": 1,
          "startKey": ""
        }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "startTime": STime ,"endTime": ETime ,"pageSize": 1,"startKey": ""}
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)

    return resp.json()

def ToGetDailyReadinessInsightList(url, FinalaccessToken,STime,ETime): # modify 20230531
    logdef.info(url)
    """
    For UNRegisterDevice
    ##################
    curl -X 'POST' \
      'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/GetDailyReadinessInsightList' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
      -H 'Content-Type: application/json' \
      -d '{
      "userId": "{{userId}}",
      "startTime": {{before10days}},
      "endTime": {{currenttime}},
      "pageSize": 1,
      "startKey": ""
    }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "startTime": STime ,"endTime": ETime , "pageSize": 1 , "startKey": ""}
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)

    return resp.json()



def ToGetReadinessInsightSummary(url, FinalaccessToken,STime,ETime): # modify 20230531
    logdef.info(url)
    """
    For UNRegisterDevice
    ##################
    curl -X 'POST' \
      'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/UGetReadinessInsightSummary' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
      -H 'Content-Type: application/json' \
      -d '{
           "userId": "62a2d6708a13a8000a1b40b9",
           "startTime": 1684598400,
           "endTime": 1685203199,
           "interval": "week",
           "utcTimeOffset": 8
     }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "startTime": STime ,"endTime": ETime ,"interval": "week",  "utcTimeOffset": 8 }
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)

    return resp.json()

def ToGetFitnessInsightSummary(url, FinalaccessToken,STime,ETime): # modify 20230526
    logdef.info(url)
    """
    For UNRegisterDevice
    ##################
    curl -X 'POST' \
      'https://nordic-dog1-usw2-api.data.minfeng.tech/pwb/UnregisterDevice' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
      -H 'Content-Type: application/json' \
      -d '{
           "userId": "62a2d6708a13a8000a1b40b9",
           "startTime": 1685030400,
           "endTime": 1685116799,
           "interval": "day",  
            "utcTimeOffset": 8
     }'
    """
    USERID = (configure['userinfo']['devuserid'])
    DEVID = (configure['userinfo']['devid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "startTime": STime ,"endTime": ETime ,"interval": "day",  "utcTimeOffset": 8 }
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)

    return resp.json()



def TOLogfilgetfromCI(url, FinalaccessToken, Cpages): # add 20230313
    # ESW-15382
    # Step 3 : /pwb/GetLogFile
    """
    ##################
    curl -X 'POST' \
      'https://nordic-ci-usw2-api.data.minfeng.tech/pwb/GetLogFile' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
      -H 'Content-Type: application/json' \
      -d '{
      "userId": "640b737dbeabe800221edb59",
      "pageSize": 1
    }'
    """
    USERID = (configure['userinfo']['devuserid'])
    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(USERID), "pageSize": int(Cpages)}
    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()

    logdef.info(url)

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }
    json = {"userId": str(clouduserid), "pageSize": int(Cpages)}

    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()    


def Generalpost(url, json ,FinalaccessToken):


    # Step 4 : Test All of the API

    # For Over-all API purpose (no need to add more in parser)

    logdef.info(url)
    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }

    #response = requests.get(bl_url, headers=headers)

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()

    logdef.info(url)

    headers = { 'accept': 'application/json',
        'Authorization': "Bearer %s" % FinalaccessToken,
        'Content-Type': "application/json",
        }

    try:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    except:
        f_url = 'https://%s/pwb/%s' % (configure['dut']['ip'], url)
    # ------------------------------------------------------------------------------------------------------    

    # send post request
    try:
        resp = requests.post(f_url, headers=headers, json=json, verify=False, timeout=requests_timeout)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.post() failed with exception: %s' % str(ex))
        return None

    # pretty request and response into API log file
    # Note: request print is common instead of checking if it is JSON body. So pass pretty formatted json string as argument to the request for pretty logging. 
    pretty_print_request_json(resp.request)
    pretty_print_response_json(resp)


    return resp.json()


## Put file to AWS Cloud
def Generalput(url,FinalaccessToken,JSONfileName,awslink):
    path = JSONfileName
    upload_url = awslink
    logdef.info(path)
    f = open(path, mode = 'r', encoding='utf-8')
    DESFILE = json.load(f)
    DESFILE = json.dumps(DESFILE)
    ###DESFILE = json.dumps(DESFILE,sort_keys=True)
    logdef.info(DESFILE)

    upload_headers = {'Content-Type': "application/json"}

    try:
        resp = requests.put(awslink, DESFILE, headers=upload_headers)
        #resp = requests.put(awslink, , headers=upload_headers)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.put() failed with exception: %s' % str(ex))
        return None

    #return upload_res
    logdef.info(resp.status_code)
    return resp

 

def telHasText(text, cliOutput):
    for line in cliOutput.split('\n'):
        if re.search(text, line, re.IGNORECASE | re.DOTALL):
            return True
    return False

def allurewiget():
    # 20220926 for allure wiget display info
    # Generate environment.properties
    try:
        deviceinfo =  (configure['allurewiget']['Device'])
        devver = (configure['allurewiget']['DevVersion'])
        firmwareurl =  (configure['allurewiget']['FirmwareURL'])
        user = (configure['userinfo']['usrid'])
    except:
        deviceinfo =  (configure['allurewiget']['Device'])
        devver = (configure['allurewiget']['DevVersion'])
        firmwareurl =  (configure['allurewiget']['FirmwareURL'])

    path = './allure-results/environment.properties'
    f = open(path, 'w')
    f.write("Device="+str(deviceinfo)+"\n")
    f.write("DevVersion="+str(devver)+"\n")
    f.write("FirmwareURL="+str(firmwareurl)+"\n")             
    f.close()    


class TestAPIWrap:
    def setup_class(cls):
        logdef.debug('%s Star to run: <%s> %s' % ('=' * 40, cls.__name__, '=' * 40))

    def teardown_class(cls):
        logdef.debug('teardown_class')

    def setup_method(self, method):
        logdef.debug('%s Star to run: <%s> %s' % ('=' * 40, method.__name__, '=' * 40))

    def teardown_method(self, method):
        logdef.debug('teardown_method')



if __name__ != '__main__':
    setupLog()
    setupConfig()
    setupRequest()