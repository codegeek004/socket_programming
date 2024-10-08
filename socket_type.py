import socket

# Create a TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to google.com on port 80
sock.connect(('google.com', 80))

# Get the socket type
sock_type = sock.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE)

# Compare the socket type to SOCK_STREAM and SOCK_DGRAM
is_stream = sock_type == socket.SOCK_STREAM  # Should be True
is_dgram = sock_type == socket.SOCK_DGRAM    # Should be False

print(f"Socket type is STREAM: {is_stream}")
print(f"Socket type is DGRAM: {is_dgram}")

# Close the socket
sock.close()
