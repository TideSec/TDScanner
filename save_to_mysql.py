
import mysql.connector
import hashlib
try:
    conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    cur=conn.cursor()
except mysql.connector,e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def checkurl(url):
    conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    cur=conn.cursor()
    sql = "select url from target_baseinfo WHERE url = '{}'".format(url)
    cur.execute(sql)
    result_infos = cur.fetchall()
    cur.close()
    print len(result_infos)
    if len(result_infos)>0:
        url = url+str(len(result_infos))
        return url
    else:
        return url



def addurls(url,collect_urls,collect_ips,collect_dirs,ports,services_check):
    urla = checkurl(url)
    id = hashlib.md5()
    id.update(urla)
    hashid = id.hexdigest()
    print "web_hash:"+hashid
    # collect_dirs = "http://127.0.0.1/phpmyadmin"
    pam = (hashid,url,collect_urls,collect_ips,collect_dirs,ports,services_check)
    #print type(collect_dirs)
    sql = "insert into target_baseinfo values(%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sql,pam)
    conn.commit()
    return hashid

#addurls("http://127.0.0.1",1,1,1,1,1)

'''class urls(object):
    def __init__(self):
        self.id = None
        self.url = None
        self.collect_urls = None
        self.collect_ips = None
        self.collect_dirs = None
        self.ports = None
        self.services_check = None
    def __addctime__(self, val):
        self.ctime = val
    def __addtitle__(self, val):
        self.title = val
    def __addntime__(self, val):
        self.ntime = val
    def __addurl__(self, val):
        self.url = val
    def __addcon__(self,val):
        self.con = val
'''
def addtask(siteid,taskid,url):
    pam = (siteid,url,taskid)
    sql = "insert into sqlmaptask values(%s,%s,%s)"
    cur.execute(sql,pam)
    conn.commit()
def adtasklog(siteid,log,data):
    pam = (siteid,log,data)
    sql = "insert into sqlmaptask_info values(%s,%s,%s)"
    cur.execute(sql,pam)
    conn.commit()
def addnetlist(siteid,url,title):
    pam = (siteid,url,title)
    sql = "insert into netlist values(%s,%s,%s)"
    cur.execute(sql,pam)
    conn.commit()