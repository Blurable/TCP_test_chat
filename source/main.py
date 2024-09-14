from tcp_threading_chat.server import ChatServer

if __name__ == '__main__':
    chat_server = ChatServer(54321)
    chat_server.start_server()