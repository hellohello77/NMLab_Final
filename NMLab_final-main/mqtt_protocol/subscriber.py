import argparse

import json
import paho.mqtt.client as mqtt
import requests
import cv2
import numpy as np
import io

class Subscriber():
    def __init__(self, args=None):
        self.url_pre = 'http://114.33.135.105:4000/'
        self.client = mqtt.Client()
        self.data = {
            "gps": [121.543764, 25.019388],
        }
        self.ip = "192.168.21.134"
        self.port = 1883
        if args:
            self.ip = args.ip
            self.port = args.port

    def on_message(self, client, obj, msg):
        if msg.topic == 'gps':
            print('gps received')
            self.data = {'gps': json.loads(msg.payload.decode())}
            print('decode', json.loads(msg.payload.decode()))
            res = requests.post(self.url_pre+'api/updateLocation', data=self.data)
        elif msg.topic == 'face':
            print('face received')
            # self.data = {'face': json.loads(msg.payload.decode())}
            # print('decoded')
            is_success, im_buf_arr = cv2.imencode(".jpg", np.array(json.loads(msg.payload.decode())))
            print('1')
            byte_im = im_buf_arr.tobytes()
            print('2')
            image = io.BufferedReader(io.BytesIO(byte_im))
            print('3')
            files= {'image': ("test.jpg",image,'multipart/form-data',{'Expires': '0'}) }
            print('4')
            res = requests.post(self.url_pre+'api/compare', files=files)
            print(res.json())
            # cv2.imwrite('test_img_s.jpeg', np.array(self.data))
            # print('saved')
        
        # self.data[msg.topic] = json.loads(msg.payload.decode())
        # print(f"TOPIC:{msg.topic}, VALUE:{msg.payload}")
        # print(self.data)

    def main(self):
        # Establish connection to mqtt broker
        self.client.on_message = self.on_message
        self.client.connect(host=self.ip, port=self.port)
        self.client.subscribe('gps', 0)
        self.client.subscribe('face', 0)

        try:
            self.client.loop_forever()
        except KeyboardInterrupt as e:
            print("terminate subscriber")
            self.client.loop_stop()
            print("terminate subscriber done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    args = vars(parser.parse_args())
    subscriber = Subscriber()
    subscriber.main()
