import base64
import cv2
import zmq

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://192.168.137.224:5555')

camera = cv2.VideoCapture(0)  # init the camera


while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        #print(grabbed, frame)

        if frame is None:
            print('Wrong path:', path)
        else:
            frame = cv2.resize(frame, dsize=(1280, 720))  # resize the frame
            pixels.append(img)
        
        encoded, buffer = cv2.imencode('.jpg', frame)
        #cv2.imshow('abc', )
        jpg_as_text = base64.b64encode(buffer)

        footage_socket.send(jpg_as_text)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break