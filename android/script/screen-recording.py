import subprocess
import cv2

# Set up the ADB command to start screen recording
subprocess.call(['adb', 'shell', 'screenrecord', '/sdcard/screen.mp4'])

# Set up OpenCV to read frames from the screen recording
cap = cv2.VideoCapture('adb shell screenrecord --output-format=h264 - | ffplay -')

# Create a VideoWriter object to save the recording to a file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('recorded_screen.mp4', fourcc, 20.0, (1920, 1080))

# Start recording and writing frames to the output file
while True:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)

# Release the VideoWriter and capture objects
out.release()
cap.release()

# Stop the screen recording on the Android device
subprocess.call(['adb', 'shell', 'pkill', 'screenrecord'])
