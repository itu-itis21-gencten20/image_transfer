import cv2
import base64
import time

def gstreamer_pipeline(
   
):
    return (
        "v4l2src device=/dev/video0 ! image/jpeg ! jpegparse ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink"
        """
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
        """
    )


def show_camera():

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            while True:
                ret_val, frame = video_capture.read()
                return_key, encoded_image = cv2.imencode(".jpg", video_frame)
                if not return_key:
                    continue
                jpg_as_text = base64.b64encode(encoded_image)
                print(jpg_as_text)
                time.sleep(.5)

                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break
        finally:
            video_capture.release()
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()