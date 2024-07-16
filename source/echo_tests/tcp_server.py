import socket

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname())
PORT = 54321

tcp_server_socket.bind((HOST, PORT))
tcp_server_socket.listen()

while True:
    client_socket, client_adress = tcp_server_socket.accept()
    print(type(client_socket))
    print(client_socket)
    print(type(client_adress))
    print(client_adress)

    print(f'Connected to {client_socket}')
    client_socket.send("You are connected!".encode())
    