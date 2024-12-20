import chess.engine
from moveRobot import RobotBoard
import logging

class nedChess:
    def __init__(self, ipAddr, boardCorners, chessEnginePath):
        '''
        Class that combiness all the logic for playing chess with the robot
        Args: 
            - ipAddr: IP address of the robot
            - boardCorners: File with the corners of the chess board
            - chessEnginePath: Path to the chess engine
        '''

        #=== Initialize the robot ===
        self.robot_board = RobotBoard(ipAddr, boardCorners)
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(chessEnginePath)

    def playChessWhite(self, moveInput):
        '''
        Function that plays chess with the robot
        Args:
            - move: Move of the player
        Returns:
            - 1 if the game is not over
            - 0 if the game is over
        '''
        #---- Check if the game is over ----
        if not self.board.is_game_over():
            self.move = chess.Move.from_uci(moveInput)                                                                          #Convert input to chess move
            #
            #== Check if move is legal and if it is not too long ==
            if not self.board.is_legal(self.move) or len(moveInput) != 4:
                logging.error("Error: Invalid move. Move impossible or inputed move is too long.")                              #Log error
            else:
                #---- Push move to the board ----
                self.board.push(self.move)
                logging.info(f"Board after PLAYER moves\n----------------\nblack\n{self.board}\nwhite\n----------------")
                #
                #---- Calculate robot's move ----
                self.result_move = self.engine.play(self.board, chess.engine.Limit(time = 0.1))
                logging.info(f"Robot's move: {self.result_move}")
                #
                #---- Check if move is a capture ----
                self.capture = self.board.is_capture(self.result_move.move)
                self.piece_to_move = self.board.piece_at(self.result_move.move.from_square)
                if self.capture:
                    self.piece_to_capture = self.board.piece_at(self.result_move.move.to_square)
                else:
                    self.piece_to_capture = 0
                logging.info(f"True if pice is captured. {self.capture}")
                #
                #---- Push robot's move to the board ----
                self.board.push(self.result_move.move)
                logging.info(f"Board after PLAYER moves\n----------------\nblack\n{self.board}\nwhite\n----------------")
                #
                #---- Move pices ----
                self.robot_board.do_move(self.result_move.move, self.capture, self.piece_to_move, self.piece_to_capture)
            return 1
        else:
            logging.info(f"Game over. {self.board.outcome()}")
            self.engine.quit()
            self.robot_board.end()
            return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s", datefmt="%y-%m-%d %H:%M") #logging setup
    nedChessRobot = nedChess("10.10.10.10", "board_poses4.txt", r"/home/glinek/Projects/Stockfish/stockfish-ubuntu-x86-64-avx2/stockfish/stockfish-ubuntu-x86-64-avx2")
    outcome = 1

    while outcome == 1:
        move = input("Players move: ")
        outcome = nedChessRobot.playChessWhite(move)