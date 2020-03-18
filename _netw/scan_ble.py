import subprocess
import redis
import json
import os
import time

r = redis.StrictRedis(host='localhost', port=6370, db=0, charset="utf-8", decode_responses=True)
r1 = redis.StrictRedis(host='localhost', port=6370, db=1, charset="utf-8", decode_responses=True)

def data_split(data):
  a = data
  a = a.split()
  #print(a)
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
  received = {'mac':mac, 'rssi':rssi, 'adv':adv, 'uuid':uuid, 'maj':maj, 'mina':mina, 'tx':tx} 
  return received

def verify_mac(v_mac):
    obj = r.scan_iter()
    blk_ble = r.lrange("white_listed", 0, -1)
    print(blk_ble)
    if v_mac in blk_ble:
      #r.rpush("white_listed", wht_mac)
      return 1
    else:
      return 0

def insert_r1(data1):
    print("This is R1 data insert Function!--------------------------------------------------------------------------00000000000000000000000000000000000000000000000000")
    print(data1)
    r1.hmset(data1['mac'], {'mac':data1['mac'], 'rssi':data1['rssi'], 'adv':data1['adv'], 'uuid':data1['uuid'], 'maj':data1['maj'], 'mina':data1['mina'], 'tx':data1['tx']})
    r1.expire(data1['mac'], 300)
    print(r1.hgetall(data1['mac']))




d1 = json.load(open('/www/web/_netw/conf/ble_conf.text','r'))
print(d1['enable_post_data'])
post_ble = d1['enable_post_data']

def kill_proc():
	print("I'm the Process Killer haaa!")

	proc = subprocess.Popen(["ps ax | grep 'python3 /www/web/_netw/_httplib.py' | grep -v grep | awk '{print $1}'"], stdout=subprocess.PIPE, shell=True)
	(pid, err) = proc.communicate()
	cmd = "kill -9 " + str(pid)
	os.system(cmd)
	subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
	print("This is the process ID of heartbeat", pid)

def start_proc():
	print("I'm the Healer of my lovely processes haaa!")
	os.system("python3 /www/web/_netw/_httplib.py")
	#proc = subprocess.Popen(["ps ax | grep 'python3 /www/web/_netw/scan_ble.py' | grep -v grep | awk '{print $1}'"], stdout=subprocess.PIPE, shell=True)
	#(pid, err) = proc.communicate()
	#cmd = "kill -9 " + str(pid)
	#os.system(cmd)
	#(out, err) = proc.communicate()



def scan_it():
	a=1
	while(a != 80):
		proc = subprocess.Popen(["/www/web/_netw/ble_read"], stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		os.system("/www/web/_autoConfig/gpio_led /sys/class/leds/blue67/brightness 2 2")
		data = out.decode()
		#print(data)
		if len(data) > 0:
			print("The data length is ", len(data))	
			if len(data) > 102 and len(data) < 120:
				data1 = data_split(data)
				r.hmset(data1['mac'], {'mac':data1['mac'], 'rssi':data1['rssi'], 'adv':data1['adv'], 'uuid':data1['uuid'], 'maj':data1['maj'], 'mina':data1['mina'], 'tx':data1['tx']})
				r.expire(data1['mac'], 1000)
				print(r.hgetall(data1['mac']))
				#v_chk = verify_mac(data1['mac'])
				#if v_chk == 1:
				#  print("White listed mac address")
				#  insert_r1(data1)
				#else:
				#  print("this is the black listed mac address")
	   			#print(data1['mac'])
				a=a+1

def turn_post(stat):
	with open('/www/web/_netw/conf/ble_conf.text', 'r+') as f:
		data = json.load(f)
		data['enable_post_data'] = stat # <--- add `id` value.
		f.seek(0)        # <--- should reset file position to the beginning.
		json.dump(data, f, indent=4)
		f.truncate()



if post_ble == 'on':
	stat = 'off'
	turn_post(stat)
	#kill_proc()

	#time.sleep(2)
	scan_it()
	stat = 'on'
	turn_post(stat)
	#time.sleep(2)
	#os.system("python3 /www/web/_netw/_httplib.py")
	proc = subprocess.Popen(["python3 /www/web/_netw/_httplib.py"], stdout=subprocess.PIPE, shell=True)

	#start_proc()	
elif post_ble == 'off':
	scan_it()



'''
for key in r.scan_iter():
  print(key)
  if key != 'white_listed':
    print(r.hgetall(key))
'''