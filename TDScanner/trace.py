# coding:utf-8

import sys
import json
import time
import mysql.connector
from flask import Flask, render_template, Blueprint, g, request, send_from_directory
from site_info_collect import runscan
from playsqlmap import start
from save_to_mysql import checkurl
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

app = Blueprint("trace", __name__)
'''
@app.before_request
def before_request():
    g.conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    g.cur=g.conn.cursor()


@app.teardown_request
def tear_down(response):
    g.conn.close()
    return response
'''


@app.route("/trace", methods=['GET', 'POST'])
def trace():

    try:
        result_infos = {}
        target = request.form["target"]
        target_urllist, iplist, collect_dirs, collect_ports, subdomain ,hashid = runscan(target)

        # urla = checkurl(target)
        # id = hashlib.md5()
        # id.update(urla)
        # siteid = id.hexdigest()
        # print "sql_hash:" + siteid

        #print hashid

        for url in target_urllist[0:10:1]:
            print "checksql_url：",url
            start(hashid, url)
            time.sleep(0.3)
    except:
        pass


    # print "target:",target
    # print "target_urllist:",target_urllist
    # print "iplist:",iplist
    # print collect_dirs
    # print collect_ports
    # print subdomain

    #target_urllist, iplist, collect_dirs, collect_ports, subdomain = 'abc', 'abc', 'abc', 'abc', 'abc'

    return render_template("trace.html", target=target, target_urllist=target_urllist, iplist=iplist,
                           collect_dirs=collect_dirs, collect_ports=collect_ports, subdomain=subdomain)

# return render_template("trace.html")
