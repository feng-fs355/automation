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
import allure # allure report
root_path = os.path.dirname(os.path.realpath(__file__))
allurewiget() # for allure wiget display info
class PWBFunc:

    def __init__(self):
        self.cloudtokenid = None
        self.clouduserid = None  

    def LoadJSONFile(self):
        global desrinationfile  # Target json file
        listtemp = 0
        listtemp = int(listtemp)  # for how much steps
        
        current_GMT = time.gmtime()
        logdef.info(current_GMT)
        logdef.info("\n\n")
        time_stamp = calendar.timegm(current_GMT)
        logdef.info("************************************************\n\n")
        #sourcefile = 'CI_CLOUD_Example.json'
        sourcefile = 'dogfood_cloud-example_1018.json'
        with open(sourcefile,'r+') as file:
            data = json.load(file)            
            logdef.info("\n\n")

        data1 = data    

        # Target json file generate
        ID =  (configure['userinfo']['devuserid']) 
        ##desrinationfile = str(ID)+'-android-'+str(time_stamp)+'.json'
        ##with open(desrinationfile, 'w') as f:
        ##    json.dump(data1, f)       

        # DUTID / mhsieh 20221018
        DUTID = (configure['userinfo']['devid']) 
        desrinationfile = str(ID)+'-'+str(DUTID)+'-android-'+str(time_stamp)+'.json'
        with open(desrinationfile, 'w') as f:
            json.dump(data1, f)      

        #### Target json file generate           
        ####desrinationfile = '62a2d6708a13a8000a1b40b9-60B4F7B306AD-android-'+str(time_stamp)+'.json'
        ####with open(desrinationfile, 'w') as f:
        ####    json.dump(data1, f)     
        
                              
class TestAPI(TestAPIWrap):
 
    def test_timeshift_func(self):

        """
        Please modify this address before test script
        """
        logdef.info("####################################################################\n")
        logdef.info("#  thrive-ci-usw2-api.data.plume.tech/ #)\n")
        logdef.info("# ---------------------------------------------------------------- #)\n")
        logdef.info("#  Test case : ( Filename-updatetime #)\n")        
        logdef.info("####################################################################)\n") 
        logdef.info("#####################################")

        PWBFunc().LoadJSONFile()
        

