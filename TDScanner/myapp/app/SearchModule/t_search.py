#!/opt/python27/bin/python
#coding:utf-8

import json
import urllib2

from ..Config import config

t_behaviors = { 'is_danger': '具有典型行为',
                'is_network': '具有网络行为', 
                'is_process': '具有进程操作行为',
                'is_file': '具有文件操作行为', 
                'is_registry': '具有注册表操作行为',
                'is_other':'具有其他行为'
                }


def t_search(hash):
    '''
    T system backup information
    for static_status:1 for started, 2 for finished
    for breed_status:0 and 1 for started, 2 for finished
    '''
    t_result = {
        'sign':'t', 'virus_name':'', 'is_virus':'', 'cast_time':'',\
        'format_name':'', 'static_status': '未完成', 'dynamic_status':'未完成', \
        'analysis_steps': ['预处理','多引擎扫描','静态分析'], 'behaviors':[]
    }
    t_static_url = config.t_static_url + hash
    
    try:
        t_static_result = json.loads((urllib2.urlopen(t_static_url)).read())
    except Exception as e:
        raise e
    else:
        t_result['static_status'] = "已完成"
        t_result['is_virus'] = '恶意' if t_result['virus_name'] else '非恶意'
        if t_static_result["basic_info"]:       
            t_result['virus_name'] = t_static_result['basic_info']['virus_name']
            t_result['cast_time'] = t_static_result['basic_info']['cp_time']
            t_result['format_name'] = t_static_result['basic_info']['file_format']
            

    t_dynamic_url = config.t_dynamic_url + hash
    try:
        t_dynamic_result = json.loads((urllib2.urlopen(t_dynamic_url)).read())        
    except Exception as e:
        raise e

    if t_dynamic_result['succeed']:
        t_result['dynamic_status'] = '已完成'
        t_result['analysis_steps'].append('动态分析')
        t_result['behaviors'] = [t_behaviors[key] for key in t_behaviors \
                                    if t_dynamic_result["content"][key] ]

    t_result["analysis_steps"] = '-'.join(t_result["analysis_steps"])
    t_result["behaviors"] = '-'.join(t_result["behaviors"])
    
    return t_result      