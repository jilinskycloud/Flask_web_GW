import httplib2
import time
import json
import os
import signal
import urllib
import base64

HB = "OFF"

def status_():
	global HB
	d1 = json.load(open('/www/web/_netw/conf/ble_conf.text','r'))
	d2 = json.load(open('/www/web/_netw/conf/wifi_conf.text','r'))
	#print(d1['hb_en'])
	#print(d2['hb_en'])
	#time.sleep(10)
	if d1['hb_en'] == 'on' or d2['hb_en'] == 'on':
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

signal.signal(signal.SIGUSR1, receive_signal)
pidis = str(os.getpid())
print('My PID:', pidis)

f= open("/var/run/heartbeat.pid","w+")
f.write(pidis)
f.close()

while(1):
	time.sleep(2)
	global HB
	print("in while loop")
	_sr = "000000002".encode()
	_sr = base64.b64encode(_sr)
	print(_sr)
	body = {'sr':_sr}
	if HB == "ON":
		print("Heartbeat is enabled")
		http = httplib2.Http(".cache",  disable_ssl_certificate_validation=True)
		#content = http.request("http://192.168.1.74:5000/heartBeat/000000002|192.168.1.58|heartbeat", method="GET")[1] 
		content = http.request("http://192.168.1.74:5000/heartBeat/", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body) )[1]
