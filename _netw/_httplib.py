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

http = httplib2.Http(".cache",  disable_ssl_certificate_validation=True)
#http = httplib2.Http()



HB = "OFF"
PRO = "OFF"

def status_():
  global HB
  global PRO
  d1 = json.load(open('/www/web/_netw/conf/ble_conf.text','r'))
  #print(d1['hb_en'])
  #print(d2['hb_en'])
  #time.sleep(10)
  if d1['ble_en_post'] == 'on' and d1['ble_proto'] == 'HTTP':
    HB = "ON"
    PRO = 'HTTP'

  elif d1['ble_en_post'] == 'on' and d1['ble_proto'] == 'MQTT':
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

def encrypt(out):
  print("()OK*(JM()*NH*()---------------")
  print(out)
  data = out 
  key = b'\xa5}\x9a\xee\xf1Q\x1e\x93\x18\xb6\xc9\t\x1c&\xad\x05'
  cipher = AES.new(key, AES.MODE_EAX)
  ciphertext, tag = cipher.encrypt_and_digest(data)
  data = {'nonce': cipher.nonce.hex(), 'ciptext':ciphertext.hex(), 'tag':tag.hex()}
  return data 

def send():
  global HB
  global PRO
  d1 = json.load(open('/www/web/_netw/conf/ble_conf.text','r'))
  print(d1)
  #d2 = json.load(open('/www/web/_netw/conf/wifi_conf.text','r'))
  while(1):
    time.sleep(2)
    
    print("in while loop-----------------------------------")
    print(HB)
    if HB == "ON":
      proc = subprocess.Popen(["/www/web/_netw/ble_read"], stdout=subprocess.PIPE, shell=True)
      (out, err) = proc.communicate()
      print("this is the original out data")
      print(out)
      print(len(out))
      data = encrypt(out)
      print("here is the post data type./..")
      body = data 
      print(type(body))
      if(len(out) > 0):
        #print("This is the Length of the packet!")
        print(out)
        #print(out.decode('utf-8'))
        #time.sleep(2)
        #content = http.request("http://192.168.1.74:5000/http_test/datas", method="GET")#[1]
        #content = http.request("https://192.168.1.74/http_data/0003|7473653845|-87|djkfgh|192.167.1.89", method="GET")[1] 
        #print(content.decode())
        if PRO == 'HTTP':
          print("data encrypted -----------------------------------------------------------------THIS IS THE HTTP-----------------------------------------------------------")
          content = http.request("http://192.168.1.74:5000/http_test", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body) )[1]
        #print(content.decode())
        elif PRO == 'MQTT':
          print("data encrypted -----------------------------------------------------------------THIS IS THE MQTT-----------------------------------------------------------")
          print("mqtt")
          data = encrypt(out)
          a = json.dumps(data)
          #print(a)

          add = 'tcp://192.168.1.74:1883'
          cid = 'ExampleClientPub'
          tpc = 'exp'
          cmd = '/www/web/_netw/mqtt_post '+add+' '+cid+' '+tpc+' '+"'"+a+"'"
          proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)                                                      
          (out1, err1) = proc.communicate()
          print("Data sending...")
      else:
        print("Length Error....")
    elif HB == "OFF":
      if os.path.exists("/var/run/ble_post.pid") == 'True':
        print(os.system("cat /var/run/ble_post.pid"))
        pi1 = open("/var/run/ble_post.pid", 'r')
        pid_1 = pi1.read()
        pi1.close()
        os.system('kill -s 10 ' + pid_1)

send()





