import socket
import ssl

def ssl_client():
    # Create an SSL context for the client
    ctx = ssl.create_default_context()

    # Load the server's self-signed certificate to trust it
    ctx.load_verify_locations('server_cert.pem')  # Trust the server's certificate
    ctx.check_hostname = False  # Skip hostname checking
    ctx.verify_mode = ssl.CERT_REQUIRED  # Require certificate validation

    # Connect to the SSL server
    conn = ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname='localhost')
    conn.connect(('localhost', 4481))

    # Receive and print the message from the server
    message = conn.recv(1024)
    print(f"Received from server: {message.decode()}")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    ssl_client()

