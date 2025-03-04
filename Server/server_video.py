import os
import socket
import pickle
import struct

# Add DLL directories (for Windows)
# os.add_dll_directory(r'C:\opencv\gbuild\install\x64\vc16\bin')
os.add_dll_directory(r'C:\gstreamer\1.0\msvc_x86_64\bin')
import cv2

HOST = '162.152.1.122'  # Server's IP
PORT = 50000  # Must match the client port

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# ✅ GStreamer pipeline for webcam (Linux & Windows)
gst_pipeline = (
    "ksvideosrc ! videoconvert ! appsink" if os.name == "nt"  # Windows
    else "v4l2src ! videoconvert ! appsink"  # Linux/macOS
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: GStreamer pipeline failed to open.")
    conn.close()
    server_socket.close()
    exit()

print("🎥 Streaming started from Webcam...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ ERROR: Frame capture failed.")
        break

    # Show video locally on the server
    cv2.imshow("Server - Webcam Stream", frame)

    # Serialize frame
    data = pickle.dumps(frame)
    message_size = struct.pack("Q", len(data))  # Pack frame size
    conn.sendall(message_size + data)  # Send frame to client

    # Stop on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
server_socket.close()
