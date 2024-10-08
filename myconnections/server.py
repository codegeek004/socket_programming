import socket 
one_kb = 1024
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 4481))
server_socket.listen(5)
while True:
    connection, _ = server_socket.accept()
    while True:
        data = connection.recv(one_kb)
        if not data:
            break
        print(data.decode())
    connection.close




