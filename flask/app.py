from flask import Flask, request, render_template, make_response
import json
from time import time
import graph, alert
import pandas as pd
from datetime import datetime
app = Flask(__name__, static_url_path='/static')

##################### index ###############################
@app.route('/')
@app.route('/setgrasph')
def set_graph():
    #df = pd.read_csv("./test.csv")
    client = alert.get_ifdb()
    graph.delete_db(client)
    alarmList = alert.read(client)

    alarm = []
    if (alarmList.size != 0):
        for i in range(len(alarmList)):
            s = [alarmList['con_name'][i], alarmList['cpu_per'][i], alarmList['mem_usage_MiB'][i], alarmList['net_I_kB'][0]]
            alarm.append(s)


    runconList = graph.get_runconList(client)
    if '--' in runconList:
        runconList.remove('--')

    allconList = alert.get_conList(client)
    if '--' in allconList:
        allconList.remove('--')

    conList = list(set(allconList) - set(runconList))
    runconList.sort()

    cpuser = ""
    for con in runconList:
        cpuser += "{ name : '" + con + "', data : [] } ,"
                
#    milli = round(datetime.utcnow().timestamp()*1000)

    constats = graph.my_test(client)
    index = list()
    for con in runconList:
        index.append(list(constats[con]['time']))

    return render_template('index.html', cpuser=cpuser, runconList = runconList, conList = conList, index = index, alarm = alarm)
    

##################### oooo ###############################

@app.route('/chart')
def chart():
    # html file은 templates 폴더에 위치해야 함
    return render_template('charts.html')



##################### db data json 출력###############################
@app.route('/live-data')
def live_data():
    # Create a PHP array and echo it as JSON
    client = alert.get_ifdb()
    graph.delete_db(client)
    runconList = graph.get_runconList(client)
    if '--' in runconList:
        runconList.remove('--')

    client = alert.get_ifdb()
    constats = graph.my_test(client)

    runconList.sort()
#    index= list(constats['influxdb']['cpu_per'])
    index = list()
    for con in runconList:
        index.append(list(constats[con]['time']))

    data = list()
    now = time()*1000
    for i, con in enumerate(runconList):
        data.append([now, constats[con]])

    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

##################### ooo ###############################

@app.route('/icon')
def icon():
    # html file은 templates 폴더에 위치해야 함
    return render_template('icons.html')


##################### 경고창 형식 ###############################
@app.route('/alarm_action')
def alarmaction():
    client = alert.get_ifdb()
    con_name = request.args.get('con_name')
    cpu_per = request.args.get('cpu_per')
    mem_usage_MiB = request.args.get('mem_usage_MiB')
    net_I_kB = request.args.get('net_I_kB')
    alert.write(client, cpu_per, mem_usage_MiB, net_I_kB, con_name)
    # html file은 templates 폴더에 위치해야 함
    # 정상 리턴을 위해..
    client = alert.get_ifdb()
    alarmList = alert.read(client)
    runconList = alert.get_runconList(client)
    alarmsize = len(alarmList)
    return render_template('alarm.html', alarmsize = alarmsize, alarmList = alarmList, runconList = runconList)

@app.route('/alarm')
def alarm():
    client = alert.get_ifdb()
    alarmList = alert.read(client)
    runconList = alert.get_runconList(client)
    alarmsize = len(alarmList)
    return render_template('alarm.html', alarmsize = alarmsize, alarmList = alarmList, runconList = runconList)


###################################################################
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")









