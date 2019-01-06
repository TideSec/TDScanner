#!/usr/bin/env python
# encoding: utf-8
# email: ringzero@0x557.org
# github: http://github.com/ring04h

'''
	多线程并行计算，Queue.get_nowait()非阻塞
		* 生成线程数组
		* 启动线程组
		* 线程组遍历，使每个独立的线程join()，等待主线程退出后，再进入主进程
'''

import json
import sys
import libs.requests as requests
from libs.output import *
from libs.utils.FileUtils import FileUtils
import threading
import Queue

# 全局配置
using_dic = './dics/dirs.txt'  # 使用的字典文件
threads_count = 100  # 线程数
timeout = 3  # 超时时间
allow_redirects = True  # 是否允许URL重定向
headers = {  # HTTP 头设置
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    'Referer': 'http://www.google.com',
    'Cookie': 'whoami=wyscan_dirfuzz',
}
proxies = {  # 代理配置
    # "http": "http://user:pass@10.10.1.10:3128/",
    # "https": "http://10.10.1.10:1080",
    # "http": "http://127.0.0.1:8118", # TOR 洋葱路由器
}


def dir_check(url):
    return requests.get(url, stream=True, headers=headers, timeout=timeout, proxies=proxies,
                        allow_redirects=allow_redirects)


class WyWorker(threading.Thread):
    # 线程初始化，使用OOP传递参数
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.output = CLIOutput()

    def run(self):
        while True:
            if self.queue.empty():
                break
            # 用hack方法，no_timeout读取Queue队列，直接异常退出线程避免阻塞
            try:
                url = self.queue.get_nowait()
                results = dir_check(url)
                if results.status_code == requests.codes.ok:

                    dir_exists.append(url)
                msg = "[%s]:%s \n" % (results.status_code, results.url)
            # self.output.printInLine(msg)
            except Exception, e:
                pass
                break


def fuzz_start(siteurl):
    output = CLIOutput()

    global dir_exists
    dir_exists = []

    # 生成队列堆栈
    queue = Queue.Queue()

    for line in FileUtils.getLines(using_dic):
        line1 = '%s/%s' % (siteurl.rstrip('/'), line.replace('%EXT%', 'asp'))
        line2 = '%s/%s' % (siteurl.rstrip('/'), line.replace('%EXT%', 'php'))
        line3 = '%s/%s' % (siteurl.rstrip('/'), line.replace('%EXT%', 'jsp'))
        # print "line1"+line1
        # print "line2"+line2

        queue.put(line1)
        queue.put(line2)
        queue.put(line3)

    #	output.printHeader('-' * 60)
    #	output.printTarget(siteurl)
    #	output.printConfig( str(threads_count), str(queue.qsize()))
    #	output.printHeader('-' * 60)

    # 初始化线程组
    threads = []
    for i in xrange(threads_count):
        threads.append(WyWorker(queue))
    # 启动线程
    for t in threads:
        t.start()
    # 等待线程执行结束后，回到主线程中
    for t in threads:
        t.join()
    #print type(dir_exists)

    abuff = []
    for a in dir_exists:
        if a not in abuff:
            abuff.append(a)
    dir_exists = abuff

    return dir_exists


#print fuzz_start('http://127.0.0.1')
