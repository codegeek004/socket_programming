import socket
import select

def handle_client(client_socket):
    response = b""
    total_bytes_received = 0
    expected_size = 110000  # We know the client will send this many bytes
    
    while True:
        try:
            data = client_socket.recv(4096)
            if data:
                print('if data mai gaya')
                response += data
                total_bytes_received += len(data)
                print(f"Received {len(data)} bytes, total: {total_bytes_received} bytes.")
                
                # If we've received the full payload, send the acknowledgment
                if total_bytes_received >= expected_size:
                    print("Full payload received, sending acknowledgment.")
                    break
            else:
                print('client finish wale else mai gaya')
                print("Client finished sending data.")
                break  # No more data, client finished sending
        except BlockingIOError:
            print('blocking error wale exception mai')
            select.select([client_socket], [], [])
        except Exception as e:
            print(f"Error: {e}")
            break

    # After receiving all the data, send acknowledgment
    if response:
        print(f"Total received: {len(response)} bytes.")
        try:
            print('sent acknowledgement wale try mai gaya')
            client_socket.sendall(b"Server received your payload successfully\n")
            print("Acknowledgment sent to the client.")
        except Exception as e:
            print('sent exception wale exception mai gaya', e)
            print(f"Error while sending acknowledgment: {e}")
    else:
        print("No data received.")
        try:
            client_socket.sendall(b"No data received\n")
        except Exception as e:
            print(f"Error while sending no-data acknowledgment: {e}")

    client_socket.close()

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.setblocking(False)
        handle_client(client_socket)

if __name__ == "__main__":
    start_server(4481)

