import cv2
# Import the video capturing function
from video_capture import VideoCaptureAsync
import time

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
    print("creating video")
    # The loop goes through the array of images and writes each image to the video file
    for i in range(len(images)):
        out.write(images[i])
    images = []
    print("Recording Done")

    key = db.generate_key()

    storage.child(key).child("videos/video.avi").put("video.avi", user['idToken'] )

    print('Video uploaded')




