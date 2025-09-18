from pyniryo2 import *
import chess.engine
from countBoardPicks import count_board_pick_coordinates
import logging

class RobotBoard:
    def __init__(self, ip, boardCorners):
        self.dz = 0
        self.dimensions = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
        self.pick_poses = count_board_pick_coordinates(boardCorners)
        self.ip = ip
        self.home = PoseObject(0.140, 0.0, 0.203, 0.0, 0.760, 0.0)
        self.board_grab_pose = []
        for i in range(0, 6):
            self.board_grab_pose.append(self.pick_poses[0][0][i] + (self.pick_poses[7][7][i] - self.pick_poses[0][0][i]) / 2)

        self.robot = NiryoRobot(self.ip)

        self.robot.arm.calibrate_auto()
        self.robot.tool.update_tool()
        self.tool_id = self.robot.tool.get_current_tool_id()
        print(self.tool_id)


    def do_move(self, move, capture, piece_to_move, piece_to_capture):
        # print(move, capture)
        # decode move
        y1 = self.dimensions[str(move)[0]]
        x1 = int(str(move)[1]) - 1
        y2 = self.dimensions[str(move)[2]]
        x2 = int(str(move)[3]) - 1
        print(x1, y1, x2, y2)

        if capture:
            if piece_to_capture == chess.PAWN:
                if self.tool_id == ToolID.GRIPPER_1:
                    self.dz = 0.005
                else:
                    # self.tool_id == ToolID.GRIPPER_2:
                    self.dz = 0.01
            else:
                if self.tool_id == ToolID.GRIPPER_1:
                    self.dz = 0.01
                else:
                    # self.tool_id == ToolID.GRIPPER_2:
                    self.dz = 0.03

            self.robot.arm.move_pose(PoseObject(self.pick_poses[x2][y2][0], self.pick_poses[x2][y2][1],
                                                self.pick_poses[x2][y2][2] + self.dz + 0.1,
                                                self.pick_poses[x2][y2][3], self.pick_poses[x2][y2][4],
                                                self.pick_poses[x2][y2][5]))
            self.robot.tool.release_with_tool()
            self.robot.arm.move_pose(PoseObject(self.pick_poses[x2][y2][0], self.pick_poses[x2][y2][1], self.pick_poses[x2][y2][2] + self.dz,
                                                self.pick_poses[x2][y2][3], self.pick_poses[x2][y2][4], self.pick_poses[x2][y2][5]))
            self.robot.tool.grasp_with_tool()
            self.robot.arm.move_pose(PoseObject(self.pick_poses[x2][y2][0], self.pick_poses[x2][y2][1], self.pick_poses[x2][y2][2] + self.dz + 0.1,
                                                self.pick_poses[x2][y2][3], self.pick_poses[x2][y2][4], self.pick_poses[x2][y2][5]))
            self.robot.arm.move_pose(PoseObject(self.pick_poses[4][7][0],
                                                self.pick_poses[4][7][1] + 0.1,
                                                self.pick_poses[4][7][2] + self.dz + 0.1,
                                                self.pick_poses[4][7][3],
                                                self.pick_poses[4][7][4],
                                                self.pick_poses[4][7][5]))
            self.robot.arm.move_pose(PoseObject(self.pick_poses[4][7][0],
                                                self.pick_poses[4][7][1] + 0.1,
                                                self.pick_poses[4][7][2] + self.dz + 0.03,
                                                self.pick_poses[4][7][3],
                                                self.pick_poses[4][7][4],
                                                self.pick_poses[4][7][5]))
            self.robot.tool.release_with_tool()

        if piece_to_move == 1:
            if self.tool_id == ToolID.GRIPPER_1:
                self.dz = 0.005
            else:
                # self.tool_id == ToolID.GRIPPER_2:
                self.dz = 0.01
        else:
            if self.tool_id == ToolID.GRIPPER_1:
                self.dz = 0.01
            else:
                # self.tool_id == ToolID.GRIPPER_2:
                self.dz = 0.03

        self.robot.arm.move_pose(PoseObject(self.pick_poses[x1][y1][0],
                                            self.pick_poses[x1][y1][1],
                                            self.pick_poses[x1][y1][2] + self.dz + 0.1,
                                            self.pick_poses[x1][y1][3],
                                            self.pick_poses[x1][y1][4],
                                            self.pick_poses[x1][y1][5]))
        self.robot.tool.release_with_tool()
        self.robot.arm.move_pose(PoseObject(self.pick_poses[x1][y1][0],
                                            self.pick_poses[x1][y1][1],
                                            self.pick_poses[x1][y1][2] + self.dz,
                                            self.pick_poses[x1][y1][3],
                                            self.pick_poses[x1][y1][4],
                                            self.pick_poses[x1][y1][5]))
        self.robot.tool.grasp_with_tool()
        self.robot.arm.move_pose(PoseObject(self.pick_poses[x1][y1][0],
                                            self.pick_poses[x1][y1][1],
                                            self.pick_poses[x1][y1][2] + self.dz + 0.1,
                                            self.pick_poses[x1][y1][3],
                                            self.pick_poses[x1][y1][4],
                                            self.pick_poses[x1][y1][5]))
        self.robot.arm.move_pose(PoseObject(self.pick_poses[x2][y2][0],
                                            self.pick_poses[x2][y2][1],
                                            self.pick_poses[x2][y2][2] + self.dz + 0.1,
                                            self.pick_poses[x2][y2][3],
                                            self.pick_poses[x2][y2][4],
                                            self.pick_poses[x2][y2][5]))
        self.robot.arm.move_pose(PoseObject(self.pick_poses[x2][y2][0],
                                            self.pick_poses[x2][y2][1],
                                            self.pick_poses[x2][y2][2] + self.dz,
                                            self.pick_poses[x2][y2][3],
                                            self.pick_poses[x2][y2][4],
                                            self.pick_poses[x2][y2][5]))
        self.robot.tool.release_with_tool()
        self.robot.arm.move_pose(PoseObject(self.pick_poses[x2][y2][0],
                                            self.pick_poses[x2][y2][1],
                                            self.pick_poses[x2][y2][2] + self.dz + 0.1,
                                            self.pick_poses[x2][y2][3],
                                            self.pick_poses[x2][y2][4],
                                            self.pick_poses[x2][y2][5]))
        if piece_to_move == "k" and str(move) == "e8g8":
            self.do_move("h8f8", False, "r", 0)
        elif piece_to_move == "k" and str(move) == "e8c8":
            self.do_move("a8d8", False, "r", 0)
        else:
            self.robot.arm.move_pose(self.home)


    def end(self):
        self.robot.arm.move_pose(self.home)
        self.robot.end()
