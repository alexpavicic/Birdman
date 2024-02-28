import PIL
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2






def test_with_image():

    # Load image and perform inference
    img = r'C:\Users\cheng\picture\Screenshot 2024-02-13 191412.png'
    results = model(img)
    # Print detection results
    results.print()
    # Display detection results
    results.show()



def test_with_webcam():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        # make detection
        results = model(frame)
        cv2.imshow('YOLO', np.squeeze(results.render()))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def test_with_videos():
    try:
        # Open the video file
        cap = cv2.VideoCapture('2023-12-15T14-08-56Z.mp4')

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Resize the frame to 416x416 pixels
            frame_resized = cv2.resize(frame, (416, 416))
            # Make detection
            results = model(frame_resized)
            # Display detection results
            cv2.imshow('YOLO', np.squeeze(results.render()))
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        # Release the video capture object and close all windows
        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print("Error:", e)

        
# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
test_with_videos()