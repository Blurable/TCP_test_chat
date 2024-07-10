import socket

HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 55555
ENCODER = "utf-8"
BYTESIZE = 1024
NAME = 'Artyom'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, HOST_PORT))
client_socket.send(NAME.encode(ENCODER))
connection = client_socket.recv(BYTESIZE).decode(ENCODER)
print(connection)
server_name = client_socket.recv(BYTESIZE).decode(ENCODER)


while True:
    msg = input(NAME+': ')
    client_socket.send(msg.encode(ENCODER))

    msg = client_socket.recv(BYTESIZE).decode(ENCODER)

    if msg == 'quit':
        client_socket.send('quit'.encode(ENCODER))
        print('Quitting chat... goodbye!')
        break
    print(server_name+': ', msg)

client_socket.close()

