import socket
import threading
from tcp_threading_chat.client_connection import Connection


class Client:

    def __init__(self, server_host_port, server_host_ip = socket.gethostbyname(socket.gethostname())):
        self.server_host_port = server_host_port
        self.server_host_ip = server_host_ip
        self.stop_event = threading.Event()
        self.close_client_lock = threading.Lock()
        self.connect_to_server()


    def connect_to_server(self):
        server = Connection(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        try:
            server.sock.connect((self.server_host_ip, self.server_host_port))          
        except Exception as e:
            print(f'Error {e} while connecting to server')
        threading.Thread(target=self.recieve_messages, args=(server,)).start()
        threading.Thread(target=self.broadcast, args=(server,)).start()
    

    def close_connection(self, server):
        with self.close_client_lock:
            if not self.stop_event.is_set():
                self.stop_event.set()
                server.sock.shutdown(socket.SHUT_WR)
                try:
                    while True:
                        msg = server.recv()
                        if len(msg) == 0:
                            raise socket.error
                        print(msg)
                except Exception as e:
                    print('Connection closed.', e)
                    server.sock.shutdown(socket.SHUT_RD)
                    server.close()


    def broadcast(self, server):
        try:
            while not self.stop_event.is_set():
                msg = input('You: ')
                server.send(msg)
                if msg.lower() == '\\quit':
                    print('Quitting chat...')
                    break
        except Exception as e:
            if not self.stop_event.is_set():
                print(f'Error {e} while broadcasting.')
        finally:
            self.close_connection(server)
            

    def recieve_messages(self, server):
        try:
            while not self.stop_event.is_set():
                print(dir(server))
                msg = server.recv()
                if msg:
                    print(msg)
        except Exception as e:
            if not self.stop_event.is_set():
                print(f'Error {e} while recieving messages')
        finally:
            self.close_connection(server)


if __name__ == '__main__':
    chat_server = Client(54321)