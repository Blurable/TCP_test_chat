import socket
import threading
from tcp_threading_chat.client_connection import Connection


class Client:

    def __init__(self, server_host_port, server_host_ip = socket.gethostbyname(socket.gethostname())):
        self.server_host_port = server_host_port
        self.server_host_ip = server_host_ip
        self.bytesize = 1024
        self.client = None
        self.stop_event = threading.Event()
        self.close_client_lock = threading.Lock()
        


    def connect_to_server(self):
        self.client = Connection(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        try:
            self.client.sock.connect((self.server_host_ip, self.server_host_port))          
        except Exception as e:
            print(f'Error {e} while connecting to server')
        threading.Thread(target=self.recieve_messages).start()
        threading.Thread(target=self.broadcast).start()
    

    def close_connection(self):
        with self.close_client_lock:
            if not self.stop_event.is_set():
                self.stop_event.set()
                self.client.sock.shutdown(socket.SHUT_WR)
                try:
                    while True:
                        msg = self.client.recv(self.bytesize)
                        if len(msg) == 0:
                            raise socket.error
                        print(msg)
                except Exception as e:
                    print('Connection closed.', e)
                    self.client.sock.shutdown(socket.SHUT_RD)
                    self.client.close()


    def broadcast(self):
        try:
            while not self.stop_event.is_set():
                msg = input('You: ')
                self.client.send(msg)
                if msg.lower() == '\\quit':
                    print('Quitting chat...')
                    break
        except Exception as e:
            if not self.stop_event.is_set():
                print(f'Error {e} while broadcasting.')
        finally:
            self.close_connection()
            

    def recieve_messages(self):
        try:
            while not self.stop_event.is_set():
                msg = self.client.recv(self.bytesize)
                if msg:
                    print(msg)
        except Exception as e:
            if not self.stop_event.is_set():
                print(f'Error {e} while recieving messages')
        finally:
            self.close_connection()


if __name__ == '__main__':
    chat_server = Client(54321)