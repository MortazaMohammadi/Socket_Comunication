import os 
os.add_dll_directory(r'C:\opencv\gbuild\install\x64\vc16\bin')
os.add_dll_directory(r'C:\gstreamer\1.0\msvc_x86_64\bin')
import cv2

# GStreamer pipeline to receive the stream
gst_pipeline = (
    "udpsrc port=5000 ! application/x-rtp, encoding-name=H264, payload=96 ! "
    "rtpjitterbuffer latency=0 ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false"
)


cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Failed to receive video stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No video received")
        break

    cv2.imshow("Ground Station Stream (Low Latency)", frame)

    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
