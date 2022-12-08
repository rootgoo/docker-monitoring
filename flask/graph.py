import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, time, timedelta
import pprint
from influxdb import InfluxDBClient
from time import sleep

running_con = list()

################################################################################

def my_test(ifdb, t = 1, u = "h"):
    #dt = datetime.now() - timedelta(seconds=6)
    #now_nano = dt.timestamp() * 1000000000
    tablename = 'monitor'
    #sec = 1000000000
    #min = 60 * sec
    #result = ifdb.query('select * from %s where time >= %f' % (tablename, (now_nano - 10*min)))
    DataQ = 'select * from %s where time >= now() - 2200ms' % (tablename)
    #DataQ = 'select * from %s runtime limit 1000' % (tablename, t, u)
    Data = pd.DataFrame(ifdb.query(DataQ, chunked=True, chunk_size=10000).get_points())  # Returns all points

    while(Data.empty):
        Data = pd.DataFrame(ifdb.query(DataQ, chunked=True, chunk_size=10000).get_points())

   
    ifdb.close()
    conList = list(set(Data['con_name']))

 #   Data['time'] = pd.to_datetime(Data['time']) + timedelta(hours=9)

    constats = dict()
    for i,con in enumerate(conList):
        constats[con]= (Data[Data['con_name'] == conList[i]])
    
    for i,con in enumerate(conList):
        constats[con]= constats[con].to_dict()

    #mem_pi(conList, constats)
    return constats

################################################################################

def delete_db(client):
    delmonitor = "delete from monitor where time <= now() - 1m"
    delallcon = "delete from all_container where time <= now() - 1m"
    client.query(delmonitor)
    client.query(delallcon)

##########################################################################################

def get_conList(client):
    query = "select * from all_container where time >= now() - 5m"
    Data = pd.DataFrame(client.query(query, chunked=True, chunk_size=10000).get_points())
    client.close()
    if(Data.empty):
        return list()
    else:
        conList = list(set(Data['con_name']))
        return conList


def get_runconList(client):
    query = "select * from monitor where time >= now() - 5m"
    Data = pd.DataFrame(client.query(query, chunked=True, chunk_size=10000).get_points())
    client.close()
    if(Data.empty):
        return list()
    else:
        runconList = list(set(Data['con_name']))
        return runconList

##########################################################################################

# def get_ifdb(db='easythem', host='localhost', port=8086, user='user01', passwd='password'):
#     client = InfluxDBClient(host, port, user, passwd, db)
#     try:
#         client.create_database(db)
#     except:
#         pass
#     return client

# ##########################################################################################
# def mem(conList, constats):
#     plt.figure(figsize=(25,10))
#     plt.rcParams['font.size'] = 8
    
#     xs = np.array(constats[conList[0]].minute.tolist())
#     for con in conList:
#         plt.plot(constats[con].minute, constats[con].mem_usage_MiB, "-", label=con)

# #    plt.plot(mem_usage_MiB.index, mem_usage_MiB, "-",label="total")
#     plt.legend(fontsize=8)
#     plt.yticks(np.arange(0,200,5)) 
#     plt.xticks(xs, rotation=45)
#     plt.locator_params(axis='x', nbins=len(xs)/25)
#     plt.grid()
#     plt.xlabel("1 hour graph")
#     plt.ylabel("MiB")
#     plt.title("mem_usage_MiB")
#     plt.show()

# ##########################################################################################
# def mem_pi(conList, constats):

#     plt.figure(figsize=(25,10))
#     plt.rcParams['font.size'] = 12

#     ratio=[]
#     label = conList
#     for con in conList:
#         ratio.append(constats[con].mem_per.values.mean())
#     ratio.append(100 - sum(ratio))
#     label.append("remain")
#     plt.pie(ratio,labels=label,autopct='%1.1f%%')
#     plt.title('Memory Usage')
#     plt.show()

# ##########################################################################################
# def cpu(conList, constats):
#     plt.figure(figsize=(25,10))
#     plt.rcParams['font.size'] = 8
    
#     xs = np.array(constats[conList[0]].minute.tolist())
#     for con in conList:
#         plt.plot(constats[con].minute, constats[con].cpu_per, "-", label=con)

#     plt.legend(fontsize=8)
#     plt.yticks(np.arange(0,200,5))    
#     plt.xticks(xs, rotation=45)
#     plt.locator_params(axis='x', nbins=len(xs)/25)
#     plt.grid()
#     plt.xlabel("1 hour graph")
#     plt.ylabel("%")
#     plt.title("cpu%")
#     plt.show()
 
# ##########################################################################################
# def blockIO(constats, conname="influxdb"):    
#     plt.figure(figsize=(25,10))
#     plt.rcParams['font.size'] = 8
    
#     xs = np.array(constats[conname].minute.tolist())
#     plt.plot(constats[conname].minute, constats[conname].Block_I_MB, "-", label="in")
#     plt.plot(constats[conname].minute, constats[conname].Block_O_MB, "-", label="out")

#     plt.legend(fontsize=8)
#     plt.yticks(np.arange(0,1000,50))
#     plt.xticks(xs, rotation=45)
#     plt.locator_params(axis='x', nbins=len(xs)/25)
#     plt.grid(1)
#     plt.xlabel("1 hour graph")
#     plt.ylabel("MB")
#     plt.title("Block I/O")
#     plt.show()
    
    

# ##########################################################################################

# #def netIO(conList, constats, conname="influxdb"):
# def netIO(constats, conname="influxdb"):
#     plt.figure(figsize=(25,10))
#     plt.rcParams['font.size'] = 8

#     xs = np.array(constats[conname].minute.tolist())
#     plt.plot(constats[conname].minute, constats[conname].net_I_kB, "-", label="in")
#     plt.plot(constats[conname].minute, constats[conname].net_O_kB, "-", label="out")

#     plt.legend(fontsize=8)
#     plt.yticks(np.arange(0,1000,50))
#     plt.xticks(xs, rotation=45)
#     plt.locator_params(axis='x', nbins=len(xs)/25)
#     plt.grid()
#     plt.xlabel("1 hour graph")
#     plt.ylabel("KB")
#     plt.title("Net I/O")
#     plt.show()

##########################################################################################

