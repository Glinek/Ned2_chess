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
        #---- Check if inputed string is corect ----
        if len(moveInput) > 4:
            logging.error("Error: Inputed string is too long!")
            return 1
        #---- Check if the game is over ----
        elif self.board.is_game_over() == False and moveInput != "q" and len(moveInput) <= 4:
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
                self.result_move = self.engine.play(self.board, chess.engine.Limit(time = 1))
                logging.info(f"Robot's move: {self.result_move}")
                #
                #---- Check if move is a capture ----
                self.capture = self.board.is_capture(self.result_move.move)
                self.piece_to_move = self.board.piece_at(self.result_move.move.from_square)
                if self.capture:
                    self.piece_to_capture = self.board.piece_at(self.result_move.move.to_square)
                else:
                    self.piece_to_capture = 0
                logging.info(f"Piece captured: {self.capture}")
                #
                #---- Push robot's move to the board ----
                self.board.push(self.result_move.move)
                logging.info(f"Board after ROBOT moves\n----------------\nblack\n{self.board}\nwhite\n----------------")
                #
                #---- Move pices ----
                self.robot_board.do_move(self.result_move.move, self.capture, self.piece_to_move, self.piece_to_capture)
                if self.board.is_game_over() == True:
                    logging.info(f"Game over. {self.board.outcome()}")
                    self.engine.quit()
                    self.robot_board.end()
                    return 0
            return 1
        else:
            logging.info(f"Game over. {self.board.outcome()}")
            self.engine.quit()
            self.robot_board.end()
            return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%y-%m-%d %H:%M") #logging setup
    #IP: 192.168.0.55 (wired) or 10.10.10.10 (hotspot)
    nedChessRobot = nedChess("10.10.10.10", "board_poses4.txt", r"C:/Users/szymo/Desktop/RoboChess/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2")
    outcome = 1
    moves = 0

    while outcome == 1:
        move = input("Players move (press Q to EXIT): ")
        outcome = nedChessRobot.playChessWhite(move)
        moves += 1

    logging.info(f"Player's moves total: {moves}")
