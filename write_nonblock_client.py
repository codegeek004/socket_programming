import socket
import errno
import select

def send_large_payload(host, port, payload):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)  # Non-blocking mode

    try:
        # Initiate the connection to the server
        client_socket.connect((host, port))
    except BlockingIOError:
        pass  # It's fine if this raises BlockingIOError since it's non-blocking

    # Wait for the connection to complete
    select.select([], [client_socket], [])

    total_sent = 0
    payload_size = len(payload)

    while total_sent < payload_size:
        try:
            # Send data in non-blocking mode
            sent = client_socket.send(payload[total_sent:].encode('utf-8'))
            total_sent += sent
            print(f"Sent {sent} bytes, Total sent: {total_sent}/{payload_size} bytes")
        except socket.error as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                raise  # Re-raise any other socket errors
            # Use select to wait until the socket is ready to send again
            select.select([], [client_socket], [])
    
    print("Full payload sent.")

    # Receive response from the server
    response = b""
    while True:
        try:
            data = client_socket.recv(4096)  # Receive server's response
            if not data:
                break
            response += data
        except BlockingIOError:
            # If there's no data, wait for the server to send
            select.select([client_socket], [], [])
            continue

    print("Response from server:", response.decode('utf-8'))
    client_socket.close()

# Usage Example
if __name__ == "__main__":
    host = 'localhost'
    port = 4481
    payload = 'Lorem ipsum' * 10000  # Large payload
    send_large_payload(host, port, payload)

