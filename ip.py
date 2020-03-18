import socket
#???????
myname = socket.getfqdn(socket.gethostname(  ))
#????ip
myaddr = socket.gethostbyname(myname)
print(myname)
print(myaddr)
