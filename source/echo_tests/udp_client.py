import socket

udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345

udp_client_socket.sendto('Hello server'.encode(), (HOST, PORT))