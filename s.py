import os 
os.add_dll_directory(r'C:\opencv\gbuild\install\x64\vc16\bin')
os.add_dll_directory(r'C:\gstreamer\1.0\msvc_x86_64\bin')
import cv2

# Device camera index
camera_index = 0

# Open device camera
cap = cv2.VideoCapture(camera_index)

# Forward video without re-encoding
forward_pipeline = (
    "appsrc ! videoconvert ! queue ! "
    "x264enc speed-preset=ultrafast tune=zerolatency ! "
    "rtph264pay ! udpsink host=127.0.0.1 port=5000"
)

# Open UDP stream
out = cv2.VideoWriter(forward_pipeline, cv2.CAP_GSTREAMER, 0, 30.0, (640, 480))

if not cap.isOpened() or not out.isOpened():
    print("Failed to open camera stream or output stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera")
        break

    out.write(frame)  # Send to ground PC

    # Display locally (Optional)
    cv2.imshow("Jetson Camera Stream", frame)

    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

cap.release()
out.release()
cv2.destroyAllWindows()
