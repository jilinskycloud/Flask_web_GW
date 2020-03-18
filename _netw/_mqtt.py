import subprocess
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json

add = 'tcp://192.168.1.74:1883'
cid = 'ExampleClientPub'
tpc = 'exp'
plo = '-------bc--'
#cmd = '/www/web/_netw/mqtt_post '+add+' '+cid+' '+tpc+' '+plo


def encrypt(out):
  print("()OK*(JM()*NH*()---------------")
  print(out)
  data = out 
  key = b'\xa5}\x9a\xee\xf1Q\x1e\x93\x18\xb6\xc9\t\x1c&\xad\x05'
  cipher = AES.new(key, AES.MODE_EAX)
  ciphertext, tag = cipher.encrypt_and_digest(data)
  data = {'nonce': cipher.nonce.hex(), 'ciptext':ciphertext.hex(), 'tag':tag.hex()}
  return data 




while(1):
	proc = subprocess.Popen(["/www/web/_netw/ble_read"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	if(len(out) == 117):
		#out2 = out.decode('utf-8')
		data = encrypt(out)
		a = json.dumps(data)
		print(a)
		print("data encrypted ----------------------------------------------------------------------------------------------------------------------------")
		cmd = '/www/web/_netw/mqtt_post '+add+' '+cid+' '+tpc+' '+"'"+a+"'"
		proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)                                                      
		(out1, err1) = proc.communicate()
		print("Data sending...")
	else:
		print("length error !")




