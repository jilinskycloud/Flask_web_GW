import subprocess
while(1):
  proc = subprocess.Popen(["./ble_read"], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  if(len(out) > 0):
    print(out.decode('utf-8'))
