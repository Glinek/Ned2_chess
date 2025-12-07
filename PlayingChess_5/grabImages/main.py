# This is a sample Python script.
from pyniryo2 import *
from pyniryo2 import Vision
import pyniryo.vision as v

import cv2

from FirstChess.tool_move import robot

robot = NiryoRobot("10.10.10.10")
vision = Vision(robot)

robot.arm.calibrate_auto()
robot.tool.update_tool()

home = PoseObject(0.140, 0.0, 0.203, 0.0, 0.760, 0.0)
board_grab_pose = PoseObject(0.266, 0.0, 0.362, 3.127, 1.285, 3.103)

robot.arm.move_pose(board_grab_pose)

img_compressed = vision.get_img_compressed()
camera_info = vision.get_camera_intrinsics()
img = v.uncompress_image(img_compressed)
img = v.undistort_image(img, camera_info.intrinsics, camera_info.distortion)

cv2.imwrite("~/PycharmProjects/NiryoChess/board.jpg", img)
cv2.imshow('Color image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

robot.arm.move_pose(home)
robot.end()
