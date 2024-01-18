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
logging.basicConfig()
# get config from config.ini
macaddr = (configure['userinfo']['mac'])
devuserid = (configure['userinfo']['devuserid'])
devid = (configure['userinfo']['devid'])
usermail = (configure['userinfo']['usrid'])
userpassword = (configure['userinfo']['pwd'])
sn = (configure['userinfo']['sn'])
devid = (configure['userinfo']['devid'])

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

        For UnregisterDevice


        return ToUNRegdevicepost(apiNameRegisterDevice, finaltokenid,clouduserid,SN)

    def GetDeviceStatusByUser(self,finaltokenid,clouduserid):

        #Step 4 : Test API /pwb/GetDeviceStatusByUser
        #curl -k -H "Content-Type:application/json" -d '{"pingTest": {"action": 1,"ipVersion": 4,"host": "10.10.10.100","count": 3,"size": 64,"timeout": 60,"interval": "1",}}' -u admin:password https://10.10.10.8:8443/api/v1/ping_test_start
        # 
        data = {"userId": clouduserid}

        return Generalpost(apiName, data ,finaltokenid)        

class TestAPI(TestAPIWrap):
 
    def test_devstatus_func(self):

        """
        Please modify this address before test script
        """
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
        logdef.info("Step 3 : UnRegisterDevice SN\n")
        self.result3 = PWBFunc().ToUNregisterdevice(finaltokenid,clouduserid,sn)
        logdef.info("\n")
        time.sleep(3)
        logdef.info("#####################################")
        logdef.info("Step 4 : To Do API Test : GetDeviceStatusByUser\n")
        self.result4 = PWBFunc().GetDeviceStatusByUser(finaltokenid,clouduserid)
        logdef.info(self.result4)
        time.sleep(3)                 

        """
        "data": {
            "getDeviceResult": "Success",
             "deviceStatus": "registered

        """
        #logdef.info('HTTPS Response Code :'+str(self.result))
