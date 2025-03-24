import socket,os
os.add_dll_directory(r'C:\gstreamer\1.0\msvc_x86_64\bin')

import cv2
import pickle
import struct

HOST = '127.0.0.1' # Replace with your server's IP
PORT = 5000 #Must match the server port

# Create a socket to receive video
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

data = b""
payload_size = struct.calcsize("Q")  # Struct size for frame size

while True:
    try:
        # Receive frame size
        while len(data) < payload_size:
            packet = client_socket.recv(4096)  
            if not packet:
                print("Server disconnected.")
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Receive frame data
        while len(data) < msg_size:
            data += client_socket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize frame
        frame = pickle.loads(frame_data)
        cv2.imshow("Live Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
cv2.destroyAllWindows()
