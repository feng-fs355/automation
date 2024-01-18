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
        
        # For timestamp purpose ------------------
        current_GMT = time.gmtime()
        logdef.info(current_GMT)
        logdef.info("\n\n")
        time_stamp = calendar.timegm(current_GMT)
        current_Base = int(time_stamp)  # Current time Base
        logdef.info(current_Base)
        
        logdef.info("************************************************\n\n")
        
        #sourcefile = 'Min-60B4F7B30695-example.json'

        #sourcefile = 'CI_CLOUD_Example.json'

        sourcefile = 'dogfood_cloud-example_1018.json'

        with open(sourcefile,'r+') as file:
            data = json.load(file)            
            logdef.info("\n\n")
            for index in data:
               if 'timestamp' in index:
                  listtemp = listtemp + 1 
            logdef.info(listtemp)  # Step for how much steps we get
            logdef.info("\n")

        
        data1 = data    
        # First timestamp is 9 / append 
        for i in range(9,listtemp):
            timeslot = (data1[i]['timestamp'])
            fintimes = random.randint(1,5) # shfit how much times via radom
            data1[i]['timestamp'] = timeslot + (fintimes) 

            logdef.info(str(data1[i]['timestamp']) +" = "+str(timeslot)+ "+" +str(fintimes)) 

            logdef.info("\n")
            
        # Target json file generate
        ID =  (configure['userinfo']['devuserid']) 
        #desrinationfile = str(ID)+'-android-'+str(time_stamp)+'.json'
        #with open(desrinationfile, 'w') as f:
        #    json.dump(data1, f)       

        # DUTID / mhsieh 20221018
        DUTID = (configure['userinfo']['devid']) 
        desrinationfile = str(ID)+'-'+str(DUTID)+'-android-'+str(time_stamp)+'.json'
        with open(desrinationfile, 'w') as f:
            json.dump(data1, f)              
                  
                              
class TestAPI(TestAPIWrap):
 
    def test_loadjson_func(self):

        """
        Please modify this address before test script
        """
        logdef.info("####################################################################\n")
        logdef.info("#  LoadJSONFile API (thrive-ci-usw2-api.data.plume.tech/ #)\n")
        logdef.info("# ---------------------------------------------------------------- #)\n")
        logdef.info("#  Test case : ( Generate new JSON File #)\n")        
        logdef.info("####################################################################)\n") 
        logdef.info("#####################################")

        PWBFunc().LoadJSONFile()
        

