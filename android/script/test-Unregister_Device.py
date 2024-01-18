# coding=utf-8
from runnerWrapper import *
import pytest 
import logging 
import random
import os
import re
import time
import toml
import allure # allure report
root_path = os.path.dirname(os.path.realpath(__file__))
allurewiget() # for allure wiget display info
# authorize step

######################################################################

# Before CheckRingRegistrationStatus before ,should Use Authorize process first

# API1 (For Authorize / Per session base)

apiNameCloudLogin = 'PlumeCloudLogin'

apiNameAuthPlumeToken = 'AuthenticateWithPlumeToken'
#---------------------------------------------------

# API3
# /pwb/RegisterDevice
apiNameRegisterDevice = 'RegisterDevice'
# API4
# /pwb/UnregisterDevice
apiName = 'UnregisterDevice'


sn = 'kd8c0000c6'
devid = '60B4F7B307B5'
mac = '60:B4:F7:B3:07:B5'

SN1= 'kd8c0000c6'
SN2= '6489599c9a2357000b2dc384'


class PWBFunc:

    def __init__(self):
        self.cloudtokenid = None
        self.clouduserid = None

    def Authtoken(self,cloudtokenid,clouduserid):

        # Step 2 :  /pwb/AuthenticateWithPlumeToken   

        return authtokenpost(apiNameAuthPlumeToken, cloudtokenid, clouduserid)

    def CloudLoginProcess(self):

        # Step 1 :  /pwb/PlumeCloudLogin

        return CloudLoginpost(apiNameCloudLogin)


    def ToUNregisterdevice(self,finaltokenid,clouduserid,SN):
        
        # Step 3 : /pwb/UnregisterDevice
        sessionId = hex(random.randrange(200, 655))        
        logdef.info(SN)
        """
        For UnregisterDevice
        ##################
        curl -X 'POST' \
          'https://thrive-ci-dog1-api.data.plume.tech/pwb/UnregisterDevice' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
          -H 'Content-Type: application/json' \
          -d '{
          {
             "userId": "62a2d6708a13a8000a1b40b9",
             "deviceId": "{{deviceid}}"
          
          }'

        """

        return ToUNRegdevicepost(apiNameRegisterDevice, finaltokenid,clouduserid,SN)

    def GetDeviceStatusByUser(self,finaltokenid,clouduserid):

        #Step 4 : Test API /pwb/GetDeviceStatusByUser
        #curl -k -H "Content-Type:application/json" -d '{"pingTest": {"action": 1,"ipVersion": 4,"host": "10.10.10.100","count": 3,"size": 64,"timeout": 60,"interval": "1",}}' -u admin:password https://10.10.10.8:8443/api/v1/ping_test_start
        # 
        """
        curl -X 'POST' \
        'https://thrive-ci-usw2-api.data.plume.tech/pwb/GetDeviceStatusByUser' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6ZWM0YjUwNmItMDJiOC00NmRjLWFmOTgtNjkxMzk2YTgxYzYyIiwiYXVkIjoidXMtd2VzdC0yOjYxZWY2YjcyLTk0NzctNDYzYy1iOTQ2LWFhODk3MDhiZTg3ZCIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwicHdiLnBsdW1lLmNvbSIsInB3Yi5wbHVtZS5jb206dXMtd2VzdC0yOjYxZWY2YjcyLTk0NzctNDYzYy1iOTQ2LWFhODk3MDhiZTg3ZDpVNTdIV3VoVkNnTXdYVXVGU293eU5yQVZ4TTJQSXptSlh5cDA1NzNlTDlVVnozTmVZSkViYVhqcXlZWFg5cTU2Il0sImlzcyI6Imh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tIiwiaHR0cHM6Ly9jb2duaXRvLWlkZW50aXR5LmFtYXpvbmF3cy5jb20vaWRlbnRpdHktcG9vbC1hcm4iOiJhcm46YXdzOmNvZ25pdG8taWRlbnRpdHk6dXMtd2VzdC0yOjY0Mzc5NTA3NzcxNTppZGVudGl0eXBvb2wvdXMtd2VzdC0yOjYxZWY2YjcyLTk0NzctNDYzYy1iOTQ2LWFhODk3MDhiZTg3ZCIsImV4cCI6MTY2MDAwMzQzNSwiaWF0IjoxNjU5OTE3MDM1fQ.JHAgjaZRl8CJb_beFWmDiU2uldbphub2Ksx8KA6FnLPxTxyl9CS3NRQUd-Yzu5ZJy1P3iq5UV9iSAoXUhBpwh2l8e68n-DywmjolB4ZQYhC3bIMMffc-MGLozPDAyI036Dv7sgzZ48ugh1R_MVLuuRpmW8lGplGjX0Oj1Ls1FEDsJVM0u_O6RCMW7IkLksK8TYRF6W0zIvTVxEQAQZwFsEo3zen8Ja10tnTDWlYPFoEWgavsmGTF6VDQ6tGL_vfe-iOc3xLW1ZJVOcv6AeYu4lh2BBBGwdfjxDZ5EgBmcQklmG4x8dhnddXiLd88R-3tt--0bPP9m_l5f632Tgq_MQ' \
        -H 'Content-Type: application/json' \
        -d '{
        "userId": "62e89e5391a0ca000a6d18b7"
        }'
            
        """
        data = {"userId": clouduserid}

        return Generalpost(apiName, data ,finaltokenid)        

class TestAPI(TestAPIWrap):
 
    def test_devstatus_func(self):

        """
        Please modify this address before test script
        """
        logdef.info("####################################################################\n")
        logdef.info("# thrive-dog1-usw2-api.data.plume.tech/ #)\n")
        logdef.info("# ---------------------------------------------------------------- #)\n")
        logdef.info("#  Test case : ( /pwb/GetDeviceStatusByUser #)\n")        
        logdef.info("####################################################################)\n")
        self.result = PWBFunc().CloudLoginProcess()
        logdef.info("Step 1 :  PlumeCloudLogin\n")
        Data1 = self.result['data']
        # Get token-id via staging cloud
        cloudtokenid = Data1['id']
        logdef.info(Data1['id'])
        # Get userid via staging
        clouduserid = Data1['user']['id']
        logdef.info(Data1['user']['id'])
        logdef.info("\n")
        logdef.info("Step 2 :  AuthenticateWithPlumeToken\n")        
        self.result2 = PWBFunc().Authtoken(cloudtokenid,clouduserid)
        Data2 = self.result2['data']
        # Get final access-token via staging cloud
        finaltokenid = Data2['accessToken']
        logdef.info(Data2['accessToken'])
        logdef.info("\n")
        time.sleep(3)
         logdef.info("Step 3 : UnRegisterDevice SN2\n")
        self.result3 = PWBFunc().ToUNregisterdevice(finaltokenid,clouduserid,SN1)
        logdef.info("\n")
        time.sleep(3)
        logdef.info("#####################################")
        logdef.info("Step 4 : To Do API Test : GetDeviceStatusByUser\n")
        self.result4 = PWBFunc().GetDeviceStatusByUser(finaltokenid,clouduserid)
        logdef.info(self.result4)
         time.sleep(3)                 
        logdef.info("Step 5 : UnRegisterDevice SN2\n")
        self.result3 = PWBFunc().ToUNregisterdevice(finaltokenid,clouduserid,SN2)
        logdef.info("\n")
        time.sleep(3)
        logdef.info("#####################################")
        logdef.info("Step 6 : To Do API Test : GetDeviceStatusByUser\n")
        self.result4 = PWBFunc().GetDeviceStatusByUser(finaltokenid,clouduserid)
        logdef.info(self.result4)        
        

        """
        "data": {
            "getDeviceResult": "Success",
             "deviceStatus": "registered

        """
        #logdef.info('HTTPS Response Code :'+str(self.result))
