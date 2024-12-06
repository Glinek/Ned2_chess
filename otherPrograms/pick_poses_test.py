from pyniryo2 import *
import chess.engine
from count_board_picks import count_board_pick_coordinates

ip = "192.168.1.10"
home = PoseObject(0.140, 0.0, 0.203, 0.0, 0.760, 0.0)

pick_poses = count_board_pick_coordinates("board_poses4.txt")
robot = NiryoRobot(ip)

robot.arm.calibrate_auto()
robot.tool.update_tool()

def test_board_poses(test_robot, pick_pos):
    for i in range(0, 8):
        for j in range(0, 8):
            pose = PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2],
                              pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5])
            test_robot.arm.move_pose(pose)

def test_corners(test_robot, pick_pos):
    dz = 0.03

    i = 0
    j = 0
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz,
                              pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.grasp_with_tool()
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.release_with_tool()
    i = 7
    j = 0
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))

    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.grasp_with_tool()
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.release_with_tool()
    i = 0
    j = 7
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))

    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.grasp_with_tool()
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.release_with_tool()
    i = 7
    j = 7
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))

    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.grasp_with_tool()
    test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                        pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
    test_robot.tool.release_with_tool()

def test_line_8(test_robot, pick_pos):
    dz = 0.03

    i = 7 # row 8 close to robot...
    for j in range(0, 8):
        test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                            pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
        test_robot.tool.release_with_tool()
        test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz,
                                            pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
        test_robot.tool.grasp_with_tool()
        test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                            pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
        test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz,
                                            pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))
        test_robot.tool.release_with_tool()
        test_robot.arm.move_pose(PoseObject(pick_pos[i][j][0], pick_pos[i][j][1], pick_pos[i][j][2] + dz + 0.1,
                                            pick_pos[i][j][3], pick_pos[i][j][4], pick_pos[i][j][5]))


robot.arm.move_pose(home)

# test_board_poses(robot, pick_poses)
# test_corners(robot, pick_poses)
test_line_8(robot, pick_poses)

robot.arm.move_pose(home)

robot.end()
