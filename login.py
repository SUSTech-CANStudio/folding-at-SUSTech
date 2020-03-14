#!/usr/bin/python3
from http.client import *
import json
import webbrowser
import uuid
import time

TIMEOUT = 60
# paths
SERVER = "175.24.73.201"
PORT = 80
BASE = "/folding-at-SUSTech-server/src/index.php/api/"
CAS = "login/"
CONFIG = "accessConfiguration/"
# links
CAS_LINK = "http://" + SERVER + BASE + CAS
CONFIG_LINK = "http://" + SERVER + BASE + CONFIG
# connection
CONN = HTTPConnection(SERVER, PORT, 10)

def OpenCAS(hash_code):
    webbrowser.open(CAS_LINK + hex(hash_code))
    
def GetConfig(hash_code):
    CONN.request('GET', BASE + CONFIG + hex(hash_code))
    r = CONN.getresponse()
    content = json.load(r)
    if content['status'] == 'ok':
        return (content['config']['ssh_usr'], content['config']['ssh_pwd'])
    else:
        return False
    
def GetHashCode():
    return hash(uuid.uuid4())
    
if __name__ == "__main__":
    
    hash_code = GetHashCode()
    OpenCAS(hash_code)
    
    start_time = time.time()
    
    while time.time() < start_time + TIMEOUT:
        time.sleep(5)
        config = GetConfig(hash_code)
        if config:
            break
    
    print(config)