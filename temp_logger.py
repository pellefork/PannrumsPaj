
import os
import glob
import time
import datetime
import board
import busio
import digitalio

import adafruit_max31865

import pyrebase
from pyfcm import FCMNotification

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

device_dict = {}

device_dict["accTank1BottomTemp"] = "28-00000b20b40e"
device_dict["accTank1TopTemp"] = "28-00000a9d9cea"

device_dict["accTank2BottomTemp"] = "28-00000b203fe6"
device_dict["accTank2TopTemp"] = "28-00000a73cf7c"

# device_dict["accTank3BottomTemp"] = "28-00000a9d517c"
device_dict["accTank3TopTemp"] = "28-00000b20b243"

# spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
#
# smoke_temp_sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, wires=3)

def new_temprec():
    data = {
      "accTank1BottomTemp" : -273.15,
      "accTank1TopTemp" : -273.15,
      "accTank2BottomTemp" : -273.15,
      "accTank2TopTemp" : -273.15,
      "accTank3BottomTemp" : -273.15,
      "accTank3TopTemp" : -273.15,
      "boilerTemp" : -273.15,
      "pumpLeftTemp" : -273.15,
      "pumpRightTemp" : -273.15,
      "pumpTopTemp" : -273.15,
      "smokeTemp" : -273.15
    }
    return data


def read_w1_temps():
    temp_rec = new_temprec()
    for key in device_dict:
        print('Reading ' + key)
        lines = read_w1_temp(device_dict[key])
        if w1_status(lines) == 'YES':
            temp_rec[key] = parse_w1_temp(lines)

    print(temp_rec)
    return temp_rec

# def read_pt1000_temp():
#     return smoke_temp_sensor.temperature

def parse_w1_temp(lines):
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    else:
        return -273.16

def w1_status(lines):
    return lines[0].strip()[-3:]

def read_w1_temp(device):
    print('Reading from device ' + device)
    device_dir = glob.glob(base_dir + device)[0]
    device_file = device_dir + '/w1_slave'
    file = open(device_file, 'r')
    lines = file.readlines()
    file.close()
    return lines

def write_data(data, db, user):
    db.child("CurrentValues").child("Temperatures").update(data, user['idToken'])
    print("Data written")

def write_history(data, db, user):
    data["datetime"] = str(datetime.datetime.now())
    data["timestamp"] = int(datetime.datetime.now().timestamp() * 1000)
    db.child("History").child("Temperatures").push(data, user['idToken'])
    print("History written")

def record_temps(sleep_time, db, user):
    while True:
        rec = read_w1_temps()
#        rec["smokeTemp"] = read_pt1000_temp()
        write_data(rec, db, user)
        write_history(rec, db, user)
        time.sleep(sleep_time)

