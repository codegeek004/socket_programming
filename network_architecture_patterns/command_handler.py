import os
import socket

CRLF = "\r\n"

class CommandHandler:
    def __init__(self, connection):
        self.connection = connection
        self.pwd = None
        self.data_socket = None

    def get_pwd(self):
        return self.pwd or os.getcwd()

    def handle(self, data):
        cmd = data[:4].strip().upper()
        options = data[4:].strip()

        if cmd == 'USER':
            # Accept any username anonymously
            return "230 Logged in anonymously"

        elif cmd == 'SYST':
            # What's your system name?
            return "215 UNIX Working With FTP"

        elif cmd == 'CWD':
            # Change working directory
            if os.path.isdir(options):
                self.pwd = options
                return f"250 directory changed to {self.get_pwd()}"
            else:
                return "550 directory not found"

        elif cmd == 'PWD':
            # Print working directory
            return f"257 \"{self.get_pwd()}\" is the current directory"

        elif cmd == 'PORT':
            # Open data connection on the specified port
            parts = options.split(',')
            ip_address = '.'.join(parts[:4])
            port = int(parts[4]) * 256 + int(parts[5])
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((ip_address, port))
            return f"200 Active connection established ({port})"

        elif cmd == 'RETR':
            # Retrieve a file
            file_path = os.path.join(self.get_pwd(), options)
            try:
                with open(file_path, 'rb') as file:
                    file_size = os.path.getsize(file_path)
                    self.connection.send(f"125 Data transfer starting {file_size} bytes{CRLF}".encode())
                    bytes_sent = self._transfer_data(file)
                    return f"226 Closing data connection, sent {bytes_sent} bytes"
            except FileNotFoundError:
                return "550 File not found"

        elif cmd == 'LIST':
            # List directory contents
            try:
                self.connection.send(f"125 Opening data connection for file list{CRLF}".encode())
                result = CRLF.join(os.listdir(self.get_pwd())) + CRLF
                self.data_socket.send(result.encode())
                self.data_socket.close()
                return f"226 Closing data connection, sent {len(result)} bytes"
            except Exception as e:
                return f"550 Error listing directory: {str(e)}"

        elif cmd == 'QUIT':
            # Quit the session
            return "221 Ciao"

        else:
            # Unknown command
            return f"502 Don't know how to respond to {cmd}"

    def _transfer_data(self, file):
        # Helper method to send file data over the data connection
        bytes_sent = 0
        while True:
            data = file.read(1024)
            if not data:
                break
            self.data_socket.send(data)
            bytes_sent += len(data)
        self.data_socket.close()
        return bytes_sent

# Example usage:
if __name__ == "__main__":
    # Placeholder connection for testing
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 4481))
    server_socket.listen(1)

    print("Server listening on port 4481...")
    conn, addr = server_socket.accept()

    handler = CommandHandler(conn)
    
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        response = handler.handle(data)
        conn.send((response + CRLF).encode())

    conn.close()
    server_socket.close()

