import pytest
from tcp_threading_chat.client import Client
import time


def test_client():
    client = Client(54321)
    client.connect_to_server()
    client.server.send('Artyom')
    time.sleep(1)
    msgs = ["Welcome to the chat server. Please enter your username (must contain only letters): ", 
                           "\n\\info for possible commands\n\\members for all chat members\n"\
                    "\\username to switch to DMs\n\\all switch to all chat\n\\quit to quit chat"]
    assert msgs == client.server.storage.all_messages
