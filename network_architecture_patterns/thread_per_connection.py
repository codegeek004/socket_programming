import socket
import threading
import signal  # Import the signal module
from command_handler import CommandHandler

CRLF = "\r\n"

class Connection:
    def __init__(self, client):
        self.client = client

    def gets(self):
        # Receive data from the client.
        return self.client.recv(1024).decode().strip(CRLF)

    def respond(self, message):
        # Send a response to the client with CRLF ending.
        self.client.sendall(f"{message}{CRLF}".encode())

    def close(self):
        # Close the client connection.
        self.client.close()

class ThreadPerConnection:
    def __init__(self, port=21):
        # Set up the control socket to listen for incoming connections.
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.bind(('localhost', port))
        self.control_socket.listen(5)

        # Handle interrupt signals (Ctrl+C) to exit gracefully.
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("Shutting down server...")
        self.control_socket.close()
        exit()

    def run(self):
        # Set abort_on_exception behavior for threads.
        threading.excepthook = lambda t, e: print(f"Thread {t} raised {e}")

        while True:
            # Accept new client connections.
            print("Waiting for connection...")
            client_socket, address = self.control_socket.accept()
            print(f"Connected by {address}")

            conn = Connection(client_socket)
            # Start a new thread for each connection.
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        conn.respond("220 OHAI")  # FTP welcome message.
        handler = CommandHandler(conn)

        while True:
            request = conn.gets()
            if request:
                # Handle the request using the command handler.
                response = handler.handle(request)
                conn.respond(response)
            else:
                # Close the connection when the client disconnects.
                print("Connection closed by client.")
                conn.close()
                break

# Instantiate and run the FTP server on port 4481
if __name__ == "__main__":
    server = ThreadPerConnection(4481)
    server.run()

