from datetime import datetime
import json
import requests
import time 
import boto3

def consumeGETRequestSync():

    clientCrt = ""
    clientKey = ""
    url = "http://cluster1-2146860487.us-east-1.elb.amazonaws.com" #changer le url
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

# cloudwatch = boto3.resource('cloudwatch')
# metric = cloudwatch.Metric('namespace','name')
cloudwatch = boto3.client('cloudwatch')
response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'string',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'string',
                    'MetricName': 'string',
                    'Dimensions': [
                        {
                            'Name': 'string',
                            'Value': 'string'
                        },
                    ]
                },
                'Period': 123,
                'Stat': 'string',
                'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
            },
            'Expression': 'string',
            'Label': 'string',
            'ReturnData': True|False,
            'Period': 123,
            'AccountId': 'string'
        },
    ],
    StartTime=datetime(2021, 10, 3),
    EndTime=datetime(2021, 10, 4),
)
#scenario 2
#for i in range(500):
#time.sleep(60)
#for i in range(1000):
consumeGETRequestSync()
