import cv2
import time
import imagezmq
import traceback
import socket
from simplejpeg import encode_jpeg


def gstreamer_pipeline(
    # sensor_id=0,
    # capture_width=720,
    # capture_height=480,
    # display_width=720,
    # display_height=480,
    # framerate=60,
    # flip_method=0,
):
    return '''nvarguscamerasrc sensor_id=1 ! 
   'video/x-raw(memory:NVMM),width=3264, height=2464, framerate=21/1, format=NV12' ! 
   nvvidconv flip-method=0 ! 'video/x-raw, width=816, height=616' ! 
   nvvidconv ! nvegltransform ! nveglglessink -e'''
    # return (
    #     "nvarguscamerasrc sensor-id=%d !"
    #     "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
    #     "nvvidconv flip-method=%d ! "
    #     "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
    #     "videoconvert ! "
    #     "video/x-raw, format=(string)BGR ! appsink"
    #     % (
    #         sensor_id,
    #         capture_width,
    #         capture_height,
    #         framerate,
    #         flip_method,
    #         display_width,
    #         display_height,
    #     )
    # )


def send_cam_stream():

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    jetson_name = socket.gethostname()
    image_window_name = 'From Sender'
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(0)
    time.sleep(3)
    if video_capture.isOpened():
        try:
            with imagezmq.ImageSender(connect_to='tcp://192.168.137.1:5555') as sender:
                while True:                 # send images as a stream until Ctrl-C
                    ret_val, frame = video_capture.read()
                    print('ret_val is:', ret_val)
                    #jpg_buffer = encode_jpeg(frame, quality=90, colorspace='BGR')
                    #reply_from = sender.send_jpg(jetson_name, jpg_buffer)
                    reply_from = sender.send_image(image_window_name, frame)
                    print(reply_from)
        except (KeyboardInterrupt):
            pass                            # Ctrl-C was pressed to end program
        except Exception as ex:
            print('Python error with no Exception handler:')
            print('Traceback error:', ex)
            traceback.print_exc()
        finally:
            video_capture.release()


if __name__ == "__main__":
    send_cam_stream()
