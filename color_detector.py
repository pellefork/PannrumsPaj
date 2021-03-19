
import cv2
import numpy as np

lower_green = np.array([37,42,0])
upper_green = np.array([84,255,255])

lower_red = np.array([[155,25,0]])
upper_red = np.array([179,255,255])

def detect_redness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)
    return np.sum(mask)
