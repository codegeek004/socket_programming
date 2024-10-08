import socket
#creating server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server socket bind where it will listen for connections
server.bind(('127.0.0.1', 5100,))






