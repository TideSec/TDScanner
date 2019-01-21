#!/opt/python27/bin/python
#-- coding: utf-8 -*-


import json
import sys
import urllib2
import psycopg2

from flask import g, Blueprint, render_template, request, url_for

from Config import config
from Config.errorlog import logger
from SearchModule.breed_search import get_breed_results

app = Blueprint('breed_track', __name__)


#the log to record the exception of the breed_track page
recordLog = logger('breed_track.py', config.breed_track_log_path)


@app.before_request
def before_requesr():
    g.db = psycopg2.connect(config.config_db_info)
    g.cur = g.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


@app.teardown_request
def tear_down(response):
    g.db.close()
    return response




@app.route("/breed_track")
@app.route('/breed_track/<page_num>/<page_size>/<order>')
@app.route("/breed_track/<page_num>/<page_size>/<order>/status/<status>")
@app.route("/breed_track/<page_num>/<page_size>/<order>/condition/<condition>")
@app.route('/breed_track/<page_num>/<page_size>/<order>/<status>/<condition>')
def breed_track(page_num = 1, page_size = 15, order="start_down", status = '', condition = ''):
    '''getting the data restricted with the page_num,
       page_size, status, up_time, condition and the order mode.
    '''    
    print "enter"
    result = {
                "content":[], "count": 0, "status":status, "page_num":int(page_num),
                 "page_size":int(page_size), "condition": condition, "order":order
            }

    orders = {
                "hash_up": "md5", "hash_down": "md5 desc", 
                "status_up":"status", "status_down":"status desc",
                "start_up": "date_create", "start_down":"date_create desc", 
                "cast_up": "date_start", "cast_down": "date_start desc", 
                "breed_up":"breed_time", "breed_down":"breed_time desc", 
                "size_up":"t1.file_size", "size_down":"t1.file_size desc", 
                "name_up":"t1.file_name", "name_down":"t1.file_name desc",
                "type_up":"file_type", "type_down": "file_type desc", 
                "person_up": "username", "person_down":"username desc", 
            }
          
    if orders.has_key(order):
        order = orders[order]
    else:
        order = "date_create desc"


    #the sql of the getting the count
    count_sql = """select count(1) from t_user_operat_info t1 
                    left join task t2 on t1.task_id = t2.task_id 
                    where cast_type = 2
                        and t2.status like '%s'
                        and (
                                t1.file_name like '%s' 
                                or t1.md5 like '%s' 
                                or t1.md5|| '.'|| t1.crc32 like '%s'
                                or t1.up_time::text like '%s'
                            )"""%('%'+str(status)+'%', '%'+str(condition)+'%',\
                                    '%'+str(condition)+'%','%'+str(condition)+'%','%'+str(condition)+'%')
    

    #the sql of the getting the breed information content
    base_sql = """select t1.md5, t1.crc32, t1.batch_id,t1.md5||'.'||t1.crc32 as hash,
                         to_char(t1.up_time,'YYYY-MM-DD HH24:MI:SS' ) as date_create, 
                         to_char(t2.date_start,'YYYY-MM-DD HH24:MI:SS' ) as date_start, 
                         to_char(t2.date_done,'YYYY-MM-DD HH24:MI:SS' ) as date_done, t2.task_id,
                         t1.username, t1.file_size/1024||'KB' as file_size, t1.file_type, t1.file_name,
                    case when t2.status = 'SUCCESS' then '已完成' 
                         when t2.status = 'TIMEOUT' then '分析超时'
                         when t2.status = 'STARTED' then '分析中'
                         when t2.status = 'FAILURE' then '分析失败'
                         when t2.status = 'CANCELED' then '取消分析' 
                         when t2.status = 'PENDING' then '待分析'  
                         else '未知' end status,
                    case when t2.status = 'SUCCESS' then to_char(date_done - date_start,'HH24小时MI分SS秒' )
                         when t2.status = 'TIMEOUT' then to_char(date_done - date_start,'HH24小时MI分SS秒' )
                         when t2.status = 'STARTED' then to_char((now() - date_start),'HH24小时MI分SS秒' )
                         when t2.status = 'FAILURE' then to_char(date_done - date_start,'HH24小时MI分SS秒' )
                         when t2.status = 'CANCELED' then to_char(date_done - date_start,'HH24小时MI分SS秒' )
                         when t2.status = 'PENDING' then  '00小时00分00秒'
                         end as breed_time
                    from t_user_operat_info t1 
                    left join task t2 on t1.task_id = t2.task_id 
                    where cast_type = 2
                    and t2.status like '%s'
                    and (
                        t1.file_name like '%s' 
                        or t1.md5 like '%s'  
                        or t1.md5|| '.'|| t1.crc32 like '%s'
                        or t1.up_time::text like '%s'
                        )
                    order by %s 
                """%('%'+str(status)+'%','%'+str(condition)+'%',\
                    '%'+str(condition)+'%','%'+str(condition)+'%','\
                    %'+str(condition)+'%',order)


    base_sql += 'offset %s limit %s'%((int(page_num) - 1) * int(page_size), int(page_size))

    print 1
    #getting the the count of the breed
    try:
        g.cur.execute(count_sql)
        print 2
    except Exception as e:
        recordLog.error(str(e))
    else:
        result["count"] =  g.cur.fetchone()["count"]


    #getting the breed data
    try:   
        g.cur.execute(base_sql)
    except Exception as e:
        recordLog.error(str(e))
    else:
        result["content"] = g.cur.fetchall()

    print result
    #make sure the unicode mode
    reload(sys)
    sys.setdefaultencoding('utf-8')


    return render_template("/breed_track.html", result = result)


@app.route("/get_history_record/<md5>/<crc32>")
def get_history_record(md5, crc32):
    print 1
    history_url = config.get_history_url + "?md5=" + md5 + "&crc32=" + crc32 + "&category=dynamic_avml"
    print history_url
    response = (urllib2.urlopen(history_url)).read()
    print response
    return json.dumps(response)