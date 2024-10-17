import socket
import os
import signal
from command_handler import CommandHandler

CRLF = "\r\n"

class FTPProcessPerConnection:
    def __init__(self, port=21):
        # Set up the control socket to listen for incoming connections.
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.bind(('localhost', port))
        self.control_socket.listen(5)

        # Handle interrupt signals (Ctrl+C) to exit gracefully.
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        # Close the server on interrupt.
        print("Shutting down server...")
        self.control_socket.close()
        exit()

    def gets(self):
        # Receives data from the client.
        return self.client.recv(1024).decode().strip(CRLF)

    def respond(self, message):
        # Sends a response to the client with CRLF ending.
        self.client.sendall(f"{message}{CRLF}".encode())

    def run(self):
        while True:
            # Accept new client connections.
            print("Waiting for connection...")
            self.client, address = self.control_socket.accept()
            print(f"Connected by {address}")

            # Fork a new process to handle the client.
            pid = os.fork()
            if pid == 0:  # Child process.
                self.respond("220 OHAI")  # FTP welcome message.
                
                # Create a command handler instance.
                handler = CommandHandler(self)

                while True:
                    # Receive requests from the client.
                    request = self.gets()
                    if request:
                        # Handle the request using the command handler.
                        response = handler.handle(request)
                        self.respond(response)
                    else:
                        # Close the connection when the client disconnects.
                        print(f"Connection closed by {address}")
                        self.client.close()
                        break

                os._exit(0)  # Child process exits after handling the connection.

            else:
                # Parent process continues to listen for new connections.
                os.waitpid(pid, os.WNOHANG)  # Detach the child process.

# Instantiate and run the FTP server on port 4481
if __name__ == "__main__":
    server = FTPProcessPerConnection(4481)
    server.run()

