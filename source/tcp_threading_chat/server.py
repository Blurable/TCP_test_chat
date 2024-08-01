import socket
import threading
import re
from tcp_threading_chat.client_connection import Connection
from tcp_threading_chat.client_dict import ThreadSafeDict

class ChatServer:

    def __init__(self, host_port, host_ip = socket.gethostbyname(socket.gethostname()), 
                 encoder = 'utf-8'):
        self.host_port = host_port
        self.host_ip = host_ip
        self.encoder = encoder
        self.clients_dict: ThreadSafeDict = ThreadSafeDict()

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
                client = Connection(client_socket, None)
                threading.Thread(target=self.client_handler, args=(client, )).start()
            except Exception as e:
                print(f'Error {e} while accepting the client')
                client_socket.close()


    def authorize_client(self, client: Connection):
        client.send("Welcome to the chat server. Please enter your username (must contain only letters): ".encode(self.encoder))
        while True:
            username = client.recv(1024).decode(self.encoder)
            if username.isalpha() and username.lower() not in ['info', 'members', 'quit', 'all', 'username', 'you']:
                client.username = username
                if self.clients_dict.add_if_not_exist(username, client):
                    print(username, 'has connected to the server', client.sock)
                    break
            client.send("Username is already in use or not valid, enter another one: ".encode(self.encoder))
        return client

    
    
    def client_cleaner(self, client):
        del self.clients_dict[client.username]
        client.close()


    def client_handler(self, client: Connection):
        try:
            client = self.authorize_client(client)
        except Exception as e:
            print(f'Error {e} while authorizing the client')
            client.close()
            return
        
        try:
            self.send_message(self.info, [client])
            clients = [connection for connection in self.clients_dict.copy_values() if connection != client]
            self.send_message(f"{client.username} has joined our chat! Everyone greet him!", clients)
            
            self.receive_message(client)
        except Exception as e:
            print(f'Error {e} while handling the client')
            self.client_cleaner(client)
            

    def broadcast_message(self, msg: str, clients: list[Connection]):
        for client in clients:
            try:
                client.send(msg)
            except Exception as e:
                print(f'Error {e} while broadcasting a message')
                self.client_cleaner(client)


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
                        client_names = self.clients_dict.copy_keys()
                        msg = '\n'+'\n'.join(client_names)
                        self.send_message(msg, [client])
                    case '\\all':
                        receiver = None
                    case msg if re.fullmatch(r'\\[a-zA-Z]+', msg):
                        username = msg[1:]
                        if username != client.username:
                            if username in self.clients_dict:
                                receiver = self.clients_dict[username]
                    case _:
                        if receiver:
                            msg = f'DM from {client.username}: {msg}'
                            self.send_message(msg, [receiver])
                        else:
                            msg = f'{client.username}: {msg}'            
                            clients = self.clients_dict.copy_values()
                            self.send_message(msg, clients)

        except Exception as e:
            print(f'Error {e} while recieving messages from client')
        finally:
            self.client_cleaner(client)
