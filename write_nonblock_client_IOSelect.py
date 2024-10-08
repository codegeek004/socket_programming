import socket
import select
import errno

def send_large_payload(host, port, payload):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)

    try:
        client_socket.connect((host, port))
    except BlockingIOError:
        pass

    select.select([], [client_socket], [])

    while payload:
        try:
            bytes_sent = client_socket.send(payload.encode('utf-8'))
            print(f"Sent {bytes_sent} bytes")
            payload = payload[bytes_sent:]
        except socket.error as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                raise
            select.select([], [client_socket], [])

    print("Full payload sent.")

    # Wait for acknowledgment from the server
    response = b""
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data
            if b"\n" in response:  # Check for the acknowledgment ending
                break
        except BlockingIOError:
            select.select([client_socket], [], [])
            continue

    print("Response from server:", response.decode('utf-8').strip())
    client_socket.close()

# Usage
if __name__ == "__main__":
    host = 'localhost'
    port = 4481
    payload = 'Lorem ipsum' * 10000  # Large payload to send
    send_large_payload(host, port, payload)

