import socket
import threading
from numpngw import write_png

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.1.139', 10000))
sock.listen(1)

connections = []

def handler (c,a):
    global connections
    while True:
        data = c.recv(52428800)
        #print(c)
        #print(a)
        print(data.decode())
        # write_png('example1.png', data)
        if not data:
            connections.remove(c)
            c.close()
            break

while True:
    print("start")
    c,a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c,a))
    cThread.daemon = True
    cThread.start()
    connections.append(c)
    print(connections)