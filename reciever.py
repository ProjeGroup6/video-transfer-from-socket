import cv2
import numpy as np
import socket

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'  # Listen on all available network interfaces
port = 8080  # Use the same port number as in the sender
sock.bind((host, port))
sock.listen(1)

# Accept a connection
conn, addr = sock.accept()
print('Connected by', addr)

while True:
    # Receive the frame size
    data_size = int.from_bytes(conn.recv(4), byteorder='big')

    # Receive the frame data
    data = b''
    while len(data) < data_size:
        packet = conn.recv(data_size - len(data))
        if not packet:
            break
        data += packet

    # Decode and display the frame
    frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow('Received Frame', frame)

    # Press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
conn.close()
sock.close()