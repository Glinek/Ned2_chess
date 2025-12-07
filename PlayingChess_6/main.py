import chess.engine
from moveRobot import RobotBoard
import logging
import cv2
import time
from vision_module import ChessVision  # Importujemy nowy moduł

class nedChess:
    def __init__(self, ipAddr, boardCorners, chessEnginePath):
        '''
        Class that combines all the logic for playing chess with the robot
        '''

        #=== Initialize the robot ===
        self.robot_board = RobotBoard(ipAddr, boardCorners)
        # Przekazujemy instancję robota do Vision, aby korzystała z tego samego połączenia
        self.vision = ChessVision(self.robot_board.robot) 
        
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(chessEnginePath)
        
        self.img_before_move = None
        self.img_after_move = None

    def update_before_state(self):
        """Moves robot to camera, takes photo BEFORE player moves"""
        logging.info("Moving to camera pose for reference photo...")
        self.robot_board.move_to_camera_pose()
        time.sleep(1.0) # Czas na stabilizację ramienia
        self.img_before_move = self.vision.take_photo()
        logging.info("Reference photo taken.")
        self.robot_board.robot.arm.move_pose(self.robot_board.home)

    def get_player_move_from_vision(self):
        """Moves robot to camera, takes photo AFTER player moves, returns move string"""
        logging.info("Moving to camera pose to detect move...")
        self.robot_board.move_to_camera_pose()
        time.sleep(1.0)
        self.img_after_move = self.vision.take_photo()
        
        if self.img_before_move is None or self.img_after_move is None:
            logging.error("Missing images for comparison.")
            return None

        detected_move = self.vision.detect_move(self.img_before_move, self.img_after_move, self.board)
        return detected_move

    def playChessWhite(self):
        '''
        Main Logic Loop
        '''
        # 1. Zrób zdjęcie stanu PRZED ruchem gracza
        self.update_before_state()
        
        # 2. Czekaj na gracza
        print("\n>>> It's YOUR turn (White).")
        user_input = input("Make your move physically on the board and press ENTER (or 'q' to quit): ")
        if user_input.lower() == 'q':
            self.engine.quit()
            self.robot_board.end()
            return 0

        # 3. Zrób zdjęcie PO ruchu i wykryj różnicę
        moveInput = self.get_player_move_from_vision()
        
        if not moveInput:
            print("Could not detect a valid move. Please type it manually as backup.")
            moveInput = input("Manual move entry (e.g., e2e4): ")

        logging.info(f"Detected Move: {moveInput}")

        #---- Logic from original function starts here ----
        if self.board.is_game_over() == False:
            try:
                self.move = chess.Move.from_uci(moveInput)
            except ValueError:
                logging.error("Invalid move format")
                return 1

            #== Check if move is legal ==
            if not self.board.is_legal(self.move):
                logging.error(f"Error: Illegal move {moveInput} detected/entered.")
                return 1
            else:
                #---- Push move to the board ----
                self.board.push(self.move)
                logging.info(f"Board after PLAYER moves\n----------------\nblack\n{self.board}\nwhite\n----------------")
                
                # Check for game over after player move
                if self.board.is_game_over():
                    logging.info(f"Game over. {self.board.outcome()}")
                    return 0

                #---- Calculate robot's move ----
                self.result_move = self.engine.play(self.board, chess.engine.Limit(time=1))
                logging.info(f"Robot's move: {self.result_move}")
                
                #---- Check if move is a capture ----
                self.capture = self.board.is_capture(self.result_move.move)
                self.piece_to_move = self.board.piece_at(self.result_move.move.from_square)
                
                if self.capture:
                    self.piece_to_capture = self.board.piece_at(self.result_move.move.to_square)
                else:
                    self.piece_to_capture = 0
                
                logging.info(f"Piece captured: {self.capture}")
                
                #---- Push robot's move to the board logic ----
                self.board.push(self.result_move.move)
                logging.info(f"Board after ROBOT moves\n----------------\nblack\n{self.board}\nwhite\n----------------")
                
                #---- Move pieces physically ----
                logging.info(f"Is check: {self.board.is_check()}")
                
                # Robot wykonuje ruch fizyczny
                self.robot_board.do_move(self.result_move.move, self.capture, self.piece_to_move, self.piece_to_capture)
                
                if self.board.is_game_over():
                    logging.info(f"Game over. {self.board.outcome()}")
                    self.engine.quit()
                    self.robot_board.end()
                    return 0
            return 1
        else:
            logging.info(f"Game Over")
            self.engine.quit()
            self.robot_board.end()
            return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%y-%m-%d %H:%M") 
    
    # SETUP
    # Pamiętaj o ustawieniu poprawnych ścieżek
    nedChessRobot = nedChess(
        "192.168.0.55", 
        "board_poses4.txt", 
        r"C:/Users/szymo/Desktop/School/Zawodowe/RoboChess/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2"
    )
    
    outcome = 1
    moves = 0

    while outcome == 1:
        # Pętla została przeniesiona do playChessWhite, wywołujemy ją raz na turę
        outcome = nedChessRobot.playChessWhite()
        moves += 1

    logging.info(f"Moves total: {moves}")