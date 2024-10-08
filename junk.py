import socket

def connect_to_google():
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Get the remote address (google.com) and port (80)
        remote_addr = ('google.com', 80)
        
        # Connect to the remote server
        sock.connect(remote_addr)
        
        print(f"Connected to {remote_addr[0]} on port {remote_addr[1]}")

if __name__ == "__main__":
    connect_to_google()
