import socket

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        
        # Handle the client connection
        handle_client(client_socket)

def handle_client(client_socket):
    try:
        response = b""
        
        while True:
            data = client_socket.recv(4096)  # Receive data in chunks
            if data:
                print(f"Received {len(data)} bytes: {data.decode('utf-8', errors='ignore')}")
                response += data
            else:
                print("Client finished sending data.")
                break  # No more data, client finished sending
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Client connection closed.")

if __name__ == "__main__":
    start_server(4481)

