import cv2
import numpy as np
from pathlib import Path
import os
input_folder = "input"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
files = os.listdir(input_folder)
def prepare():
    for filename in files:
        file_path = os.path.join(input_folder, filename)
        if os.path.isfile(file_path):
            img = cv2.imread(file_path)
            if img is not None:
                ready_to_go = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                output_path = os.path.join(output_folder, filename)
                cv2.imwrite(output_path, ready_to_go)

                print(f"Przetworzono: {filename}")
            else:
                print(f"Nie można wczytać pliku: {filename}")
prepare()

top_left = (64, 24)
bottom_right = (510, 454)

p1= Path("output/start_position.jpg")
img = cv2.imread(p1)
x = 73
y = 28
w = 510
h = 460
roi = img[y:h, x:w]
start_x = 75
start_y = 31
start_w = 138
start_h = 89
nazwy_pol = ['a1','b1','c1','d1','e1','f1','g1','h1',
             'a2','b2','c2','d2','e2','f2','g2','h2',
             'a3','b3','c3','d3','e3','f3','g3','h3',
             'a4','b4','c4','d4','e4','f4','g4','h4',
             'a5','b5','c5','d5','e5','f5','g5','h5',
             'a6','b6','c6','d6','e6','f6','g6','h6',
             'a7','b7','c7','d7','e7','f7','g7','h7',
             'a8','b8','c8','d8','e8','f8','g8','h8'
             ]

cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
pole_szer = 52
pole_wys = 52

nazwy_pol = [
    'a1','b1','c1','d1','e1','f1','g1','h1',
    'a2','b2','c2','d2','e2','f2','g2','h2',
    'a3','b3','c3','d3','e3','f3','g3','h3',
    'a4','b4','c4','d4','e4','f4','g4','h4',
    'a5','b5','c5','d5','e5','f5','g5','h5',
    'a6','b6','c6','d6','e6','f6','g6','h6',
    'a7','b7','c7','d7','e7','f7','g7','h7',
    'a8','b8','c8','d8','e8','f8','g8','h8'
]


pola = {}
for row in range(8):
    for col in range(8):
        x1 = col * pole_szer
        y1 = row * pole_wys
        x2 = x1 + pole_szer
        y2 = y1 + pole_wys

        nazwa = nazwy_pol[row * 8 + col]

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

        pola[nazwa] = roi[y1:y2, x1:x2]

# --- Podgląd testowy ---
cv2.imshow("Pole e2", pola['e1'])
cv2.waitKey(0)
cv2.destroyAllWindows()