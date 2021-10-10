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
def getDimensionInfos(type_dimension):
    name = 'LoadBalancer' if type_dimension == 'ELB' else 'TargetGroup'
    response = cloudwatch.list_metrics(Namespace= 'AWS/ApplicationELB', MetricName= 'RequestCount', Dimensions=[
        {
            'Name': name,
        },
    ])

    cluster1 = findNameValue(response["Metrics"], 1, type_dimension)
    cluster2 = findNameValue(response["Metrics"], 2, type_dimension)
    print(cluster1)
    print(cluster2)
    #print(json.dumps(response, indent=4, sort_keys=True, default=str))
    return (cluster1['Name'], cluster1['Value'], cluster2['Name'], cluster2['Value'])

def findNameValue(responses, n_cluster, type_dimension):
    keyword_elb = "app/" + ("test12/" if n_cluster == 1 else "testcluster2/")
    keyword_tg = "targetgroup/" + ("test1/" if n_cluster == 1 else "testcluster2/")
    keyword = keyword_elb if type_dimension == "ELB" else keyword_tg
    for response in responses:
        dimension = response["Dimensions"][0]
        value = dimension["Value"]
        if keyword in value:
            return dimension
    return None
#
def constructQuery():
    name_c1_tg, value_c1_tg, name_c2_tg, value_c2_tg =  getDimensionInfos("TG")
    name_c1, value_c1, name_c2, value_c2 =  getDimensionInfos("ELB")
    metric_query = []
    #ELB metrics Cluster1
    constructMetricQuery(metric_query, metrics_elb, name_c1, value_c1, '1')
    #ELB metrics Cluster2
    constructMetricQuery(metric_query, metrics_elb, name_c2, value_c2, '2')
    #TargetGroup metrics Cluster1
    constructMetricQuery(metric_query, metrics_tg, name_c1_tg, value_c1_tg, '1')
    #TargetGroup  metrics Cluster2
    constructMetricQuery(metric_query, metrics_tg, name_c2_tg, value_c2_tg, '2')
    return metric_query

def constructMetricQuery(metric_query, metrics, name, value, n_cluster):
    for metric in metrics:
        metric_query.append({
                'Id': metric.lower() + name + n_cluster,
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

metrics_tg = ['UnHealthyHostCount', 'HealthyHostCount', 'TargetResponseTime', 'RequestCount', 'HTTPCode_Target_4XX_Count', 'HTTPCode_Target_2XX_Count', 'RequestCountPerTarget']

data_response = cloudwatch.get_metric_data(MetricDataQueries=constructQuery(),
    StartTime=datetime.utcnow() - timedelta(minutes=120),
    EndTime=datetime.utcnow())

data_set = data_response["MetricDataResults"]

data_elb_cluster1 = data_set[:len(metrics_elb)] # 0 to len(metrics_elb)-1
data_elb_cluster2 = data_set[len(metrics_elb):len(metrics_elb)*2] # len(metrics_elb) to len(metrics_elb)
data_tg_cluster1 = data_set[len(metrics_elb)*2:len(metrics_elb)*2+len(metrics_tg)]  # 0 to len(metrics_elb)
data_tg_cluster2 = data_set[len(metrics_elb)*2+len(metrics_tg):] # 0 to len(metrics_elb)
data_cluster1 = data_elb_cluster1 + data_tg_cluster1
data_cluster2 = data_elb_cluster2 + data_tg_cluster2

print(json.dumps(data_tg_cluster1, indent=4, sort_keys=True, default=str))

import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = 10,5
for i in range(len(data_cluster1)):
    data1_dict = data_cluster1[i]
    data2_dict = data_cluster2[i]
    metrics_label = data1_dict.get('Label').split()[1]
    my_data1 = pd.DataFrame.from_dict(data1_dict)[["Timestamps","Values"]]
    my_data1.rename(columns={'Values': 'Cluster1'}, inplace=True)
    my_data2 = pd.DataFrame.from_dict(data2_dict)[["Timestamps","Values"]]
    my_data2.rename(columns={'Values': 'Cluster2'}, inplace=True)
    # Parse strings to datetime type
    my_data1["Timestamps"] = pd.to_datetime(my_data1["Timestamps"], infer_datetime_format=True)
    my_data2["Timestamps"] = pd.to_datetime(my_data2["Timestamps"], infer_datetime_format=True)
    #merge_data = pd.concat([my_data1,my_data2])
    if (len(my_data1)!=0 and len(my_data2)!=0):
        #my_data1.plot(x="Timestamps", y="Cluster1")
        #my_data2.plot(x="Timestamps", y="Cluster2")
        #ax = my_data1.plot(y="Cluster1")
        #my_data2.drop("Timestamps",axis=1).plot(ax=ax)
        #merge_data.plot(x="Timestamps", y=["Cluster1","Cluster2"])
        fig=plt.figure()
        ax=fig.add_subplot(111, label="1")
        ax.legend()
        ax2=fig.add_subplot(111, label="2", frame_on=False)
        ax2.legend()

        ax.plot(my_data1["Timestamps"], my_data1["Cluster1"], color="C0", label="Cluster1")
        ax.set_xlabel("x label 1", color="C0")
        ax.set_ylabel("y label 1", color="C0")

        ax2.plot(my_data2["Timestamps"], my_data2["Cluster2"], color="C3", label="Cluster2")
        ax2.set_xticks([])
        ax2.set_yticks([])

        plt.legend()
        plt.title(metrics_label)
        #plt.xlabel("Timestamps")
        plt.savefig(f'{metrics_label}')