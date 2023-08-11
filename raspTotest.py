import cv2, threading
import time

from threading import Thread
from queue import Queue

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication([])

my_dir = QFileDialog.getExistingDirectory(
    None,
    "Open a folder",
    '/data/FIF/',
    QFileDialog.ShowDirsOnly
    )

'''
b1 = QtWidgets.QPushButton("Click Me")
b1.show()

def on_click_cb():
    print("Clicked")

b1.clicked.connect(on_click_cb)
'''

queue=Queue()

cap = cv2.VideoCapture("/dev/video0")

fps = int(cap.get(5))
print("fps:", fps)

while(cap.isOpened()):

    ret,frame = cap.read()
    if not ret:
        break

    print("Captured")
    time.sleep(1)

    cv2.imshow('frame', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break
