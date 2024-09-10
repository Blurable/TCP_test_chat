import socket
import threading
import re
from tcp_threading_chat.client_connection import Connection
from tcp_threading_chat.client_dict import ThreadSafeDict


class ChatServer:

    def __init__(self, host_port, host_ip = socket.gethostbyname(socket.gethostname())):
        self.host_port = host_port
        self.host_ip = host_ip
        self.clients_dict: ThreadSafeDict = ThreadSafeDict()

        self.info = ("\n\\info for possible commands\n\\members for all chat members\n"\
                    "\\username to switch to DMs\n\\all switch to all chat\n\\quit to quit chat")
        
        self.stop_server_event = threading.Event()
        self.server_socket = None
        self.start_server()


    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host_ip, self.host_port))
            self.server_socket.listen()
            print('Server is listening...\n')
        except Exception as e:
            print(f'Error: {e} while starting the server')
            self.server_close()
        while not self.stop_server_event.is_set():
            try:
                client_socket, client_addr = self.server_socket.accept()
                print(f"Accepted connection from {client_addr[0]}:{client_addr[1]}")
                client = Connection(client_socket)
                threading.Thread(target=self.client_handler, args=(client, )).start()               
            except Exception as e:
                print(f'Error {e} while accepting the client')
                client_socket.close()
        return


    def server_close(self):
        if self.server_socket:
            self.server_socket.close()
            self.stop_server_event.set()
            print('Server closed')   


    def authorize_client(self, client: Connection):
        greetings = client.send("Welcome to the chat server. Please enter your username (must contain only letters): ")
        client.send(greetings)
        while True:
            username = client.recv(self.bytesize)
            if len(username) == 0:
                print('Client has disconnected while entering username')
                raise socket.error
            if username.isalpha() and username.lower() not in ['info', 'members', 'quit', 'all', 'username', 'you']:
                client.username = username
                if self.clients_dict.add_if_not_exist(username, client):
                    print(username, 'has connected to the server', client.sock)
                    break
            not_valid = "Username is already in use or not valid, enter another one: "
            client.send(not_valid)


    def client_cleaner(self, client):
        self.clients_dict.del_item(client.username)
        client.close()


    def client_handler(self, client: Connection):
        try:
            self.authorize_client(client)
            client.send(self.info)       
        except Exception as e:
            print(f'Error {e} while handling the client')
            self.client_cleaner(client)
            return
        self.broadcast_message(f"{client.username} has joined our chat! Everyone greet him!", client)     
        
        self.receive_message(client)


    def broadcast_message(self, msg: str, cur_client: Connection):
        msg = cur_client.encode(msg)
        clients = [client for client in self.clients_dict.copy_values() if client != cur_client]
        for client in clients:
            try:
                client.send(msg)
            except Exception as e:
                print(f'Error {e} while broadcasting a message')


    def receive_message(self, client: Connection):
        try:
            receiver = None
            while True:
                try:
                    msg = client.recv()
                except Exception:
                    print(f'{client.sock} socket was closed.')
                    break
                print(client.username + ': ' + msg)

                match msg.lower():
                    case 'close_server':
                        self.server_close()
                    case '\\quit':
                        print(f'{client.username} has disconnected.')
                        break
                    case '\\info':
                        client.send(self.info)
                    case '\\members':
                        client_names = self.clients_dict.copy_keys()
                        msg = '\n'+'\n'.join(client_names)
                        client.send(msg)
                    case '\\all':
                        receiver = None
                    case _ if re.fullmatch(r'\\[a-zA-Z]+', msg):
                        username = msg[1:]
                        if username != client.username:
                            if self.clients_dict.is_contains(username):
                                try:
                                    receiver = self.clients_dict.get_item(username)
                                    client.send(f'Switched to DM with {username}')
                                except KeyError:
                                    receiver = None
                                    client.send(f'User {username} has left the chat')
                            else:
                                client.send(f'User {username} is not in the chat')
                        else:
                            client.send(f"Can't message to yourself")
                    case _:
                        if receiver:
                            msg = f'DM from {client.username}: {msg}'
                            try:
                                receiver.send(msg)
                            except Exception as e:
                                print(f'Error {e} while sending a DM')
                                receiver = None
                                client.send(f'User {username} has left the chat')
                        else:
                            msg = f'{client.username}: {msg}'           
                            self.broadcast_message(msg, client)

        except Exception as e:
            print(f'Error {e} while recieving messages from client')
        finally:
            self.client_cleaner(client)