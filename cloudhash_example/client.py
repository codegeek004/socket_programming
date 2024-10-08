import socket

class CloudHashClient:
    host = 'localhost'
    port = 4481

    @classmethod
    def get(cls, key):
        # Send a GET request to the server
        request = f"GET {key}"
        return cls.request(request)

    @classmethod
    def set(cls, key, value):
        # Send a SET request to the server
        request = f"SET {key} {value}"
        return cls.request(request)

    @classmethod
    def request(cls, request_string):
        # Create a new connection for each operation
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((cls.host, cls.port))
            client_socket.sendall(request_string.encode())  # Send request

            # Close write operation after sending the request
            client_socket.shutdown(socket.SHUT_WR)

            # Read the response until EOF
            response = client_socket.recv(1024).decode()  # Read response from the server
            return response

# Test the client
print(CloudHashClient.set('prez', 'obama'))
print(CloudHashClient.get('prez'))
print(CloudHashClient.get('vp'))




