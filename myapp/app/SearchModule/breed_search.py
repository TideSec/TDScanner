#!/opt/python27/bin/python
#coding:utf-8

from ..Config import config

'''
PLEASE BE CAREFUL THAT the task table from taskmanager database
which are able to accessed by a view, as a result,you are able to
use the sql directly, like 'select * from task' and so on.

the unbreed and the breed searching means all artificial casting,
the unbreed searching means static and dynamic operation result,
the breed searching means static and breed operation result.
'''

def get_breed_results(sql_condition, cursor):
    breed_results_info = []
    sql_get_breed_results = """
        select 
            a.md5 as md5, a.file_name as file_name, 
            a.task_deploy, a.username as username, 
            to_char(a.up_time,'YYYY-MM-DD hh24:mi:ss') as cast_time, a.stat as static_status, 
            a.batch_id, a.task_id, a.cast_type,
            CASE WHEN b.status = 'PENDING' THEN '待分析' 
                WHEN b.status = 'STARTED' THEN '分析中'
                WHEN b.status = 'SUCCESS' THEN '已完成'
                WHEN b.status = 'FAILURE' THEN '分析失败' 
                WHEN b.status = 'TIMEOUT' THEN '分析超时' 
                WHEN b.status = 'CANCLED' THEN '取消分析'else'未知' end
            AS breed_status, 
            to_char(b.date_create ,'YYYY-MM-DD hh24:mi:ss') as date_create, 
            to_char(b.date_start ,'YYYY-MM-DD hh24:mi:ss') as date_start,
            to_char(b.date_done ,'YYYY-MM-DD hh24:mi:ss') as date_done
        from t_user_operat_info a left outer join task b
        on a.file_name = b.task_name where cast_type = 2 """ + sql_condition

    cursor.execute(sql_get_breed_results)
    all_breed_results = cursor.fetchall()

    for each_result in all_breed_results:        
        breed_result = {
            'sign':'breed', 'username':'','static_status': '未完成', \
            'breed_status':'未完成', 'date_create':'', 'date_start':'',\
            'date_done':'', 'task_name':'', "task_id": 0, "cast_time":'',\
            'analysis_steps': ['预处理','多引擎扫描','静态分析']
        }
        
        breed_result['username'] = each_result['username']

        if each_result["static_status"]:
            breed_result['static_status'] = "已完成"

        breed_result["cast_time"] = each_result["cast_time"]
        breed_result['breed_status'] = each_result['breed_status']
        breed_result['date_create'] = each_result['date_create']
        breed_result['date_start'] = each_result['date_start']
        breed_result['date_done'] = each_result['date_done']
        breed_result["task_id"] = each_result["task_id"]
        print "date_create: ",breed_result['cast_time']
        if each_result["cast_type"] == 2:
            breed_result['analysis_steps'].append("养殖分析")

        breed_result['analysis_steps'] = '-'.join(breed_result["analysis_steps"])
        breed_results_info.append(breed_result)
    
    return breed_results_info
