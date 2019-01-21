#!/opt/python27/bin/python
#coding:utf-8

import psycopg2

from ..Config import config


'''
the unbreed and the breed searching means all artificial casting,
the unbreed searching means static and dynamic operation result,
the breed searching means static and breed operation result.
'''

unbreed_behavior = {
            'is_danger_behavior': '具有典型行为',
            'is_network_monitor': '具有网络行为', 
            'is_process_monitor': '具有进程操作行为',
            'is_file_monitor': '具有文件操作行为', 
            'is_register_monitor': '具有注册表操作行为',
            'is_other_behavior':'具有其他行为'
            }


def get_dynamic_behavious(sql_condition, cursor):
    '''
    get the virus dynamic behavior
    '''
    sql_dynamic_analysed_behavior = "\
        SELECT is_danger_behavior,is_file_monitor, is_register_monitor\
            is_other_behavior, is_network_monitor, is_process_monitor \
        FROM t_final_cp c\
        full join t_user_operat_info a\
        on a.md5 = c.md5 and a.batch_id = c.batch_id\
        full join t_auto_analysis_cp b\
        on b.md5 = c.md5 and c.batch_id = b.batch_id where a.batch_id = '" + sql_condition + "'"
    cursor.execute(sql_dynamic_analysed_behavior)
    dynamic_analysed_behavior = cursor.fetchone()
    dynamic_behavior = [unbreed_behavior[key] for key\
            in dynamic_analysed_behavior if dynamic_analysed_behavior[key] ]
    return dynamic_behavior


def get_unbreed_results(sql_condition, cursor):
    '''
    get each unbreed result to 
    add to unbreed results' information
    '''
    unbreed_results_info = []
    sql_check_unbreed= "\
    SELECT  file_name,md5,crc32,stat,cast_type,\
            CASE when is_virus='FALSE' then '非恶意' \
                 WHEN is_virus='TRUE' then '恶意' \
                 ELSE '未知'END AS is_virus,stat,\
            v_name, task_deploy ,batch_id, \
            auto_stat, TO_CHAR(up_time,'YYYY-MM-DD HH24:MI:SS') as cast_time\
    FROM t_user_operat_info\
    WHERE  cast_type!=2  " + sql_condition + ' order by up_time desc'
    
    cursor.execute(sql_check_unbreed)
    all_unbreed_results = cursor.fetchall()

    for each_result in all_unbreed_results:        
        unbreed_result = {
            'sign':'unbreed', 'virus_name':'','cast_time':'',\
            'batch_id': 0 , 'static_status':'未完成', 'dynamic_status':'未完成','is_virus':'未知',\
            'behaviors':[], 'analysis_steps': ['预处理','多引擎扫描','静态分析']
            }
        unbreed_result['virus_name'] = each_result['v_name']
        unbreed_result['cast_time'] = each_result['cast_time']        
        unbreed_result['batch_id'] = each_result['batch_id']  
        unbreed_result["md5"] = each_result["md5"]
        unbreed_result["crc32"] = each_result["crc32"]
        #stat 0 for started ,1 for finished
        if each_result['stat']:        
            unbreed_result["static_status"] = "已完成" 
        #dynamic_stat 0 for waiting, 1 for started, 2 for finished
        if each_result['auto_stat'] == 2:
            unbreed_result['dynamic_status'] = "已完成" 

        unbreed_result['is_virus'] = each_result["is_virus"]                           
        unbreed_result['behaviors'] = get_dynamic_behavious(each_result['batch_id'],cursor)
        unbreed_result["behaviors"] = '-'.join(unbreed_result['behaviors'])
        
        if each_result["cast_type"] == 1:
            unbreed_result['analysis_steps'].append("动态分析") 
        unbreed_result['analysis_steps'] = '-'.join(unbreed_result["analysis_steps"])
        
        unbreed_results_info.append(unbreed_result)

    return unbreed_results_info        

