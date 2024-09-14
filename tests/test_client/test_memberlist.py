import pytest
from tcp_threading_chat.server import ChatServer
from tcp_threading_chat.client import Client
import threading
import time
from queue import Queue


creation_queue = Queue()
dc_queue = Queue()


def start_client(id):
    client = Client(54321)
    nicknames = ['Baho', 'Vlados', 'Poteha']
    client.connect_to_server()
    client.server.send(nicknames[id])
    while True:
        if len(client.server.storage.all_messages)>=2:
            creation_queue.put('ready')
            break

    dc_queue.get()
    client.close_connection()


def test_client():
    for i in range(3):
        threading.Thread(target=start_client, args=(i,)).start()
        creation_queue.get()
    client = Client(54321)
    client.connect_to_server()
    client.server.send('Artyom')
    client.server.send('\\members')

    time.sleep(1)
    assert '\nBaho\nVlados\nPoteha\nArtyom' == client.server.storage.all_messages[-1]
 
    dc_queue.put('ready')
    time.sleep(1)
    client.server.send('\\members')
    time.sleep(1)
    assert '\nVlados\nPoteha\nArtyom' == client.server.storage.all_messages[-1]