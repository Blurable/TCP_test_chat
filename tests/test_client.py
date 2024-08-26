import pytest
import time
import threading
import socket
from tcp_threading_chat.server import ChatServer
from tcp_threading_chat.client import Client
 

class TestClient:
    def __init__(self, server_host_port, snd, rcv, server_host_ip = socket.gethostbyname(socket.gethostname()), 
                 encoder = 'utf-8', bytesize = 1024):
        self.server_host_port = server_host_port
        self.server_host_ip = server_host_ip
        self.encoder = encoder
        self.bytesize = bytesize
        self.client_socket = None
        self.stop_event = threading.Event()    
        self.snd = snd
        self.rcv = rcv
        self.test_connect_to_server()

    def test_connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_host_ip, self.server_host_port))           
        except Exception as e:
            print(f'Error {e} while connecting to server')
        self.test_snd_rcv()
     

    def test_snd_rcv(self):
        rec = self.client_socket.recv(self.bytesize).decode(self.encoder)
        assert rec == self.rcv[0]
        print(f'\033[31m{rec}\033[0m')
        time.sleep(1)
        self.client_socket.send(self.snd[0].encode(self.encoder))
        rec = self.client_socket.recv(self.bytesize).decode(self.encoder)
        assert rec == self.rcv[1]
        print(f'\033[31m{rec}\033[0m')
        names = ['Art', 'Bob', 'Bah', 'Vlad', 'Diman']
        time.sleep(20)
        rec = self.client_socket.recv(self.bytesize)
        print(f'\033[31m{rec}\033[0m')
        self.client_socket.send('\\members'.encode(self.encoder))
        rec = self.client_socket.recv(self.bytesize).decode(self.encoder)
        print('\033[31m'+rec+"\033[0m")
        assert rec == '\n' + '\n'.join(['Baho'] + names)
        self.client_socket.send('\\Art'.encode(self.encoder))
        rec = self.client_socket.recv(self.bytesize).decode(self.encoder)
        assert rec == 'Switched to DM with Art'
        self.client_socket.send('Hello'.encode(self.encoder))
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()

        
def run_client(name):
    client = Client(54321)
    time.sleep(1)
    client.client.send(name)


def run_test_client(snd, rcv):
    TestClient(54321, snd, rcv)


def test_clients_broadcast():
    threading.Thread(target=run_test_client, args=(['Baho'], ["Welcome to the chat server."\
                    " Please enter your username (must contain only letters): ", "\n\\info for possible commands\n\\members for all chat members\n"\
                    "\\username to switch to DMs\n\\all switch to all chat\n\\quit to quit chat"],)).start()
    time.sleep(6)
    for i in range(5):
        names = ['Art', 'Bob', 'Bah', 'Vlad', 'Diman']
        run_client(names[i])
    
    
    
test_clients_broadcast()




