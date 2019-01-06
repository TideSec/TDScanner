import threading
import time

import mysql
from flask import json

from urls_to_sqlmapapi import creat_task,run_server,viewtask,viewdata,task_start,get_status
from save_to_mysql import addtask, adtasklog


def savelog(id):
    while True:
        ret = get_status(id)
        jdata = json.loads(ret)
        status = str(jdata['status'])
        if status == 'terminated':
            log = viewtask(id)
            data = viewdata(id)
            adtasklog(id, log, data)
        else:
            log = "Sqlmap is running,please wait for a moment!"
            print log
        time.sleep(30)


    # conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    # cur=conn.cursor()
    # sql = "select * from sqlmaptask_info where taskid = '{}'".format(id)
    # cur.execute(sql)
    # result_infos = cur.fetchone()
    # if result_infos:
    #     id = result_infos[0]
    #     log = result_infos[1]
    #     data = result_infos[2]
    #else:

    #cur.close()

def start(siteid,url):
    #run_server()
    #print "ok"
    taskid = creat_task()
    task_start(taskid,url)
    addtask(siteid,taskid,url)
    try:
        savelog_t = threading.Thread(target=savelog,args=(taskid,))
        savelog_t.start()
    except Exception as e:
        print(e)

#start('asd1s','http://10.211.55.2/index.php?222=phpinfo')
#start('http://61.158.99.152/zzcx/search_sgxkz.jsp?xid=200705240303575851&workAction=Init')