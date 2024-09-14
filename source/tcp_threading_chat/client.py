import socket
import threading
from tcp_threading_chat.communication_manager import CommunicationManager


class Client:

    def __init__(self, server_host_port, server_host_ip = socket.gethostbyname(socket.gethostname())):
        self.server_host_port = server_host_port
        self.server_host_ip = server_host_ip
        self.stop_event = threading.Event()
        self.close_client_lock = threading.Lock()
        self.server = None


    def connect_to_server(self):
        self.server = CommunicationManager(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        try:
            self.server.sock.connect((self.server_host_ip, self.server_host_port))          
        except Exception as e:
            print(f'Error {e} while connecting to server')

        threading.Thread(target=self.receive_messages).start()
        threading.Thread(target=self.broadcast).start()
    

    def close_connection(self):
        with self.close_client_lock:
            if not self.stop_event.is_set():
                self.stop_event.set()
                try:
                    self.server.sock.shutdown(socket.SHUT_RDWR)
                except Exception as e:
                    print(f'Error {e} while shutting down.')
                finally:
                    self.server.close()


    def broadcast(self):
        try:
            while not self.stop_event.is_set():
                msg = input('You: ')
                self.server.send(msg)
                if msg.lower() == '\\quit':
                    print('Quitting chat...')
                    break
        except Exception as e:
            if not self.stop_event.is_set():
                print(f'Error {e} while broadcasting.')
        finally:
            self.close_connection()
            

    def receive_messages(self):
        try:
            while not self.stop_event.is_set():
                msg = self.server.recv()
                print(msg)
        except Exception as e:
            if not self.stop_event.is_set():
                print(f'Error {e} while recieving messages')
        finally:
            self.close_connection()


if __name__ == '__main__':
    chat_server = Client(54321)
    chat_server.connect_to_server()