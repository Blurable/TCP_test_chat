import socket
import threading
from time import sleep


class Client:

    def __init__(self, server_host_port, server_host_ip = socket.gethostbyname(socket.gethostname()), 
                 encoder = 'utf-8', bytesize = 1024):
        self.server_host_port = server_host_port
        self.server_host_ip = server_host_ip
        self.encoder = encoder
        self.bytesize = bytesize
        self.client_socket = None        
        self.connect_to_server()


    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_host_ip, self.server_host_port))
            print('You have connected to the chat!')            
        except Exception as e:
            print(f'Error {e} while connecting to server')
        recieve_messages = threading.Thread(target=self.recieve_messages).start()
        broadcast = threading.Thread(target=self.broadcast).start()
        

    def broadcast(self):
        try:
            while True:
                msg = input('You: ')
                self.client_socket.send(msg.encode(self.encoder))
                print(msg)
                if msg.lower() == '\\quit':
                    print('Quitting chat.')
                    break
        except Exception as e:
            print(f'Error {e} while broadcasting.')
        finally:
            self.client_socket.close()
            

    def recieve_messages(self):
        try:
            while True:
                msg = self.client_socket.recv(self.bytesize).decode(self.encoder)
                if msg:
                    print(msg)
                else:
                    print('Lost connection...')
                    sleep(1)
                    break
        except Exception as e:
            print(f'Error {e} while recieving messages')
        finally:
            self.client_socket.close()


if __name__ == '__main__':
    chat_server = Client(54321)