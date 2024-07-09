import socket

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname())
PORT = 54321

tcp_server_socket.bind((HOST, PORT))
tcp_server_socket.listen()
