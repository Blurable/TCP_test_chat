import pytest
from tcp_threading_chat.client import Client
import time

@pytest.mark.parametrize('msg', [
                        (''),
                        (' '), 
                        ('iNfo'), 
                        ('qUIt'), 
                        ('MeMbErS'), 
                        ('all'), 
                        ('YOU'), 
                        ('UsErNaMe'),
                        ('123'), 
                        ('-`@'), 
                        ("''")
                        ])
def test_client(msg):
    client = Client(54321)
    client.connect_to_server()
    client.server.send(msg)
    time.sleep(1)
    assert client.server.storage.all_messages[-1] == "Username is already in use or not valid, enter another one: "
    client.close_connection()

    
    
