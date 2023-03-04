import threading, time
import requests
import io
# for face
import cv2

def detect_face():
    pipeline = (
        "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)1920, height=(int)1080, "
            "format=(string)NV12, framerate=(fraction)30/1 ! "
        "queue ! "
        "nvvidconv flip-method=2 ! "
            "video/x-raw, "
            "width=(int)1920, height=(int)1080, "
            "format=(string)BGRx, framerate=(fraction)30/1 ! "
        "videoconvert ! "
            "video/x-raw, format=(string)BGR ! "
        "appsink"
    )
    # Complete the function body
    time.sleep(5) # set an situation to trigger
    print('start')
    try:
        cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        if True:
            ret, frame = cap.read()
            if not ret:
                print('no camera')
            else:
                print('capture!!!')
                is_success, im_buf_arr = cv2.imencode(".jpg", frame)
                byte_im = im_buf_arr.tobytes()
                image = io.BufferedReader(io.BytesIO(byte_im))
                files= {'image': ("test.jpg",image,'multipart/form-data',{'Expires': '0'}) }
                res = requests.post('http://114.33.135.105:4000/api/compare', files=files)
                print(res.json())
    except KeyboardInterrupt as e:
        cap.release()

if __name__ == "__main__":
    detect_face()