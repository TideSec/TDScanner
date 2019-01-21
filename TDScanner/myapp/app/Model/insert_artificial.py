#!/opt/python27/bin/python
#coding:utf-8

import json
import psycopg2
import psycopg2.extras
from time import sleep

from ..Config import config

def insert_unbreed_data(form, condition, cursor, db):
	'''cast_type 0 for static operatin only, 
	   1 for static and dynamic,
	   and 2 for static and breed 
	'''

	cursor.execute('''
		INSERT INTO t_user_operat_info(person_id, 
			username, md5, crc32, batch_id, up_time, note,file_name,
			task_deploy, sha1, sha256, file_size, file_type,cast_type) 
		VALUES(%(person_id)s, %(username)s, %(sample_md5)s, %(sample_crc32)s,
				%(batch_id)s,now(), %(note)s, %(file_name)s, %(task_deploy)s, 
		%(sha1)s,%(sha256)s,%(file_size)s,%(file_type)s,0);''',condition)
	db.commit()
	print form
	if form.has_key('MISSION'):
		cursor.execute('UPDATE t_user_operat_info set auto_stat = 1,cast_type = 1\
                        where batch_id = %(batch_id)s',{"batch_id":condition['batch_id']})
	
		db.commit()


def insert_breed_data(form, file_info_obj, batch_id, task_id_pre, note, cursor, db):
	'''cast_type 0 for static operatin only, 
	   1 for static and dynamic,
	   and 2 for static and breed 
	'''
	person_id = form['person_id'] 
	username = form['username'] 
	print "basic info: ", username, person_id
	task_id = 0
	count = 0
	precedure = {"node_list": ["PREP","PROC","SCAN","BREED"]}

	condition = {
					"person_id": person_id, "sample_md5":file_info_obj.get_md5(), \
		 			"username": username,"sample_crc32": file_info_obj.get_crc32(),\
					"batch_id": batch_id, "task_deploy":json.dumps(precedure),
					"sha1":file_info_obj.get_sha1(), "sha256":file_info_obj.get_sha256(),\
					"file_name":file_info_obj.get_name(),"file_size":file_info_obj.get_len(),\
					"file_type":file_info_obj.get_type(), "note": note
				}
				
	task_name = str(file_info_obj.get_md5()) +'.'+ str(file_info_obj.get_crc32())
	
	while ((task_id <= task_id_pre) and (count < 4)):
		sleep(1)
		cursor.execute("""select max(task_id) task_id from task 
							where task_name='%(task_name)s'"""%{"task_name":task_name})
		task_id = cursor.fetchone()["task_id"]
		print "find task_id: ", task_id
		count += 1

	if (task_id > task_id_pre):
		print "this task_id: ",task_id
		condition["task_id"] = task_id
		cursor.execute("""insert into t_user_operat_info(
							person_id, username, md5, crc32, batch_id,
							 up_time, note,file_name, task_deploy, sha1, 
							 sha256, file_size, file_type, task_id,cast_type) 
								VALUES(%(person_id)s, %(username)s, %(sample_md5)s, 
								%(sample_crc32)s, %(batch_id)s,now(), %(note)s, 
									%(file_name)s, %(task_deploy)s,	%(sha1)s,%(sha256)s,
										%(file_size)s,%(file_type)s,%(task_id)s,2)""",condition)
		db.commit()
		print "commit ok"
		return True
	else:
		return False

