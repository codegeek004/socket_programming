import socket
import select
import time  # Added to introduce a delay

def start_server(port):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow the address to be reused immediately after the program ends
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the address and port
    server_socket.bind(('0.0.0.0', port))
    
    # Start listening for incoming connections (backlog of 5)
    server_socket.listen(5)
    
    # Set socket to non-blocking mode
    server_socket.setblocking(False)
    print(f"Server listening on port {port}")

    while True:
        try:
            # Accept connections non-blocking (will raise an error if no connection available)
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            
            # Handle client connection in non-blocking mode
            client_socket.setblocking(False)
            
            # Process the connection
            handle_client(client_socket)
        
        except BlockingIOError:
            # No connections ready to accept
            pass
        
        # Do other important work while waiting for connections
        do_other_important_work()
        
        # Add a short delay to avoid overwhelming the system with continuous loops
        time.sleep(1)  # Wait 1 second before the next iteration

def handle_client(client_socket):
    try:
        data = client_socket.recv(4096)
        if data:
            print(f"Received data: {data.decode('utf-8')}")
            client_socket.sendall(b"Server acknowledgment")
        else:
            client_socket.close()
    except BlockingIOError:
        # If no data is ready to be read, do nothing
        pass

def do_other_important_work():
    # Simulating other important work being done
    print("Doing other important work...")

if __name__ == "__main__":
    start_server(4481)

