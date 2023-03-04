import threading, time
import argparse
import json

import paho.mqtt.client as mqtt

# gps packages
import serial
import time
import string
import pynmea2


class Publisher():
    def __init__(self, args=None):
        if args:
            self.port = args["port"]
            self.ip = args["ip"]
            self.topics = args["topic"]
        else:
            self.port = 1883
            self.ip = "192.168.21.134"
            self.topics = ['gps']
        
        self.client = mqtt.Client()
        self.possible_data = [
            [121.544764, 25.019388], 
            [121.544864, 25.019388], 
            [121.544964, 25.019388], 
            [121.544964, 25.019488], 
            [121.543964, 25.019588], 
            [121.543864, 25.019588],
            [121.543764, 25.019588], 
            [121.543764, 25.019488]]

        self.gps_signal_port = "/dev/tty.usbmodem12101" # the signal port connecting gps sensor, should depend on devices

    def publish(self, topic, data):
        payload = json.dumps(data).encode()
        self.client.publish(topic=topic, payload=payload)

    def gps_sensor(self):
        self.ser = serial.Serial(self.gps_signal_port, baudrate = 9600, timeout = 0.5)
        # i = 0
        # data = []
        while True:
            ## TODO: change gps data
            # dataout = pynmea2.NMEAStreamReader()
            newdata = self.ser.readline() # bytestring
            ndata = newdata.decode('UTF-8') # decode bytestring

            if ndata[0:6] == '$GPRMC':
                head = '$GPRMC: '
                newmsg = pynmea2.parse(ndata)
                # <RMC(timestamp=None, status='', lat='', lat_dir='', lon='', lon_dir='', spd_over_grnd=None, true_course=None, datestamp=None, mag_variation='', mag_var_dir='') data=['']>
                print(head, "decoded msg", newmsg)
                print(head, "latitude", newmsg.lat, " ,longitude", newmsg.lon)
            elif ndata[0:6] == '$GPGGA':
                head = '$GPGGA: '
                newmsg = pynmea2.parse(ndata)
                print(head, "decoded msg", newmsg)
                print(head, "latitude", newmsg.lat, " ,longitude", newmsg.lon)
            elif ndata[0:6] == '$GPGLL':
                head = '$GPGLL: '
                newmsg = pynmea2.parse(ndata)
                print(head, "decoded msg", newmsg)
                print(head, "latitude", newmsg.lat, " ,longitude", newmsg.lon)

            # data = self.possible_data[i]
            data = [newmsg.lat/100, newmsg.lon/100]
            i += 1
            if (i >= len(self.possible_data)):
                i = 0

            if len(data) == 0:
                continue
            elif data[0] == 0:
                continue
            self.publish("gps", data)
            time.sleep(1)
    
    def main(self):
        # Establish connection to mqtt broker
        self.client.connect(host=self.ip, port=self.port)
        self.client.loop_start()
        
        try:
            self.gps_sensor()
            
        except KeyboardInterrupt as e:
            self.client.loop_stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="localhost",
                        help="service ip of MQTT broker")
    parser.add_argument("--port",
                        default=1883,
                        type=int,
                        help="service port of MQTT broker")
    parser.add_argument("--topic",
                        default="gps",
                        choices=['gps', 'compass'],
                        nargs="+",
                        help="Available information to publish")
    args = vars(parser.parse_args())
    publisher = Publisher(args)
    publisher.main()
