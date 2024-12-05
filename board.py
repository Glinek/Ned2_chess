# import numpy as np
import cv2
from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()

# img = cv2.imread("ch3.webp")
img = cv2.imread("board_empty.jpg")

# img = cv2.resize(img, (800, 800))

cv2.imshow('Original', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray scale', gray)

ret, thresh = cv2.threshold(gray, 135, 255, cv2.THRESH_BINARY)
canny = cv2.Canny(thresh, 30, 200)
cv2.imshow("Threshold", thresh)
contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print("Number of Contours = " ,len(contours))
for l in contours:
    print(l)
cv2.imshow('Canny Edges', canny)

cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
cv2.imshow('Contours', img)

cv2.waitKey(0)
cv2.destroyAllWindows()



