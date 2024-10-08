import socket
import select

def read_nonblock(connection):
    response = b""
    while True:
        try:
            # Try to receive data from the connection
            data = connection.recv(4096)
            if data:
                print(f"Received: {data.decode('utf-8')}")
                response += data
            else:
                # If no data is received, the connection might be closed
                print("Connection closed by peer")
                break
        except socket.error as e:
            # Handle non-blocking read with EAGAIN or EWOULDBLOCK
            if e.errno == socket.errno.EAGAIN or e.errno == socket.errno.EWOULDBLOCK:
                # Wait until the connection is ready for reading using select
                select.select([connection], [], [])
                # Retry the recv call
                continue
            else:
                # Handle other socket errors
                print(f"Socket error: {e}")
                break

    # After reading the request, send a response to the client
    if response:
        connection.sendall(b"Server received: " + response)
    else:
        connection.sendall(b"No data received from client.")
    
    connection.close()

# Example server setup
def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Listening on port {port}")

    while True:
        connection, address = server_socket.accept()
        print(f"Connection from {address}")
        connection.setblocking(False)  # Set to non-blocking mode
        read_nonblock(connection)

# Start the server
server(4481)

