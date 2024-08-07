import pytest
import time
import threading
from unittest.mock import Mock, patch
from tcp_threading_chat.server import ChatServer
from tcp_threading_chat.client import Client


class TestClient:
    def __init__(self):
        pass

    def run_client():
        ChatServer(54321)


def run_client(side_effect):
    client = Client(54321)
    for user_input in side_effect:
        time.sleep(2)
        client.client_socket.send(user_input.encode())


def test_clients_broadcast():
    # th0 = threading.Thread(target=run_server)
    th1 = threading.Thread(target=run_client, args=(['Baho', 'Hello', 'How are you?', '\\quit'], ))
    th2 = threading.Thread(target=run_client, args=(['Baho', 'Hello', 'How are you?', '\\quit'], ))
    th3 = threading.Timer(10, run_client, args=(['Killer', 'close_server'],))

    # th0.start()
    th1.start()
    th2.start()
    th3.start()


    # th0.join()
    th1.join()
    th2.join()
    th3.join()
