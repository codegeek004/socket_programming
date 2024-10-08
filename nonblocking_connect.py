import socket
import errno
import select

def nonblocking_connect(host, port):
    # Create a non-blocking TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)  # Set the socket to non-blocking mode
    
    # Get the remote address for the specified host and port
    remote_addr = (host, port)

    try:
        # Initiate the non-blocking connection
        sock.connect(remote_addr)
    except BlockingIOError as e:
        if e.errno == errno.EINPROGRESS:
            print("Connection in progress...")
        elif e.errno == errno.EALREADY:
            print("A previous non-blocking connect is already in progress.")
        elif e.errno == errno.ECONNREFUSED:
            print("Connection refused by the server.")
        else:
            print(f"Unexpected error: {e}")

    # Use select to wait for the connection to be ready
    _, writable, _ = select.select([], [sock], [], 5)  # 5-second timeout

    if writable:
        print("Connected to the server successfully.")
    else:
        print("Connection timed out.")

    return sock

if __name__ == "__main__":
    # Usage example
    nonblocking_connect('google.com', 80)

