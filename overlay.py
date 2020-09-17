from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import win32gui
import win32api

import sys

class Overlay(QMainWindow):

    def __init__(self):
        
        super().__init__()

        self.top = 0
        self.left = 0
        self.getFacts()
        self.initOverlay() 
        self.debug = False


    def getFacts(self):
        
        hwnd = win32gui.FindWindow(None, "Path Of Exile")

        rect = win32gui.GetWindowRect(hwnd)

        win32api.SetCursorPos((rect[2],rect[0]))

        self.x = rect[0]
        self.y = rect[1]
        self.width = rect[2] - self.x
        self.height = rect[3] - self.y
    

    def initOverlay(self):    
    
        self.label1 = QLabel(self)
        self.label1.setText("F10 to dump inventory")
        self.label1.setStyleSheet("QLabel {color: #39ff14 ;}")
        self.label1.resize(200,50)
        self.label1.move(10,5)


        self.label2 = QLabel(self)
        self.label2.setText("F11 to quit")
        self.label2.setStyleSheet("QLabel {color: #39ff14 ;}")
        self.label2.move(10,50)
 

        self.setGeometry(self.top, self.left, 200, 200)

 
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
            

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.show()


    def updateLabel():
        pass
    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec_())