import socket

def send_request(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Send the request to the server
        client_socket.sendall(message.encode('utf-8'))

        # Shutdown the write side of the socket after sending the message
        client_socket.shutdown(socket.SHUT_WR)

        # Receive and print the server response
        response = b""
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break
                response += data
            except socket.error as e:
                if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                    continue
                else:
                    raise
        print("Response from server:", response.decode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Usage
host = 'localhost'
port = 4481
message = "Hello, Server!"  # Replace with the desired message
send_request(host, port, message)

