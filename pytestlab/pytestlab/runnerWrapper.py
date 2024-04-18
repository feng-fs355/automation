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
from pprint import pprint


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

def pretty_print_request_json(request):

    #  body = request.body.replace('true', 'True').replace('false', 'False') # for python2
    #  For python3 as below
    #  Reference : https://stackoverflow.com/questions/33054527/typeerror-a-bytes-like-object-is-required-not-str-when-writing-to-a-file-in
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


def print_request(request):
    logapi.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )
def pretty_print_request(request):
    pprint(request)


def GeneralGet(url, auth=None):

    logging.info(url)
    if auth == None:
        try:
            f_url = 'https://%s%s' % (configure['dut']['ip1'], url)
        except:
            f_url = 'https://%s%s' % (configure['dut']['ip1'], url)
    else:
        try:
            f_url = 'https://%s%s' % (configure['dut']['ip2'], url)
        except:
            f_url = 'https://%s%s' % (configure['dut']['ip2'], url)

    print(f_url)

    # ------------------------------------------------------------------------------------------------------    

    headers = { 'accept': 'application/json',
        'Content-Type': "application/json",
        }

    # send get request
    try:
        resp = requests.get(f_url)
        time.sleep(2)
    except Exception as ex:
        logapi.error('requests.get() failed with exception: %s' % str(ex))
        return None

    try:
        pretty_print_request(resp)
    except:
        print_request(resp)
    return resp.json()


def JSONGet(url, auth=None , query=None):

    logging.info(url)
    if auth == None:
        try:
            f_url = 'https://%s%s' % (configure['dut']['ip1'], url)
        except:
            f_url = 'https://%s%s' % (configure['dut']['ip1'], url)
    if auth != None or query != None:
        try:
            f_url = 'https://%s%s' % (configure['dut']['ip2'], url)
        except:
            f_url = 'https://%s%s' % (configure['dut']['ip2'], url)
    # ------------------------------------------------------------------------------------------------------
    print(f_url)
    headers = {"Accept": "application/json"}

    params1 = {
        "api_key": auth
    }
    params = {
        "api_key": auth,
        "feedtype": 'json',
        "ver": '1.0'
    }
    if auth != None and query == None:
       print(auth)
       # API with Params
       # Send HTTP get
       response = requests.get(f_url,params=params1)
       # return
       data = response.json()
       return data

    if auth != None and query != None:
        # Only for nasa mars weather query
        print(auth)
        # API with Params
        # Send HTTP get
        #f_url = f_url + '/&feedtype=json&ver=1.0'
        response = requests.get(f_url,params=params)
        print(response)
        # return
        data = response.json()
        return data
    if auth == None:
        response = requests.get(f_url, headers=headers)
        if response.status_code == 200:
            # The request was successful
            json_data = response.json()
            return json_data
            #print("JSON response:", json_data)
        else:
            # Handle the error
            print("Error:", response.status_code, response.text)

def telHasText(text, cliOutput):
    for line in cliOutput.split('\n'):
        if re.search(text, line, re.IGNORECASE | re.DOTALL):
            return True
    return False

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