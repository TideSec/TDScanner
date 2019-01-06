#!/opt/python27/bin/python
#coding:utf-8


import json
import random
import time

import config
from ..FileOperateModule.fileinfo import fileinfo
 
def get_unbreed_param(form, file_info_obj):
    '''get the condition and param when choose dynamic analysis
    '''
    kwargs =  config.kwargs
    precedure = {"node_list": ["PREP","PROC","SCAN"]}
    if form.has_key('MISSION'):
        precedure['node_list'].append("AUTO")
    else:
        kwargs["SOURCEINFO"]["TREATMENT"]["AUTO"] = {}

    condition = {
        'person_id': form["person_id"], 'username': form["username"], \
        'file_name': file_info_obj.get_name(), 'file_size': file_info_obj.get_len(),\
        'file_type' : file_info_obj.get_type(), 'sample_md5': file_info_obj.get_md5(),\
        'sample_crc32': file_info_obj.get_crc32(), 'sha256': file_info_obj.get_sha256(),\
        'sha1': file_info_obj.get_sha1(), 'task_deploy': json.dumps(precedure), 'note': json.dumps(kwargs)
    }
    
    return kwargs, condition

def get_breed_param(file_info_obj, breed_time):
    '''get the param for artificial breeding operation 
    '''
    test = config.test
    
    md5 = file_info_obj.get_md5()
    crc32 = file_info_obj.get_crc32()
    hash = md5 +'.'+ crc32

    test["task"] = hash
    test['kwargs']['FILEINFO']['SHA1'] = file_info_obj.get_sha1()
    test['kwargs']['FILEINFO']['NAME'] = hash
    test['kwargs']['FILEINFO']['FILE_LOCATION']= config.file_location+ hash

    # produce a random fo the batch_id
    rand_nums = ''.join([str(random.randint(1,10)) for i in range(6)])
    test['kwargs']['FILEINFO']['BATCH_ID'] = time.strftime('%Y%m%d_%H%M%S',\
                                    time.localtime(time.time()))+"_"+rand_nums+'_auto'
    
    test['kwargs']['FILEINFO']['CRC32']= file_info_obj.get_crc32()
    test['kwargs']['FILEINFO']['MD5']= file_info_obj.get_md5()
    test['kwargs']['FILEINFO']['SIZE']= file_info_obj.get_len()

    #setting the breeding time
    test['kwargs']['SOURCEINFO']['TREATMENT']['AUTO']['MISSION']['MAX_TIME']= int(breed_time)
    
    condition = {'kwargs': json.dumps(test)}

    return condition, test['kwargs']['FILEINFO']['BATCH_ID']