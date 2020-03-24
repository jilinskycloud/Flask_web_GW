import httplib2
import time
import json
import os
import signal
import urllib
import base64
import subprocess
import redis


r = redis.StrictRedis(host='localhost', port=6370, db=0, charset="utf-8", decode_responses=True)

HB = "OFF"
server_socket = "NULL"
serial_no = "NULL"
mac = 'NULL'
#proc = subprocess.Popen(["cat /sys/class/net/eth0/address"], stdout=subprocess.PIPE, shell=True)
#(mac, err) = proc.communicate()

#print("^^^^^^^^^^^^^^^^^^^^")
#print(mac)


def status_():
	global HB
	global server_socket
	global serial_no
	d1 = json.load(open('/www/web/_netw/conf/ble_conf.text','r'))
	d2 = json.load(open('/www/web/_netw/conf/wifi_conf.text','r'))
	#print(d1['hb_en'])
	#print(d2['hb_en'])
	server_socket = d1['server_socket']
	print("Server Socket :: ", server_socket)
	serial_no = d1['serial_no']
	#time.sleep(10)
	if d1['heart_beat'] == 'on' or d2['w_heart_beat'] == 'on':
		HB = "ON"
	else:
		HB = "OFF"
	#print("signal is here")
	#print(HB)
	return HB

HB = status_()




def receive_signal(signum, stack):
	global HB
	#print('Received signal:', signum)
	HB = status_()

def redis_started():
	proc = subprocess.Popen(["redis-cli -p 6370 ping"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	out = out.decode("utf-8")
	#print("luli luli luli luli______________-", out)
	if out == "PONG\n":
		out = 1
	else:
		out = 0
	return out

signal.signal(signal.SIGUSR1, receive_signal)
pidis = str(os.getpid())
print('My PID:', pidis)

f= open("/var/run/heartbeat.pid","w+")
f.write(pidis)
f.close()

while(1):
	time.sleep(1)
	global HB
	global mac
	#print("in while loop")
	#print("---------------------------------------------------------------------||||----")
	#serial_no12 = serial_no+"."+mac.decode("utf-8") 
	_sr = serial_no.encode()
	#print(_sr)
	_sr = base64.b64encode(_sr)   
	#print(_sr)
	print("Heart Beat Status :: ",HB)
	body = {'sr':_sr}
	if HB == "ON":
		#print("Heartbeat is enabled")
		http = httplib2.Http(".cache",  disable_ssl_certificate_validation=True)
		#content = http.request("http://192.168.1.74:5000/heartBeat/000000002|192.168.1.58|heartbeat", method="GET")[1]
		url_ = "http://"+server_socket+"/heartBeat/"
		print("Server URL :: ", url_)
		try:
		 	content = http.request(url_, method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body) )[1]
		except Exception as e:
		 	pass
		 	#raise e 
		content = content.decode("utf-8") 
		print("[ Time :: ",time.ctime()," ] | Server Response to Gateway :: ",content)
		if redis_started() == 1:
			if content == 'success':
				r.set("hbeat", 'connected')
				print("Redis Server is Connected!")
				os.system("/www/web/_autoConfig/gpio_led /sys/class/leds/green66/brightness 2 2")
			else:
				print("Not Connected!")
				r.set("hbeat", 'disconnected')
				os.system("/www/web/_autoConfig/gpio_led /sys/class/leds/green66/brightness 100000 2")
	elif HB == 'OFF':
		if redis_started() == 1:
			print("Server Not Connected!")
			r.set("hbeat", 'disconnected')
		else:
			print("Redis wanna die !!!!!")