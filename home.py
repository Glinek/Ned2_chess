from pyniryo2 import *

ip = "192.168.1.10"

robot = NiryoRobot(ip)

robot.arm.calibrate_auto()
robot.tool.update_tool()

home = PoseObject(0.140, 0.0, 0.203, 0.0, 0.760, 0.0)
robot.arm.move_pose(home)

robot.end()