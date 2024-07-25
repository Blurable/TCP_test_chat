import socket
import threading


class Connection:
    def __init__(self, sock: socket.socket, encoder = 'utf-8'):
        self.sock = sock
        self.lock = threading.Lock()
        self.encoder = encoder
        self.bytesize = 1024
        

    def send(self, msg):
        with self.lock:
            self.sock.send(msg.encode(self.encoder))


    def recv(self):
        return self.sock.recv(self.bytesize).decode(self.encoder)
    

    def close(self):
        with self.lock:
            self.sock.close()

