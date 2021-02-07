import cv2
# Import the video capturing function
from video_capture import VideoCaptureAsync
import time
import datetime
import os

#Specify width and height of video to be recorded
vid_w = 320
vid_h = 240

vid_framerate = 10

#Intiate Video Capture object
capture = VideoCaptureAsync(src=0, width=vid_w, height=vid_h)

#Intiate codec for Video recording object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

def record_videos(duration, sleep_time, user, db, storage):
    while True:
        record_video(duration, user, db, storage)
        time.sleep(sleep_time)

def record_video(duration, user, db, storage):

    print('Before start, size = ' + str(os.path.getsize('video.avi')))

    #start video capture
    print('Starting capture')
    capture.start()
    time_end = time.time() + duration
    print('Started capture')

    frames = 0
    prev = 0

    #Create array to hold frames from capture
    images = []
    # Capture for duration defined by variable 'duration'

    print('Recording...')

    while time.time() <= time_end:
        time_elapsed = time.time() - prev
        ret, new_frame = capture.read()

        if time_elapsed > 1. / vid_framerate:
            prev = time.time()
            frames += 1
            images.append(new_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.stop()

    # cv2.destroyAllWindows()

    # The fps variable which counts the number of frames and divides it by
    # the duration gives the frames per second which is used to record the video later.
    fps = frames/duration
    print('frames ' + str(frames))
    print('vid_framerate ' + str(vid_framerate))

    print('fps (measured) ' + str(fps))

    print('len(images) ' + str(len(images)))

    # The following line initiates the video object and video file named 'video.avi'
    # of width and height declared at the beginning.
    out = cv2.VideoWriter('video.avi', fourcc, fps, (vid_w,vid_h))

    size = os.path.getsize('video.avi')

    print('Before adding frames, size = ' + str(os.path.getsize('video.avi')))

    print("creating video")
    # The loop goes through the array of images and writes each image to the video file
    for i in range(len(images)):
        out.write(images[i])
    out.release()
    images = []

    print("Recording Done")

    print('After adding frames, size = ' + str(os.path.getsize('video.avi')))

    key = db.generate_key()


    print('After release, size = ' + str(os.path.getsize('video.avi')))

    # path = "videos/video.avi"

    # storage.child("videos2/video.avi").put("video.avi", user['idToken'])

    result = storage.child("videos").child(key).child("video.avi").put('video.avi', user['idToken'] )
    print('Video put, result = ' + str(result))

    url = storage.child("videos").child(key).child("video.avi").get_url(user['idToken'])
    path = result["name"]

    print('Video uploaded to URL ' + str(url))
    rec = write_db_rec(db, user, key, url)

    print('DB video rec written' + str(rec))

def write_db_rec(db, user, key, url):
    data = {}
    data["datetime"] = str(datetime.datetime.now())
    data["timestamp"] = int(datetime.datetime.now().timestamp() * 1000)
    data["path"] = url
    data["url"] = url
    db.child("Videos").child(key).child("videoRec").set(data, user['idToken'])
    return data



