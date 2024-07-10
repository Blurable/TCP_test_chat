import socket

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 55555
ENCODER = "utf-8"
BYTESIZE = 1024
NAME = 'Server'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST_IP, HOST_PORT))
server_socket.listen()
print('Server is listening...\n')
client_socket, client_addr = server_socket.accept()
client_socket.send("You are connected to the chat!".encode(ENCODER))
client_socket.send(NAME.encode(ENCODER))
client_name = client_socket.recv(BYTESIZE).decode(ENCODER)

while True:
    msg = client_socket.recv(BYTESIZE).decode(ENCODER)

    if msg == 'quit':
        client_socket.send('quit'.encode(ENCODER))
        print('Quitting chat... goodbye!')
        break

    print(client_name+': ', msg)
    msg = input(NAME+': ')
    client_socket.send(msg.encode(ENCODER))

server_socket.close()