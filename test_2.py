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
import nanocamera as nano

# Create 2 different test images to send
# A green square on a black background
# A red square on a black background

sender = imagezmq.ImageSender(connect_to='tcp://192.168.137.224:5555')

camera =nano.Camera(flip=0, width=1280, height=720, fps=30)

image_window_name = 'From Sender'
while camera.isReady():  # press Ctrl-C to stop image sending program
    # Increment a counter and print it's value to console
    try:
        image = camera.read()
    
        sender.send_image(image_window_name, image)
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("Error")
        break


camera.release()
del camera
