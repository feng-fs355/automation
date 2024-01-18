# coding=utf-8
from runnerWrapper import *
import pytest 
import logging 
import random
# 20220811
import os
import re
import calendar
import time
import toml
import shutil
import glob   # 20220816 for newest file search
import allure # allure report

root_path = os.path.dirname(os.path.realpath(__file__))
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

# /pwb/UploadFile
apiName = 'UploadFile'

allurewiget() # for allure wiget display info

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

    
    def Toregisterdevice(self,finaltokenid,clouduserid):
        
        # Step 3 : /pwb/RegisterDevice
        sessionId = hex(random.randrange(200, 655))        
        subscriptionIdnumber = "kd8b00"+str(sessionId)
        logdef.info(subscriptionIdnumber)
        """
        For RegisterDevice
        ##################
        curl -X 'POST' \
          'https://thrive-ci-usw2-api.data.plume.tech/pwb/RegisterDevice' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJraWQiOiJ1cy13ZXN0LTIxIiwidHlwIjoiSldTIiwiYWxnIjoiUlM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
          -H 'Content-Type: application/json' \
          -d '{
          "userId": "62a2d6708a13a8000a1b40b9",
          "deviceId": "60B4F7B30457",
          "subscriptionId": "kd8b0002f6"
        }'
        """
     
        return ToRegdevicepost(apiNameRegisterDevice, finaltokenid,clouduserid,subscriptionIdnumber)

    def UploadFile(self,finaltokenid,clouduserid):
        global desrinationfile
        global DESFILE
        # For timestamp purpose ------------------
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        list_of_files = glob.glob('*.json') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)  # sorting by create time
        logdef.info(latest_file)
        desrinationfile = latest_file        
        DESFILE = desrinationfile
        #data = {"userId": clouduserid, "fileName": desrinationfile,
        #        "fileType": "application/json", "dataType": "rawdata"}     
        data = {"userId": clouduserid, "fileName": DESFILE,
               "fileType": "application/json", "dataType": "json"}   

                 
        return Generalpost(apiName, data,finaltokenid)
           

    def PUTFile(self,finaltokenid,AWSURL):

        logdef.info(DESFILE)


        return Generalput(apiName,finaltokenid,DESFILE,AWSURL)       


class TestAPI(TestAPIWrap):
 
    def test_loadjson_func(self):

        """
        Please modify this address before test script
        """
        logdef.info("####################################################################\n")
        logdef.info("#  thrive-ci-usw2-api.data.plume.tech/ #)\n")
        logdef.info("# ---------------------------------------------------------------- #)\n")
        logdef.info("#  Test case : ( /pwb/UploadFile #)\n")        
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
        #logdef.info("Step 3 : RegisterDevice\n")
        #self.result3 = PWBFunc().Toregisterdevice(finaltokenid,clouduserid)
        #logdef.info("\n")
        logdef.info("#####################################")
        logdef.info("Step 4 : To Do API Test : /pwb/UploadFile\n")
        self.Uploadresult = PWBFunc().UploadFile(finaltokenid,clouduserid)
        Data4 = self.Uploadresult['data']
        AWS_URL_TEMP =  Data4['url']
        logdef.info('\n')
        logdef.info('AWS upload URL is :'+str(AWS_URL_TEMP))
        logdef.info('\n')
        logdef.info("Step 5 : PUT JSON File to AWS\n\n")        
        self.PUTresult = PWBFunc().PUTFile(finaltokenid,AWS_URL_TEMP)          
        logdef.info('PUT File to AWS Response Code : '+str(self.PUTresult))
        logdef.info('\n')    