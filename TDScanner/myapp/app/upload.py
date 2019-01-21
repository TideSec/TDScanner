#coding:utf-8


'''this function of the module is for index page.
   first and foremost, it is checking the history affair 
   if the file has been casting ,from 2 methods,T SYSTEM 
   and artificial casting database.
   what's more, the user makes the choice among only static,
   static + dynamic , and  static + breeding  
'''

import os
import sys
import json
import yaml
import urllib2
from time import sleep

import urllib3
import requests
import psycopg2
import psycopg2.extras
from flask import g, render_template, Blueprint, request, send_from_directory, make_response, send_file

from .Config import config
from .Config.errorlog import logger
from .Config.get_param import get_unbreed_param,get_breed_param
from .FileOperateModule.fileinfo import fileinfo
from .Model.insert_artificial import insert_breed_data, insert_unbreed_data
from .SearchModule.t_search import t_search
from .SearchModule.breed_search import get_breed_results
from .SearchModule.unbreed_search import get_unbreed_results

app = Blueprint("upload", __name__)

#the log for recording all exception and error during the uplaod
uploadLog = logger('upload.py', config.upload_log_path)


@app.before_request
def before_request():
    g.db = psycopg2.connect(config.config_db_info)
    g.cur = g.db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

 
@app.teardown_request
def teardown_request(response):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()
    g.db.close()
    return response


@app.route("/check_upload", methods = ['POST'])
def check_upload():
    '''check the upload file history infomation  
    '''
    results = []
    files = request.files.getlist('file')

    for each_file in files:
        # each md5 has a result containing a lot of data
        result ={   
                    'file_feature':{}, 'details':[], 
                    "total":0, "analysed":"未分析", 
                } 
        

        # get the file infomation
        file_info = fileinfo(each_file)
        md5 = file_info.get_md5()
        crc = file_info.get_crc32()
        hash = str(md5) + '.' + str(crc)


        # save the file in to the directory
        if not os.path.isdir(config.file_download_path ):
            os.mkdir(config.file_download_path)

        file_location = config.file_download_path  + hash        
        # save the file
        if not os.path.exists(file_location):            
            file_dst = open(file_location,'w')            
            for line in file_info.get_buf():
                file_dst.write(line)
            file_dst.close()


        result["file_feature"] = file_info.get_fileinfo()
        

        # check the T system
        try:
            if t_search(hash)["cast_time"]:
                result["details"].append(t_search(hash))
        except Exception as e:
            print e
            uploadLog.error("Checking T system  %s" %str(e))


        #check the unbreed results
        sql_condition = "and md5 ='"+ md5 + "'"
        try:
            unbreed_search_result = get_unbreed_results(sql_condition, g.cur)
        except Exception as e:
            print e
            uploadLog.error(str(e))
        else:
            for each_result in unbreed_search_result:
                result['details'].append(each_result)


        #check the breed results
        sql_condition = "and md5 ='"+ md5 + "'"
        try:
            breed_search_result = get_breed_results(sql_condition, g.cur)
        except Exception as e:
            print e
            uploadLog.error(str(e))
        else:
            for each_result in breed_search_result:
                result['details'].append(each_result)


        #get the count of the all source
        result['total'] = len(result["details"])
        if result["total"]:
            result["analysed"] = "已分析"


        #collect all result for all files    
        results.append(result)


    return json.dumps(results)


@app.route("/upload_unbreed", methods = ['POST'])
def upload_unbreed():
    '''upload for static only or static 
        and dynamic method to artificial operation
    '''

    form = request.form
    files = request.files.getlist('file')

    print form
    #the set of the the upload result
    unbreed_upload_result = {"success":[], "return_fail":[], "upload_fail":[]}

    for each_file in files:        
        file_info = fileinfo(each_file)
        hash = file_info.get_md5() +'.'+ file_info.get_crc32()


        # setting the param, calling the unbreed interface in the post method, 
        # getting the bach_id and insert the relative infomation to the db 
        # if batch_id not error, at the same time, updating unbreed_upload_result
        unbreed_param, condition = get_unbreed_param(form, file_info)       
        param = {
            "kwargs": json.dumps(unbreed_param),
            "file_body": (file_info.get_name(), file_info.get_buf()),
            "md5": file_info.get_md5()
        }

        try:
            http = urllib3.PoolManager()
            response = http.request('POST', config.unbreed_upload_url, param)
            print param["kwargs"]
        except Exception as e:
            print "haha",e
            uploadLog.error(str(e))
            unbreed_upload_result["upload_fail"].append(file_info.get_name())

        else:
            return_info = response.data
            print return_info
            if return_info == 'error':
                unbreed_upload_result["return_fail"].append(file_info.get_name())
            else:
                condition['batch_id'] = return_info
                insert_unbreed_data(form, condition, g.cur, g.db)
                unbreed_upload_result["success"].append(file_info.get_name())


    return json.dumps(unbreed_upload_result)
            

@app.route("/upload_breed/<breed_time_setting>", methods=["POST"])
def upload_breed(breed_time_setting):
    '''artificial casting for breeding
    '''
    form = request.form
    files = request.files.getlist('file')


    #the set of the uplaod of breed
    breed_upload_result = {"success":[], "return_fail":[], "upload_fail":[]}
    for each_file in files:
        file_info = fileinfo(each_file)
        hash = file_info.get_md5() +'.'+ file_info.get_crc32()


        # setting the param and call the breed interface. 
        # the key of the step is how to get the task_id, 
        # we do not know the time point when the cloud department update the task_id in their db.
        # As a result, we get the task_id before calling interface to compare the task_id 
        # which we call the interface to make sure the task_id updated.we had better open the multi-thread
        # on the server with the gunicorn or other tools. On the contrary, the task_id must not be updated        
        condition, batch_id = get_breed_param(file_info, breed_time_setting)

        g.cur.execute("""select max(task_id) task_id from task 
                        where task_name='%(task_name)s'"""%{"task_name":hash})
        task_id_pre = g.cur.fetchone()["task_id"]
        print task_id_pre
        if not task_id_pre:
            task_id_pre = 0        

        try:
            http = urllib3.PoolManager()
            response = http.request('POST', config.task_assign, condition)
            print response.data

        except Exception as e:
            print e
            breed_upload_result["upload_fail"].append(file_info.get_name())
            uploadLog.error("breed upload trouble: %s" %str(e))

        else:            
            # insert into t_user_operat_info table of the db
            insert_result = insert_breed_data(form, file_info, batch_id, \
                                            task_id_pre, condition["kwargs"], g.cur, g.db)

            if insert_result:
                breed_upload_result["success"].append(file_info.get_name())

            else:
                breed_upload_result["upload_fail"].append(file_info.get_name())

    print breed_upload_result
    return json.dumps(breed_upload_result)


@app.route("/download/<hash>")
def download_sample(hash):
    '''the route for downloading
    '''
    if os.path.exists(config.file_download_path+hash):
        return send_from_directory(config.file_download_path, hash, as_attachment=True)
        
    else:
        return str("文件不存在")


# @app.route("/realTimeAvml/<hash>/<task_id>")
# def get_realtime_avml(hash, task_id):
#     '''calling the interface of the download real time avml
#     '''
#     print "enter"
#     data = {"key":hash, "task_id": task_id}
#     response = requests.post(config.real_time, data)

#     filename = hash + ".avml"
#     if not os.path.exists("/srv/myapp/"+filename):
#         with open(filename, "w") as f:
#             for line in response.content:
#                 f.write(line)

#     return send_from_directory('/srv/myapp/', filename, as_attachment=True)
