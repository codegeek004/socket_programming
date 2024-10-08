import socket
import errno

def tcp_server_loop(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Listening on port {port}")

    while True:
        connection, address = server_socket.accept()
        print(f"Connection from {address}")
        connection.setblocking(False)  # Set to non-blocking mode

        try:
            while True:
                try:
                    # Read non-blocking
                    data = connection.recv(4096).decode('utf-8')
                    if not data:
                        break  # EOF or empty data, close connection
                    print(f"Received from client: {data}")
                    
                    # Send response back to client
                    response = f"Server received, {data}"
                    connection.sendall(response.encode('utf-8'))
                except socket.error as e:
                    if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                        # Resource temporarily unavailable, retry
                        continue
                    else:
                        raise
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()

# Start the server
tcp_server_loop(4481)

