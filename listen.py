import socket 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server listening for incoming connections
server.listen(5)
