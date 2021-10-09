from datetime import datetime
from datetime import timedelta
import json
import requests
import boto3

def consumeGETRequestSync():

    clientCrt = ""
    clientKey = ""
    url = "http://test12-2135488930.us-east-1.elb.amazonaws.com" #changer le url
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
response = cloudwatch.list_metrics(Namespace= 'AWS/ApplicationELB', MetricName= 'RequestCount')
last_dimension = response["Metrics"][len(response["Metrics"])-1] ["Dimensions"]
name = last_dimension[0] ['Name']
value = last_dimension[0] ['Value']

data_response = cloudwatch.get_metric_data(MetricDataQueries=[
        {
            'Id': 'testffd',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/ApplicationELB',
                    'MetricName': 'RequestCount',
                    "Dimensions": [
                {
                    'Name': name,
                    'Value': value
                }
            ],
                },
                'Period': 120,
                'Stat': 'Sum',
            },
        },
    ],
    StartTime=datetime.utcnow() - timedelta(minutes=120),
    EndTime=datetime.utcnow())
data_set = zip(data_response["MetricDataResults"][0]["Timestamps"], data_response["MetricDataResults"][0]["Values"])
#print(data_set)
print(json.dumps(list(data_set), indent=4, sort_keys=True, default=str))
