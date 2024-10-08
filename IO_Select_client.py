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

        # Receive the response from the server
        response = b""
        while True:
            try:
                data = client_socket.recv(4096)
                if not data:
                    break  # If no more data, break the loop
                response += data
            except socket.error as e:
                if e.errno == socket.errno.EAGAIN or e.errno == socket.errno.EWOULDBLOCK:
                    continue  # Non-blocking wait
                else:
                    raise  # Re-raise any other socket errors

        # Print the full response from the server
        print("Response from server:", response.decode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Usage Example
if __name__ == '__main__':
    host = 'localhost'  # The server address
    port = 4481          # The server port
    message = "Hello, Server!"  # Message to send to the server
    
    send_request(host, port, message)

