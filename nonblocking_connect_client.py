import socket
import select
import errno

def send_request(sock):
    try:
        # HTTP GET request to google.com
        request = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
        sock.sendall(request.encode('utf-8'))
        print("Request sent to the server.")
    except socket.error as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            raise
        select.select([], [sock], [])
    
    # Receiving response
    response = b""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        except BlockingIOError:
            select.select([sock], [], [])
            continue

    print("Response from server:")
    print(response.decode('utf-8'))

if __name__ == "__main__":
    # Use the nonblocking connection to Google
    sock = nonblocking_connect('google.com', 80)
    
    # Send an HTTP request and receive the response
    send_request(sock)
    
    sock.close()

