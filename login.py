#!/usr/bin/python3
import json
import time
import hashlib
import requests
import os
import re
from keygenerator import *

# paths
NB_URL = "https://folding-api.citric-acid.zzwcdn.com/url.json"
res = requests.get(NB_URL).json()
global API_LOGIN
global API_GET_CONFIG
API_LOGIN = res["api_login"]
API_GET_CONFIG = res["api_get_config"]

def Login(username : str, password : str, hash_code : str) -> bool:
    '''
    Login the SUSTech CAS.
    
    :param username: CAS user name.
    
    :param password: CAS password.
    
    :param hash_code: unique hashcode generated from `GetHashCode(username)`
    
    :return: succeed or not.
    '''
    global API_LOGIN
    url = API_LOGIN
    usr_info = {"username" : username, "password" : password, "key" : hash_code}
    data = {"usr_info" : json.dumps(usr_info)}
    res = requests.post(url=url, data=data)
    if not res.text:
        return True
    else:
        # print(res.text)
        return False
    
def GetConfig(hash_code : str, logger, time_out = 60, retry = 5) -> str:
    '''
    Get configution by hash code.
    
    :param hash_code: the same hash code as login.
    
    :param time_out: time limit (seconds) for this action.
    
    :param retry: sleep time after failed once (seconds).
    
    :return: configution of TunSafe. If failed, return false.
    '''
    start_time = time.time()
    
    print('正在拉取配置信息...')
    logger.debug("Pulling config info...")
    while time.time() < start_time + time_out:
        global API_GET_CONFIG
        url = API_GET_CONFIG + hash_code
        print(url)
        res = requests.get(url)
        content = res.json()
        logger.debug('status: {}'.format(content['status']))
        if content['status'] == 'ok':
            return content['config']
        time.sleep(retry)
    
    return False
    
def GetHashCode(username : str) -> str:
    '''
    Generate a new hash code.
    
    :param username: CAS user name.
    
    :return: hash code.
    '''
    plain = '{}-{}'.format(username, time.time)
    return hashlib.sha256(plain.encode()).hexdigest()
    
def WriteConfig(config : str):
    '''
    Write configution to file.
    
    :param config: configuation get from `GetConfig(hash_code)`
    '''
    # replace the public & private keys in the config
    # (private_key, public_key) = get_key_pair('./TunSafe/')
    # config = re.sub('PrivateKey[ ]*=[ ]*[^ ]+\n', 'PrivateKey = {}\n'.format(private_key), config)
    # config = re.sub('PublicKey[ ]*=[ ]*[^ ]+\n', 'PublicKey = {}\n'.format(public_key), config)
    conf = open("./TunSafe/Config/SUSTech.conf", 'w')
    conf.write(config)
    conf.close()
    