import socket

class CloudHashServer:
    def __init__(self, port):
        # Create the underlying server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', port))
        self.server.listen(5)
        print(f"Listening on port {port}")
        self.storage = {}  # Dictionary to store key-value pairs

    def start(self):
        # The familiar accept loop
        while True:
            connection, client_address = self.server.accept()
            try:
                self.handle(connection)
            finally:
                connection.close()

    def handle(self, connection):
        # Read from the connection until EOF
        request = connection.recv(1024).decode()  # Read request from the client

        # Write back the result of the hash operation
        response = self.process(request)
        connection.sendall(response.encode())  # Send response back to the client

    def process(self, request):
        # Split the request into command, key, and value
        parts = request.split()
        command = parts[0].upper()

        # Handle GET and SET commands
        if command == 'GET':
            key = parts[1]
            return self.storage.get(key, 'Key not found')

        elif command == 'SET':
            key = parts[1]
            value = parts[2]
            self.storage[key] = value
            return 'OK'

        return 'Unknown command'

# Start the server on port 4481
server = CloudHashServer(4481)
server.start()

