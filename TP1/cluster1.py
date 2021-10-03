import json
import requests
import time 

def consumeGETRequestSync():

    clientCrt = ""
    clientKey = ""
    url = "http://cluster1-2146860487.us-east-1.elb.amazonaws.com/" #changer le url
    certServer = ""
    headers = { "Accept": "application/json" }
    r = requests.get(url,
    verify=certServer,
    headers=headers,
    cert =(clientCrt, clientKey) )
    print(r.status_code)
    print("******************")
    print("headers:"+ str(r.headers))
    print("******************")
    print("content:"+ str(r.text))

#scenario 1
#for i in range(1000):
consumeGETRequestSync()

#scenario 2
#for i in range(500):
time.sleep(60)
#for i in range(1000):
consumeGETRequestSync()
