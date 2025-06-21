import mediapipe
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 1280) # width
cap.set(4, 720) # height

'''
From the mediapipe website: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
Thumb: 4, 3, 2, 1
Index: 8, 7, 6, 5
Middle: 12, 11, 10, 9
Ring: 16, 15, 14, 13
Pinky: 20, 19, 18, 17
Base of palm / wrist: 0 (connected to 1, 5, 9, 13, 17)
'''


detector = HandDetector(detectionCon=0.8, maxHands=2)
    
# Using a measuring tape, x is calculated distance, y is actual distance in cm
# Have calculated and calibrated for my palm and camera. Hance not universally accurate. 
x = [260, 190, 167, 140, 120, 110, 101, 84]
y = [20, 25, 30, 35, 40, 45, 50, 55]


coefficients = np.polyfit(x, y, 2)


while True:
    success, img = cap.read()
    if not success:
        break

    hands = detector.findHands(img, draw=False)    # draws the points on the hand
    
    if hands:
        hands = hands[0]
        if hands==[]:
            skip_block = True
        else:
            skip_block = False
        if not skip_block:
            lmList = hands[0]['lmList']  # List of landmarks
            x, y, w, h = hands[0]['bbox'] # bounding box around the hand
    
            # distance between index and little finger (width of hand).
            # Can proportionally estimate the distance from webcam wrt this
            x1, y1 = lmList[5][0], lmList[5][1]
            x2, y2 = lmList[17][0], lmList[17][1]

            width = round(math.sqrt ((x2 - x1) ** 2 + (y2 - y1) ** 2))
            A, B, C = coefficients
            distance_cm = (A*width**2 + B*width + C)*0.9  # Adjusted for the measurement error

            print(width, distance_cm)
            cvzone.putTextRect(img, f'{int(distance_cm)} cm', (x+10, y-15))
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2) # 2 is thickness of border

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

