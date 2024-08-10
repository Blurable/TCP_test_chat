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
        msg = self.sock.recv(bytesize).decode(self.encoder)
        if len(msg) == 0:
            raise socket.error
        return msg
    

    def close(self):
        with self.lock:
            self.sock.close()

