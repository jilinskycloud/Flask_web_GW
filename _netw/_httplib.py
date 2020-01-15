import httplib2
import time
import subprocess
import urllib
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

http = httplib2.Http(".cache",  disable_ssl_certificate_validation=True)
#http = httplib2.Http()


def encrypt(out):
  #print(out)
  data = out 
  key = b'\xa5}\x9a\xee\xf1Q\x1e\x93\x18\xb6\xc9\t\x1c&\xad\x05'
  cipher = AES.new(key, AES.MODE_EAX)
  ciphertext, tag = cipher.encrypt_and_digest(data)
  data = {'nonce': cipher.nonce.hex(), 'ciptext':ciphertext.hex(), 'tag':tag.hex()}
  return data 

def send():
  while(1):
    proc = subprocess.Popen(["./ble_read"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    #print("this is the original out data")
    #print(out)
    #print(len(out))
    data = encrypt(out)
    body = data 
    #print(body)
    if(len(out) > 0):
      #print("This is the Length of the packet!")
      print(out)
      #print(out.decode('utf-8'))
      #time.sleep(2)
      #content = http.request("http://192.168.1.74:5000/http_test/datas", method="GET")#[1]
      #content = http.request("https://192.168.1.74/http_data/0003|7473653845|-87|djkfgh|192.167.1.89", method="GET")[1] 
      #print(content.decode())
      content = http.request("http://192.168.1.74:5000/http_test", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body) )[1]
      #print(content.decode())

send()





