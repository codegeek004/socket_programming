import socket

class CloudHashClient:
    host = 'localhost'
    port = 4481

    @classmethod
    def get(cls, key):
        return cls.request(f"GET {key}")

    @classmethod
    def set(cls, key, value):
        return cls.request(f"SET {key} {value}")

    @classmethod
    def request(cls, string):
        # Create a new connection for each operation
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((cls.host, cls.port))
            client.sendall(string.encode('utf-8'))

            # Send EOF after writing the request
            client.shutdown(socket.SHUT_WR)

            # Read until EOF to get the response
            response = b""
            while True:
                data = client.recv(1024)
                if not data:
                    break
                response += data
            return response.decode('utf-8')

# Setting host and port for the client
CloudHashClient.host = 'localhost'
CloudHashClient.port = 4485

# Example usage
print(CloudHashClient.set('prez', 'obama'))
print(CloudHashClient.get('prez'))
print(CloudHashClient.get('vp'))

