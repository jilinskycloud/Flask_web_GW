import httplib2
import time
import subprocess
import urllib
import json
import signal
import os
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import redis

r = redis.StrictRedis(host='localhost', port=6370, db=1, charset="utf-8", decode_responses=True)

def read_ble():
	proc = subprocess.Popen(["/www/web/_netw/ble_read"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	return out

def data_split(data):
  a = data.decode()
  a = a.split()
  print(a)
  mac_ = [3,4,5,6,7,8]
  rssi_ = [9]
  adv_ = [10,11,12,13,14,15,16,17,18]
  uuid_ = [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]
  maj_ = [35,36]
  min_ = [37,38]
  tx_ = [39]
  st = ""
  mac = st.join(list(map(a.__getitem__, mac_)))
  rssi = st.join(list(map(a.__getitem__, rssi_)))
  adv = st.join(list(map(a.__getitem__, adv_)))
  uuid = st.join(list(map(a.__getitem__, uuid_)))
  maj = st.join(list(map(a.__getitem__, maj_)))
  mina = st.join(list(map(a.__getitem__, min_)))
  tx = st.join(list(map(a.__getitem__, tx_)))
  received = {'mac':mac, 'rssi':rssi, 'adv':adv, 'uuid':uuid, 'maj':maj, 'min':mina, 'tx':tx}
  #print(received)
  return received

def cache(data):
    print("-----------------------------------------------ssssssssssssssss\n")
    tm_k = time.time()
    print(tm_k)
    r.hmset(tm_k, {'_uuid':data['uuid'], '_mac':data['mac'], '_rssi':data['rssi'], '_adv':data['adv'], '_tx':data['tx'], '_maj':data['maj'], '_min':data['min']})
    print("saved data in chache+++++++++++++++++++++++++++++++++++++++++++++++")
    print(r.hgetall(tm_k))
    r.expire(tm_k, 10)
    return "data saved"


while(1):
	data = read_ble()
	if len(data) > 0:
		s_data = data_split(data)
		status = cache(s_data)
		print(status)
		print("done")




