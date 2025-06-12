import cv2 as cv
import numpy as np
import HandTracking as ht
import subprocess
import math

# reduce volume by 20% of max volume each time set_volume is called
def set_volume():
    apple_script = 'set volume output volume (output volume of (get volume settings) - 20)'
    # Run the AppleScript using osascript
    subprocess.run(['osascript', '-e', apple_script])

# update volume flag based on the length between finger tips
def volFlag(volumeFlag, length, lengthMax, lengthMin):
    if (length < lengthMin) & (volumeFlag == 1):
        set_volume()
        volumeFlag = 0
        
    if (length > lengthMax):
        volumeFlag = 1

    return volumeFlag

# initialise parameters
camWidth, camHeight = 640, 480
lengthMax = 150
lengthMin = 50
length = 100
volumeFlag = 1

cap = cv.VideoCapture(0)

# set web came height and width
cap.set(3, camWidth)
cap.set(4, camHeight)

# create hand tracking object
detector = ht.handDetector(detectionConfidence = 0.7)

while True:
    
# read web cam and save as img matrix of pixels
    sucess, img = cap.read()

    # find singular hand
    img = detector.findHands(img)
    # landmark list
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        # co-ordinates of 4rth id position (thumb) and 8th (tip of index)
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # draw line between two finger nodes
        cv.line(img, (x1, y1), (x2, y2), (255,0,255), 3)

        # compute ditance between thumb and index finger tips
        length = math.hypot(x2-x1, y2-y1)
        
        volumeFlag = volFlag(volumeFlag, length, lengthMax, lengthMin)
        
        print(length, volumeFlag)


    cv.imshow("Image", img)
    if cv.waitKey(1) & 0xFF == ord('`'):
        break 
    