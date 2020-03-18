import subprocess
import json
import os
import os.path
import sqlite3
from os import path
import base64
from Crypto.Cipher import AES

def read_file(path_):
  file_p = "/mnt/config_t.text"
  #print(file_p)
  if path.exists(file_p) == True:
    with open(file_p) as json_file:
      data = json.load(json_file)
      return data
  return 'null'

def read_file1(path_):
  file_p = "/mnt/config_t.text"
  if path.exists(file_p) == True:
    with open(file_p,'r') as data:
      dd = data.read()
      return dd
  else:
    return 'null'


def dec_data(data):
  dd = data.split(',')
  print(dd)
  nonce = base64.b64decode(dd[0])
  ciphertext = base64.b64decode(dd[1])
  mac = base64.b64decode(dd[2])
  key = base64.b64decode(dd[3])
  #cipher = AES.new(key, AES.MODE_CCM, nonce)
  cipher = AES.new(key, AES.MODE_EAX, nonce)
  plaintext = cipher.decrypt(ciphertext)
  print(plaintext)
  plaintext = plaintext.decode("utf-8")
  plaintext = plaintext.split("~")
  return plaintext

def get_key(data):
  dd = data.split(',')
  key = dd[3]
  return key

def format_data(data):
  dd = data.split(',')
  print(dd)
  nonce = base64.b64decode(dd[0])
  ciphertext = base64.b64decode(dd[1])
  mac = base64.b64decode(dd[2])
  key = base64.b64decode(dd[3])
  print("*******************************************************************************************************************************************")
  print(key)
  cipher = AES.new(key, AES.MODE_EAX, nonce)
  #cipher = AES.new(key, AES.MODE_CCM, nonce)
  plaintext = cipher.decrypt(ciphertext)
  print(plaintext)
  plaintext = plaintext.decode("utf-8")
  plaintext = plaintext.split("~")
  data = {
    "enable_post_data": plaintext[0],
    "cache_size": plaintext[1],
    "gw_pass": plaintext[2],
    "heart_beat": plaintext[3],
    "server_socket": plaintext[4],
    "data_interval": plaintext[5],
    "serial_no": plaintext[6],
    "gw_uname": plaintext[7],
    "rssi_range": plaintext[8],
    "sniffer_type": plaintext[9],
    "protoc": plaintext[10]
    #"key": dd[3]
  }
  try:
    cipher.verify(mac)
    #print("The message is authentic: pt=%s" % (data))
    with open("/www/web/_netw/conf/ble_conf.text", "w") as f:
      json.dump(data, f, indent=4)
      return data
  except ValueError:
    print("Key incorrect or message corrupted")

def bs64(vl):
  return str(base64.b64encode(vl), 'utf-8')

def re_write(data1):
  dd = data1.split(',')
  print(dd)
  nonce = base64.b64decode(dd[0])
  ciphertext = base64.b64decode(dd[1])
  mac = base64.b64decode(dd[2])
  key = base64.b64decode(dd[3])
  cipher = AES.new(key, AES.MODE_EAX, nonce)
  #cipher = AES.new(key, AES.MODE_CCM, nonce)
  plaintext = cipher.decrypt(ciphertext)
  print(plaintext)
  plaintext = plaintext.decode("utf-8")
  plt = plaintext.split("~")
  plt1 = str(int( plt[6]) + 1).zfill(7)
  print(plt1)
  re_data = plt[0]+"~"+plt[1]+"~"+plt[2]+"~"+plt[3]+"~"+plt[4]+"~"+plt[5]+"~"+plt1+"~"+plt[7]+"~"+plt[8]+"~"+plt[9]+"~"+plt[10]
  re_data = str.encode(re_data)
  cipher12 = AES.new(key, AES.MODE_EAX)
  re_data = bs64(cipher12.nonce),bs64(cipher12.encrypt(re_data)),bs64(cipher12.digest()),bs64(key)
  return re_data

def read_usb():
  path1 = "/dev/sda"
  for i in range(3):
    path_ = path1+str(i) 
    mm = path.exists(path_)
    print(mm)
    if mm == True:
      #print(path_)
      os.system("mount "+path_ +" /mnt/")
      #print("Path exist!")
      data1 = read_file1(path_)
      if data1 != 'null':
        data = format_data(data1)
        print("Lets do Configuration!!!!!!")
        print(data)
        #os.system("cp /mnt/config_t.text /www/web/_netw/conf/ble_conf123.text") 
        #return 0
        #print(data['serial_no'])
        insert_sqlite(data)   
        ax = str(int(data['serial_no']) + 1).zfill(7)
        data['serial_no'] = ax  #str(int(data['serial_no']) + 1).zfill(7)
        print("thi is done really")
        re_data = re_write(data1)

        with open("/mnt/config_t.text",'w') as f:
          f.write(str(re_data))
        key_ = get_key(data1)
        d1 = {
          "auto_config" : "yes",
          "key" :  key_
        }
        with open("/www/web/_autoConfig/config.txt",'w') as jsonfile:                    
          json.dump(d1, jsonfile, indent=4)                               
        print(d1) 




        '''
        with open("/mnt/config_t.text",'w') as jsonfile:
          json.dump(re_data, jsonfile, indent=4)
        print(re_data)
        '''
        os.system("umount "+path_)
        return 1
      else:
        print("File not exist!!!!")
  return 0


def insert_sqlite(data):
  conn = sqlite3.connect('/www/web/gw_FlaskDb.db')
  #conn.execute('CREATE TABLE login (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
  print("Table created successfully");
  # Insert Data to Login table
  print("UNAME::  ",data['gw_uname'])
  print("PASS:: ", data['gw_pass'])
  conn.execute("INSERT INTO login (username,password) VALUES (?,?)",(data['gw_uname'], data['gw_pass']) )
  conn.commit()
  msg = "Record successfully added"



def main():
  d1 = json.load(open('/www/web/_autoConfig/config.txt','r'))
  print(d1['auto_config'])
  if d1['auto_config']  == 'no':
    print("Going to config the GateWay...")
    read_usb() 
    os.system("/www/web/_autoConfig/gpio_led /sys/class/leds/cpu/brightness 100000 20")
  elif d1['auto_config'] == 'yes':
     print("GateWay Already Configured!")
     os.system("/www/web/_autoConfig/gpio_led /sys/class/leds/cpu/brightness 10000 20")





if __name__ == '__main__':
    main()
