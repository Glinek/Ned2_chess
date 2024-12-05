# import numpy as np
import cv2
from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()

pattern_size = (7, 7)
img = cv2.imread("board_empty.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray scale', gray)

ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
cv2.drawChessboardCorners(img, pattern_size, corners, ret)

print(ret)
print(corners)

cv2.imshow("Board", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
