#!/usr/bin/python3
import json
import time
import hashlib
import requests
import os
import re
from keygenerator import *

# paths
SERVER = "175.24.73.201"
PORT = 80
BASE = "/folding-at-SUSTech-server/src/index.php/api/"
LOGIN = "login"
CONFIG = "accessConfiguration/"

def Login(username : str, password : str, hash_code : str) -> bool:
    '''
    Login the SUSTech CAS.
    
    :param username: CAS user name.
    
    :param password: CAS password.
    
    :param hash_code: unique hashcode generated from `GetHashCode(username)`
    
    :return: succeed or not.
    '''
    url = "http://" + SERVER + BASE + LOGIN
    usr_info = {"username" : username, "password" : password, "key" : hash_code}
    data = {"usr_info" : json.dumps(usr_info)}
    res = requests.post(url=url, data=data)
    if not res.text:
        return True
    else:
        print(res.text)
        return False
    
def GetConfig(hash_code : str, time_out = 60, retry = 5) -> str:
    '''
    Get configution by hash code.
    
    :param hash_code: the same hash code as login.
    
    :param time_out: time limit (seconds) for this action.
    
    :param retry: sleep time after failed once (seconds).
    
    :return: configution of TunSafe. If failed, return false.
    '''
    start_time = time.time()
    
    print('getting config...')
    while time.time() < start_time + time_out:
        res = requests.get("http://" + SERVER + BASE + CONFIG + hash_code)
        content = res.json()
        print(content['status'])
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
    (private_key, public_key) = get_key_pair('./TunSafe/')
    print(config)
    config = re.sub('PrivateKey[ ]*=[ ]*[^ ]+\n', 'PrivateKey = {}\n'.format(private_key), config)
    config = re.sub('PublicKey[ ]*=[ ]*[^ ]+\n', 'PublicKey = {}\n'.format(public_key), config)
    conf = open("./TunSafe/Config/SUSTech.conf", 'w')
    print("---------------------------------")
    print(config)
    conf.write(config)
    conf.close()
    
    
def Test():
    
    # Get user name and password
    username = input('username: ')
    password = input('password: ')
    # Generate hash code
    hash_code = GetHashCode(username)
    
    # Try login
    while not Login(username, password, hash_code):
        print('Wrong user name or password.')
        username = input('username: ')
        password = input('password: ')
    
    # Get configution
    config = GetConfig(hash_code)
    
    if not config:
        print('Failed to get config file.')
    else:
        WriteConfig(config)
        print('Write config successfully.')
    
if __name__ == "__main__":
    Test()