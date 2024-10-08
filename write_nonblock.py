import socket
import select

def handle_client(client_socket):
    # Non-blocking read from the client
    response = b""
    while True:
        try:
            data = client_socket.recv(4096)  # Read in chunks of 4096 bytes
            if not data:
                break
            print(f"Received {len(data)} bytes")
            response += data
        except BlockingIOError:
            # If the operation would block, use select to wait for data
            select.select([client_socket], [], [])
            continue
        except Exception as e:
            print(f"Error: {e}")
            break

    if response:
        print(f"Total received: {len(response)} bytes")
        # Echo the response back to the client
        client_socket.sendall(b"Server received your data")
    else:
        client_socket.sendall(b"No data received")

    client_socket.close()

def server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.setblocking(False)  # Set to non-blocking mode
        handle_client(client_socket)

# Start the server
if __name__ == "__main__":
    server(4481)

