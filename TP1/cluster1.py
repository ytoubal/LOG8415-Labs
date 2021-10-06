from datetime import datetime
import json
import re
import requests
import time 
import boto3

def consumeGETRequestSync():

    clientCrt = ""
    clientKey = ""
    url = "http://test-2074630864.us-east-1.elb.amazonaws.com" #changer le url
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
#time.sleep(60)
#for i in range(1000):
#consumeGETRequestSync()

#CloudWatch
# cloudwatch = boto3.resource('cloudwatch')
# metric = cloudwatch.Metric('namespace','name')
cloudwatch = boto3.client('cloudwatch')

#list of metrics 
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.list_metrics
response = cloudwatch.list_metrics(Namespace= 'AWS/ApplicationELB')

print(json.dumps(response, indent=4, sort_keys=True))