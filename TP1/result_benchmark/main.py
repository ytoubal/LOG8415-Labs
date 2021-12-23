from datetime import datetime 
from datetime import timedelta
import time
import requests
import boto3
import pandas as pd
import matplotlib.pyplot as plt

def consumeGETRequestSync(cluster):

    clientCrt = ""
    clientKey = ""
    url_cluster1 = "http://alb-1-2039841016.us-east-1.elb.amazonaws.com/"  
    url_cluster2 = "http://alb-2-1568179889.us-east-1.elb.amazonaws.com/"
    url = url_cluster1 if cluster == 1 else url_cluster2
    certServer = ""
    headers = { "Accept": "application/json" }
    r = requests.get(url,
    verify=certServer,
    headers=headers,
    cert =(clientCrt, clientKey) )

def runScenario1():
    #scenario 1
    for _ in range(50):
        consumeGETRequestSync(cluster=1)
        #consumeGETRequestSync(cluster=2)

def runScenario2():
    #scenario 2
    for _ in range(150):
        #consumeGETRequestSync(cluster=1)
        consumeGETRequestSync(cluster=2)
    #time.sleep(60)
    #for _ in range(1000):
        #consumeGETRequestSync(cluster=1)
        #consumeGETRequestSync(cluster=2)

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
    #print(json.dumps(response, indent=4, sort_keys=True, default=str))
    return (cluster1['Name'], cluster1['Value'], cluster2['Name'], cluster2['Value'])

def findNameValue(responses, n_cluster, type_dimension):
    keyword_elb = "app/ALB-" + ("1/" if n_cluster == 1 else "2/")
    keyword_tg = "targetgroup/Cluster" + ("1/" if n_cluster == 1 else "2/")
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

def generateGraphs(data_cluster1, data_cluster2):
    plt.rcParams["figure.figsize"] = 10,5
    for i in range(len(data_cluster1)):
        data1_dict = data_cluster1[i]
        data2_dict = data_cluster2[i]
        # retrieving the metrics label
        metrics_label = data1_dict.get('Label').split()[1]
        # Convert dictionnary data into pandas
        my_data1 = pd.DataFrame.from_dict(data1_dict)[["Timestamps","Values"]]
        my_data1.rename(columns={'Values': 'Cluster1'}, inplace=True)
        my_data2 = pd.DataFrame.from_dict(data2_dict)[["Timestamps","Values"]]
        # Renanme columns
        my_data2.rename(columns={'Values': 'Cluster2'}, inplace=True)
        # Parse strings to datetime type
        my_data1["Timestamps"] = pd.to_datetime(my_data1["Timestamps"], infer_datetime_format=True)
        my_data2["Timestamps"] = pd.to_datetime(my_data2["Timestamps"], infer_datetime_format=True)
        if (len(my_data1)!=0 and len(my_data2)!=0):
            plt.xlabel("Timestamps")
            plt.plot("Timestamps", "Cluster1", color="red", data=my_data1)
            plt.plot("Timestamps", "Cluster2", color="green", data=my_data2)
            plt.title(metrics_label)
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            plt.legend(by_label.values(), by_label.keys())
            plt.savefig(f"images/{metrics_label}")      
            

runScenario1()
runScenario2()

#CloudWatch
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1',
                            aws_access_key_id="AKIAV3ACVM46KNZW4U4A",
                            aws_secret_access_key="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")
                            #aws_session_token="FwoGZXIvYXdzEGQaDNeMUCKRhKWTa3oXlSLHAf8w2AppOqF7znHqhT+oH5MnctlMqVHtoMf184fsFbkP7D2IE7mULT3q+sjQ2ONibGlwWs6vEsYc1fsjstVC40s5M19rxkfhf/7HPVppJsSCSIEmxzf0DXwiHqEfOC0sDsLpSloCMWse+IhvHlDui/fxlUByiRlTYPdF9qbjM7uOMrpfMDMEEXF6+7dc7N9mLhYkal4CjvGbOm/8PxeRr5clIJ8IAafb4obJXgi1t9j3YPVrrWTW9PJAEJjsrtvXGAfTaokCyVso56mJiwYyLZliNNAthHHufBW59oTelnqn3/jWiTqT0yxEtGrtJjdz41iEPlhK9t+BVny7cg==")


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

generateGraphs(data_cluster1, data_cluster2)

