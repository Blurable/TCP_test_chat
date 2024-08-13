import pytest
import time
from tcp_threading_chat.client import Client


@pytest.mark.parametrize('msg', [(' '), ('iNfo'), ('qUIt'), ('MeMbErS'), ('all'), ('YOU'), ('UsErNaMe'),
                         ('123'), ('-`@'), ("''")])
def test_send(capsys, msg):
    try:
        client = Client(54321)
        time.sleep(1)
        captured = capsys.readouterr()
        assert captured.out.replace('You: ', '') == "Welcome to the chat server. Please enter your username (must contain only letters): \n"
        client.client_socket.send(msg.encode(client.encoder))
        time.sleep(1)
        captured = capsys.readouterr()
        assert captured.out.replace('You: ', '') == "Username is already in use or not valid, enter another one: \n"
        time.sleep(2)
    finally:
        client.client_socket.close()