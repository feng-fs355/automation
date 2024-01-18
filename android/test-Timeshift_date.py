# coding=utf-8
from runnerWrapper import *
import pytest 
import logging 
import random
import os
import re
import calendar
import time
import math
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
        listtemp = int(listtemp)

        #source=open("CI_CLOUD_Example.json")
        source=open("dogfood_cloud-example_1018.json")
        output_arr=json.loads(source.read())

        current = time.localtime()
        logdef.info(current)
        logdef.info("\n\n")
        time_stamp = calendar.timegm(current)
        logdef.info("************************************************\n\n")

        for line_obj in output_arr:
            if 'starttime' in line_obj:
                time_diff=time_stamp - line_obj["starttime"]
                logdef.info('Time diff :' + str(time_diff) )
                dateshift = math.floor(time_diff/86400)
                left_sec = time_diff%86400
                logdef.info('Left Second :' + str(left_sec) )
                # if left_sec >=86400:
                #     total_dateshift = dateshift + 1
                # else:
                #     total_dateshift = dateshift
            else:
                time_diff=time_stamp - output_arr[9]["timestamp"]
                logdef.info('Time diff :' + str(time_diff) )
                dateshift = math.floor(time_diff/86400)
                left_sec = time_diff%86400
                logdef.info('Left Second :' + str(left_sec) )

        # logdef.info('Total date shift :' + str(total_dateshift) + 'day(s)' )
        logdef.info('Total date shift :' + str(dateshift) + 'day(s)' )

        # time_shift= total_dateshift * 86400
        time_shift= dateshift * 86400 - 86400

        logdef.info('Total dateshift :' + str(time_shift) + 'seconds' )


        for line_obj in output_arr:
            if 'timestamp' in line_obj:
                line_obj["timestamp"]=line_obj["timestamp"]+time_shift

        for line_obj in output_arr:
            if'starttime' in line_obj:
                line_obj["starttime"]=line_obj["starttime"]+time_shift
            if'endtime' in line_obj:
                line_obj["endtime"]=line_obj["endtime"]+time_shift


        # ID =  (configure['userinfo']['devuserid'])
        # output_arr[0]["user"]= ID      

        
        # Target json file generate
        ID =  (configure['userinfo']['devuserid'])
        DEV = (configure['userinfo']['devid'])
        HW = (configure['userinfo']['HW'])
        sn = (configure['userinfo']['sn'])
        MAC = (configure['userinfo']['mac'])
        destinationfile = str(ID)+'-'+str(sn)+'-ANDROID-'+str(time_stamp)+'.json'
        output_arr[0]["user"]= ID
        output_arr[3]['Version'] = HW
        output_arr[4]["Value"]=sn
        output_arr[5]["Value"]= MAC     
        with open(destinationfile, 'w') as f:
            json.dump(output_arr, f)     


                              
class TestAPI(TestAPIWrap):
 
    def test_timeshift_func(self):

        """
        Please modify this address before test script
        """
        logdef.info("####################################################################\n")
        logdef.info("#  PWB API (thrive-ci-usw2-api.data.plume.tech/ #)\n")
        logdef.info("# ---------------------------------------------------------------- #)\n")
        logdef.info("#  Test case : ( Via Timeshift_date / Generate new JSON File #)\n")        
        logdef.info("####################################################################)\n") 
        logdef.info("#####################################")

        PWBFunc().LoadJSONFile()
        

