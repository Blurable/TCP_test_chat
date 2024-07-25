import socket
import threading
import re
from client_connection import Connection


class ChatServer:

    def __init__(self, host_port, host_ip = socket.gethostbyname(socket.gethostname()), 
                 encoder = 'utf-8', bytesize = 1024):
        self.host_port = host_port
        self.host_ip = host_ip
        self.encoder = encoder
        self.bytesize = bytesize
        self.clients_dict: dict = {}
        self.clients_lock = threading.RLock()
        self.choice_lock = threading.RLock()

        self.start_server()


    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self.host_ip, self.host_port))
            server_socket.listen(5)
            print('Server is listening...\n')
        except Exception as e:
            print(f'Error: {e} while starting the server')
            server_socket.close()

        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                print(f"Accepted connection from {client_addr[0]}:{client_addr[1]}")
                client = Connection(client_socket)
                client_handler = threading.Thread(target=self.client_handler, args=(client, ))
                client_handler.start()
            except Exception as e:
                print(f'Error {e} while accepting the client')
                client_socket.close()


    def client_handler(self, client: Connection):
        try:
            client.send("Welcome to the chat server. Please enter your username (must contain only letters): ")
            username = client.recv()

            with self.clients_lock:
                usernames = list(self.clients_dict.keys())

            while not username.isalpha() or username.lower() in ['info', 'members', 'quit', 'all', 'username', 'you'] or username in usernames:
                client.send("Username is already in use or not valid, enter another one: ")
                username = client.recv()
            client.send("You are conneced to the chat!")

            self.broadcast_message(f"{username} has joined our chat! Everyone greet him!")
            self.broadcast_message('''\n\\info for possible commands\n\\members for all chat members\n\\username to switch to DMs
                                   \\all switch to all chat\n\\quit quit chat''')
            
            self.recieve_message(username)
        except Exception as e:
            print(f'Error {e} while handling the client')
            with self.clients_lock:
                if username in self.clients_dict:
                    del self.clients_dict[username]
            client_socket.close()
            

    def broadcast_message(self, msg: str, client_name, reciever_name): #reciever_name = None for allchat
        try:

            with self.clients_lock:
                client_socket = self.clients_dict[client_name]
                reciever_socket = self.clients_dict[reciever_name]
                clients_sockets = [value for value in self.clients_dict.values()]

            client_socket.send(f'You: {msg}'.encode(self.encoder))

            if reciever_socket in clients_sockets:
                reciever_socket.send(f'{client_name}: {msg}'.encode(self.encoder))
            elif reciever_name is None and len(clients_sockets)>1:
                for socket in clients_sockets:
                    if socket != client_socket:
                        socket.send(f'{client_name}: {msg}'.encode(self.encoder))
            elif reciever_name and reciever_name not in clients_sockets:
                client_socket.send('User is not in the chat.'.encode(self.encoder))
            else:
                client_socket.send('Error occured while sending a message or you are alone in the chat.'.encode(self.encoder))

        except Exception as e:
            print(f'Error {e} while broadcasting a message')


    def recieve_message(self, client_name: str):
        try:
            client_socket = self.clients_dict[client_name]
            username_pattern = r'\\[a-zA-Z]+'
            allchat_pattern = r'\\all'
            reciever_name = None
            while True:
                msg = client_socket.recv(self.bytesize).decode(self.encoder)
                print(client_name + ': ' + msg)

                match msg.lower():
                    case '\\quit':
                        with self.clients_lock:
                            del self.clients_dict[client_name]
                        print(f'{client_name} has disconnected.')
                        break
                    case '\\info':
                        client_socket.send('\n\\info for possible commands\n\\members for all chat members\n\\username to switch to DMs\n\\all switch to all chat\n\\quit quit chat'.encode(self.encoder))
                    case '\\members':
                        with self.clients_lock:
                            keys_copy = list(self.clients_dict.keys())
                        clients = '\n'
                        for client_name in keys_copy:
                            clients += client_name + '\n'
                        client_socket.send(clients.encode(self.encoder))
                    case _:
                        username_match = re.fullmatch(username_pattern, msg)
                        allchat_match = re.fullmatch(allchat_pattern, msg)
                        if allchat_match:
                            reciever_name = None
                        elif username_match:
                            reciever_name = username_match.group()[1:]
                        else:
                            self.broadcast_message(msg, client_name, reciever_name)
        except Exception as e:
            print(f'Error {e} while recieving messages from client')
        finally:
            with self.clients_lock:
                if client_name in self.clients_dict:
                    del self.clients_dict[client_name]
            client_socket.close()
