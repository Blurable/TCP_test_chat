import pytest
import socket
from tcp_threading_chat.server import ChatServer
import time
import multiprocessing



class Test_Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostbyname(socket.gethostname()), 54321))


def start_server():
    ChatServer(54321)


def first_client():
    client = Test_Client()
    time.sleep(1)
    client.client.send('Artyom'.encode())
    client.client.send('\\Baho'.encode())
    time.sleep(2)
    client.client.send('this is dm'.encode())
    client.client.send('\\quit'.encode())
    time.sleep(1)
    client.client.shutdown(socket.SHUT_RDWR)
    client.client.close()


def second_client():
    client = Test_Client()
    client.client.send('Baho'.encode())
    time.sleep(2)
    client.client.recv(4096)
    
    recv = client.client.recv(1024).decode()
    assert recv == 'DM from Artyom: this is dm'
    time.sleep(2)
    client.client.send('\\quit'.encode())
    time.sleep(1)
    client.client.shutdown(socket.SHUT_RDWR)
    client.client.close()



if __name__ == '__main__':
    server = multiprocessing.Process(target=start_server).start()
    time.sleep(1)
    artyom = multiprocessing.Process(target=first_client).start()
    baho = multiprocessing.Process(target=second_client).start()

