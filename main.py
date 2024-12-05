#!/usr/bin/env python3
# from calendar import weekday

# import chess
import chess.engine
from robot_move import RobotBoard

robot_board = RobotBoard()
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci(r"/usr/games/stockfish")

print("White or Black (w/b)? ")
side = input()

if side == "w":
    while not board.is_game_over():
        move = chess.Move.from_uci(input("Enter your move:"))
        while not board.is_legal(move):
            move = chess.Move.from_uci(input("Enter your move:"))
        board.push(move)
        print(board, '\n')
        result_move = engine.play(board, chess.engine.Limit(time = 0.1))
        print(result_move)
        capture = board.is_capture(result_move.move)
        piece_to_move = board.piece_at(result_move.move.from_square)
        if capture:
            piece_to_capture = board.piece_at(result_move.move.to_square)
        else:
            piece_to_capture = 0

        print(capture)
        board.push(result_move.move)
        print(board, '\n')
        robot_board.do_move(result_move.move, capture, piece_to_move, piece_to_capture)

elif side == "b":
    while not board.is_game_over():
        result_move = engine.play(board, chess.engine.Limit(time = 0.1))
        capture = board.is_capture(result_move.move)
        piece_to_move = board.piece_at(result_move.move.from_square)
        if capture:
            piece_to_capture = board.piece_at(result_move.move.to_square)
        else:
            piece_to_capture = 0

        print(result_move)
        board.push(result_move.move)
        print(board, '\n')
        robot_board.do_move(result_move.move, capture, piece_to_move, piece_to_capture)
        move = chess.Move.from_uci(input("Enter your move:"))
        while not board.is_legal(move):
            move = chess.Move.from_uci(input("Enter your move:"))
        board.push(move)
        print(board, '\n')
else:
    print("Only white or black...")

# TODO
print("Finally: ", chess.Outcome)

engine.quit()
robot_board.end()
