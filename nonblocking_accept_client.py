import socket

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Send some data
    payload = "Hello from the client!"
    client_socket.sendall(payload.encode('utf-8'))
    
    # Wait for a response from the server
    response = client_socket.recv(4096)
    print(f"Response from server: {response.decode('utf-8')}")
    
    client_socket.close()

if __name__ == "__main__":
    host = 'localhost'
    port = 4481
    start_client(host, port)

