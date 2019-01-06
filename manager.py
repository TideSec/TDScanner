#coding:utf-8

import os
import sys

import time
from flask import Flask, render_template, Blueprint, g, request
import json
import mysql.connector
from playsqlmap import get_status,viewdata,viewtask
from save_to_mysql import adtasklog
import socket
from net_explore import netmain
app = Blueprint("address_manager", __name__)



@app.route("/manager", methods = ["GET",'POST'])
def get_info():
    conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    cur=conn.cursor()
    sql = "select id,url from target_baseinfo"
    cur.execute(sql)
    result_infos = cur.fetchall()
    #print result_infos
    reload(sys)
    sys.setdefaultencoding('utf-8')
    cur.close()
    return render_template("manager.html", result_infos = result_infos)


@app.route("/view/<id>", methods=["GET",'POST'])
def view(id):
    conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    cur=conn.cursor()
    sql = "select * from target_baseinfo where id = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchone()

    reload(sys)
    sys.setdefaultencoding('utf-8')
    cur.close()
    target_urllist = result_infos[2]
    print type(target_urllist)
    # return render_template("view.html",result_infos = result_infos)
    # target = result_infos[0]
    return render_template("view.html", result_infos = result_infos,target=result_infos[1], id=result_infos[0],target_urllist=result_infos[2], iplist=result_infos[3],
                           collect_dirs=result_infos[4], collect_ports=result_infos[5], subdomain=result_infos[6])

@app.route("/checksqli/<id>", methods=["GET",'POST'])
def checksqli(id):
    conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    cur=conn.cursor()
    sql = "select * from sqlmaptask where siteid = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchall()
    reload(sys)
    sys.setdefaultencoding('utf-8')


    return render_template("checksqli.html",result_infos = result_infos)
    cur.close()

@app.route("/dellog/<id>", methods=["GET",'POST'])
def dellog(id):
    conn = mysql.connector.connect(user='root', password='123456', host='localhost', database='TDScan')
    cur = conn.cursor()
    sql = "delete from target_baseinfo where id = '{}'".format(id)
    cur.execute(sql)

    cur.close()
    # return render_template("manager.html", result_infos=result_infos)
    conn2=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    cur2=conn2.cursor()
    sql2 = "select id,url from target_baseinfo"
    cur2.execute(sql2)
    result_infos2 = cur2.fetchall()
    #print result_infos
    reload(sys)
    sys.setdefaultencoding('utf-8')
    cur.close()
    return render_template("manager.html", result_infos = result_infos2)


@app.route("/getlog/<id>", methods=["GET",'POST'])
def getlog(id):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    cur=conn.cursor()
    sql = "select * from sqlmaptask_info where taskid = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchone()
    if result_infos:
        id = result_infos[0]
        log = result_infos[1]
        data = result_infos[2]
    else:
        ret = get_status(id)
        jdata = json.loads(ret)
        status = str(jdata['status'])
        if status == 'terminated':
            log = viewtask(id)
            data = viewdata(id)
            adtasklog(id,log,data)
        else:
            log = "Sqlmap is running,please wait for a moment!"
            data = "None"
    return render_template("getlog.html",id=id,log = log,data=data)
    cur.close()

@app.route("/netexplore/<url>", methods=["GET",'POST'])
def netexplore(url):
    #url = id
    try:
        addr = socket.getaddrinfo(url, 'http')[0][4][0]
        netmain(addr)
        # print os.getcwd()
        f = open('./netlog/' + addr + '.txt', 'r')
        alllines = f.readlines()
        f.close()
        #time.sleep(15)
    except:
        pass

    return render_template("netlist.html",alllines=alllines)

'''
@app.route("/inject/<id>", methods=["GET",'POST'])
def view(id):
    conn=mysql.connector.connect(user='root',password='pass',host='localhost',database='TDScan')
    cur=conn.cursor()
    sql = "select collect_urls from target_baseinfo where id = '{}'".format(id)
    cur.execute(sql)
    result_infos = cur.fetchone()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    cur.close()
'''

