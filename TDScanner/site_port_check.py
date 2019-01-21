#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import *
from socket import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

screenLock = Semaphore(value=1)
port = [21, 22, 23, 25, 53, 80, 389, 8080, 1433, 2375,3389, 6379, 11211, 27017]


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))  # establishes a connection to target
        connSkt.send('PythonPortScan\r\n')  # send a string of data to the open port and wait for the response
        results = connSkt.recv(104)  # the response might give us an indication of the appliction running on the target host and port
        screenLock.acquire()
        #print str(results)
        return '[+]%d/tcp open' % tgtPort + '[+] ' + str(results)

    except:
        screenLock.acquire()
        return '[-]%d/tcp closed' % tgtPort

    finally:
        screenLock.release()
        connSkt.close()


def portScan(tgtHost):
    '''try:
        tgtName=gethostbyaddr(tgtIP)
        print '\n[+] Scan results for: '+tgtName[0]
    except:
        print 'Scan Results for: '+ tgtIP'''
    #setdefaulttimeout(1)
    ports = []
    tgtHost = tgtHost.strip('http:').strip('/')
    for tgtPort in port:
        i = connScan(tgtHost, int(tgtPort))
        ports.append(i)
    return ports



#print portScan('http://127.0.0.1/')
