from pyniryo2 import *


ip = "192.168.1.10"

robot = NiryoRobot(ip)

robot.arm.calibrate_auto()
robot.tool.update_tool()

i = 0
poses = []
c = 'y'

while c != 'n':
    pose = robot.arm.get_pose()
    poses.append(str(pose))
    print(pose)
    c = input("Next?")

file = open("board_poses3.txt", "w")
for pose in poses:
    file.write(pose)
    file.write('\n')
file.close()

robot.end()
