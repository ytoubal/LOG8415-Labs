from datetime import datetime
from datetime import timedelta
import json
import requests
import boto3

def consumeGETRequestSync(cluster):

    clientCrt = ""
    clientKey = ""
    url_cluster1 = "http://test12-2135488930.us-east-1.elb.amazonaws.com"  
    url_cluster2 = "http://testcluster2-1696725025.us-east-1.elb.amazonaws.com"
    url = url_cluster1 if cluster == 1 else url_cluster2
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

def runScenario1():
    #scenario 1
    #for i in range(1000):
    consumeGETRequestSync(cluster=1)

def runScenario2():
    #scenario 2
    #for i in range(500):
        #time.sleep(60)
    #for i in range(1000):
    consumeGETRequestSync(cluster=2)

#get load balancer 
def getLoadBalancerInfos():
    response = cloudwatch.list_metrics(Namespace= 'AWS/ApplicationELB', MetricName= 'NewConnectionCount', Dimensions=[
        {
            'Name': 'LoadBalancer',
        },
    ])

    cluster1 = findELBValue(response["Metrics"], 1)
    cluster2 = findELBValue(response["Metrics"], 2)
    #print(json.dumps(response, indent=4, sort_keys=True, default=str))
    return (cluster1['Name'], cluster1['Value'], cluster2['Name'], cluster2['Value'])

def getTargetGroupInfos():
    response = cloudwatch.list_metrics(Namespace= 'AWS/ApplicationELB', MetricName= 'NewConnectionCount', Dimensions=[
        {
            'Name': 'LoadBalancer',
        },
    ])

    cluster1 = findELBValue(response["Metrics"], 1)
    cluster2 = findELBValue(response["Metrics"], 2)
    #print(json.dumps(response, indent=4, sort_keys=True, default=str))
    return (cluster1['Name'], cluster1['Value'], cluster2['Name'], cluster2['Value'])

def findELBValue(responses, n_cluster):
    keyword = "test12" if n_cluster == 1 else "testcluster2"
    for response in responses:
        dimension = response["Dimensions"][0]
        value = dimension["Value"]
        if keyword in value:
            return dimension
    return None
#
def constructQuery():
    name_c1, value_c1, name_c2, value_c2 = getLoadBalancerInfos()
    metric_query = []
    constructMetricQuery(metric_query, name_c1, value_c1, '1')
    constructMetricQuery(metric_query, name_c2, value_c2, '2')
    return metric_query

def constructMetricQuery(metric_query, name, value, n_cluster):
    for metric in metrics_elb:
        metric_query.append({
                'Id': metric.lower() + n_cluster,
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/ApplicationELB',
                        'MetricName': metric,
                        "Dimensions": [
                        {
                            'Name': name,
                            'Value': value
                        }
                        ],
                    },
                    'Period': 120,
                    'Stat': 'Sum',
                }
            })

runScenario1()
runScenario2()

#CloudWatch
cloudwatch = boto3.client('cloudwatch')

#list of metrics 
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.list_metrics
metrics_elb = ['TargetResponseTime', 'RequestCount', 'HTTPCode_ELB_5XX_Count', 'HTTPCode_ELB_503_Count', 'HTTPCode_Target_2XX_Count', 'ActiveConnectionCount', 'NewConnectionCount', 'ProcessedBytes', 'ConsumedLCUs']

data_response = cloudwatch.get_metric_data(MetricDataQueries=constructQuery(),
    StartTime=datetime.utcnow() - timedelta(minutes=120),
    EndTime=datetime.utcnow())

data_set = data_response["MetricDataResults"]
size_cluster_data = int(len(data_set)/2)
data_cluster1 = data_set[:size_cluster_data]
data_cluster2 = data_set[size_cluster_data:]
#print(json.dumps(data_cluster1, indent=4, sort_keys=True, default=str))

import pandas as pd
import matplotlib.pyplot as plt
metrics_data = data_set
plt.rcParams["figure.figsize"] = 10,5
for i in range(len(metrics_data)):
    data_dict = metrics_data[i]
    metrics_label = data_dict.get('Label').split()[1]
    my_data = pd.DataFrame.from_dict(data_dict)[["Timestamps","Values"]]
    # Parse strings to datetime type
    my_data["Timestamps"] = pd.to_datetime(my_data["Timestamps"], infer_datetime_format=True)
    #my_data.plot(x="Timestamps", y=["Values","Values_for_C2"])
    my_data.plot(x="Timestamps", y="Values")
    plt.title(metrics_label)
    #plt.ylabel("Values")
    # plt.show()


    # ax = s.hist()  # s is an instance of Series
    # fig = ax.get_figure()
    plt.savefig(f'{metrics_label}')