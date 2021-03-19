# This is a sample Python script.

# Press Skift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time

# import pyrebase

from firebase import Firebase

from notifier import notify_clients
from temp_logger import record_temps
from camera_record import record_videos

from multiprocessing import Process

operation_status = {
    "tempRecording": "unknown",
    "videoRecording": "unknown"
}

config = {
    "apiKey": "AIzaSyDVM3CSRisI4YiYQqKIu8nTqYTsZ2nur88",
    "authDomain": "pannrum-7e210.firebaseapp.com",
    "databaseURL": "https://pannrum-7e210-default-rtdb.firebaseio.com",
    "storageBucket": "pannrum-7e210.appspot.com"
}

is_video_recording = False
is_temperature_logging = False

def init_fb():
    firebase = Firebase(config)
    return firebase

def auth(firebase):

    auth = firebase.auth()
    print('Got auth')

    user = auth.sign_in_with_email_and_password('lillhagsbacken@gmail.com', 'pnr2021')
    print('Got user')
    return user

def command_handler(message):
    print(message)
    print('Command received: event = ' + str(message["event"]) + ', path = ' + str(message["path"]) + ', data = ' + str(message["data"]))
    path = message["path"]
    command = message["data"]
    if command is not None and path != "/":
        key = path[1:]
        print('Key = ' + str(key) + ', command = ' + str(command))
        exec_command(key, command)

def exec_command(key, command):
    todo = command["commandString"]
    print('Executing: ' + todo)
    time.sleep(1)
    parts = todo.split()
    obj = parts[0]
    action = parts[1]

    if obj == "video":
        if action == "on":
            start_video_recording()
        elif action == "off":
            stop_video_recording()
    elif obj == "temp":
        if action == "on":
            start_temp_logging()
        elif action == "off":
            stop_temp_logging()

    print('Executed: obj = ' + obj + ', action = ' + action)
    move_command_to_history(key, command)

def move_command_to_history(key, command):
    print('Writing history: key = ' + key + ', command = ' + str(command))
    global db, user
    db.child('Commands').child(key).remove(user['idToken'])
    db.child('History').child('Commands').child(key).set(command, user['idToken'])

def start_video_recording():
    global is_video_recording
    if not is_video_recording:
        record_time = 5
        sleep_time = 60
        cam_record = Process(target=record_videos, args=(record_time, sleep_time, user, db, storage,))
        cam_record.start()
        is_video_recording = True
        write_status()
        print('Video recording started')
        return cam_record

def stop_video_recording():
    global is_video_recording, video_proc
    if is_video_recording:
        video_proc.kill()
        video_proc.join()
        video_proc.close()
        is_video_recording = False
        write_status()
        print('Video recording stopped')

def start_temp_logging():
    global is_temperature_logging
    if not is_temperature_logging:
        sleep_time = 10
        temp_record = Process(target=record_temps, args=(sleep_time, db, user,))
        temp_record.start()
        is_temperature_logging = True
        write_status()
        print('Temp logging started')
        return temp_record

def stop_temp_logging():
    global is_temperature_logging, temp_proc
    if is_temperature_logging:
        temp_proc.kill()
        temp_proc.join()
        temp_proc.close()
        is_temperature_logging = False
        write_status()
        print('Temp logging stopped')

def write_status():
    global operation_status, is_temperature_logging, is_video_recording
    operation_status["tempRecording"] = is_temperature_logging
    operation_status["videoRecording"] = is_video_recording
    db.child("CurrentValues").child("OperationStatus").update(operation_status, user['idToken'])
    print("Status written")


if __name__ == '__main__':

    firebase = init_fb()
    user = auth(firebase)
    db = firebase.database()
    storage = firebase.storage()

    print('Firebase ready')

    command_stream = db.child("Commands").stream(command_handler, user['idToken'])

    # video_proc = start_video_recording()
    # print('Video recording started')

    # temp_proc = start_temp_logging()
    # print('Temp logging started')

    # notify_clients('Test message', 'Lots and lots of text...', db, user)

    time.sleep(120)

    command_stream.close()
    stop_temp_logging()
    stop_video_recording()

    print('Finished - exiting')


