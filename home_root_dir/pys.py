import serial
ser = serial.Serial('/dev/ttymxc2', 115200, timeout=1)




while True:
    l  = ser.readline().decode("ascii")
    #print(type(reading))
    #l = reading.replace("\\x",' ')
    #print(type(l))
    print(l)
    #print(l.decode('utf-8'))
    
