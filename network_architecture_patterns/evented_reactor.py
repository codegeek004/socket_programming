import socket
import asyncio
from command_handler import CommandHandler

CHUNK_SIZE = 1024 * 16
CRLF = "\r\n"

class Connection:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.request = ""
        self.response = ""
        self.handler = CommandHandler(self)
        self.respond("220 OHAI")
        asyncio.create_task(self.monitor_writing())

    def on_data(self, data):
        self.request += data.decode()
        if self.request.endswith(CRLF):
            # Request is completed.
            response = self.handler.handle(self.request)
            self.respond(response)
            self.request = ""

    def respond(self, message):
        self.response += message + CRLF

    async def monitor_writing(self):
        while True:
            if self.response:
                self.on_writable()
            await asyncio.sleep(0.1)  # Yield control to the event loop.

    def on_writable(self):
        if self.response:
            bytes_written = self.writer.write(self.response.encode())
            self.writer.drain()  # Ensure all data is sent.
            self.response = self.response[bytes_written:]

    def monitor_for_reading(self):
        return True  # Always ready for reading.

    def monitor_for_writing(self):
        return bool(self.response)

class Evented:
    def __init__(self, port=21):
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.bind(('localhost', port))
        self.control_socket.listen()
        self.handles = {}
        print(f"Server started on port {port}")

    async def handle_client(self, reader, writer):
        connection = Connection(reader, writer)
        self.handles[writer.get_extra_info('socket').fileno()] = connection
        while True:
            try:
                data = await reader.read(CHUNK_SIZE)
                if not data:
                    break
                connection.on_data(data)
            except Exception as e:
                print(f"Connection error: {e}")
                break
        # Clean up connection
        del self.handles[writer.get_extra_info('socket').fileno()]
        writer.close()
        await writer.wait_closed()

    async def run(self):
        while True:
            client_socket, address = await asyncio.get_event_loop().sock_accept(self.control_socket)
            print(f"Accepted connection from {address}")
            reader, writer = await asyncio.open_connection(sock=client_socket)
            asyncio.create_task(self.handle_client(reader, writer))

if __name__ == "__main__":
    server = Evented(4481)
    asyncio.run(server.run())

