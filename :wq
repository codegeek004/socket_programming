import socket

class CloudHashServer:
    def __init__(self, port):
        # Create the underlying server socket.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)
        print(f"Listening on port {port}")
        self.storage = {}

    def start(self):
        # Accept loop to handle client connections.
        while True:
            connection, address = self.server.accept()
            try:
                self.handle(connection)
            finally:
                connection.close()

    def handle(self, connection):
        # Read from the connection until EOF.
        request = connection.recv(1024).decode('utf-8')
        # Write back the result of the hash operation.
        response = self.process(request)
        connection.sendall(response.encode('utf-8'))

    def process(self, request):
        # Supported commands: SET key value, GET key
        try:
            command, key, value = request.split()
        except ValueError:
            command, key = request.split()
            value = None
        
        command = command.upper()

        if command == "GET":
            return self.storage.get(key, "")
        elif command == "SET" and value:
            self.storage[key] = value
            return "OK"
        else:
            return "ERROR"

# Start the server on port 4481
server = CloudHashServer(4485)
server.start()

