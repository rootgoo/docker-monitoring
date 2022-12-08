import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta
import pprint
from influxdb import InfluxDBClient
from time import sleep

def get_ifdb(db='easythem', host='localhost', port=8086, user='user01', passwd='password'):
    client = InfluxDBClient(host, port, user, passwd, db)
    try:
        client.create_database(db)
    except:
        pass
    return client

def write(client, cpu_per, mem_usage_MiB, net_I_kB, con_name):
    alertData = pd.DataFrame(client.query("select * from alert", chunked=True, chunk_size=10000).get_points())
    if(alertData.empty):
        line='alert,con_name=%s cpu_per=%s,mem_usage_MiB=%s,net_I_kB=%s' % (con_name,cpu_per,mem_usage_MiB, net_I_kB)
        client.write([line],{'db':'easythem'},204,'line')
        client.close()
    else:
        alertList = list(set(alertData["con_name"]))
        for i in alertList:
            if(con_name == i):
                q = "delete from alert where con_name = '%s'" %(i)
                client.query(q)
                break
        line='alert,con_name=%s cpu_per=%s,mem_usage_MiB=%s,net_I_kB=%s' % (con_name,cpu_per,mem_usage_MiB, net_I_kB)
        client.write([line],{'db':'easythem'},204,'line')
        client.close()

def read(client):
    alertData = pd.DataFrame(client.query("select * from alert", chunked=True, chunk_size=10000).get_points())
    client.close()
    # alertData.empty 확인하기
    return alertData


##########################################################################################

def get_runconList(client):
    query = "select * from monitor where time >= now() - 5m"
    Data = pd.DataFrame(client.query(query, chunked=True, chunk_size=10000).get_points())
    client.close()
    if(Data.empty):
        return list()
    else:
        runconList = list(set(Data['con_name']))
        return runconList


def get_conList(client):
    query = "select * from all_container where time >= now() - 5m"
    Data = pd.DataFrame(client.query(query, chunked=True, chunk_size=10000).get_points())
    client.close()
    if(Data.empty):
        return list()
    else:
        conList = list(set(Data['con_name']))
        return conList


def read_csv():
    return pd.read_csv("./test.csv")