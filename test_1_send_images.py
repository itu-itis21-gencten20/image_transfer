"""test_1_send_images.py -- basic send images test.

A simple test program that uses imagezmq to send images to a receiving program
that will display the images.

This program requires that the image receiving program to be running first.
Brief test instructions are in that program: test_1_receive_images.py.
"""

import sys
import time
import numpy as np
import cv2
import imagezmq
from imutils.video import VideoStream

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=960,
    display_height=540,
    framerate=20,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


# Create 2 different test images to send
# A green square on a black background
# A red square on a black background


def send_camera_image():
    FPS = 15
    image_window_name = 'From Sender'
    sender = imagezmq.ImageSender(connect_to='tcp://192.168.137.1:5555')
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    # print(gstreamer_pipeline(flip_method=0))
    # video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    vs = VideoStream(src=0, resolution=(480, 720),
                     framerate=FPS).start()
    while True:
        try:
            frame = vs.read()
            sender.send_image(image_window_name, frame)
            time.sleep(1 / FPS) 
            # Check to see if the user closed the window
            # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
            # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
        except Exception as e:
            print(e)


if __name__ == '__main__':
    send_camera_image()
