#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import Queue
import socket
import threading
from threading import Thread
import time
import re
import os
import sys
import subprocess
import urllib2
import urllib

os_char = 'utf-8'

# PORT = {80: "web", 8080: "web", 3311: "kangle主机管理系统", 3312: "kangle主机管理系统", 3389: "远程登录", 4440: "rundeck是用java写的开源工具",
#         5672: "rabbitMQ", 5900: "vnc", 6082: "varnish", 7001: "weblogic", 8161: "activeMQ", 8649: "ganglia",
#         9000: "fastcgi", 9090: "ibm", 9200: "elasticsearch", 9300: "elasticsearch", 9999: "amg", 10050: "zabbix",
#         11211: "memcache", 27017: "mongodb", 28017: "mondodb", 3777: "大华监控设备", 50000: "sap netweaver", 50060: "hadoop",
#         50070: "hadoop", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns", 123: "ntp", 161: "snmp",
#         8161: "snmp", 162: "snmp", 389: "ldap", 443: "ssl", 512: "rlogin", 513: "rlogin", 873: "rsync", 1433: "mssql",
#         1080: "socks", 1521: "oracle", 1900: "bes", 2049: "nfs", 2601: "zebra", 2604: "zebra", 2082: "cpanle",
#         2083: "cpanle", 3128: "squid", 3312: "squid", 3306: "mysql", 4899: "radmin", 8834: 'nessus', 4848: 'glashfish'}
PORT = {80: "web"}
#PORT = {80: "web"}

global queue


# ip to num
def urlip(ip):
    apiurl = "http://www.gpsspg.com/ip/?q=%s" % ip
    content = urllib2.urlopen(apiurl).read()
    reli = re.findall(u'<span class="fcg">(.*?)</span>', content)
    return reli


def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

# num to ip
def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,
                            (num & 0x00ff0000) >> 16,
                            (num & 0x0000ff00) >> 8,
                            num & 0x000000ff)


# get all ips list between start ip and end ip
def ip_range(start, end):
    return [num2ip(num) for num in range(ip2num(start), ip2num(end) + 1) if num & 0xff]
# main function
def bThread(iplist):
    global LOGFILE
    LOGFILE = open('./netlog/TEMP.txt', 'w+')
    SETTHREAD = 1000
    threadl = []
    queue = Queue.Queue()
    hosts = iplist
    for host in hosts:
        for port in PORT.keys():
            queue.put((host,port))

    threadl = [tThread(queue) for x in xrange(0, int(SETTHREAD))]
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()

# create thread

class tThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            host,port = self.queue.get()
            print host,port

            #checkIP(host, port)
            # try:
            #     #print host,port
            #     checkIP(host,port)
            # except:
            #     continue

def checkIP(host,port):
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.settimeout(1)
    try:
        ss.connect((host, port))
        print "%s 开放端口 %s   %s" % (host, port, PORT[port])
        getdata(host,port)
        ss.close()
    except:
        pass

def getdata(host,port):
    port = str(port)
    aimurl = "http://" + host + ":" + str(port)
    print "aimurl:"+aimurl
    data = urllib2.urlopen(aimurl, timeout=5)
    htmlcontent = data.read()
    print htmlcontent(100)
    data.close()
    retitle = re.findall(u'<title>(.*?)</title>', htmlcontent)
    deip = urlip(host)
    # print "http://" + host + ":" + PORT + "/" + " #" + retitle[0].decode("utf-8").encode(os_char) + "#" + deip[0].decode("utf-8").encode(os_char)
    print "http://" + host + ":" + port + "/" + " #" + retitle[0].decode("utf-8").encode(os_char) + "#" + deip[0]
    try:
        LOGFILE.write("http://" + host + ":" + port + "/" + " #" + retitle[0] + "#" + deip[0] + '\n')
    finally:
        LOGFILE.flush()

    # try:
    #     data = urllib2.urlopen(aimurl,timeout = 5)
    #     htmlcontent = data.read()
    #     data.close()
    #
    #     retitle = re.findall(u'<title>(.*?)</title>',htmlcontent)
    #     deip = urlip(host)
    #     print "http://"+host+":"+PORT+"/" + " #"+retitle[0].decode("utf-8").encode(os_char)+"#"+deip[0].decode("utf-8").encode(os_char)
    #     try:
    #
    #         LOGFILE.write("http://"+host +":"+PORT+"/"+" #"+retitle[0]+"#"+deip[0]+'\n')
    #     finally:
    #         LOGFILE.flush()
    # except:
    #     pass


def netmain(addr):
    ipn = str(addr).split('.')
    ipcs = int(ipn[2]) - 1
    ipce = int(ipn[2]) + 1
    startip = ipn[0] + '.' + ipn[1] + '.' + str(ipcs) + '.' + '1'
    endip = ipn[0] + '.' + ipn[1] + '.' + str(ipce) + '.' + '255'
    iplist = ip_range(startip, endip)
    bThread(iplist)

netmain('61.158.105.224')


