# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time

import pyrebase

from notifier import notify_clients
from temp_logger import record_temps
from camera_record import record_videos

from multiprocessing import Process

config = {
    "apiKey": "AIzaSyDVM3CSRisI4YiYQqKIu8nTqYTsZ2nur88",
    "authDomain": "pannrum-7e210.firebaseapp.com",
    "databaseURL": "https://pannrum-7e210-default-rtdb.firebaseio.com",
    "storageBucket": "pannrum-7e210.appspot.com"
}

def init_fb():
    firebase = pyrebase.initialize_app(config)
    return firebase

def auth(firebase):

    auth = firebase.auth()
    print('Got auth')

    user = auth.sign_in_with_email_and_password('lillhagsbacken@gmail.com', 'pnr2021')
    print('Got user')
    return user

def read_command(db, user):
    print('Getting next command')
    commands = db.child("CommandBuffer").get(user['idToken'])
    print("Commands:")
    print(commands)
    return commands


def start_video_recording():

    record_time = 5
    sleep_time = 60

    cam_record = Process(target=record_videos, args=(record_time, sleep_time, user, db, storage,))
    cam_record.start()

    return cam_record

def start_temp_logging():
    sleep_time = 10
    temp_record = Process(target=record_temps, args=(sleep_time, db, user,))
    temp_record.start()

    return temp_record


if __name__ == '__main__':
    print('Pannrumspaj starting reading')

    firebase = init_fb()
    user = auth(firebase)
    db = firebase.database()
    storage = firebase.storage()

    print('Firebase ready')

    video_proc = start_video_recording()
    print('Video recording started')

    temp_proc = start_temp_logging()
    print('Temp logging started')

    notify_clients('Test message', 'Lots and lots of text...', db, user)

    time.sleep(300)

    video_proc.kill()
    video_proc.join()
    video_proc.close()
    print('Video recording stopped')

    temp_proc.kill()
    temp_proc.join()
    temp_proc.close()
    print('Temp logging stopped')

    print('Finished - exiting')


