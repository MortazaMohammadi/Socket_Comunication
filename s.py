import os
os.add_dll_directory(r'C:\opencv\gbuild\install\x64\vc16\bin')
os.add_dll_directory(r'C:\gstreamer\1.0\msvc_x86_64\bin')
import cv2

# RTSP Camera URL (No re-encoding)
camera_rtsp_url = "rtsp://192.168.2.119:554"

# GStreamer pipeline (Direct RTSP forwarding)
gst_pipeline = f"rtspsrc location={camera_rtsp_url} latency=0 ! decodebin ! videoconvert ! appsink"

# Open camera stream
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

# Forward video without re-encoding
forward_pipeline = (
    "appsrc ! videoconvert ! queue ! "
    "x264enc speed-preset=superfast tune=zerolatency bitrate=2000 key-int-max=10 ! "
    "rtph264pay ! queue ! udpsink host=162.152.0.60 port=5000 sync=false"
)


# Open UDP stream
out = cv2.VideoWriter(forward_pipeline, cv2.CAP_GSTREAMER, 0, 30.0, (1280, 720))

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
