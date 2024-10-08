import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5100))
server.listen(socket.SOMAXCONN)
#accept new connection
connection, client_address = server.accept()
print("Connection class: ", type(connection))
print("Server fileNo: ", server.fileno())
print("Connection fileNo: ", connection.fileno())
print("Local Address: ", connection.getsockname())
print("Remote address: ", client_address)



