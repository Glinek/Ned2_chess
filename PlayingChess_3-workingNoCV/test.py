#MOVE: e8g8
#Piece: k
#move:e7e5,capture:False,pieceMove:p,pieceCaptured:0

from moveRobot import *


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%y-%m-%d %H:%M")
robotBoard = RobotBoard("192.168.0.55", "board_poses4.txt")
robotBoard.do_move("e8g8",False,"k",0)