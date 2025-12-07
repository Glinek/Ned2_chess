import cv2
import numpy as np
from pyniryo2 import Vision
import pyniryo.vision as v
import chess
import logging

class ChessVision:
    def __init__(self, robot_instance):
        self.i = 0
        self.robot = robot_instance
        
        # Konfiguracja współrzędnych do cięcia (z Twojego findMove.py)
        self.crop_params = {
            'y': 28, 'h': 460, 'x': 73, 'w': 510,
            'pole_szer': 52, 'pole_wys': 52
        }
        self.nazwy_pol = [
            'a1','b1','c1','d1','e1','f1','g1','h1',
            'a2','b2','c2','d2','e2','f2','g2','h2',
            'a3','b3','c3','d3','e3','f3','g3','h3',
            'a4','b4','c4','d4','e4','f4','g4','h4',
            'a5','b5','c5','d5','e5','f5','g5','h5',
            'a6','b6','c6','d6','e6','f6','g6','h6',
            'a7','b7','c7','d7','e7','f7','g7','h7',
            'a8','b8','c8','d8','e8','f8','g8','h8'
        ]

    def take_photo(self):
        """Captures an image using the robot's camera and preprocesses it."""
        self.i = self.i + 1
        try:
            img_compressed = self.robot.vision.get_img_compressed()
            camera_info = self.robot.vision.get_camera_intrinsics()
            img = v.uncompress_image(img_compressed)
            img = v.undistort_image(img, camera_info.intrinsics, camera_info.distortion)
            
            # Konwersja na szarość dla łatwiejszego porównywania
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Crop do ROI (Region of Interest)
            roi = gray[self.crop_params['y']:self.crop_params['h'], 
                       self.crop_params['x']:self.crop_params['w']]
            cv2.imwrite(f"test{self.i}.jpg", roi)
            return roi
        except Exception as e:
            logging.error(f"Failed to take photo: {e}")
            return None

    def _split_into_squares(self, roi_img):
        """Splits the board image into a dictionary of squares { 'a1': img_a1, ... }"""
        squares = {}
        pole_szer = self.crop_params['pole_szer']
        pole_wys = self.crop_params['pole_wys']

        for row in range(8):
            for col in range(8):
                x1 = col * pole_szer
                y1 = row * pole_wys
                x2 = x1 + pole_szer
                y2 = y1 + pole_wys

                nazwa = self.nazwy_pol[row * 8 + col]

                # Twoje korekty z findMove.py
                if nazwa.startswith('h'):
                    x1 += 10
                    x2 += 10
                elif nazwa.startswith('e'):
                    x1 -= 21
                    x2 -= 21

                rank = int(nazwa[1])
                if rank >= 5:
                    y1 += 10
                    y2 += 10
                
                # Zabezpieczenie przed wyjściem poza obraz
                h_img, w_img = roi_img.shape
                x1, x2 = max(0, x1), min(w_img, x2)
                y1, y2 = max(0, y1), min(h_img, y2)

                squares[nazwa] = roi_img[y1:y2, x1:x2]
        return squares

    def detect_move(self, img_before, img_after, current_board_obj):
        """
        Compares two images and returns the UCI move string (e.g., 'e2e4').
        Uses the chess logic to determine direction.
        """
        squares_before = self._split_into_squares(img_before)
        squares_after = self._split_into_squares(img_after)
        
        diffs = []

        for sq in self.nazwy_pol:
            if sq in squares_before and sq in squares_after:
                # Oblicz średnią różnicę pikseli dla pola
                diff = cv2.absdiff(squares_before[sq], squares_after[sq])
                score = np.mean(diff)
                diffs.append((score, sq))
        
        # Sortuj pola wg największej zmiany (malejąco)
        diffs.sort(key=lambda x: x[0], reverse=True)
        
        # Zakładamy, że 2 pola z największą różnicą to ruch (Start i Stop)
        sq1 = diffs[0][1] # Największa zmiana
        sq2 = diffs[1][1] # Druga największa zmiana
        score1 = diffs[0][0]
        score2 = diffs[1][0]

        logging.info(f"Vision changes detected: {sq1}({score1:.1f}), {sq2}({score2:.1f})")

        # Logika: Które pole jest 'From', a które 'To'?
        # Sprawdzamy na logicznej planszy szachowej (przed ruchem)
        # Pole startowe MUSI mieć figurę gracza (tu: Białego, bo robot gra czarnymi lub na odwrót - w kodzie playChessWhite sugeruje, że gracz to Białe)
        
        piece_at_sq1 = current_board_obj.piece_at(chess.parse_square(sq1))
        piece_at_sq2 = current_board_obj.piece_at(chess.parse_square(sq2))

        # Jeżeli robot to Black, a gracz to White:
        # Pole startowe musi zawierać figurę gracza.
        # Pole końcowe może być puste (ruch) lub zawierać wroga (bicie).
        
        move_str = ""
        
        # Sprawdź wariant sq1 -> sq2
        if piece_at_sq1 is not None and piece_at_sq1.color == current_board_obj.turn:
            move_str = f"{sq1}{sq2}"
        # Sprawdź wariant sq2 -> sq1
        elif piece_at_sq2 is not None and piece_at_sq2.color == current_board_obj.turn:
            move_str = f"{sq2}{sq1}"
        else:
            logging.warning("Vision confused: neither changed square had a valid player piece.")
            return None

        # Prosta walidacja czy ruch jest legalny
        try:
            move = chess.Move.from_uci(move_str)
            if move in current_board_obj.legal_moves:
                return move_str
            
            # Obsługa promocji (domyślnie na hetmana)
            move_promo = chess.Move.from_uci(move_str + 'q')
            if move_promo in current_board_obj.legal_moves:
                return move_str + 'q'
                
        except:
            pass
            
        logging.warning(f"Vision detected move {move_str} but it is illegal.")
        return None