# This is a sample Python script.
from pyniryo2 import *
from pyniryo2 import Vision
import pyniryo.vision as v

import cv2

from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"

suppress_qt_warnings()

ip = "192.168.1.10"

robot = NiryoRobot(ip)
ros_instance = NiryoRos(ip)
vision = Vision(ros_instance)

robot.arm.calibrate_auto()
robot.tool.update_tool()

home = PoseObject(0.140, 0.0, 0.203, 0.0, 0.760, 0.0)
board_grab_pose = PoseObject(0.208, 0.0, 0.362, 3.14, 1.285, 3.103)

robot.arm.move_pose(board_grab_pose)

img_compressed = vision.get_img_compressed()
camera_info = vision.get_camera_intrinsics()
img = v.uncompress_image(img_compressed)
img = v.undistort_image(img, camera_info.intrinsics, camera_info.distortion)

cv2.imwrite("board_empty.jpg", img)
cv2.imshow('Grabbed chessboard', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

robot.arm.move_pose(home)
robot.end()

