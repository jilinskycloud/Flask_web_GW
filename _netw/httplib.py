import httplib2
import time
import subprocess
import urllib


from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


http = httplib2.Http(".cache",  disable_ssl_certificate_validation=True)
#http = httplib2.Http()




def encrypt(out1):
  data = out1
  file_out = open("../_include/encrypted_data.bin", "wb")
  recipient_key = RSA.import_key(open("../_include/public.pem").read())
  session_key = get_random_bytes(16)
  # Encrypt the session key with the public RSA key
  cipher_rsa = PKCS1_OAEP.new(recipient_key)
  enc_session_key = cipher_rsa.encrypt(session_key)
  # Encrypt the data with the AES session key
  cipher_aes = AES.new(session_key, AES.MODE_EAX)
  ciphertext, tag = cipher_aes.encrypt_and_digest(data.read())
  [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
  print("File is encrypted!")




def send():
  while(1):
    proc = subprocess.Popen(["./ble_read"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    body = {'ble_data': out} 
    out1 = "abc"
    encrypt(out1)
    if(len(out) > 0):
      #print(out.decode('utf-8'))
      #time.sleep(2)
      #content = http.request("http://192.168.1.74:5000/http_test/datas", method="GET")#[1]
      #content = http.request("https://192.168.1.74/http_data/0003|7473653845|-87|djkfgh|192.167.1.89", method="GET")[1] 
      #print(content.decode())
      content = http.request("http://192.168.1.74:5000/http_test", method="POST", headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urllib.parse.urlencode(body) )[1]
      #print(content.decode())




send()





