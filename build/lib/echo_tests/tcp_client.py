import socket

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname())
PORT = 54321

tcp_client_socket.connect((HOST, PORT))
msg = tcp_client_socket.recv(1024).decode()
print(msg)


