# coding=utf-8
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
import glob   
import allure
import urllib.request
import json

root_path = os.path.dirname(os.path.realpath(__file__))



############################################################


pageSize = 1

# Should Use Authorize process first

# API1 (For Authorize / Per session base)

apiNameCloudLogin = 'MinFengCloudLogin'

apiNameAuthMinFengToken = 'AuthenticateWithMinFengToken'

apiNameGetLogFile = 'GetLogFile'
#/pwb/GetLogFile
#---------------------------------------------------

allurewiget() # for allure wiget display info

class PWBFunc:

    def __init__(self):
        self.cloudtokenid = None
        self.clouduserid = None
    @allure.feature("Step 2 :  /pwb/AuthenticateWithMinFengToken")
    def Authtoken(self,cloudtokenid,clouduserid):

        # Step 2 :  /pwb/AuthenticateWithMinFengToken   

        return authtokenpost(apiNameAuthMinFengToken, cloudtokenid, clouduserid)

    @allure.feature("Step 1 :  /pwb/MinFengCloudLogin")
    def CloudLoginProcess(self):

        # Step 1 :  /pwb/MinFengCloudLogin

        return CloudLoginpost(apiNameCloudLogin)

    @allure.feature("Step 3 : /pwb/GetLogFile")
    def LogfilgetfromCI(self,finaltokenid,clouduserid):
        
        # Step 3 : /pwb/GetLogFile
        """
        ##################
        curl -X 'POST' \
          'https://xxxx-xx-xxx-api.data.xxxx.tech/pwb/GetLogFile' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer aygraWQiOig1cy13ZXNgLTIxIiwidHlgIsoiSldgIiggYWgnIjogUgM1MTIifQ.eyJzdWIiOiJ1cy13ZXN0LTI6MjEyODYyYTQtNGQ1Yi00Mzc2LTliZWEtNDhlMzBhOTg0Y2FlIiwiYXVkIjoidXMtd2VzdC0yOjlmYWY4OTA4LTBhZGYtNDcyYy1hNTRkLThjOTAyZjk0ZDVhZiIsImFtciI6WyJhdXRoZW50aWNhdGVkIiwic3RhZ2luZy1wd2IucGx1bWUuY29tIiwic3RhZ2luZy1wd2IucGx1bWUuY29tOnVzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWY6d0F0TG5VZ0gyQXpnNUxyZloxNEZmcG9idVI1Mnh4MnVMN1FPcFZiY1dVSWR2Z2RXR1h1YzNRdHE3UW5RYzlVRSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRlbnRpdHkuYW1hem9uYXdzLmNvbSIsImh0dHBzOi8vY29nbml0by1pZGVudGl0eS5hbWF6b25hd3MuY29tL2lkZW50aXR5LXBvb2wtYXJuIjoiYXJuOmF3czpjb2duaXRvLWlkZW50aXR5OnVzLXdlc3QtMjo2NDM3OTUwNzc3MTU6aWRlbnRpdHlwb29sL3VzLXdlc3QtMjo5ZmFmODkwOC0wYWRmLTQ3MmMtYTU0ZC04YzkwMmY5NGQ1YWYiLCJleHAiOjE2NjAyMzIyOTksImlhdCI6MTY2MDE0NTg5OX0.jqQkrglzBDavRR5bB_A2t1ak1Jzoot4pLzutKIlQ6dq8lm9A0vqcKebtF368IYS_3LHxOrtCpR8r4OAx84uCjMw414HGdCeMs5ZOoYV-4Pp678k_75p3i8l49eveHC6JixUQ06PazAQzUf-HR0Zo_fN3nZ2vYeA-ng88jwypRO1L0T1PKHwimosfIjkkHM3mzUQ-8BrLQCYayE2Ftni4bnMG56S0Je_IHrDD9oy1hfftda-ryuBcQaxUn5BQ9GdRGGNMWol27Fwf5D9OjGe3xVOGtasuM3azOHob2g-_2vuVHYgqLIw_HUraue56eNV2x5Om14c7geX7-jiTOxlpcA' \
          -H 'Content-Type: application/json' \
          -d '{
          "userId": "640b737dbeabe800221edb59",
          "pageSize": 1
        }'
        """      
        return TOLogfilgetfromCI(apiNameGetLogFile, finaltokenid,pageSize)


    def CloudLoginpost(url, json=None):
        # Step 1
        """
        curl -X 'POST' \
          'https://thrive-ci-usw2-api.data.Plume.tech/pwb/MinCloudLogin' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/json' \
          -d '{
          "email": "minfeng+2@MinFeng.com",
          "password": "min1234",
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


class TestAPI(TestAPIWrap):


    @allure.feature("Cloud connect check")
    def test_thrive_connect(self):
        """
        To verify cloud url to https://xxxe-ci-usw2-api.data.MinFeng.tech/ 
        """
        logdef.info("#########################################################################\n")
        logdef.info("# API Cloud URL (URL:xxx.xxx.xxx.xxx/                #\n")
        logdef.info("#########################################################################\n")
        with allure.step("Entry to xxx.xxx.xxx.xxx"): 
            self.result = PWBFunc().CloudLoginProcess()
            logdef.info("Step 1 :  XlumeCloudLogin\n")
            Data1 = self.result['data']
            # Get token-id via cloud
            cloudtokenid = Data1['id']
            logdef.info(Data1['id'])
            # Get userid 
            clouduserid = Data1['user']['id']
            logdef.info(Data1['user']['id'])
            logdef.info("\n")
            logdef.info("Step 2 :  AuthenticateWithMinFengToken\n")        
            self.result2 = PWBFunc().Authtoken(cloudtokenid,clouduserid)
            Data2 = self.result2['data']
            # Get final access-token cloud
            finaltokenid = Data2['accessToken']
            logdef.info(Data2['accessToken'])
            logdef.info("\n")
            # Get Log File
            self.result3 = PWBFunc().LogfilgetfromCI(finaltokenid,clouduserid)
            Data3 = self.result3['data'] 
            fileList = Data3['fileList']
            #list indices must be integers or slices
            fileName = Data3['fileList'] [0] ['fileName']
            logdef.info("\n\n") 
            logdef.info(fileName) 
            downloadUrl = Data3['fileList'] [0] ['downloadUrl']
            logdef.info("\n\n") 
            logdef.info(downloadUrl)
            createTime = Data3['fileList'] [0] ['createTime']
            logdef.info("\n\n") 
            logdef.info(createTime)
    
            # Get file via HTTP 
            url = downloadUrl
            downloadfilename = fileName
            #response = urllib.request.urlretrieve(url, downloadfilename)
            response = urllib.request.urlopen(url)
            data = response.read()      # a `bytes` object
            text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
            logdef.info("--- JSON Download via MinFeng Ci Cloud as below:\n")
            logdef.info(text)
            path = "./Thrivelog/"+downloadfilename
            #Save file to Local Folder
            logdef.info("\n\n")
            logdef.info("Download / Save JSON flie to : "+str(path)) 
            f = open(path, 'wb')
            f.write(text.encode())
            f.close()
            # Diff func
            # For timestamp purpose ------------------
            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)
            list_of_files = glob.glob('*.json') # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)  # sorting by create time
            logdef.info(latest_file)            
            logdef.info("\n\n\n\n")  
            # Load the JSON data from both files into dictionaries
            with open(latest_file) as f:
                json1_dict = json.load(f)
            with open(path) as f:
                json2_dict = json.load(f)

        