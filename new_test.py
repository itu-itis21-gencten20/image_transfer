import base64
import cv2
import zmq

#context = zmq.Context()
#footage_socket = context.socket(zmq.PUB)
#footage_socket.connect('tcp://192.168.137.224:5555')

camera = cv2.VideoCapture(0)  # init the camera


while True:
    try:
        grabbed, frame = camera.read()
        if frame:
            frame = cv2.resize(frame, dsize=(1280, 720)) 
        
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        print(jpg_as_text)
        #footage_socket.send(jpg_as_text)
    except KeyboardInterrupt:
        camera.release()
        break