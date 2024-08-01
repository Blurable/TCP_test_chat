import socket
import threading


class Connection:
    def __init__(self, sock: socket.socket, encoder: str = 'utf-8'):
        self.sock = sock
        self.username = ''
        self.lock = threading.Lock()
        self.encoder = encoder
        

    def send(self, msg):
        with self.lock:
            self.sock.send(msg.encode(self.encoder))


    def recv(self, bytesize):
        return self.sock.recv(bytesize).decode(self.encoder)
    

    def close(self):
        with self.lock:
            self.sock.close()

