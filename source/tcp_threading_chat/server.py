import socket
import threading
import re


class ChatServer:

    def __init__(self, host_port, host_ip = socket.gethostbyname(socket.gethostname()), 
                 encoder = 'utf-8', bytesize = 1024):
        self.host_port = host_port
        self.host_ip = host_ip
        self.encoder = encoder
        self.bytesize = bytesize
        self.clients_dict: dict = {}
        self.client_choice: dict = {}

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
                client_handler = threading.Thread(target=self.client_handler, args=(client_socket,))
                client_handler.start()
            except Exception as e:
                print(f'Error {e} while accepting the client')
                client_socket.close()


    def client_handler(self, client_socket):
        try:
            client_socket.send("Welcome to the chat server. Please enter your username (must contain only letters): ".encode(self.encoder))
            username = client_socket.recv(self.bytesize).decode(self.encoder)

            while username in self.clients_dict or not username.isalpha() or username.lower() in ['info', 'members', 'quit', 'all', 'username', 'you']:
                client_socket.send("Username is already in use or not valid, enter another one: ".encode(self.encoder))
                username = client_socket.recv(self.bytesize).decode(self.encoder)

            self.clients_dict[username] = client_socket
            self.client_choice[username] = None
            client_socket.send("You are conneced to the chat!".encode(self.encoder))
            for client in self.clients_dict:
                if client != username:
                    self.clients_dict[client].send(f"{username} has joined our chat! Everyone greet him!".encode(self.encoder))
            
            client_socket.send('''\\info for possible commands\n \\members for all chat members\n 
                            \\username to switch to DMs\n \\all switch to all chat\n \\quit quit chat'''.encode(self.encoder))
            
            recieve_message = threading.Thread(target = self.recieve_message, args = username)
            recieve_message.start()
        except Exception as e:
            print(f'Error {e} while handling the client')
            client_socket.close()
            

    def broadcast_message(self, msg: str, client_name):
        try:
            msg = f'{client_name}: {msg}'.encode(self.encoder)
            if client_name in self.client_choice:
                reciever = self.client_choice[client_name]
            if reciever in self.clients_dict:
                self.clients_dict[reciever].send(msg)
            elif reciever is None and len(self.clients_dict)>1 :
                for client in self.clients_dict:
                    if client != client_name:
                        self.clients_dict[client].send(msg)
            else:
                self.clients_dict[client_name].send('Error occured while sending a message or you are alone in the chat.')

        except Exception as e:
            print(f'Error {e} while broadcasting a message')


    def recieve_message(self, client_name: str):
        client_socket = self.clients_dict[client_name]
        username_pattern = r'\\[a-zA-Z]+'
        allchat_pattern = r'\\all'
        try:
            while True:
                msg = client_socket.recv(self.bytesize).decode(self.encoder)
                username_match = re.fullmatch(username_pattern, msg)
                allchat_match = re.fullmatch(allchat_pattern, msg)
                if username_match:
                    username = username_match.group()[1:]
                    self.client_choice[client_name] = username
                elif allchat_match:
                    self.client_choice[client_name] = None
                else:
                    match msg.lower():
                        case '\\quit':
                            msg = f'{client_name} has disconnected.'
                            self.broadcast_message(msg, client_name)
                            del self.clients_dict[client_name]
                        case '\\info':
                            client_socket.send('\\info for possible commands\n\\members for all chat members\n\\username to switch to DMs\n\\all switch to all chat\n\\quit quit chat'.encode(self.encoder))
                        case '\\members':
                            clients = ''
                            for client_name in self.clients_dict:
                                clients += client_name + '\n'
                            client_socket.send(clients.encode(self.encoder))
                        case _:
                            self.broadcast_message(msg, client_name)
        except Exception as e:
            print(f'Error {e} while recieving messages from client')
        finally:
            del self.clients_dict[client_name]
            del self.client_choice[client_name]
            client_socket.close()


if __name__ == '__main__':
    chat_server = ChatServer(54321)