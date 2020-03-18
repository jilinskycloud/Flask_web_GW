import httplib2
import time
import subprocess
import urllib
import json
import signal
import os
import redis
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64



r = redis.StrictRedis(host='localhost', port=6370, db=0, charset="utf-8", decode_responses=True)
r1 = redis.StrictRedis(host='localhost', port=6370, db=1, charset="utf-8", decode_responses=True)
http = httplib2.Http(".cache",  disable_ssl_certificate_validation=True)
#http = httplib2.Http()



HB = "OFF"
PRO = "OFF"
sr_no = "0000000"

def status_():
  global HB
  global PRO
  global sr_no
  d1 = json.load(open('/www/web/_netw/conf/ble_conf.text','r'))
  #print(d1['hb_en'])
  #print(d2['hb_en'])
  #time.sleep(10)
  sr_no = d1['serial_no']
  if d1['enable_post_data'] == 'on' and d1['protoc'] == 'HTTP':
    HB = "ON"
    PRO = 'HTTP'

  elif d1['enable_post_data'] == 'on' and d1['protoc'] == 'MQTT':
    HB = "ON"
    PRO = 'MQTT'
  else:
    HB = "OFF"
    PRO = "OFF"
  return HB

HB = status_()
#print(HB)

def receive_signal(signum, stack):
  global HB
  print('Received signal--------------------------------------------------------------------------------------------!!!!!!!!!!------:', signum)
  HB = status_()

signal.signal(signal.SIGUSR1, receive_signal)
pidis = str(os.getpid())
print('My PID:', pidis)

f= open("/var/run/ble_post.pid","w+")
f.write(pidis)
f.close()

def encrypt_http(out):
  print("ENCRYPT THE SENDING DATA----------------------------")
  #print(out)
  data = out 
  d1 = json.load(open('/www/web/_autoConfig/config.txt','r'))

  key = d1['key']
  key = base64.b64decode(key)
  
  cipher = AES.new(key, AES.MODE_EAX)
  ciphertext, tag = cipher.encrypt_and_digest(data)
  data = {'nonce':bs64(cipher.nonce), 'ciphertext':bs64(ciphertext), 'tag':bs64(tag)}
  return data 


#--------------------------------------------------------------------------------------------------

def bs64(vl):
  return str(base64.b64encode(vl), 'utf-8')

def encrypt(out):
  #print("ENCRYPT THE SENDING DATA----------------------------")
  #print(out)
  data = out 
  d1 = json.load(open('/www/web/_autoConfig/config.txt','r'))

  key = d1['key']
  key = base64.b64decode(key)
  
  cipher = AES.new(key, AES.MODE_EAX)
  data = bs64(cipher.nonce),bs64(cipher.encrypt(data)),bs64(cipher.digest())
  return data 

#--------------------------------------------------------------------------------------------------


def data_split(data):
  global sr_no
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
  tx = int(tx, 16)
  received = {'mac':mac, 'rssi':rssi, 'adv':adv, 'uuid':uuid, 'maj':maj, 'mina':mina, 'tx':tx, 'sr_no':sr_no} 
  return received

def verify_mac(v_mac):
    obj = r.scan_iter()
    blk_ble = r.lrange("white_listed", 0, -1)
    print(blk_ble)
    if v_mac in blk_ble:
    	print(v_mac)
    	#time.sleep(2)
    	return 1
    else:
    	print(v_mac)
    	return 0

def get_average(t_rssi):
	plus = 0
	for v in range(len(t_rssi)):
		plus  = plus + int(t_rssi[v])
		#print('plus',plus)
		avg = plus/len(t_rssi)
	return avg



def insert_r1(data1, cache_lim):
    print("This is R1 data insert Function!--------------!!!!!!!!!!!!!!!!---------00000000000000000000000000000000000000000000000000")
    x = int(data1['rssi'], 16)
    r1.lpush(data1['mac'], x)
    r1.ltrim(data1['mac'],0, cache_lim)
    t_rssi = r1.lrange(data1['mac'],0,-1)
    #print(t_rssi)
    avg = get_average(t_rssi)
    #print(avg)
    #time.sleep(3)
    return avg




def send():
	global HB
	global PRO
	d1 = json.load(open('/www/web/_netw/conf/ble_conf.text','r'))
	print(d1)
	#d2 = json.load(open('/www/web/_netw/conf/wifi_conf.text','r'))
	print("Data Post Status is ::", HB, "and Protocol is ::", PRO)
	while(1):
		time.sleep(int(d1['data_interval']))
		#print(HB)
		if HB == "ON":
			proc = subprocess.Popen(["/www/web/_netw/ble_read"], stdout=subprocess.PIPE, shell=True)
			(out, err) = proc.communicate()
			os.system("/www/web/_autoConfig/gpio_led /sys/class/leds/blue67/brightness 2 2")
			#print("BLE READ DATA | READY TO SEND")
			#if len(out) > 0:
			if len(out) > 102 and len(out) < 120:
				avg = 0
				out1 = data_split(out.decode())
				v_chk = verify_mac(out1['mac'])
				#print(out1)
				ble_rssi = int(out1['rssi'], 16)
				rssi_lim = d1['rssi_range']
				rssi_lim = rssi_lim.split("|")
				#print(rssi_lim)
				cache_lim = d1['cache_size']
				#print(cache_lim)
				if v_chk == 1 and ble_rssi > int(rssi_lim[0]) and ble_rssi < int(rssi_lim[1]):
					print("White listed mac address-----------Ready to send")
					print(out1['mac'])
					avg = insert_r1(out1, int(cache_lim))  #it returns avg value
					#print(int(out1['rssi'], 16))
					out1['rssi'] = avg
					print("After RSSI Normalization",out1)
					#time.sleep(3)
					#print(out1)
					#print(out)
					out1 = json.dumps(out1).encode('utf-8')
					print("out1 butes ::", out1)
					print(out1)
					'''
					data = encrypt(out1)
					print(encrypt_old(out1))
					body = encrypt_old(out1)
					'''
					#print("here is the post data type./..")
					#print("after encryption", data)
					#print("This is the Length of the packet!", body)
					#print(len(out))
					#print(out.decode('utf-8'))
					#time.sleep(2)
					#content = http.request("http://192.168.1.74:5000/http_test/datas", method="GET")#[1]
					#content = http.request("https://192.168.1.74/http_data/0003|7473653845|-87|djkfgh|192.167.1.89", method="GET")[1] 
					#print(content.decode())
					if PRO == 'HTTP':
						print("data encrypted -------------------------THIS IS THE HTTP--------------------------------------")
						body = encrypt_http(out1)
						http_url = "http://"+d1['server_socket']+"/http_test"	      			
						#content = http.request("http://192.168.0.74:5000/http_test", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body) )[1]
						try:
							content = http.request(http_url, method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body))[1]
						except Exception as e:
							raise e
						print("SENDING BY HTTP PROTOCOL")
						#print(content.decode())
					elif PRO == 'MQTT':
						print("data encrypted -----------------------------------------------------------------THIS IS THE MQTT-----------------------------------------------------------")
						data = encrypt(out1)
						a = json.dumps(data)
						#print(a)
						add = d1['server_socket']
						add = add.split(":")
						ip =  add[0]
						add = "tcp://"+ip+":1883"   #'tcp://192.168.0.74:1883'
						#add = 'tcp://192.168.0.74:1883'
						cid = 'ExampleClientPub'
						tpc = 'exp'
						cmd = '/www/web/_netw/mqtt_post '+add+' '+cid+' '+tpc+' '+"'"+a+"'"
						proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)                                                      
						(out1, err1) = proc.communicate()
						print("SENDING BY MQTT PROTOCOL")
					else:
						print("Black listed MAC or RSSI is out of Range...")
				else:
					print("DATA LENGTH ERROR!!!-----")
		elif HB == "OFF":
			if os.path.exists("/var/run/ble_post.pid") == 'True':
				print(os.system("cat /var/run/ble_post.pid"))
				pi1 = open("/var/run/ble_post.pid", 'r')
				pid_1 = pi1.read()
				pi1.close()
				os.system('kill -s 10 ' + pid_1)

send()





