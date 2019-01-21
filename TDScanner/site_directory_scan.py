# -*- coding: utf-8 -*-
# @Site    : www.TDScan.org

import Queue
import os
from threading import Thread
import sys
import urllib
reload(sys)
sys.setdefaultencoding('utf-8')
def bThread(iplist):
    SETTHREAD = 800
    #print '[Note] Running...\n'
    threadl = []
    queue = Queue.Queue()
    hosts = iplist
    for host in hosts:
        queue.put(host)

    threadl = [tThread(queue) for x in xrange(0, int(SETTHREAD))]
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()

#create thread
class tThread(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            host = self.queue.get()
            try:
                Dirbruteforce(host)
            except:
                continue
def Dirbruteforce(mydir):
    target_url = 'http://jf.cmbchina.com'
    #print target_url
    print  target_url+mydir
    status=urllib.urlopen(target_url+mydir).code
    #if status == '200':
    print target_url+mydir +"###:"+status

dicdir = []
print os.getcwd()
fp=open("dic/dir.list", "r")
alllines=fp.readlines()
for eachline in alllines:
        eachline=eachline.strip('\n')
        dicdir.append(eachline)
        bThread(dicdir)