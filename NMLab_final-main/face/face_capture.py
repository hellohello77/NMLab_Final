import threading, time
import requests
import io

# for face
import cv2
# for button
import RPi.GPIO as GPIO

# for arduino
import serial

class Detect_Face():

    def __init__(self):

        self.BUTTON_PIN = 15
        self.BUTTON_STATE = 0
        self.ARDUINO_DEVICE = '/dev/ttyUSB1'
        self.BAUD_RATE = 9600
        self.lock_open = False
        self.lock = False

        # initialize GPIO state, please use it when booting jetson nano
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN)
        self.BUTTON_STATE = GPIO.input(self.BUTTON_PIN)

    def button_check(self):
        self.BUTTON_STATE = GPIO.input(self.BUTTON_PIN)

        if self.BUTTON_STATE:
            GPIO.setup(self.BUTTON_PIN, GPIO.OUT)
            GPIO.output(self.BUTTON_PIN, 0)
            GPIO.setup(self.BUTTON_PIN, GPIO.IN)
            self.BUTTON_STATE = 0
            return True

        return False

    def detect_face(self):
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
        # cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        # Complete the function body
        # Only read face when button state is changed, indicates that button has been pressed
        self.button_check()
        while True:
            # time.sleep(1)
            if not self.button_check():
                # print('not pushed')
                time.sleep(1)
                continue
                # break

            # modified below
            if not self.lock:
                with serial.Serial(self.ARDUINO_DEVICE, self.BAUD_RATE) as ser:
                    # close lock
                    print('lock my lock')
                    ser.write(bytes('0', 'utf-8'))
                    res = ser.readline()
                    self.lock = True
                    print(res)
                # time.sleep(1)
                continue
            # modified above


            # time.sleep(5) # set an situation to trigger
            print('start')
            try:
                cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
                ret, frame = cap.read()

                now = time.time()
                while not ret:
                    ret, frame = cap.read()
                    if (time.time() - now > 2):
                        print('no camera')
                        break
                if ret:
                    print('capture!!!')
                    is_success, im_buf_arr = cv2.imencode(".jpg", frame)
                    byte_im = im_buf_arr.tobytes()
                    image = io.BufferedReader(io.BytesIO(byte_im))
                    files= {'image': ("test.jpg",image,'multipart/form-data',{'Expires': '0'}) }
                    res = requests.post('http://114.33.135.105:4000/api/compare', files=files)
                    print(res.json())
                    self.lock_open = res.json()['Success']
                cap.release()
                # break

                if self.lock_open:
                    with serial.Serial(self.ARDUINO_DEVICE, self.BAUD_RATE) as ser:
                        # open lock
                        print('open')

                        res = None
                        now = time.time()
                        ser.write(bytes('1', 'utf-8'))
                        res = ser.readline()
                        self.lock = False # modified
                        print(res)
                else:
                    with serial.Serial(self.ARDUINO_DEVICE, self.BAUD_RATE) as ser:
                        # close lock
                        print('close')
                        
                        res = None
                        now = time.time()
                        ser.write(bytes('0', 'utf-8'))
                        res = ser.readline()
                        print(res)
                        self.lock = True
                
            except KeyboardInterrupt as e:
                cap.release()
            # time.sleep(1)

if __name__ == "__main__":
    face_detect = Detect_Face()
    face_detect.detect_face()
