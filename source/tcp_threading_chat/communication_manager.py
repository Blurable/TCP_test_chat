import socket
import threading
from tcp_threading_chat.msg_protocol import MsgProtocol
from tcp_threading_chat.msg_storage import Storage

class CommunicationManager:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.username = ''
        self.sendlock = threading.Lock()
        self.recvlock = threading.Lock()
        self.protocol = MsgProtocol()
        self.storage = Storage()
        

    def encode(self, msg):
        return self.protocol.pack(msg)


    def send(self, msg):
        if type(msg) != bytes:
            msg = self.encode(msg)
        with self.sendlock:
            self.sock.sendall(msg)

    
    def recv(self):
        info = self.sock_recv(5)
        if len(info) != 5:
            print('error in con.recv')
            raise ValueError
        command_id, msg_length = self.protocol.unpack(info)
        if command_id != 0:
            return self.protocol.decode_command(command_id)
        return self.msg_recv(msg_length)


    def msg_recv(self, msg_length):
        final_msg = b''
        bytes_received = 0
        while bytes_received < msg_length:
            msg = self.sock_recv(min(self.protocol.bytesize, msg_length))
            final_msg += msg
            bytes_received += len(msg)
        final_msg = self.protocol.decode(final_msg)
        self.storage.put(final_msg)
        return final_msg
    

    def sock_recv(self, bytesize):
        msg = self.sock.recv(bytesize)
        if len(msg) == 0:
            print('socket closed')
            raise socket.error
        return msg


    def close(self):
        self.sock.close()