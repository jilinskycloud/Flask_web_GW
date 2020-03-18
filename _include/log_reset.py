import threading, time
import os

def check():
    #print(time.ctime())
    flask = "/tmp/flask_daemon.log"
    hb = "/tmp/hb_daemon.log"
    http = "/tmp/http_daemon.log"
    autoC = http = "/tmp/autoC_daemon.log"
    size = [] 
    size.append(get_file_size(flask))
    size.append(get_file_size(hb))
    size.append(get_file_size(http))
    size.append(get_file_size(autoC))       
    print("Size in MB: ",size) 
    return size

def get_file_size(file_name):
  size = os.path.getsize(file_name)
  #print("in bytes", size)
  kb = size/(1024)
  return kb


#hours_5 = 18000
WAIT_TIME_SECONDS = 5 

ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    size = check()
    if size[0] > 200:
        print("File is more than 1 MB", size)
        print("File need to be delete!!")
        open("/tmp/flask_daemon.log", "w").close()
    if size[1] > 200:
        open("/tmp/hb_daemon.log", "w").close()
    if size[2] > 200:
        open("/tmp/http_daemon.log", "w").close()
    if size[3] > 200:
        open("/tmp/autoC_daemon.log", "w").close()
    else:
        print("File size is less than 1 MB no need to delete!", size)
