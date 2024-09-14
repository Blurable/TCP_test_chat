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


def start_client(id):
    client = Client(54321)
    client.connect_to_server()
    client.server.send(nicknames[id])
    while True:
        if len(client.server.storage.all_messages)>=2:
            creation_queue.put('ready')
            break
    remove_user.get()
    client.close_connection()


def server():
    global server
    server = ChatServer(54321)
    server.start_server()


def test_server():
    threading.Thread(target=server).start()
    for i in range(3):
        threading.Thread(target=start_client, args=(i,)).start()
        creation_queue.get()

    assert len(server.clients_dict.dictionary) == 3
    for nickname in nicknames:
        assert server.clients_dict.is_contains(nickname)

    remove_user.put('ready')
    remove_user.put('ready')
    while True:
        if len(server.clients_dict.dictionary) == 1:
            break
    assert len(server.clients_dict.dictionary) == 1
    assert server.clients_dict.is_contains('Poteha')
