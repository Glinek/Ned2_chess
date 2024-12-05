from pyniryo2 import *
# import chess.engine
from count_board_picks import count_board_pick_coordinates

ip = "192.168.1.10"
home = PoseObject(0.140, 0.0, 0.203, 0.0, 0.760, 0.0)

pick_poses = count_board_pick_coordinates("board_poses4.txt")
robot = NiryoRobot(ip)

robot.arm.calibrate_auto()
robot.tool.update_tool()

for i in range(0, 2):
    robot.tool.grasp_with_tool()
    robot.tool.release_with_tool()

robot.end()