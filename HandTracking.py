import cv2 as cv
import mediapipe as mp

# create handDetector class
class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionConfidence = 0.5, trackConfidence = 0.5, complexity = 0):
        # initialise parameters (default)
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackConfidence = trackConfidence
        self.complexity = complexity 

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionConfidence, self.trackConfidence) 
        self.mpDraw = mp.solutions.drawing_utils     

    def findHands(self, img, draw=True):
        # convert image to rgb as hands class only uses rgb images
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #print(results.multi_hand_landmarks)
        # check for multiple hands, extract one by one

        if self.results.multi_hand_landmarks:
            # handLMS represents a single hand
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img
    
    def findPosition(self, img, handNo = 0, draw = True):

        lmList = []
        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)

                lmList.append([id, cx, cy])

                if draw: 
                    cv.circle(img, (cx,cy), 25, (255,0,255), cv.FILLED)

        return lmList


def main(): 
    cap = cv.VideoCapture(0)

    detector = handDetector()

    while True:
    # read web cam and save as image matrix
        sucess, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[0])

        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF == ord('`'):
            break 
    capture.release
    cv.destrowAllWindows()


if __name__ == "__main__":
    main()