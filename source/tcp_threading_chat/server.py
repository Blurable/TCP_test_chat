import socket
import threading
import re
from tcp_threading_chat.client_connection import Connection


class ChatServer:

    def __init__(self, host_port, host_ip = socket.gethostbyname(socket.gethostname()), 
                 encoder = 'utf-8'):
        self.host_port = host_port
        self.host_ip = host_ip
        self.encoder = encoder
        self.clients_dict: dict = {}
        self.clients_lock = threading.Lock()

        self.info = "\n\\info for possible commands\n\\members for all chat members\n"\
                    "\\username to switch to DMs\n\\all switch to all chat\n\\quit to quit chat"

        self.start_server()


    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self.host_ip, self.host_port))
            server_socket.listen()
            print('Server is listening...\n')
        except Exception as e:
            print(f'Error: {e} while starting the server')
            server_socket.close()

        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                print(f"Accepted connection from {client_addr[0]}:{client_addr[1]}")
                client_handler = threading.Thread(target=self.client_handler, args=(client_socket, ))
                client_handler.start()
            except Exception as e:
                print(f'Error {e} while accepting the client')
                client_socket.close()


    def authorize_client(self, client: socket.socket):
        try:
            client.send("Welcome to the chat server. Please enter your username (must contain only letters): ".encode(self.encoder))
            while True:
                username = client.recv(1024).decode(self.encoder)
                if username.isalpha() and username.lower() not in ['info', 'members', 'quit', 'all', 'username', 'you']:
                    client = Connection(client, username)
                    with self.clients_lock:
                        if username not in self.clients_dict:
                            self.clients_dict[username] = client
                            break
                client.send("Username is already in use or not valid, enter another one: ".encode(self.encoder))
            return client
        except Exception as e:
            pass
    
    
    def client_cleaner(self, client):
        with self.clients_lock:
            if client.username in self.clients_dict:
                del self.clients_dict[client.username]
        client.close()


    def client_handler(self, client: Connection):
        try:
            client = self.authorize_client(client)
            self.send_message(self.info, [client])
            with self.clients_lock:
                clients = [connection for connection in self.clients_dict.values() if connection != client]
            self.send_message(f"{client.username} has joined our chat! Everyone greet him!", clients)
            
            self.receive_message(client)
        except Exception as e:
            print(f'Error {e} while handling the client')
            self.client_cleaner(client)
            

    def send_message(self, msg: str, clients: list[Connection]):
        try:
            for client in clients:
                client.send(msg)
        except Exception as e:
            print(f'Error {e} while broadcasting a message')


    def receive_message(self, client: Connection):
        try:
            receiver = None
            while True:
                msg = client.recv()
                print(client.username + ': ' + msg)

                match msg.lower():
                    case '\\quit':
                        print(f'{client.username} has disconnected.')
                        break
                    case '\\info':
                        self.send_message(self.info, [client])
                    case '\\members':
                        with self.clients_lock:
                            client_names = list(self.clients_dict.keys())
                        msg = '\n'+'\n'.join(client_names)
                        self.send_message(msg, [client])
                    case '\\all':
                        receiver = None
                    case msg if re.fullmatch(r'\\[a-zA-Z]+', msg):
                        username = msg[1:]
                        with self.clients_lock:
                            if username != client.username and username in self.clients_dict.keys():
                                receiver = self.clients_dict[username]
                    case _:
                        if receiver:
                            msg = f'DM from {client.username}: {msg}'
                            self.send_message(msg, [receiver])
                        else:
                            with self.clients_lock:
                                msg = f'{client.username}: {msg}'            
                                clients = list(self.clients_dict.values())
                            self.send_message(msg, clients)

        except Exception as e:
            print(f'Error {e} while recieving messages from client')
        finally:
            self.client_cleaner(client)
