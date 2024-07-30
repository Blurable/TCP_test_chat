import socket

udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

udp_server_socket.bind((HOST, PORT))

msg, addr = udp_server_socket.recvfrom(1024)
print(addr)
print(msg.decode())

