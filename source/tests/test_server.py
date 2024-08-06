import pytest
from tcp_threading_chat.server import ChatServer
from tcp_threading_chat.client import Client


def test_launch_server():
    chat_server = ChatServer(54321)


def test_launch_client():
    Artyom = Client(55555)
    Baho = Client(44444)
    Artyom.send('Artyom')
    Baho.send('Baho')
    Artyom.send('wtf')
    Baho.send('ftw')
