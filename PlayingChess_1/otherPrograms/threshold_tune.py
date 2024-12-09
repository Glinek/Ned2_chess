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
img_origin = cv2.imread("board_empty.jpg")
threshold = 135

# img = cv2.resize(img, (800, 800))
while threshold != 0:
    # cv2.imshow('Original', img)
    img = img_origin
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Gray scale', gray)



    ret, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("Threshold", thresh)

    canny = cv2.Canny(thresh, 30, 200)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print("Number of Contours = " ,len(contours))
    # for l in contours:
    #     print(l)
    cv2.imshow('Canny Edges', canny)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
    cv2.imshow('Contours', img)
    threshold = int(input("Enter new threshold (0 - exit): "))
    cv2.destroyAllWindows()

cv2.waitKey(0)
# cv2.destroyAllWindows()



