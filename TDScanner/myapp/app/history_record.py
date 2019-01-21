#coding:utf-8

import json
import sys
import psycopg2

from flask import g, Blueprint, render_template

from Config import config
from Config.errorlog import logger
from SearchModule.unbreed_search import get_unbreed_results

app = Blueprint("history_record", __name__)

#the log for recording the exception of the history_record
historyLog = logger('history_record.py', config.history_record_log_path)

@app.before_request
def before_requesr():
    g.db = psycopg2.connect(config.config_db_info)
    g.cur = g.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


@app.teardown_request
def tear_down(response):
    g.db.close()
    return response


@app.route("/history_record")
@app.route("/history_record/<page_num>/<page_size>")
@app.route('/history_record/<page_num>/<page_size>/<condition>')
def history_record(condition = '', page_num = 1, page_size = 8):
    '''Finding the data restricted with the page_num, 
       the page_size and the condition
    '''
    result = {
                "content":[], "count": 0, "condition":condition,
                "page_size":int(page_size), "page_num": int(page_num)
            }
    
    count_sql = """select count(distinct a.file_name) 
                from t_user_operat_info a 
                where a.cast_type <> 2"""

    try:
        g.cur.execute(count_sql)
    except Exception, e:
        historyLog.error(str(e))
    else:
        all_count =  g.cur.fetchone()
        result["count"] = int(all_count["count"])

    base_sql = """select
                    t1.file_name, t1.md5, t1.cast_type,t1.crc32,
                    t2.up_time, t1.username,t1.file_size,t1.file_type,
                    t2.all_have as total_analysis, t1.is_virus, t1.v_name
                from
                    (select distinct on (file_name) file_name ,md5,crc32,cast_type,v_name,
                         case when file_size is null then '0KB' else file_size/1024||'KB' end as file_size,
                         case when file_type is null then 'none' else file_type end as file_type,
                         CASE when is_virus='FALSE' then '非恶意' 
                               when is_virus='TRUE' then '恶意'  ELSE '未知'END AS is_virus,
                        to_char(up_time,'YYYY-MM-DD HH24:MI:SS' ) as up_time ,
                        username
                    from t_user_operat_info
                    where cast_type !=2
                    and (file_name like '%s' 
                    or md5 like '%s'
                    or t1.md5|| '.'|| t1.crc32 like '%s' 
                    or up_time::text like '%s')
                    order by file_name,id desc
                    )t1
                left join
                    (select file_name,count(*) all_have,to_char(max(up_time), 'YYYY-MM-DD HH24:MI:SS') up_time
                     from t_user_operat_info where cast_type !=2
                     group by file_name
                    )t2
                on t1.file_name= t2.file_name order by t2.up_time desc """%('%'+str(condition)+'%','%'+str(condition)+'%','%'+str(condition)+'%')
    
    base_sql += 'offset %s limit %s'%((int(page_num) - 1) * int(page_size), int(page_size))

    try:
        g.cur.execute(base_sql)
    except Exception as e:
        historyLog.error(str(e))
    else:
        result["content"] = g.cur.fetchall()

    #make sure the unicode mode
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    return render_template('history_record.html', result = result)


@app.route('/get_unbreed_detail/<md5>')
def get_unbreed_detail(md5):
    '''getting the details from the db whose name is file_name
    '''
    sql_condition = " and md5 ='"+ str(md5) + "'"
    details = get_unbreed_results(sql_condition, g.cur)
    return json.dumps(details)



