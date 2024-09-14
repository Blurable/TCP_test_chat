import pytest
from tcp_threading_chat.server import ChatServer
from tcp_threading_chat.client import Client
import threading
import time
from queue import Queue


creation_queue = Queue()
remove_user = Queue()
nicknames = ['Baho', 'Vlados', 'Poteha']
server = None


def start_client():
    client = Client(54321)
    client.connect_to_server()
    client.close_connection()


def server():
    global server
    server = ChatServer(54321)
    server.start_server()


def test_server():
    threading.Thread(target=server).start()
    for i in range(3):
        threading.Thread(target=start_client).start()
    assert not server.stop_server_event.is_set()

