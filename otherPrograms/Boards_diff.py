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
img1 = cv2.imread("board3.jpg")
img2 = cv2.imread("board4.jpg")

# cv2.imshow('Original', img)

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# cv2.imshow('Gray scale', gray)

ret1, thresh1 = cv2.threshold(gray1, 135, 255, cv2.THRESH_BINARY)
ret2, thresh2 = cv2.threshold(gray2, 135, 255, cv2.THRESH_BINARY)
canny1 = cv2.Canny(thresh1, 30, 200)
canny2 = cv2.Canny(thresh2, 30, 200)

# cv2.imshow("Threshold", thresh)
contours1, hierarchy1 = cv2.findContours(canny1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours2, hierarchy2 = cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# print("Number of Contours = " ,len(contours))
# for l in contours:
#     print(l)
cv2.imshow('Canny Edges 1', canny1)
cv2.imshow('Canny Edges 2', canny2)

contours_img1 = img1
contours_img2 = img2

cv2.drawContours(contours_img1, contours1, -1, (0, 255, 0), 1)
cv2.drawContours(contours_img2, contours2, -1, (0, 255, 0), 1)
cv2.imshow('Contours', contours_img1)
cv2.imshow('Contours', contours_img2)

cv2.waitKey(0)
cv2.destroyAllWindows()



