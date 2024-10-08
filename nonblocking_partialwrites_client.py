import socket
import select

def send_large_payload(host, port, payload_size):
    # Create a non-blocking TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(False)

    # Connect to the server
    try:
        client_socket.connect((host, port))
    except BlockingIOError:
        # Connection in progress
        pass

    remaining_payload = 'Lorem ipsum ' * (payload_size // len('Lorem ipsum '))  # Create a large payload based on size
    total_payload_size = len(remaining_payload)

    while remaining_payload:
        # Determine how much data to send in this iteration
        send_size = min(1000, len(remaining_payload))  # Limit to 1000 bytes
        payload_to_send = remaining_payload[:send_size]

        try:
            # Try to send data in a non-blocking manner
            bytes_sent = client_socket.send(payload_to_send.encode('utf-8'))
            print(f"Sent {bytes_sent} bytes")
            
            # Remove the sent part from the remaining payload
            remaining_payload = remaining_payload[bytes_sent:]

        except BlockingIOError:
            # Socket is not ready for sending, wait until it's writable
            print("Waiting for the socket to be writable...")
            select.select([], [client_socket], [])
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    print("All data sent successfully.")
    client_socket.close()

# Usage
if __name__ == "__main__":
    host = 'localhost'
    port = 4481

    # Prompt the user for the amount of data to send
    payload_size = int(input("Enter the amount of data to send in bytes: "))
    
    # Send the data
    send_large_payload(host, port, payload_size)

