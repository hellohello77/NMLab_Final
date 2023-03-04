import serial
import time
import pynmea2
import requests
import json
# print(serial.__version__) #check pyserial version
def gps_sensor():
    port = "/dev/ttyUSB0" # port connecting gps module
    ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
    print('port connect')
    a=True;
    while True:
        time.sleep(1)
        # if(a):
        #     data = json.dumps({'gps': [121.543764, 25.019388]})
        #     res = requests.post('http://114.33.135.105:4000/api/updateLocation', data = data)
        #     print(res)
        #     a = False
        #     continue
        # else:
        #     data = json.dumps({'gps': [121.143764, 25.009388]})
        #     res = requests.post('http://114.33.135.105:4000/api/updateLocation', data = data)
        #     a = True
        #     continue
        newdata = ser.readline() # bytestring
    
        ndata = newdata.decode() # decode bytestring
        # print(ndata)
        if ndata[0:6] == '$GPRMC': 
            # print("good\n")
            try:
                newmsg = pynmea2.parse(ndata)
            except:
                continue
            # <RMC(timestamp=None, status='', lat='', lat_dir='', lon='', lon_dir='', spd_over_grnd=None, true_course=None, datestamp=None, mag_variation='', mag_var_dir='') data=['']>
            # print("$GPRMC decoded msg", newmsg)
            # print("$GPRMC time", newmsg.timestamp)
            print("$GPRMC latitude", newmsg.lat, " ,longitude", newmsg.lon)
        elif ndata[0:6] == '$GPGGA':
            try:
                newmsg = pynmea2.parse(ndata)
            except:
                continue
            # print("$GPGGA decoded msg", newmsg)
            # print("$GPGGA time", newmsg.timestamp)
            # print("$GPGGA latitude", newmsg.lat, " ,longitude", newmsg.lon)
        elif ndata[0:6] == '$GPGLL':
            try:
                newmsg = pynmea2.parse(ndata)
            except:
                continue
            # print("$GPGLL decoded msg", newmsg)
            # print("$GPGLL time", newmsg.timestamp)
            # print("$GPGLL latitude", newmsg.lat, " ,longitude", newmsg.lon)
        else:
            continue
        
        if (newmsg.lat and newmsg.lon):
            print(type(newmsg.lon), type(newmsg.lat))
            real_lon = 0.0
            real_lat = 0.0
            for f_lon in range(len(newmsg.lon)):
                if newmsg.lon[f_lon] == '.':
                    real_lon = float(newmsg.lon[0:f_lon-2]) + float(newmsg.lon[f_lon-2:-1])/60
                    break
            for f_lat in range(len(newmsg.lat)):
                if newmsg.lat[f_lat] == '.':
                    real_lat = float(newmsg.lat[0:f_lat-2]) + float(newmsg.lat[f_lat-2:-1])/60
                    break
            data = json.dumps({'gps': [real_lon, real_lat]})
        else:
            print('invalid')
            continue
        print('sending data:', data)
        res = requests.post('http://114.33.135.105:4000/api/updateLocation', data = data)
        print(res.text)
        print(res.json)
        

if __name__ == "__main__":
    gps_sensor()