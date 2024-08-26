import pytest
import time
import socket
from tcp_threading_chat.client import Client


@pytest.mark.parametrize('msg', [(' '), ('iNfo'), ('qUIt'), ('MeMbErS'), ('all'), ('YOU'), ('UsErNaMe'),
                         ('123'), ('-`@'), ("''")])
def test_send(capsys, msg):
    client = Client(54321)
    captured = capsys.readouterr()
    assert captured.out.replace('You: ', '') == "Welcome to the chat server. Please enter your username (must contain only letters): \n"
    client.client.send(msg)
    captured = capsys.readouterr()
    assert captured.out.replace('You: ', '') == "Username is already in use or not valid, enter another one: \n"
    client.close_connection()