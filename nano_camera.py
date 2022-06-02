import cv2
import nanocamera as nano
import time
import imagezmq
import traceback
import socket

def send_cam_stream():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    jetson_name = socket.gethostname()
    image_window_name = 'From Sender'
    camera = nano.Camera(device_id=0, camera_type = 0, flip=0, width=640, height=480, fps=30)
    time.sleep(3)
    print('CSI Camera ready? - ', camera.isReady())
    if camera.isReady():
        try:
            with imagezmq.ImageSender(connect_to='tcp://192.168.137.1:5555') as sender:
                while True:                 # send images as a stream until Ctrl-C
                    frame = camera.read()
                    reply_from = sender.send_image(image_window_name, frame)
                    print(reply_from)
        except (KeyboardInterrupt):
            pass                            # Ctrl-C was pressed to end program
        except Exception as ex:
            print('Python error with no Exception handler:')
            print('Traceback error:', ex)
            traceback.print_exc()
        finally:
            camera.release()
            del camera


if __name__ == "__main__":
    send_cam_stream()
