import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('localhost', 4481))
client_socket.sendall(b"gekko")
client_socket.close()
