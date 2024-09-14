import pytest
from tcp_threading_chat.server import ChatServer
from tcp_threading_chat.client import Client
import threading
import time


def start_server():
    server = ChatServer(54321)
    server.start_server()


@pytest.fixture(scope='session', autouse=True)
def test_client():
    threading.Thread(target=start_server, daemon=True).start()

    



