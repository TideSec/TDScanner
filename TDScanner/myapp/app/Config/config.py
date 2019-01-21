#coding=utf-8

config_db_info = """
    host='10.128.127.249'
    port='5432'
    user='postgres'
    password='zaixian321'
    dbname='single_source'
    """

# the location storing the temporary file
# and the file for downloading
file_download_path = "/srv/myapp/download/"

# log path
upload_log_path = '/srv/myapp/log/upload.log'
history_record_log_path = '/srv/myapp/log/historyrecord.log'
breed_track_log_path = '/srv/myapp/log/breedtrack.log'

# T system background search url
t_static_url = "http://10.128.127.249:5000/static_analysis_data/"
t_dynamic_url = "http://10.128.127.249:5000/auto_analysis_cp/single_upload/"

# unbreed upload url
unbreed_upload_url = "http://10.128.126.185:8000/single_sample"
 
# file location to save the file
file_location = 'http://10.128.127.249:11101/download/'

# breed upload url
task_assign = "http://10.128.126.2:8000/task_assign/"
stop_breed = "http://10.128.126.2:8000/command/?command=stop&task_id="
real_time = "http://10.128.126.2:8000/avmldata/"
get_history_url = "http://10.128.126.2:20080/download_history"


# unbreed upload param
kwargs = {
    'CONFIG': {
        'AUTO_STORAGE_IP': '10.128.77.153',
        'AUTO_STORAGE_PORT': 8081,
        'AVML_STORAGE_IP': '10.128.126.192',
        'AVML_STORAGE_PORT': 80,
        'ORIGINAL_URL': 'http://10.128.77.153:8081',
        'DERIVATIVE_URL': 'http://10.128.77.153:8081'
    },
    'SOURCEINFO': {
        'TREATMENT': {
            'PROC': 'PROC',
            'SCAN': [ 
                        'AVPSCAN', 'KAVSCAN', 
                        'MSESCAN', 'NODSCAN',
                        'CLMSCAN', 'SOHSCAN'
                    ],
            'AUTO': {
                'MISSION': {
                    'SHAREING': 'False',
                    'FILE_TYPE': 'file_unkown',
                    'INTERVAL_TIME': 10,
                    'PACK_JUDGE': 'no',
                    'SHAREING_TIME': 20,
                    'MODE': 'single',
                    'MAX_TIME': 10,
                    'TIME_TYPE': 'minute'
                }
            }
        },
        'ACTIONFLAG': { 
                        'TASKUNIQ': 0, 'TASK': 1, 
                        'DATABASE': 1, 'RECYCLE': 0, 
                        'UNPACK': 1, 'FILEUNIQ': 0, 
                        'AVML': 1
                        }
    }
}

# breed upload param
test = {
        'retries': 0,
        'task': 'E66E5B324F06A2B4FCAA16BFCBBF080F.A7F9108A',
        'expires': 172800,
        'kwargs': {
            'FILEINFO': {
                'SHA1': '75B8F4264C393BC42F8B72B529846E01B391105C',
                'NAME': 'E66E5B324F06A2B4FCAA16BFCBBF080F.A7F9108A',
                'SEQUNCE_ID': '0',
                'FILE_LOCATION': 'http: //10.128.77.153:8081/download/E66E5B324F06A2B4FCAA16BFCBBF080F.A7F9108A',
                'BATCH_ID': '20141029_153501_112126_auto',
                'CRC32': 'A7F9108A',
                'MD5': 'E66E5B324F06A2B4FCAA16BFCBBF080F',
                'SIZE': 1515520
            },
            'CONFIG': {
                'ALARM_IP': '172.16.1.40',
                'ORIGINAL_URL': 'http: //10.128.77.153: 8081',
                'AVML_STORAGE_PORT': 11111,
                'AUTO_STORAGE_PORT': 8081,
                'ALARM_PORT': 9999,
                'AVML_STORAGE_IP': '10.128.126.192',
                'DERIVATIVE_URL': 'http: //10.128.77.153: 8081',
                'AUTO_STORAGE_IP': '10.128.77.153'
            },
            'SOURCEINFO': {
                'PRIORITY': 10000,
                'SRCNAME': 'auto',
                'TREATMENT': {
                    'AUTO': {
                        'MISSION': {
                            'SHAREING': 'False',
                            'FILE_TYPE': 'file_unkown',
                            'INTERVAL_TIME': 10,
                            'PACK_JUDGE': 'no',
                            'SHAREING_TIME': 20,
                            'MODE': 'single',
                            'MAX_TIME': 10,
                            'TIME_TYPE': 'minute'
                        }
                    }
                },
                'ACTIONFLAG': {
                    'TASKUNIQ': 0,
                    'TASK': 1,
                    'DATABASE': 1,
                    'RECYCLE': 0,
                    'UNPACK': 1,
                    'FILEUNIQ': 0,
                    'AVML': 0
                }
            }
        }
    }